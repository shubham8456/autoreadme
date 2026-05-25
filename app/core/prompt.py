from importlib.resources import files

from app.core.repo import RepoContext

def load_system_prompt() -> str:
    return files("app.templates").joinpath("system_prompt.txt").read_text(encoding="utf-8")

def build_user_prompt(context: RepoContext) -> str:
    header = [
        f"Repository name: {context['repo_name']}",
        f"Repository path: {context['repo_path']}",
        f"Collected files: {context['file_count']}",
        "",
        "Repository files and excerpts:",
    ]

    body = []
    for item in context["files"]:
        body.append(f"\n--- FILE: {item['path']} ---\n{item['content']}\n")

    footer = [
        "",
        "Write a high-quality README in markdown.",
        "Infer the project purpose from the code and config files.",
        "Do not invent setup steps unless the repository strongly suggests them.",
        "If some information is uncertain, keep the wording careful and practical.",
    ]

    return "\n".join(header + body + footer)
