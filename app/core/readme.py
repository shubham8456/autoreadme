from pathlib import Path

from app.core.prompt import build_user_prompt, load_system_prompt
from app.core.repo import scan_repository
from app.ollama.service import generate_markdown

def generate_readme(repo_path: Path, model: str, output_path: Path) -> None:
    context = scan_repository(repo_path)
    system_prompt = load_system_prompt()
    user_prompt = build_user_prompt(context)
    markdown = generate_markdown(model=model, system_prompt=system_prompt, user_prompt=user_prompt)
    output_path.write_text(markdown.strip() + "\n", encoding="utf-8")
