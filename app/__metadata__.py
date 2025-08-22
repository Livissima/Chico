import tomllib
from pathlib import Path

def _get_metadata() :
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f :
        return tomllib.load(f)

_data = _get_metadata()
PROJECT_NAME = _data["project"]["name"]
PROJECT_VERSION = _data["project"]["version"]