class DiasLetivos :
    @staticmethod
    def processar(dados_json: list) -> tuple[list, dict] :
        if not dados_json :
            return [], {}

        dias_splitados = [dia.split('/') for dia in dados_json]
        lista_meses = sorted(set(dia[1] for dia in dias_splitados))

        dicionario = {mes : [dia[0] for dia in dias_splitados if dia[1] == mes] for mes in lista_meses}
        return dados_json, dicionario
