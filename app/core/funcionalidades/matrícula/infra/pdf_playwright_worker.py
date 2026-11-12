"""Processo auxiliar do GeradorPdfPlaywright. Não importa nada do projeto.

Uso: python pdf_playwright_worker.py <entrada.html> <saida.pdf> [caminho_do_chromium]
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main(entrada: str, saida: str, executavel: str | None = None) -> None:
    html = Path(entrada).read_text(encoding="utf-8")
    with sync_playwright() as playwright:
        opcoes = {"executable_path": executavel} if executavel else {}
        navegador = playwright.chromium.launch(**opcoes)
        try:
            pagina = navegador.new_page()
            pagina.set_content(html, wait_until="load")
            pagina.emulate_media(media="print")
            # prefer_css_page_size: respeita o @page (A4, margem 0) do HTML; print_background: mantém as cores de fundo.
            pagina.pdf(path=saida, prefer_css_page_size=True, print_background=True)
        finally:
            navegador.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
