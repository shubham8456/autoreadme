from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pathspec import GitIgnoreSpec

from app.config import PRIORITY_FILES, SKIP_DIRS, TEXT_EXTENSIONS


class RepoContext(dict):
    pass


def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in PRIORITY_FILES


def _safe_read(path: Path) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    return data


def _load_gitignore_spec(repo_path: Path) -> GitIgnoreSpec | None:
    gitignore_path = repo_path / ".gitignore"
    if not gitignore_path.exists() or not gitignore_path.is_file():
        return None

    lines = gitignore_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not lines:
        return None

    return GitIgnoreSpec.from_lines(lines)


def _is_ignored_by_gitignore(path: Path, repo_path: Path, spec: GitIgnoreSpec | None) -> bool:
    if spec is None:
        return False

    rel_path = path.relative_to(repo_path).as_posix()
    if path.is_dir():
        rel_path = f"{rel_path}/"

    return spec.match_file(rel_path)


def _iter_files(repo_path: Path) -> Iterable[Path]:
    gitignore_spec = _load_gitignore_spec(repo_path)

    for path in repo_path.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if _is_ignored_by_gitignore(path, repo_path, gitignore_spec):
            continue
        if not path.is_file():
            continue
        if path.name == "README.generated.md":
            continue
        if not _is_text_file(path):
            continue
        yield path


def scan_repository(repo_path: Path) -> RepoContext:
    files = list(_iter_files(repo_path))

    prioritized = []
    for name in PRIORITY_FILES:
        candidate = repo_path / name
        if (
            candidate.exists()
            and candidate.is_file()
            and candidate not in prioritized
            and candidate in files
        ):
            prioritized.append(candidate)

    remaining = [p for p in files if p not in prioritized]
    selected = (prioritized + remaining)

    entries = []
    for file_path in selected:
        rel_path = file_path.relative_to(repo_path)
        content = _safe_read(file_path)
        if not content.strip():
            continue
        entries.append({"path": str(rel_path), "content": content})

    return RepoContext(
        repo_name=repo_path.name,
        repo_path=str(repo_path),
        file_count=len(entries),
        files=entries,
    )
