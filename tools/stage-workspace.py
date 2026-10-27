#!/usr/bin/env python3
"""Stage the nested source checkout as regular files in the outer repository.

Run from this workspace, then review `git diff --cached` before committing.
The nested index and its Git metadata are never changed.
"""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'LLM-From-Scratch'


def git(*args, cwd=ROOT, data=None):
    return subprocess.run(['git', *args], cwd=cwd, input=data, stdout=subprocess.PIPE,
                          check=True).stdout


def permitted(path):
    parts = path.parts
    name = path.name.lower()
    if name in {'agents.md', 'claude.md', 'guidelines.md', 'artifacts.local.json'}:
        return False
    if name.startswith('.env') or name.endswith(('.safetensors', '.pt', '.pth', '.ckpt')):
        return False
    if any(part in {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache',
                    'outputs', 'checkpoints', 'artifacts', 'logs', 'validation',
                    'preservation', 'build', 'dist'} for part in parts):
        return False
    if parts[:2] == ('docs', 'workspace') and parts[2:3] != ('components',):
        return False
    return True


def main():
    if not (SOURCE / '.git').exists():
        sys.exit('This command requires the local nested Git checkout. In a public clone, use ordinary Git commands.')
    files = git('ls-files', '-co', '--exclude-standard', '-z', cwd=SOURCE).split(b'\0')
    git('rm', '-r', '--cached', '--ignore-unmatch', '-q', '--', 'LLM-From-Scratch')
    entries = []
    for raw in sorted(set(files)):
        if not raw:
            continue
        path = Path(os.fsdecode(raw))
        full = SOURCE / path
        if not permitted(path) or not full.is_file() or full.is_symlink():
            continue
        mode = '100755' if full.stat().st_mode & 0o111 else '100644'
        oid = git('hash-object', '-w', '--stdin', data=full.read_bytes()).strip().decode()
        entries.append(f'{mode} {oid}\tLLM-From-Scratch/{path.as_posix()}\0'.encode())
    git('update-index', '-z', '--index-info', data=b''.join(entries))
    print(f'Staged {len(entries)} nested source files; review the staged diff before committing.')


if __name__ == '__main__':
    main()
