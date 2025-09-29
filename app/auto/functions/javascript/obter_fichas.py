SCRIPT_OBTER_TABELAS_FICHAS = """
    function extrairFichas() {
        // Função para obter texto limpo com quebras de linha estratégicas
        function getCleanText(element) {
            let text = element.innerText;

            // Preservar quebras de linha estratégicas
            text = text.replace(/Dados Pessoais/g, '\\nDados Pessoais\\n');
            text = text.replace(/Filiação/g, '\\n\\nFiliação\\n');
            text = text.replace(/Endereço Residencial/g, '\\n\\nEndereço Residencial\\n');
            text = text.replace(/Dados Escolares/g, '\\n\\nDados Escolares\\n');

            // Remover múltiplas quebras de linha consecutivas
            text = text.replace(/\\n{3,}/g, '\\n\\n');

            // Remover espaços em excesso
            text = text.replace(/[\\s]{2,}/g, ' ');

            return text.trim();
        }

        var body = document.querySelector('body');
        var todasTabelas = body.querySelectorAll('table');
        var resultado = [];

        // Filtrar tabelas com height='60%' e adicionar à lista
        for (var i = 0; i < todasTabelas.length; i++) {
            var tabela = todasTabelas[i];
            if (tabela.getAttribute('height') === '60%') {
                resultado.push(getCleanText(tabela));
            }
        }

        return resultado;
    }
    return extrairFichas();
    """
