lista_xpaths = []

lista_elementos = list(range(0, 30))
for índice, justificativa in enumerate(lista_elementos) :
    xpath = f'//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]/div[{índice + 1}]'
    lista_xpaths.append(xpath)


print(lista_xpaths)