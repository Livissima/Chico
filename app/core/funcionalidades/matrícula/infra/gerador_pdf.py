"""Geração de PDF a partir do HTML da ficha, usando um navegador Chromium.

Dois motores com a mesma interface (`GeradorPdf`, ver servico.py); a escolha é feita em composicao.py:

- GeradorPdfNavegador : usa o Edge ou o Chrome que já estão instalados no Windows (não instala nada).
- GeradorPdfPlaywright: usa o Chromium do Playwright (`pip install playwright` + `playwright install chromium`).

Em ambos o fundo das seções sai impresso (as cores de fundo são forçadas) e o tamanho da página
vem do `@page` do próprio HTML (A4).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_WORKER_PLAYWRIGHT = Path(__file__).resolve().parent / "pdf_playwright_worker.py"


class ErroGeracaoPdf(RuntimeError):
    pass


def _executaveis_conhecidos() -> list[Path]:
    """Onde o Edge/Chrome costumam estar no Windows (e o que houver no PATH)."""
    pastas = [os.environ.get(v) for v in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA")]
    relativos = (
        r"Microsoft\Edge\Application\msedge.exe",
        r"Google\Chrome\Application\chrome.exe",
    )
    candidatos = [Path(pasta) / rel for rel in relativos for pasta in pastas if pasta]
    for nome in ("msedge", "chrome", "google-chrome", "chromium", "chromium-browser"):
        if (achado := shutil.which(nome)):
            candidatos.append(Path(achado))
    return candidatos


def localizar_navegador() -> Path:
    for caminho in _executaveis_conhecidos():
        if caminho.is_file():
            return caminho
    raise ErroGeracaoPdf(
        "Não encontrei o Edge nem o Chrome neste computador. Instale um deles, "
        "ou use GeradorPdfPlaywright em composicao.py."
    )


class GeradorPdfNavegador:
    """Edge/Chrome em modo headless: `--print-to-pdf`."""

    def __init__(self, executavel: str | Path | None = None, tempo_limite: int = 90) -> None:
        self._executavel = Path(executavel) if executavel else None
        self._tempo_limite = tempo_limite

    def gerar(self, html: str) -> bytes:
        executavel = self._executavel or localizar_navegador()
        with tempfile.TemporaryDirectory(prefix="ficha_pdf_") as pasta:
            pasta = Path(pasta)
            entrada, saida = pasta / "ficha.html", pasta / "ficha.pdf"
            entrada.write_text(html, encoding="utf-8")

            comando = [
                str(executavel),
                "--headless",
                "--disable-gpu",
                "--no-first-run",
                "--disable-extensions",
                "--no-pdf-header-footer",
                # Perfil temporário próprio: com um Edge/Chrome já aberto no perfil padrão, o modo headless
                # seria absorvido pela janela existente e nenhum PDF seria gerado.
                f"--user-data-dir={pasta / 'perfil'}",
                f"--print-to-pdf={saida}",
                entrada.as_uri(),
            ]
            if os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() == 0:
                comando.insert(1, "--no-sandbox")  # necessário quando roda como root (ex.: contêiner Linux)

            try:
                processo = subprocess.run(comando, capture_output=True, text=True, timeout=self._tempo_limite)
            except subprocess.TimeoutExpired as erro:
                raise ErroGeracaoPdf(f"O navegador demorou mais de {self._tempo_limite}s para gerar o PDF.") from erro

            if not saida.is_file() or saida.stat().st_size == 0:
                detalhe = (processo.stderr or processo.stdout or "").strip()[-600:]
                raise ErroGeracaoPdf(f"O navegador não gerou o PDF (código {processo.returncode}). {detalhe}")
            return saida.read_bytes()


class GeradorPdfPlaywright:
    """Chromium do Playwright. Roda em um processo separado (pdf_playwright_worker.py) para não
    brigar com o laço de eventos do Streamlit, que no Windows quebra o Playwright em alguns casos."""

    def __init__(self, executavel_chromium: str | Path | None = None, tempo_limite: int = 120) -> None:
        self._executavel = str(executavel_chromium) if executavel_chromium else None
        self._tempo_limite = tempo_limite

    def gerar(self, html: str) -> bytes:
        with tempfile.TemporaryDirectory(prefix="ficha_pdf_") as pasta:
            pasta = Path(pasta)
            entrada, saida = pasta / "ficha.html", pasta / "ficha.pdf"
            entrada.write_text(html, encoding="utf-8")

            comando = [sys.executable, str(_WORKER_PLAYWRIGHT), str(entrada), str(saida)]
            if self._executavel:
                comando.append(self._executavel)

            try:
                processo = subprocess.run(comando, capture_output=True, text=True, timeout=self._tempo_limite)
            except subprocess.TimeoutExpired as erro:
                raise ErroGeracaoPdf(f"O Playwright demorou mais de {self._tempo_limite}s para gerar o PDF.") from erro

            if processo.returncode != 0 or not saida.is_file():
                detalhe = (processo.stderr or processo.stdout or "").strip()[-800:]
                raise ErroGeracaoPdf(f"O Playwright não gerou o PDF. {detalhe}")
            return saida.read_bytes()
