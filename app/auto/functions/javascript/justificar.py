SCRIPT_JUSTIFICAR = """
    const matriculasNecessarias = new Set(arguments[0]);
    const selects = document.querySelectorAll('.listaMotivoAusencia .itens select[data-matricula]');
    const resultados = [];

    selects.forEach(select => {
        const matricula = select.getAttribute('data-matricula');
        if (matriculasNecessarias.has(matricula)) {
            const valorAntigo = select.value;
            select.value = '1';
            const valorNovo = select.value;

            ['change', 'input', 'blur'].forEach(evento => {
                select.dispatchEvent(new Event(evento, { bubbles: true }));
            });
            resultados.push({
                matricula: matricula,
                alterado: valorNovo === '1',
                valorAntigo: valorAntigo,
                valorNovo: valorNovo
            });
        }
    });
    return resultados;
    """