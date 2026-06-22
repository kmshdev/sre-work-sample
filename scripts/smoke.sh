#!/bin/sh
set -eu

if [ -x ".venv/bin/python" ]; then
  python_bin=".venv/bin/python"
else
  python_bin="python3"
fi

"$python_bin" -m sre_work_sample.cli smoke
