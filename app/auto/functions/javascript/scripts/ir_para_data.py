SCRIPT_IR_PARA_DATA = """
    var data = arguments[0];

    // Verificar se o elemento existe antes de manipulá-lo
    var campo = document.getElementById('controleDataPreSelecao');
    if (!campo) {
        return "Erro: Elemento 'controleDataPreSelecao' não encontrado";
    }

    // Tentar usar o datepicker do jQuery se disponível
    if (typeof $ !== 'undefined' && $.fn.datepicker) {
        $('#controleDataPreSelecao').datepicker('setDate', data);
    }

    // Atualizar o onclick e clicar
    var novoOnclick = "__doPostBack('ctl00$cphFuncionalidade$ControleFrequencia','" + data + "')";
    campo.setAttribute('onclick', novoOnclick);
    campo.click();

    return "Data definida e onclick atualizado para: " + data;
"""