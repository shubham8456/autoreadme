from pathlib import Path
import os

DEFAULT_MODEL = os.getenv("AUTOREADME_MODEL", "qwen2.5-coder:3b")
DEFAULT_OUTPUT = "README.generated.md"
OLLAMA_URL = os.getenv("AUTOREADME_OLLAMA_URL", "http://127.0.0.1:11434")
MAX_FILE_BYTES = 128 * 1024
MAX_FILES = 80

SKIP_DIRS = {
    ".git",
    ".next",
    ".turbo",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
}

PRIORITY_FILES = [
    "README.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".env.example",
]

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".rb", ".go", ".rs", ".java", ".kt", ".sh", ".md",
    ".toml", ".yaml", ".yml", ".json", ".txt", ".ini", ".cfg", ".sql", ".html", ".css",
}

def resolve_repo_path(raw_path: str) -> Path:
    return Path(raw_path).expanduser().resolve()
