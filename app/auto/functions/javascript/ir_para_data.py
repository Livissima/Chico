SCRIPT_IR_PARA_DATA = """
    var data = arguments[0];

    $('#controleDataPreSelecao').datepicker('setDate', data);

    var campo = document.getElementById('controleDataPreSelecao');
    var novoOnclick = "__doPostBack('ctl00$cphFuncionalidade$ControleFrequencia','" + data + "')";
    campo.setAttribute('onclick', novoOnclick);

    campo.click();

    return "Data definida e onclick atualizado para: " + data;
    """