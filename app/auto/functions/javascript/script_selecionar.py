SCRIPT_SELECIONAR_DISPARANDO_EVENTO = """
    const element = arguments[0];
    const newValue = arguments[1];
    
    element.value = newValue;
    
    // Apenas o evento change que é o mais importante
    const changeEvent = new Event('change', { bubbles: true });
    element.dispatchEvent(changeEvent);
    
    // Se houver onchange nativo, executa também
    if (element.onchange) {
        element.onchange();
    }
    """