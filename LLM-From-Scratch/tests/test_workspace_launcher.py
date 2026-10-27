"""Exercise the workspace launcher and safely recreatable navigation layout."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from tools.create_workspace_layout import COMPONENTS, create_layout


REPO = Path(__file__).resolve().parents[1]


def test_launcher_runs_packaged_module_outside_checkout(tmp_path):
    environment = os.environ.copy()
    environment.pop("NUMPY_LLM_WORKSPACE_ROOT", None)
    result = subprocess.run(
        [sys.executable, str(REPO / "run.py"), "module", "llm_numpy.cli.environment_report"],
        cwd=tmp_path, env=environment, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "numpy" in json.loads(result.stdout)


def test_launcher_forwards_test_options_without_starting_training(tmp_path):
    result = subprocess.run(
        [sys.executable, str(REPO / "run.py"), "test", "--help"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "--collect-only" in result.stdout


@pytest.mark.parametrize("arguments", [
    ["module"],
    ["module", "os"],
    ["module", "llm_numpy.cli.missing_command"],
])
def test_launcher_rejects_missing_or_unrelated_modules(tmp_path, arguments):
    result = subprocess.run(
        [sys.executable, str(REPO / "run.py"), *arguments],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "error:" in result.stderr


def make_layout_fixture(tmp_path):
    repo = tmp_path / "workspace/LLM-From-Scratch"
    docs = repo / "docs/workspace"
    (docs / "components").mkdir(parents=True)
    for name in ["OVERVIEW.md", "GUIDELINES.md", "INFRASTRUCTURE.md"]:
        (docs / name).write_text("fixture")
    for component, names in COMPONENTS.items():
        (docs / "components" / f"{component}.md").write_text("fixture")
        for name in names:
            target = repo / "src/llm_numpy" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.suffix:
                target.write_text("fixture")
            else:
                target.mkdir(exist_ok=True)
    (tmp_path / "32-LLM Source/recovery").mkdir(parents=True)
    (tmp_path / "32-LLM Source/local-evidence/build").mkdir(parents=True)
    return repo


def test_navigation_layout_is_relative_and_idempotent(tmp_path):
    repo = make_layout_fixture(tmp_path)
    (repo / "CLAUDE.md").write_text("local agent notes")
    create_layout(repo)
    create_layout(repo)
    link = repo.parent / "LLM-Architecture/tensor.py"
    assert link.resolve() == repo / "src/llm_numpy/tensor.py"
    assert not Path(os.readlink(link)).is_absolute()
    assert (repo.parent / "CLAUDE.md").resolve() == repo / "CLAUDE.md"
    assert not (repo.parent / "LLM-Memory/implementation").exists()


def test_navigation_layout_preserves_conflicting_user_file(tmp_path):
    repo = make_layout_fixture(tmp_path)
    conflict = repo.parent / "LLM-Architecture/tensor.py"
    conflict.parent.mkdir()
    conflict.write_text("preserve this file")
    with pytest.raises(FileExistsError):
        create_layout(repo)
    assert conflict.read_text() == "preserve this file"
