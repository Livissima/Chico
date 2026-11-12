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
    root.style.setProperty('--bg-valido', '#143525');
    root.style.setProperty('--border-valido', '#3FBF7F');
  } else {
    root.style.setProperty('--border-input', '#C3C6D0');
    root.style.setProperty('--border-secao', '#E0E0E0');
    root.style.setProperty('--bg-invalido', '#FFE6E6');
    root.style.setProperty('--msg-erro', '#D32F2F');
    root.style.setProperty('--bg-valido', '#E3F6E8');
    root.style.setProperty('--border-valido', '#2E9E5B');
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

// 'dd/mm/aaaa' -> Date (meia-noite local), ou null se não for uma data válida
function parseData(strData) {
  if (!validarDataValida(strData)) return null;
  const [dia, mes, ano] = strData.split('/').map(n => parseInt(n, 10));
  return new Date(ano, mes - 1, dia);
}

function calcularIdade(nascimento, hoje = new Date()) {
  let idade = hoje.getFullYear() - nascimento.getFullYear();
  const mes = hoje.getMonth() - nascimento.getMonth();
  if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) idade--;
  return idade;
}

function textoDaIdade(idade) {
  if (idade < 0) return '';
  if (idade === 0) return 'menos de 1 ano';
  return idade === 1 ? '1 ano' : idade + ' anos';
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

// --- TELEFONE (mesma lógica de dominio/telefone.py; DDD padrão 62) ---
//  8 dígitos : começa com 8 ou 9 -> celular sem o 9 extra; senão -> fixo
//  9 dígitos : precisa começar com 98 ou 99 -> celular sem DDD
// 10 dígitos : 3º dígito 8 ou 9 -> celular com DDD sem o 9 extra
// 11 dígitos : 3º dígito 9 e 4º dígito 8 ou 9 -> celular completo

const DDD_PADRAO = '62';

function interpretarTelefone(texto) {
  const invalido = (erro) => ({ ok: false, erro: erro });
  const dddInvalido = (ddd) => ddd.indexOf('0') !== -1;

  // Fixo já formatado ('(62) 3208 9777' ou '(62) 3208-9777') é aceito como está: é o valor que o próprio
  // formulário produz (10 dígitos, 3º dígito diferente de 8/9), e precisa sobreviver a ser reprocessado.
  const fixo = /^\((\d{2})\) (\d{4})[ -](\d{4})$/.exec(texto.trim());
  if (fixo) {
    if (dddInvalido(fixo[1])) return invalido('DDD inválido.');
    return { ok: true, ddd: fixo[1], numero: fixo[2] + fixo[3] };
  }

  const d = texto.replace(/\D/g, '');

  if (d.length === 8) {
    return { ok: true, ddd: DDD_PADRAO, numero: ('89'.includes(d[0]) ? '9' : '') + d };
  }
  if (d.length === 9) {
    if (d[0] !== '9' || !'89'.includes(d[1])) return invalido('com 9 dígitos, o número deve começar com 98 ou 99.');
    return { ok: true, ddd: DDD_PADRAO, numero: d };
  }
  if (d.length === 10) {
    const ddd = d.slice(0, 2), resto = d.slice(2);
    if (!'89'.includes(resto[0])) {
      return invalido('com 10 dígitos o número deve ser celular com DDD (3º dígito 8 ou 9). Telefone fixo deve ser digitado só com 8 dígitos.');
    }
    if (dddInvalido(ddd)) return invalido('DDD inválido.');
    return { ok: true, ddd: ddd, numero: '9' + resto };
  }
  if (d.length === 11) {
    const ddd = d.slice(0, 2), resto = d.slice(2);
    if (resto[0] !== '9' || !'89'.includes(resto[1])) return invalido('com 11 dígitos, o 3º dígito deve ser 9 e o 4º deve ser 8 ou 9.');
    if (dddInvalido(ddd)) return invalido('DDD inválido.');
    return { ok: true, ddd: ddd, numero: resto };
  }
  return invalido('informe 8 dígitos (fixo ou celular sem DDD), 9, 10 ou 11 dígitos.');
}

function formatarTelefone(tel, separador = ' ') {
  const corte = tel.numero.length === 9 ? 5 : 4;
  return '(' + tel.ddd + ') ' + tel.numero.slice(0, corte) + separador + tel.numero.slice(corte);
}

function mascararCep(valor) {
  const d = valor.replace(/\D/g, '').slice(0, 8);
  return d.length > 5 ? d.slice(0, 5) + '-' + d.slice(5) : d;
}

// Completa/formata o valor do campo ao sair dele (telefone com DDD e 9 extra; CEP com hífen)
function normalizarCampo(el) {
  const tipo = el.getAttribute('data-tipo');
  if (tipo === 'telefone' && el.value.trim()) {
    const tel = interpretarTelefone(el.value);
    if (tel.ok) el.value = formatarTelefone(tel, ' ');
  } else if (tipo === 'cep') {
    el.value = mascararCep(el.value);
  }
}

// --- CAMADAS DE ERRO ---
// Um campo pode ter erro de três origens; a mensagem exibida segue esta prioridade:
//   campo    : validação do próprio valor (CPF inválido, data inválida, obrigatório...)
//   regra    : regras entre campos aplicadas em tempo real (CPF repetido, datas incoerentes)
//   servidor : erros devolvidos pelo Python ao gerar o relatório (apagados quando o campo é editado)

const erros = { campo: {}, regra: {}, servidor: {} };

function idDoControle(el) {
  const grupo = el.closest('[data-multiselect]');
  return grupo ? grupo.id : el.id;
}

function mensagemDe(id) {
  return erros.campo[id] || erros.regra[id] || erros.servidor[id] || null;
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

function temValor(el) {
  if (el.hasAttribute('data-multiselect')) return el.querySelector('input:checked') !== null;
  return el.value.trim() !== '';
}

// Verde: campo preenchido, habilitado, editável e sem nenhum erro
function atualizarValido(el) {
  const elegivel = !el.disabled && !el.readOnly && !el.closest('.oculto')
    && !el.classList.contains('invalido') && temValor(el);
  el.classList.toggle('valido', elegivel);
}

function repintar(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const mensagem = mensagemDe(id);
  if (mensagem) aplicarErro(el, mensagem); else limparErro(el);
  atualizarValido(el);
}

function definirErro(camada, id, mensagem) {
  if (mensagem) erros[camada][id] = mensagem; else delete erros[camada][id];
  repintar(id);
}

function limparErrosDe(id) {
  Object.keys(erros).forEach(camada => { delete erros[camada][id]; });
  repintar(id);
}

function ignorado(el) {
  return !el || el.closest('.oculto') || el.hasAttribute('data-desab-nome');
}

function validarCampo(el) {
  if (el.type === 'checkbox') return true;

  const id = el.id;
  const tipo = el.getAttribute('data-tipo');
  const valor = el.value.trim();

  if (ignorado(el)) {
    limparErrosDe(id);
    return true;
  }

  if (!valor) {
    definirErro('campo', id, null);
    return true;
  }

  let mensagem = null;

  if (tipo === 'date') {
    if (!validarDataValida(valor)) {
      mensagem = 'Data inválida ou fora do intervalo.';
    } else if (el.hasAttribute('data-idade') && parseData(valor) > new Date()) {
      mensagem = 'A data de nascimento não pode estar no futuro.';
    }
  } else if (tipo === 'cpf') {
    if (!validarCPFValido(valor)) mensagem = 'CPF inválido.';
  } else if (tipo === 'telefone') {
    const tel = interpretarTelefone(valor);
    if (!tel.ok) mensagem = 'Telefone inválido: ' + tel.erro;
  } else if (tipo === 'cep') {
    if (valor.replace(/\D/g, '').length !== 8) mensagem = 'O CEP deve ter 8 dígitos.';
  }

  const minimo = parseInt(el.getAttribute('data-minlength') || '0', 10);
  if (!mensagem && minimo && valor.length < minimo) {
    mensagem = 'Digite no mínimo ' + minimo + ' caracteres.';
  }

  definirErro('campo', id, mensagem);
  return mensagem === null;
}

// Obrigatoriedade só é cobrada ao gerar (não incomoda quem ainda está preenchendo)
function validarObrigatorio(el) {
  if (el.type === 'checkbox' || !el.hasAttribute('data-obrigatorio')) return true;
  if (ignorado(el) || el.disabled || temValor(el)) return true;
  definirErro('campo', idDoControle(el), 'Campo obrigatório.');
  return false;
}

// --- IDADE (campos de data de nascimento) ---

function atualizarIdade(el) {
  if (!el.hasAttribute('data-idade')) return;
  const alvo = document.getElementById('idade_' + el.id);
  if (!alvo) return;
  const nascimento = (!el.disabled && !ignorado(el)) ? parseData(el.value.trim()) : null;
  alvo.textContent = nascimento ? textoDaIdade(calcularIdade(nascimento)) : '';
}

// --- VALORES E DEPENDÊNCIAS ENTRE CAMPOS ---

function valorDoCampo(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  if (el.hasAttribute('data-multiselect')) {
    return Array.from(el.querySelectorAll('input:checked')).map(i => i.value);
  }
  return el.value;
}

function dependenciaSatisfeita(box) {
  const valorPai = valorDoCampo(box.getAttribute('data-depende-de'));
  if (valorPai === null) return true;
  const esperado = box.getAttribute('data-valor-esperado');
  return Array.isArray(valorPai) ? valorPai.includes(esperado) : valorPai === esperado;
}

function restaurarPadrao(el) {
  if (el.tagName === 'SELECT') {
    const padrao = Array.from(el.options).findIndex(o => o.defaultSelected);
    el.selectedIndex = padrao >= 0 ? padrao : 0;
  } else {
    el.value = el.defaultValue;
  }
}

function limparBox(box) {
  box.querySelectorAll('input[type="checkbox"]').forEach(i => { i.checked = false; });
  box.querySelectorAll('input:not([type="checkbox"]), select, textarea').forEach(el => {
    restaurarPadrao(el);
    limparErrosDe(el.id);
    atualizarIdade(el);
  });
  box.querySelectorAll('[data-multiselect]').forEach(grupo => limparErrosDe(grupo.id));
}

function checarDependencias() {
  const caixas = document.querySelectorAll('[data-depende-de]');
  // Repete até estabilizar: esconder um campo pode esconder quem depende dele.
  for (let rodada = 0; rodada <= caixas.length; rodada++) {
    let mudou = false;
    caixas.forEach(box => {
      const visivel = dependenciaSatisfeita(box);
      if (visivel === !box.classList.contains('oculto')) return;
      box.classList.toggle('oculto', !visivel);
      if (!visivel) limparBox(box);
      mudou = true;
    });
    if (!mudou) break;
  }
  setFrameHeight();
}

// --- REGRAS ENTRE CAMPOS EM TEMPO REAL ---
// As regras vêm do Python (Esquema.regras_js) em <script id="regras-esquema">. Tipos conhecidos:
//   exige_nome    : desabilita os dados de uma pessoa enquanto o nome dela está vazio
//   cpfs_distintos: o mesmo CPF não pode aparecer em dois campos
//   ordem_datas   : uma data precisa ser anterior à outra
// As demais regras (ex.: composição familiar) só são conferidas pelo servidor ao gerar.

let regrasEsquema = [];
try {
  regrasEsquema = JSON.parse(document.getElementById('regras-esquema').textContent);
} catch (_) { /* sem regras */ }

function aplicarExigeNome(regra) {
  const nome = String(valorDoCampo(regra.nome) || '').trim();
  const bloquear = nome === '';
  regra.dependentes.forEach(id => {
    const el = document.getElementById(id);
    if (!el || el.hasAttribute('data-bloqueado')) return;
    if (bloquear) {
      el.disabled = true;
      el.setAttribute('data-desab-nome', 'true');
      limparErrosDe(id);
    } else if (el.hasAttribute('data-desab-nome')) {
      el.disabled = false;
      el.removeAttribute('data-desab-nome');
    }
    atualizarIdade(el);
  });
}

function verificarCpfsDistintos(regra, novos) {
  const porCpf = {};
  regra.chaves.forEach(id => {
    const el = document.getElementById(id);
    if (!el || ignorado(el)) return;
    const digitos = el.value.replace(/\D/g, '');
    if (digitos.length === 11) (porCpf[digitos] = porCpf[digitos] || []).push(id);
  });
  Object.values(porCpf).forEach(ids => {
    if (ids.length < 2) return;
    ids.forEach(id => {
      const outros = ids.filter(o => o !== id).map(o => regra.rotulos[o]).join(', ');
      novos[id] = 'Este CPF já foi informado em: ' + outros + '.';
    });
  });
}

function verificarOrdemDeDatas(regra, novos) {
  const elAntes = document.getElementById(regra.anterior);
  const elDepois = document.getElementById(regra.posterior);
  if (!elAntes || !elDepois || ignorado(elAntes) || ignorado(elDepois)) return;
  const antes = parseData(elAntes.value.trim());
  const depois = parseData(elDepois.value.trim());
  if (antes && depois && !(antes < depois)) novos[regra.alvo] = regra.mensagem;
}

function avaliarRegras() {
  regrasEsquema.filter(r => r.tipo === 'exige_nome').forEach(aplicarExigeNome);

  const novos = {};
  regrasEsquema.forEach(regra => {
    if (regra.tipo === 'cpfs_distintos') verificarCpfsDistintos(regra, novos);
    else if (regra.tipo === 'ordem_datas') verificarOrdemDeDatas(regra, novos);
  });

  const afetados = new Set(Object.keys(erros.regra).concat(Object.keys(novos)));
  erros.regra = novos;
  afetados.forEach(repintar);
}

// --- ERROS DEVOLVIDOS PELO SERVIDOR ---

let ultimoEnvioAplicado;

function aplicarErrosDoServidor(mapa) {
  const antes = Object.keys(erros.servidor);
  erros.servidor = Object.assign({}, mapa);
  new Set(antes.concat(Object.keys(mapa))).forEach(repintar);
  setFrameHeight();
}

// --- EVENT LISTENERS E MÁSCARAS ---

const formulario = document.getElementById('formMatricula');

formulario.addEventListener('input', (e) => {
  const el = e.target;
  const id = idDoControle(el);

  // editar um campo apaga o erro que o servidor tinha apontado nele e o verde até ser revalidado
  if (erros.servidor[id]) {
    delete erros.servidor[id];
    repintar(id);
  }
  el.classList.remove('valido');

  if (el.type !== 'checkbox') {
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
      // só dígitos enquanto digita; a formatação (DDD, 9 extra, espaço) é aplicada ao sair do campo
      v = v.replace(/\D/g, '').slice(0, 11);
    } else if (tipo === 'cep') {
      v = mascararCep(v);
    }

    if (v !== el.value) el.value = v;
    atualizarIdade(el);
  }

  avaliarRegras();
});

formulario.addEventListener('focusout', (e) => {
  const el = e.target;
  if (el.tagName === 'INPUT' || el.tagName === 'SELECT') {
    if (el.type === 'checkbox') return;
    normalizarCampo(el);
    validarCampo(el);
    avaliarRegras();
  }
});

formulario.addEventListener('change', (e) => {
  const el = e.target;
  checarDependencias();
  if (el.tagName === 'SELECT') validarCampo(el);
  if (el.type === 'checkbox') repintar(idDoControle(el));
  avaliarRegras();
});

checarDependencias();
avaliarRegras();

formulario.addEventListener('submit', (e) => {
  e.preventDefault();

  const elementos = e.target.querySelectorAll('input, select, textarea');
  let formularioValido = true;

  elementos.forEach(el => {
    if (el.type === 'checkbox') return;
    normalizarCampo(el);
    if (!validarCampo(el)) formularioValido = false;
    if (!validarObrigatorio(el)) formularioValido = false;
  });
  e.target.querySelectorAll('[data-multiselect]').forEach(grupo => {
    if (!validarObrigatorio(grupo)) formularioValido = false;
  });

  avaliarRegras();
  if (Object.keys(erros.regra).length > 0) formularioValido = false;

  if (!formularioValido) {
    setFrameHeight();
    return;
  }

  const dados = {};
  elementos.forEach(el => {
    if (el.id && !el.closest('.oculto') && !el.hasAttribute('data-desab-nome')) dados[el.id] = el.value;
  });
  e.target.querySelectorAll('[data-multiselect]').forEach(grupo => {
    if (!grupo.closest('.oculto')) {
      dados[grupo.id] = Array.from(grupo.querySelectorAll('input:checked')).map(i => i.value);
    }
  });
  // identifica esta submissão (o Python só reprocessa quando este valor muda)
  dados._envio = Date.now();

  setComponentValue(dados);
});

// ESCUTA EVENTOS DO STREAMLIT (RESIZING, TEMA E ERROS DO SERVIDOR)
window.addEventListener("message", (e) => {
  if (e.data && e.data.type === "streamlit:render") {
    if (e.data.theme) {
      aplicarTemaStreamlit(e.data.theme);
    }
    const args = e.data.args || {};
    if (args.envio !== ultimoEnvioAplicado) {
      ultimoEnvioAplicado = args.envio;
      aplicarErrosDoServidor(args.erros || {});
    }
    setFrameHeight();
  }
});

// INICIALIZAÇÃO DO COMPONENTE
sendToStreamlit("streamlit:componentReady", { apiVersion: 1 });
setTimeout(setFrameHeight, 100);
