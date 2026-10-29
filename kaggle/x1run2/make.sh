#!/usr/bin/env bash
# make.sh <role> <slug> <gpu true|false> <commit> [kernel source slugs...]: writes a kernel folder for one role
set -euo pipefail
role="$1"; slug="$2"; gpu="$3"; commit="$4"; shift 4
dir="$(dirname "$0")/$slug"
mkdir -p "$dir"
sources=""
for s in "$@"; do sources="${sources:+$sources, }\"muzakkirhussain1/$s\""; done
shape="None"; [ "$gpu" = "true" ] && shape="NvidiaTeslaT4"
cat > "$dir/kernel-metadata.json" <<JSON
{"id": "muzakkirhussain1/$slug", "title": "$slug", "code_file": "run.py", "language": "python", "kernel_type": "script", "is_private": true, "enable_gpu": $gpu, "enable_internet": true, "dataset_sources": [], "kernel_sources": [$sources], "competition_sources": [], "machine_shape": "$shape"}
JSON
cat > "$dir/run.py" <<PY
"""wardowl paper, X1 run 2 on Kaggle: role $role (benchmarks/paper/x1_run2_kaggle.py at $commit)."""

import subprocess
import sys

SRC, COMMIT, ROLE = "/tmp/wardowl-src", "$commit", "$role"
subprocess.run(["git", "clone", "-q", "https://github.com/muzakkirhussain011/wardowl.git", SRC], check=True)
subprocess.run(["git", "-C", SRC, "checkout", "-q", COMMIT], check=True)
code = subprocess.run([sys.executable, f"{SRC}/benchmarks/paper/x1_run2_kaggle.py", "--role", ROLE, "--src", SRC]).returncode
sys.exit(code)
PY
echo "$dir"
