import json
import os

from selenium.webdriver.chrome.options import Options

from app.config.parâmetros import parâmetros


class ParâmetrosWebdriver:

    @property
    def impressão(self):
        pasta_temporária = os.path.join(parâmetros.novo_diretório)

        settings = {
            "recentDestinations" : [{"id" : "Save as PDF", "origin" : "local", "account" : ""}],
            "selectedDestinationId" : "Save as PDF",
            "version" : 2,
            "isHeaderFooterEnabled" : False,
            "scalingType" : 3,
            "scaling" : "95",
            "mediaSize" : {"height_microns" : 297000,  # Paisagem: altura menor
                           "width_microns" : 420000,  # Paisagem: largura maior
                           "name" : "ISO_A3",
                           "is_continuous_feed" : False},
            "landscape" : True,  # <- ESSA LINHA garante o modo paisagem
            "backgroundGraphicsEnabled" : False
        }
        # Preferências do navegador
        prefs = {
            "printing.print_preview_sticky_settings.appState" : json.dumps(settings),
            "savefile.default_directory": pasta_temporária
        }
        # Aplicando configurações no navegador
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--kiosk-printing")  # imprime sem abrir diálogo
        return chrome_options


