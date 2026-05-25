import argparse

from app.config import DEFAULT_MODEL, DEFAULT_OUTPUT, resolve_repo_path
from app.core.readme import generate_readme

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a README for a mounted local repository")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to the repository inside the container")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model to use")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    repo_path = resolve_repo_path(args.repo_path)
    output_path = repo_path / DEFAULT_OUTPUT
    generate_readme(repo_path=repo_path, model=args.model, output_path=output_path)
    print(f"README written to {output_path}")

if __name__ == "__main__":
    main()
