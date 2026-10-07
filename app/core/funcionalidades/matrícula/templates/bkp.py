def montar_html_completo(corpo_html):
    """Gera o HTML com validação de dados em tempo real e sincronização dinâmica com o tema do Streamlit."""
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    /* Variáveis Padrão (Fallback Modo Claro) */
    :root {{
      --text-main: #31333F;
      --text-label: #31333F;
      --bg-input: #F0F2F6;
      --border-input: #C3C6D0;
      --text-input: #31333F;
      --border-secao: #E0E0E0;
      --bg-invalido: #FFE6E6;
      --border-invalido: #FF2B2B;
      --msg-erro: #D32F2F;
    }}

    body {{
      font-family: system-ui, -apple-system, sans-serif;
      color: var(--text-main);
      padding: 10px;
      margin: 0;
      background: transparent;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 12px;
      width: 100%;
      box-sizing: border-box;
    }}
    .campo-box {{
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
      min-width: 0;
      position: relative;
    }}
    label {{
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 4px;
      color: var(--text-label);
    }}
    input, select {{
      padding: 8px 10px;
      border: 1px solid var(--border-input);
      border-radius: 6px;
      font-size: 14px;
      outline: none;
      box-sizing: border-box;
      width: 100%;
      background: var(--bg-input);
      color: var(--text-input);
      transition: border-color 0.2s, background-color 0.2s, color 0.2s;
    }}
    input:focus, select:focus {{
      border-color: #FF4B4B;
      box-shadow: 0 0 0 1px #FF4B4B;
    }}
    /* Estilos de Validação */
    input.invalido, select.invalido {{
      border-color: var(--border-invalido) !important;
      background-color: var(--bg-invalido);
    }}
    .erro-mensagem {{
      color: var(--msg-erro);
      font-size: 11px;
      margin-top: 3px;
      display: none;
    }}
    .campo-box.com-erro .erro-mensagem {{
      display: block;
    }}
    .secao-titulo {{
      font-size: 18px;
      font-weight: 600;
      margin: 20px 0 12px 0;
      border-bottom: 2px solid var(--border-secao);
      padding-bottom: 6px;
      color: var(--text-main);
    }}
    .oculto {{ display: none !important; }}

    button {{
      background-color: #FF4B4B;
      color: white;
      border: none;
      padding: 12px 24px;
      font-size: 16px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 20px;
      width: 100%;
    }}
    button:hover {{ background-color: #E03E3E; }}
  </style>
</head>
<body>

  <form id="formMatricula" novalidate>
    {corpo_html}
    <button type="submit">Gerar Ficha de Matrícula</button>
  </form>

  <script>
    function sendToStreamlit(type, data) {{
      window.parent.postMessage(Object.assign({{
        isStreamlitMessage: true,
        type: type
      }}, data), "*");
    }}

    function setFrameHeight() {{
      sendToStreamlit("streamlit:setFrameHeight", {{
        height: document.body.scrollHeight + 30
      }});
    }}

    function setComponentValue(val) {{
      sendToStreamlit("streamlit:setComponentValue", {{ value: val }});
    }}

    // --- SINCRONIZAÇÃO DINÂMICA DE TEMA DO STREAMLIT ---
    function aplicarTemaStreamlit(theme) {{
      if (!theme) return;
      const root = document.documentElement;

      if (theme.textColor) {{
        root.style.setProperty('--text-main', theme.textColor);
        root.style.setProperty('--text-label', theme.textColor);
        root.style.setProperty('--text-input', theme.textColor);
      }}

      if (theme.secondaryBackgroundColor) {{
        root.style.setProperty('--bg-input', theme.secondaryBackgroundColor);
      }}

      // Detecta se o fundo do Streamlit é escuro ou claro
      const isDark = theme.base === 'dark' || (theme.backgroundColor && isCorEscura(theme.backgroundColor));

      if (isDark) {{
        root.style.setProperty('--border-input', '#464853');
        root.style.setProperty('--border-secao', '#31333F');
        root.style.setProperty('--bg-invalido', '#331A1A');
        root.style.setProperty('--msg-erro', '#FF6B6B');
      }} else {{
        root.style.setProperty('--border-input', '#C3C6D0');
        root.style.setProperty('--border-secao', '#E0E0E0');
        root.style.setProperty('--bg-invalido', '#FFE6E6');
        root.style.setProperty('--msg-erro', '#D32F2F');
      }}
    }}

    function isCorEscura(hex) {{
      if (!hex || hex.length < 7) return false;
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
      return luma < 128;
    }}

    // --- REGRAS DE VALIDAÇÃO LOGICA ---

    function validarDataValida(strData, minAno = 1900, maxAno = new Date().getFullYear()) {{
      if (!strData || strData.length < 10) return false;
      const partes = strData.split('/');
      if (partes.length !== 3) return false;

      const dia = parseInt(partes[0], 10);
      const mes = parseInt(partes[1], 10);
      const ano = parseInt(partes[2], 10);

      if (isNaN(dia) || isNaN(mes) || isNaN(ano)) return false;
      if (ano < minAno || ano > maxAno) return false;
      if (mes < 1 || mes > 12) return false;

      const dataObj = new Date(ano, mes - 1, dia);
      return (
        dataObj.getFullYear() === ano &&
        dataObj.getMonth() === (mes - 1) &&
        dataObj.getDate() === dia
      );
    }}

    function validarCPFValido(cpf) {{
      cpf = cpf.replace(/\\D/g, '');
      if (cpf.length !== 11 || /^(\\d)\\1{{10}}$/.test(cpf)) return false;

      let soma = 0, resto;
      for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
      resto = (soma * 10) % 11;
      if (resto === 10 || resto === 11) resto = 0;
      if (resto !== parseInt(cpf.substring(9, 10))) return false;

      soma = 0;
      for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
      resto = (soma * 10) % 11;
      if (resto === 10 || resto === 11) resto = 0;
      if (resto !== parseInt(cpf.substring(10, 11))) return false;

      return true;
    }}

    function aplicarErro(el, mensagem) {{
      const box = el.closest('.campo-box');
      el.classList.add('invalido');
      if (box) {{
        box.classList.add('com-erro');
        let msgSpan = box.querySelector('.erro-mensagem');
        if (!msgSpan) {{
          msgSpan = document.createElement('span');
          msgSpan.className = 'erro-mensagem';
          box.appendChild(msgSpan);
        }}
        msgSpan.innerText = mensagem;
      }}
    }}

    function limparErro(el) {{
      const box = el.closest('.campo-box');
      el.classList.remove('invalido');
      if (box) {{
        box.classList.remove('com-erro');
      }}
    }}

    function validarCampo(el) {{
      const tipo = el.getAttribute('data-tipo');
      const valor = el.value.trim();

      if (el.closest('.oculto')) {{
        limparErro(el);
        return true;
      }}

      if (!valor) {{
        limparErro(el);
        return true;
      }}

      if (tipo === 'date') {{
        if (!validarDataValida(valor)) {{
          aplicarErro(el, 'Data inválida ou fora do intervalo.');
          return false;
        }}
      }} else if (tipo === 'cpf') {{
        if (!validarCPFValido(valor)) {{
          aplicarErro(el, 'CPF inválido.');
          return false;
        }}
      }} else if (tipo === 'telefone') {{
        const num = valor.replace(/\\D/g, '');
        if (num.length < 10 || num.length > 11) {{
          aplicarErro(el, 'Telefone incompleto.');
          return false;
        }}
      }}

      limparErro(el);
      return true;
    }}

    // --- MÁSCARAS E MUDANÇAS EM TEMPO REAL ---

    document.getElementById('formMatricula').addEventListener('input', (e) => {{
      const el = e.target;
      const tipo = el.getAttribute('data-tipo');
      const soLetras = el.getAttribute('data-letras');
      const soNumeros = el.getAttribute('data-numeros');
      let v = el.value;

      if (soNumeros === 'true') {{
        v = v.replace(/[^0-9]/g, '');
      }} else if (soLetras === 'true') {{
        v = v.replace(/[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\\s]/g, '');
      }}

      if (tipo === 'cpf') {{
        v = v.replace(/\\D/g, '').replace(/(\\d{{3}})(\\d)/, '$1.$2').replace(/(\\d{{3}})(\\d)/, '$1.$2').replace(/(\\d{{3}})(\\d{{1,2}})$/, '$1-$2');
      }} else if (tipo === 'date') {{
        v = v.replace(/\\D/g, '').replace(/(\\d{{2}})(\\d)/, '$1/$2').replace(/(\\d{{2}})(\\d)/, '$1/$2').replace(/(\\d{{4}})\\d+?$/, '$1');
      }} else if (tipo === 'telefone') {{
        v = v.replace(/\\D/g, '');
        if (v.length > 10) v = v.replace(/^(\\d{{2}})(\\d{{5}})(\\d{{4}}).*/, '($1) $2-$3');
        else if (v.length > 6) v = v.replace(/^(\\d{{2}})(\\d{{4}})(\\d{{0,4}}).*/, '($1) $2-$3');
        else if (v.length > 2) v = v.replace(/^(\\d{{2}})(\\d{{0,5}})/, '($1) $2');
      }}

      el.value = v;
    }});

    document.getElementById('formMatricula').addEventListener('focusout', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {{
        validarCampo(e.target);
      }}
    }});

    function checarDependencias() {{
      const camposCondicionais = document.querySelectorAll('[data-depende-de]');
      camposCondicionais.forEach(box => {{
        const paiId = box.getAttribute('data-depende-de');
        const valorEsperado = box.getAttribute('data-valor-esperado');
        const elPai = document.getElementById(paiId);
        if (elPai) {{
          if (elPai.value === valorEsperado) {{
            box.classList.remove('oculto');
          }} else {{
            box.classList.add('oculto');
            const input = box.querySelector('input, select, textarea');
            if (input) {{
              input.value = '';
              limparErro(input);
            }}
          }}
        }}
      }});
      setFrameHeight();
    }}

    document.getElementById('formMatricula').addEventListener('change', checarDependencias);
    checarDependencias();

    document.getElementById('formMatricula').addEventListener('submit', (e) => {{
      e.preventDefault();

      const elementos = e.target.querySelectorAll('input, select, textarea');
      let formularioValido = true;

      elementos.forEach(el => {{
        if (!validarCampo(el)) {{
          formularioValido = false;
        }}
      }});

      if (!formularioValido) {{
        setFrameHeight();
        return;
      }}

      const dados = {{}};
      elementos.forEach(el => {{
        if (el.id && !el.closest('.oculto')) dados[el.id] = el.value;
      }});

      setComponentValue(dados);
    }});

    window.addEventListener("message", (e) => {{
      if (e.data && e.data.type === "streamlit:render") {{
        if (e.data.theme) {{
          aplicarTemaStreamlit(e.data.theme);
        }}
        setFrameHeight();
      }}
    }});

    sendToStreamlit("streamlit:componentReady", {{ apiVersion: 1 }});
    setTimeout(setFrameHeight, 100);
  </script>
</body>
</html>
"""