import yaml
import pathlib

def load_yaml(path_like: str | pathlib.Path) -> dict:
    p = pathlib.Path(path_like)
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def render(text: str, ctx: dict) -> str:
    return text.format(**ctx)
