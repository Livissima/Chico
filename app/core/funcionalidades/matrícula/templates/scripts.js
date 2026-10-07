// --- COMUNICAÇÃO COM O STREAMLIT ---

function sendToStreamlit(type, data) {
  window.parent.postMessage(Object.assign({
    isStreamlitMessage: true,
    type: type
  }, data), "*");
}

function setFrameHeight() {
  sendToStreamlit("streamlit:setFrameHeight", {
    height: document.body.scrollHeight + 30
  });
}

function setComponentValue(val) {
  sendToStreamlit("streamlit:setComponentValue", { value: val });
}

// --- SINCRONIZAÇÃO DINÂMICA DE TEMA (MODO CLARO / MODO ESCURO) ---

function aplicarTemaStreamlit(theme) {
  if (!theme) return;
  const root = document.documentElement;

  if (theme.textColor) {
    root.style.setProperty('--text-main', theme.textColor);
    root.style.setProperty('--text-label', theme.textColor);
    root.style.setProperty('--text-input', theme.textColor);
  }

  if (theme.secondaryBackgroundColor) {
    root.style.setProperty('--bg-input', theme.secondaryBackgroundColor);
  }

  // Detecta se o fundo do Streamlit é escuro ou claro
  const isDark = theme.base === 'dark' || (theme.backgroundColor && isCorEscura(theme.backgroundColor));

  if (isDark) {
    root.style.setProperty('--border-input', '#464853');
    root.style.setProperty('--border-secao', '#31333F');
    root.style.setProperty('--bg-invalido', '#331A1A');
    root.style.setProperty('--msg-erro', '#FF6B6B');
  } else {
    root.style.setProperty('--border-input', '#C3C6D0');
    root.style.setProperty('--border-secao', '#E0E0E0');
    root.style.setProperty('--bg-invalido', '#FFE6E6');
    root.style.setProperty('--msg-erro', '#D32F2F');
  }
}

function isCorEscura(hex) {
  if (!hex || hex.length < 7) return false;
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return luma < 128;
}

// --- VALIDAÇÕES LOGICAS ---

function validarDataValida(strData, minAno = 1900, maxAno = new Date().getFullYear()) {
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
}

function validarCPFValido(cpf) {
  cpf = cpf.replace(/\D/g, '');
  if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

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
}

function aplicarErro(el, mensagem) {
  const box = el.closest('.campo-box');
  el.classList.add('invalido');
  if (box) {
    box.classList.add('com-erro');
    let msgSpan = box.querySelector('.erro-mensagem');
    if (!msgSpan) {
      msgSpan = document.createElement('span');
      msgSpan.className = 'erro-mensagem';
      box.appendChild(msgSpan);
    }
    msgSpan.innerText = mensagem;
  }
}

function limparErro(el) {
  const box = el.closest('.campo-box');
  el.classList.remove('invalido');
  if (box) {
    box.classList.remove('com-erro');
  }
}

function validarCampo(el) {
  const tipo = el.getAttribute('data-tipo');
  const valor = el.value.trim();

  if (el.closest('.oculto')) {
    limparErro(el);
    return true;
  }

  if (!valor) {
    limparErro(el);
    return true;
  }

  if (tipo === 'date') {
    if (!validarDataValida(valor)) {
      aplicarErro(el, 'Data inválida ou fora do intervalo.');
      return false;
    }
  } else if (tipo === 'cpf') {
    if (!validarCPFValido(valor)) {
      aplicarErro(el, 'CPF inválido.');
      return false;
    }
  } else if (tipo === 'telefone') {
    const num = valor.replace(/\D/g, '');
    if (num.length < 10 || num.length > 11) {
      aplicarErro(el, 'Telefone incompleto.');
      return false;
    }
  }

  limparErro(el);
  return true;
}

// --- EVENT LISTENERS E MÁSCARAS ---

document.getElementById('formMatricula').addEventListener('input', (e) => {
  const el = e.target;
  const tipo = el.getAttribute('data-tipo');
  const soLetras = el.getAttribute('data-letras');
  const soNumeros = el.getAttribute('data-numeros');
  let v = el.value;

  if (soNumeros === 'true') {
    v = v.replace(/[^0-9]/g, '');
  } else if (soLetras === 'true') {
    v = v.replace(/[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]/g, '');
  }

  if (tipo === 'cpf') {
    v = v.replace(/\D/g, '').replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  } else if (tipo === 'date') {
    v = v.replace(/\D/g, '').replace(/(\d{2})(\d)/, '$1/$2').replace(/(\d{2})(\d)/, '$1/$2').replace(/(\d{4})\d+?$/, '$1');
  } else if (tipo === 'telefone') {
    v = v.replace(/\D/g, '');
    if (v.length > 10) v = v.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
    else if (v.length > 6) v = v.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
    else if (v.length > 2) v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
  }

  el.value = v;
});

document.getElementById('formMatricula').addEventListener('focusout', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
    validarCampo(e.target);
  }
});

function checarDependencias() {
  const camposCondicionais = document.querySelectorAll('[data-depende-de]');
  camposCondicionais.forEach(box => {
    const paiId = box.getAttribute('data-depende-de');
    const valorEsperado = box.getAttribute('data-valor-esperado');
    const elPai = document.getElementById(paiId);
    if (elPai) {
      if (elPai.value === valorEsperado) {
        box.classList.remove('oculto');
      } else {
        box.classList.add('oculto');
        const input = box.querySelector('input, select, textarea');
        if (input) {
          input.value = '';
          limparErro(input);
        }
      }
    }
  });
  setFrameHeight();
}

document.getElementById('formMatricula').addEventListener('change', checarDependencias);
checarDependencias();

document.getElementById('formMatricula').addEventListener('submit', (e) => {
  e.preventDefault();

  const elementos = e.target.querySelectorAll('input, select, textarea');
  let formularioValido = true;

  elementos.forEach(el => {
    if (!validarCampo(el)) {
      formularioValido = false;
    }
  });

  if (!formularioValido) {
    setFrameHeight();
    return;
  }

  const dados = {};
  elementos.forEach(el => {
    if (el.id && !el.closest('.oculto')) dados[el.id] = el.value;
  });

  setComponentValue(dados);
});

// ESCUTA EVENTOS DO STREAMLIT (RESIZING E TEMA)
window.addEventListener("message", (e) => {
  if (e.data && e.data.type === "streamlit:render") {
    if (e.data.theme) {
      aplicarTemaStreamlit(e.data.theme);
    }
    setFrameHeight();
  }
});

// INICIALIZAÇÃO DO COMPONENTE
sendToStreamlit("streamlit:componentReady", { apiVersion: 1 });
setTimeout(setFrameHeight, 100);