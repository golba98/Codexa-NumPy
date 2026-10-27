# Publishing from the local workspace

The local `LLM-From-Scratch` directory has its own Git repository. Its source is staged into the outer repository without a submodule by running `python3 tools/stage-workspace.py` from the workspace root. The command uses the nested checkout's tracked and non-ignored files without changing its index. Stage other intended changes with `git add`, review `git diff --cached` and scan the staged content before committing. Exclusions in the script and `.gitignore` must be reviewed when the local layout changes.

A normal clone of this public repository has no nested Git repository; use ordinary Git commands there.
