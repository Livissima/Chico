from pathlib import Path


def encontrar_raiz_projeto() -> Path:
    atual = Path(__file__).resolve().parent
    for ancestral in [atual] + list(atual.parents):
        if (
            (ancestral / ".git").exists()
            or (ancestral / "pyproject.toml").exists()
            or (ancestral / "app").is_dir()
        ):
            return ancestral
    return atual
