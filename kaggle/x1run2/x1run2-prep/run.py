"""wardowl paper, X1 run 2 on Kaggle: role prep (benchmarks/paper/x1_run2_kaggle.py at be3ea06f1d134540e87c1969bbd16d2338f083a2)."""

import subprocess
import sys

SRC, COMMIT, ROLE = "/tmp/wardowl-src", "be3ea06f1d134540e87c1969bbd16d2338f083a2", "prep"
subprocess.run(["git", "clone", "-q", "https://github.com/muzakkirhussain011/wardowl.git", SRC], check=True)
subprocess.run(["git", "-C", SRC, "checkout", "-q", COMMIT], check=True)
code = subprocess.run([sys.executable, f"{SRC}/benchmarks/paper/x1_run2_kaggle.py", "--role", ROLE, "--src", SRC]).returncode
sys.exit(code)
