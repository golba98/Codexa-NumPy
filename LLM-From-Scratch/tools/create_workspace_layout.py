"""Recreate the NumPy workspace's navigation folders without copying code."""

from __future__ import annotations

import os
from pathlib import Path


COMPONENTS = {
    "LLM-Architecture": ["backend", "tensor.py", "parameter.py", "ops", "nn", "losses", "config.py", "model_presets.py"],
    "LLM-Data": ["data"],
    "LLM-Tokenizer": ["tokenization"],
    "LLM-Training": ["training", "optim", "utils"],
    "LLM-Inference": ["generation"],
    "LLM-Memory": [],
    "LLM-Specialist": [],
}


def create_link(path: Path, target: Path) -> None:
    """Create a relative link, refusing to overwrite conflicting paths."""
    if path.is_symlink() and path.resolve() == target.resolve():
        return
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"Refusing to overwrite workspace entry: {path}")
    if not target.exists():
        raise FileNotFoundError(f"Missing workspace link target: {target}")
    path.symlink_to(os.path.relpath(target, path.parent), target_is_directory=target.is_dir())


def create_readme(path: Path, target: Path) -> None:
    """Keep an existing public README or create the local navigation link."""
    if path.is_file() and not path.is_symlink():
        return
    create_link(path, target)


def create_layout(repo: Path) -> None:
    """Generate sibling navigation sections for one canonical NumPy repository."""
    repo = repo.resolve()
    workspace = repo.parent
    docs = repo / "docs/workspace"
    records = workspace.parent / "32-LLM Source"
    for component, names in COMPONENTS.items():
        directory = workspace / component
        directory.mkdir(exist_ok=True)
        create_readme(directory / "README.md", docs / "components" / f"{component}.md")
        for name in names:
            create_link(directory / name, repo / "src/llm_numpy" / name)
    create_readme(workspace / "README.md", docs / "OVERVIEW.md")
    if (docs / "GUIDELINES.md").is_file():
        create_link(workspace / "AGENTS.md", docs / "GUIDELINES.md")
    if (repo / "CLAUDE.md").is_file():
        create_link(workspace / "CLAUDE.md", repo / "CLAUDE.md")
    infrastructure = workspace / "workspace-infrastructure"
    infrastructure.mkdir(exist_ok=True)
    (infrastructure / "validation").mkdir(exist_ok=True)
    create_readme(infrastructure / "README.md", docs / "INFRASTRUCTURE.md")
    create_link(infrastructure / "preservation", records / "recovery")
    create_link(infrastructure / "build", records / "local-evidence/build")


def main() -> None:
    """Restore this checkout's sibling navigation links."""
    create_layout(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
