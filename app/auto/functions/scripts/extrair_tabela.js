function extrairTabelas() {
    var tabelas = document.querySelectorAll('table.tabela');
    var resultados = [];

    for (var i = 0; i < tabelas.length; i++) {
        var tabela = tabelas[i];
        var dados = [];
        var cabecalhos = [];

        // Extrair cabeçalhos
        var ths = tabela.querySelectorAll('thead th');
        if (ths.length > 0) {
            for (var h = 0; h < ths.length; h++) {
                cabecalhos.push(ths[h].innerText.trim());
            }
        } else {
            // Tentar primeira linha como cabeçalho
            var primeiraLinha = tabela.querySelector('tbody tr');
            if (primeiraLinha) {
                var cells = primeiraLinha.querySelectorAll('td, th');
                for (var h = 0; h < cells.length; h++) {
                    cabecalhos.push(cells[h].innerText.trim());
                }
            }
        }

        // Se ainda não tem cabeçalhos, usa padrão
        if (cabecalhos.length === 0) {
            cabecalhos = [
                "Matrícula", "Aluno", "Data de Nascimento", "Nome da Mãe",
                "CPF do Responsável", "Nome do Responsável", "Telefone residencial",
                "Telefone responsável", "Telefone celular", "E-mail Alternativo",
                "E-mail Institucional", "E-mail Educacional", "Ponto ID"
            ];
        }

        // Extrair dados
        var linhas = tabela.querySelectorAll('tbody tr');
        for (var r = 0; r < linhas.length; r++) {
            var linha = linhas[r];

            // Pular linhas que parecem ser cabeçalhos
            if (linha.querySelectorAll('th').length > 0) continue;

            var celulas = linha.querySelectorAll('td');
            var linhaDados = {};

            for (var c = 0; c < celulas.length; c++) {
                var nomeColuna = cabecalhos[c] || 'coluna_' + c;
                linhaDados[nomeColuna] = celulas[c].innerText.trim();
            }

            // Só adiciona se tiver dados
            if (Object.keys(linhaDados).length > 0) {
                dados.push(linhaDados);
            }
        }

        resultados.push(...dados);
    }

    return resultados;
}

return extrairTabelas();