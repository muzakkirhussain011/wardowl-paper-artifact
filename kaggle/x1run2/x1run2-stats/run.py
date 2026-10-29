"""wardowl paper, X1 run 2 on Kaggle: role stats (benchmarks/paper/x1_run2_kaggle.py at a95642429d508340946ee3679b65db2eedd36dc1)."""

import subprocess
import sys

SRC, COMMIT, ROLE = "/tmp/wardowl-src", "a95642429d508340946ee3679b65db2eedd36dc1", "stats"
subprocess.run(["git", "clone", "-q", "https://github.com/muzakkirhussain011/wardowl.git", SRC], check=True)
subprocess.run(["git", "-C", SRC, "checkout", "-q", COMMIT], check=True)
code = subprocess.run([sys.executable, f"{SRC}/benchmarks/paper/x1_run2_kaggle.py", "--role", ROLE, "--src", SRC]).returncode
sys.exit(code)
