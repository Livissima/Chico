# app/__metadata__.py
"""Módulo simples para ler metadados do pyproject.toml"""

import tomllib
from pathlib import Path


def _get_metadata() :
    """Lê os metadados do pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f :
        return tomllib.load(f)


# Carrega os dados uma vez
_data = _get_metadata()

# Exporta as variáveis diretamente
PROJECT_NAME = _data["project"]["name"]
PROJECT_VERSION = _data["project"]["version"]