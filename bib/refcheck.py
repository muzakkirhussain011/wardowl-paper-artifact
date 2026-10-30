"""Check the paper's cited references against primary records.

Usage: refcheck.py main.aux references.bib web.bib report.md report.tsv

A reference with a DOI is compared with Crossref, one with an arXiv identifier with arXiv's API, and any
other link is fetched. Titles are compared after dropping case, punctuation and LaTeX, and so are the first
author's family names. Every row says what was compared, so a human can read what the machine could not settle.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

AGENT = "wardowl-paper-refcheck/1.0 (mailto:muzakkirhussain011@gmail.com)"


def cited_keys(aux_path: str) -> list[tuple[int, str]]:
    keys: dict[str, int] = {}
    with open(aux_path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = re.search(r"\\bibcite\{([^}]*)\}\{\{(\d+)\}", line)
            if match and match.group(1) not in keys:
                keys[match.group(1)] = int(match.group(2))
    return sorted((number, key) for key, number in keys.items())


def parse_bib(paths: list[str]) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        for match in re.finditer(r"^@(\w+)\{([^,\s]+),", text, flags=re.M):
            kind, key = match.group(1).lower(), match.group(2)
            if kind in ("comment", "string", "preamble"):
                continue
            body = _entry_body(text, match.end())
            fields = {"_type": kind, "_file": path}
            for field in re.finditer(r"^\s*([A-Za-z]+)\s*=\s*", body, flags=re.M):
                fields[field.group(1).lower()] = _field_value(body, field.end())
            entries[key] = fields
    return entries


def _entry_body(text: str, start: int) -> str:
    depth = 1
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start:index]
    return text[start:]


def _field_value(body: str, start: int) -> str:
    if start >= len(body):
        return ""
    if body[start] == "{":
        depth = 0
        for index in range(start, len(body)):
            if body[index] == "{":
                depth += 1
            elif body[index] == "}":
                depth -= 1
                if depth == 0:
                    return body[start + 1 : index]
    if body[start] == '"':
        end = body.find('"', start + 1)
        return body[start + 1 : end]
    return body[start:].split(",", 1)[0].strip()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = re.sub(r"\\[^a-zA-Z0-9\s]", "", text)  # LaTeX accents, so Aum{\"u}ller reads as Aumuller
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()
    return " ".join(text.split())


def similarity(left: str, right: str) -> float:
    return difflib.SequenceMatcher(None, normalize(left), normalize(right)).ratio()


def first_family(authors: str) -> str:
    first = re.split(r"\s+and\s+", authors.strip())[0]
    first = first.strip("{} ")
    if "," in first:
        return first.split(",")[0].strip("{} ")
    return first.split()[-1] if first.split() else ""


def fetch(url: str, timeout: int = 30) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read(2_000_000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return error.code, ""
    except Exception as error:  # a dead host or a timeout is a finding, not a crash
        return 0, str(error)


def check_doi(entry: dict[str, str]) -> dict[str, str]:
    doi = entry["doi"].strip()
    status, body = fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if status != 200:
        return {"source": "crossref", "result": f"DOI not found ({status})"}
    work = json.loads(body)["message"]
    title = " ".join(work.get("title", []) + work.get("subtitle", []))
    authors = work.get("author", [])
    family = authors[0].get("family", "") if authors else ""
    return _compare("crossref", entry, title, family, str(_year(work)))


def _year(work: dict) -> str:
    for field in ("published-print", "published-online", "published", "issued"):
        parts = work.get(field, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return ""


def check_arxiv(entry: dict[str, str]) -> dict[str, str]:
    identifier = entry["eprint"].strip()
    time.sleep(3.1)
    status, body = fetch("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(identifier))
    if status != 200:
        return {"source": "arxiv", "result": f"arXiv API error ({status})"}
    atom = "{http://www.w3.org/2005/Atom}"
    try:
        record = ET.fromstring(body).find(atom + "entry")
    except ET.ParseError:
        return {"source": "arxiv", "result": "arXiv API answer unreadable"}
    title_node = record.find(atom + "title") if record is not None else None
    if title_node is None or not (title_node.text or "").strip() or title_node.text.strip() == "Error":
        return {"source": "arxiv", "result": "arXiv identifier not found"}
    names = [n.find(atom + "name").text for n in record.findall(atom + "author")]
    family = names[0].split()[-1] if names else ""
    return _compare("arxiv", entry, " ".join(title_node.text.split()), family, record.find(atom + "published").text[:4])


def check_url(entry: dict[str, str]) -> dict[str, str]:
    url = entry["url"].strip()
    status, body = fetch(url)
    if status == 0:
        return {"source": "url", "result": "unreachable", "found_title": body[:100]}
    if status in (401, 403, 429):
        return {"source": "url", "result": f"blocked ({status}): read by hand"}
    if status >= 400:
        return {"source": "url", "result": f"HTTP {status}"}
    found = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.I | re.S)
    page_title = " ".join(found.group(1).split()) if found else ""
    wanted = normalize(entry.get("title", ""))
    page = normalize(body[:2_000_000])
    words = [word for word in wanted.split() if len(word) > 3]
    share = sum(word in page for word in words) / len(words) if words else 0.0
    verdict = "ok" if share >= 0.7 else "page reached; title words not found: read by hand"
    return {"source": "url", "result": verdict, "found_title": page_title[:100], "score": f"{share:.2f}"}


def _compare(source: str, entry: dict[str, str], title: str, family: str, year: str) -> dict[str, str]:
    score = similarity(entry.get("title", ""), title)
    author_ok = not family or normalize(family) in normalize(entry.get("author", ""))
    year_ok = not year or not entry.get("year") or str(year) == entry["year"].strip()
    problems = []
    if score < 0.85:
        problems.append("title differs")
    if not author_ok:
        problems.append(f"first author {family} not in the entry")
    if not year_ok:
        problems.append(f"year {year} in the record")
    return {
        "source": source,
        "result": "ok" if not problems else "; ".join(problems),
        "found_title": title[:100],
        "score": f"{score:.2f}",
    }


def main() -> int:
    aux, references, web, report_md, report_tsv = sys.argv[1:6]
    entries = parse_bib([references, web])
    rows = []
    for number, key in cited_keys(aux):
        entry = entries.get(key)
        if entry is None:
            rows.append({"n": number, "key": key, "source": "-", "result": "NOT IN THE BIB FILES"})
            continue
        if entry.get("doi"):
            outcome = check_doi(entry)
            time.sleep(0.2)
        elif entry.get("eprint"):
            outcome = check_arxiv(entry)
        elif entry.get("url"):
            outcome = check_url(entry)
        else:
            outcome = {"source": "-", "result": "no DOI, arXiv identifier or link: read by hand"}
        rows.append({"n": number, "key": key, "title": entry.get("title", ""), **outcome})
        print(number, key, outcome["result"], flush=True)

    bad = [row for row in rows if row["result"] != "ok"]
    with open(report_tsv, "w", encoding="utf-8") as handle:
        handle.write("n\tkey\tsource\tresult\tscore\tentry_title\tfound_title\n")
        for row in rows:
            handle.write(
                "\t".join(
                    str(row.get(field, ""))
                    for field in ("n", "key", "source", "result", "score", "title", "found_title")
                )
                + "\n"
            )
    with open(report_md, "w", encoding="utf-8") as handle:
        handle.write(f"# Reference check\n\n{len(rows)} cited references, {len(rows) - len(bad)} ok, {len(bad)} to read.\n\n")
        handle.write("| No. | Key | Source | Result | Entry title | Record's title |\n|---|---|---|---|---|---|\n")
        for row in bad:
            handle.write(
                f"| {row['n']} | `{row['key']}` | {row.get('source', '')} | {row['result']} | "
                f"{row.get('title', '')[:70]} | {row.get('found_title', '')[:70]} |\n"
            )
    print(f"{len(rows)} references, {len(bad)} to read")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
