from __future__ import annotations

from pathlib import Path
from typing import Iterable

from app.config import MAX_FILE_BYTES, MAX_FILES, PRIORITY_FILES, SKIP_DIRS, TEXT_EXTENSIONS

class RepoContext(dict):
    pass

def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in PRIORITY_FILES

def _safe_read(path: Path) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    return data[:MAX_FILE_BYTES]

def _iter_files(repo_path: Path) -> Iterable[Path]:
    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not _is_text_file(path):
            continue
        yield path

def scan_repository(repo_path: Path) -> RepoContext:
    files = list(_iter_files(repo_path))
    prioritized = []
    for name in PRIORITY_FILES:
        candidate = repo_path / name
        if candidate.exists() and candidate.is_file():
            prioritized.append(candidate)

    remaining = [p for p in files if p not in prioritized]
    selected = (prioritized + remaining)[:MAX_FILES]

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
