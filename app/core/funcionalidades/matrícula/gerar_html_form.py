def gerar_html_formulário(secoes) :
    """Converte o objeto TODAS_AS_SECOES em HTML calculando a proporção exata de cada coluna."""
    html_buffer = []

    for sec in secoes :
        titulo = getattr(sec, "título", getattr(sec, "titulo", ""))
        html_buffer.append(f'<div class="secao-titulo">{titulo}</div>')

        for linha in sec.linhas :
            props = getattr(linha, "proporções", getattr(linha, "proporcoes", []))
            qtd_campos = len(linha.campos)

            # Caso não haja proporções definidas, distribui uniformemente
            if not props or len(props) != qtd_campos :
                props = [1] * qtd_campos

            soma_props = sum(props) if sum(props) > 0 else 1
            html_buffer.append('<div class="grid">')

            for idx, c in enumerate(linha.campos) :
                p = props[idx]
                # Normaliza a proporção em percentagem real do container
                flex_pct = round((p / soma_props) * 100, 4)

                chave = getattr(c, "chave", "")
                rotulo = getattr(c, "rótulo", getattr(c, "rotulo", ""))
                tipo = getattr(c, "tipo", "text")
                tipo_dado = getattr(c, "tipo_dado", "str")
                letras = getattr(c, "apenas_letras", False)
                numeros = getattr(c, "apenas_numeros", False)
                c_max = getattr(c, "cumprimento_máximo", getattr(c, "cumprimento_maximo", None))
                opcoes = getattr(c, "opções", getattr(c, "opcoes", []))
                depende = getattr(c, "depende_de", None)

                style = f"flex: 0 0 calc({flex_pct}% - 12px); max-width: calc({flex_pct}% - 12px);"
                classes = ["campo-box"]
                data_attrs = []

                if depende :
                    classes.append("oculto")
                    pai_id, val_esp = depende
                    data_attrs.append(f'data-depende-de="{pai_id}"')
                    data_attrs.append(f'data-valor-esperado="{val_esp}"')

                class_str = " ".join(classes)
                data_str = " ".join(data_attrs)

                html_buffer.append(f'<div class="{class_str}" id="box_{chave}" style="{style}"'
                                   f" {data_str}>")
                html_buffer.append(f"<label>{rotulo}</label>")

                if tipo in ["select", "radio"] :
                    html_buffer.append(f'<select id="{chave}">')
                    for opt in opcoes :
                        html_buffer.append(f'<option value="{opt}">{opt}</option>')
                    html_buffer.append("</select>")
                else :
                    attrs = [f'id="{chave}"', 'type="text"']
                    if tipo_dado :
                        attrs.append(f'data-tipo="{tipo_dado}"')
                    if letras :
                        attrs.append('data-letras="true"')
                    if numeros :
                        attrs.append('data-numeros="true"')
                    if c_max :
                        attrs.append(f'maxlength="{c_max}"')

                    if tipo_dado == "cpf" :
                        attrs.append('placeholder="000.000.000-00"')
                    elif tipo_dado == "date" :
                        attrs.append('placeholder="DD/MM/AAAA"')
                    elif tipo_dado == "telefone" :
                        attrs.append('placeholder="(00) 00000-0000"')

                    html_buffer.append(f'<input {" ".join(attrs)} />')

                html_buffer.append("</div>")
            html_buffer.append("</div>")

    return "\n".join(html_buffer)
