#!/usr/bin/env python3
"""Run tests or a packaged CLI in the NumPy Codexa workspace."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> int:
    """Forward arguments using this interpreter and the selected checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("test", "module"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    tail = arguments.arguments
    if tail[:1] == ["--"]:
        tail = tail[1:]
    if arguments.command == "test":
        command = [sys.executable, "-m", "pytest", "tests", *tail]
    else:
        if not tail:
            parser.error("module requires a full llm_numpy.cli module name")
        module = tail[0]
        if not re.fullmatch(r"llm_numpy\.cli\.[a-z][a-z0-9_]*", module):
            parser.error("module must name a command inside llm_numpy.cli")
        path = REPO_ROOT / "src" / Path(*module.split("."))
        if not path.with_suffix(".py").is_file() or module.endswith(".__init__"):
            parser.error(f"unknown CLI module: {module}")
        command = [sys.executable, "-m", module, *tail[1:]]
    environment = os.environ.copy()
    paths = [str(REPO_ROOT / "src"), str(REPO_ROOT)]
    if environment.get("PYTHONPATH"):
        paths.append(environment["PYTHONPATH"])
    environment["PYTHONPATH"] = os.pathsep.join(paths)
    environment.setdefault("NUMPY_LLM_WORKSPACE_ROOT", str(REPO_ROOT))
    return subprocess.run(command, cwd=REPO_ROOT, env=environment, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
