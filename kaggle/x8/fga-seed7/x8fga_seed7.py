# X8-FGA (plan/x8-prereg.md, amendment 1): the enterprise end-to-end run with only the pgvector store
# and the OpenFGA configuration, at the pinned scripts. One change outside them: OpenFGA's request
# timeout is raised above the harness's 20 s ListObjects deadline, which OpenFGA 1.22 otherwise rejects
# at start-up. Kaggle settings: GPU T4 x2, internet on.
import os
import subprocess
import sys
import time
import traceback

SEED = 7
WARDOWL_VERSION = "2.1.0"
REF = "bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839"  # the scripts X0 ran
SRC = "/tmp/wardowl-src"
EXTRAS = "pgvector,chroma,elasticsearch,opensearch,qdrant,weaviate,redis,lancedb,faiss"
STORES = ("pgvector",)


def sh(command: str) -> None:
    print(f"+ {command}", flush=True)
    subprocess.run(command, shell=True, check=True)


started = time.time()
sh(f"rm -rf {SRC} && git clone -q https://github.com/muzakkirhussain011/wardowl.git {SRC}")
sh(f"git -C {SRC} checkout -q {REF} && git -C {SRC} log -1 --format='%H %cs %s'")
sh(f'pip install -q "wardowl[{EXTRAS}]=={WARDOWL_VERSION}" "sentence-transformers>=3" "datasets>=2.19" psutil')
sh(f"PG_TUNE=1 bash {SRC}/benchmarks/kaggle_setup.sh")

sys.path.insert(0, f"{SRC}/acceptance/kaggle")
import enterprise_rag as er  # noqa: E402

config = er.Config(
    stores=STORES,
    remote_authorizers=("openfga",),
    variants=208,
    kb_limit=0,
    embed_model="BAAI/bge-base-en-v1.5",
    llm_model="Qwen/Qwen2.5-3B-Instruct",
    seed=SEED,
)
config.wardowl_version, config.repo = WARDOWL_VERSION, SRC
os.environ["OPENFGA_REQUEST_TIMEOUT"] = "25s"  # passed to the server by the harness (env = {**os.environ, ...})
print(f"X8-FGA seed {SEED}", flush=True)
run = er.Run(config)
run.environment_check()
run.build_corpus()
run.embed()
run.baseline()
run.load_llm()
for store in STORES:
    try:
        run.store(store)
    except Exception:  # the notebook runs the next store cell after a failure; so does this
        traceback.print_exc()
        sys.stdout.flush()
failed = run.finish()
print(f"X8-FGA seed {SEED}: {failed} failed checks, {time.time() - started:.0f} s", flush=True)
