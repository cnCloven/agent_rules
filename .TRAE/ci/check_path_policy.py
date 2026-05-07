from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ALLOWED_MARKDOWN_SUFFIXES = {".md", ".mdc"}
ALLOWED_NON_TRAE_PREFIXES = {
    ".github/workflows/",
}
ALLOWED_NON_TRAE_EXACT = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
}


def _git(*args: str) -> str:
    p = subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p.stdout


def _repo_root() -> Path:
    return Path(_git("rev-parse", "--show-toplevel").strip())


def _normalize_repo_rel(path: str) -> str:
    p = path.replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_allowed_non_markdown_repo_path(rel: str) -> bool:
    if rel.startswith(".TRAE/") or rel.startswith(".trae/"):
        return True
    if rel in ALLOWED_NON_TRAE_EXACT:
        return True
    for prefix in ALLOWED_NON_TRAE_PREFIXES:
        if rel.startswith(prefix):
            return True
    return False


def _violates(rel: str) -> bool:
    if rel.replace("\\", "/").endswith(".pyc") or "/__pycache__/" in rel.replace("\\", "/"):
        return True
    suffix = Path(rel).suffix.lower()
    if suffix in ALLOWED_MARKDOWN_SUFFIXES:
        return False
    return not _is_allowed_non_markdown_repo_path(rel)


def _list_tracked_files() -> list[str]:
    out = _git("ls-files")
    return [line.strip() for line in out.splitlines() if line.strip()]


def _list_staged_files() -> list[str]:
    out = _git("diff", "--name-only", "--cached", "--diff-filter=ACMR")
    return [line.strip() for line in out.splitlines() if line.strip()]


def _list_all_files(repo_root: Path) -> list[str]:
    paths: list[str] = []
    for p in repo_root.rglob("*"):
        if p.is_file():
            paths.append(str(p.relative_to(repo_root)))
    return paths


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--tracked", action="store_true")
    mode.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)

    repo_root = _repo_root()

    if args.staged:
        candidates = _list_staged_files()
    elif args.tracked:
        candidates = _list_tracked_files()
    else:
        candidates = _list_all_files(repo_root)

    bad: list[str] = []
    for raw in candidates:
        rel = _normalize_repo_rel(raw)
        if _violates(rel):
            bad.append(rel)

    if bad:
        sys.stderr.write(
            "Path policy violation: non-Markdown files must be under .TRAE/ "
            "(only .github/workflows/ is allowed for CI config).\n"
        )
        for p in bad:
            sys.stderr.write(f"- {p}\n")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
