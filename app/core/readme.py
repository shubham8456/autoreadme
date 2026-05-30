from pathlib import Path

from app.config import OLLAMA_MODEL, OUTPUT_FILENAME
from app.core.prompt import build_user_prompt, load_system_prompt
from app.core.repo import scan_repository
from app.ollama.service import ensure_model, generate_markdown

def generate_readme(repo_path: Path, model: str, output_path: Path) -> None:
    print("[autoreadme] Starting AutoReadme\n", flush=True)

    ensure_model(OLLAMA_MODEL)
    print("[autoreadme] Ollama is ready", flush=True)
    print(f"[autoreadme] Using model: {OLLAMA_MODEL}\n", flush=True)

    context = scan_repository(repo_path)
    system_prompt = load_system_prompt()
    user_prompt = build_user_prompt(context)

    print("\n[autoreadme] Generating README with Ollama...", flush=True)
    markdown = generate_markdown(model=model, system_prompt=system_prompt, user_prompt=user_prompt)
    print("[autoreadme] README generation complete", flush=True)

    print(f"[autoreadme] Writing output to {OUTPUT_FILENAME}", flush=True)
    output_path.write_text(markdown.strip() + "\n", encoding="utf-8")
    print("\n[autoreadme] Done\n", flush=True)
