SCRIPT_MARCAR_FALTA_COMO_ADM = """
    const matriculasNecessarias = new Set(arguments[0]);
    const elementos = document.querySelectorAll('.listaDeFrequencias .itens div[data-matricula]');
    const matriculasClicadas = [];

    elementos.forEach(elemento => {
        const matricula = elemento.getAttribute('data-matricula');
        if (matriculasNecessarias.has(matricula)) {
            elemento.click();
            matriculasClicadas.push(matricula);
            }
        });
    return matriculasClicadas;
    """