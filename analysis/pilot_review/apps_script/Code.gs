/**
 * Classificador da revisão cega dos falsos positivos do piloto, com dois ou mais revisores.
 *
 * As abas geradas por scripts/build_pilot_review.py ("Resumo por variante", "Codigo" e
 * "Falsos positivos") são a fonte dos itens e não são alteradas. Cada revisor grava numa
 * aba própria, "Revisão – <revisor>", criada no primeiro acesso com uma linha por alerta. A decisão sobre cada
 * variante não é tomada individualmente: ela sai da fase de consenso entre os revisores.
 * O revisor é identificado pela conta Google de quem abre o classificador, e a
 * interface mostra apenas as classificações dessa pessoa.
 *
 * Funciona pelo menu da planilha ou como app da Web (doGet).
 */

// ID da planilha, usado quando o classificador roda como app da Web.
// É o trecho da URL entre /d/ e /edit:
// https://docs.google.com/spreadsheets/d/<ESTE_TRECHO>/edit
const PLANILHA_ID = '';

const ABAS = {
  resumo: 'Resumo por variante',
  codigo: 'Codigo',
  fp: 'Falsos positivos',
};

const CABECALHO_ITENS = ['item_id', 'sample_id', 'variant', 'tipo_erro', 'resposta', 'n_violacao',
  'classificacao', 'subcategoria_se_FP-GT', 'evidencia', 'justificativa', 'revisor', 'revisado_em'];

const CLASSES = {
  fp: ['FP-GT', 'FP-FORA', 'FP-SUG', 'FP-FALSO'],
};

const EVIDENCIAS = ['Leitura do código', 'Árvore semântica', 'Documentação Flutter', 'Diretriz/ADR'];

// Código, nome curto e descrição (tradução de dataset/taxonomy.json).
const SUBCATEGORIAS = [
  ['SEM-01', 'Rótulo acessível ausente', 'Componente interativo ou informativo não expõe um rótulo suficiente para o leitor de tela.'],
  ['SEM-02', 'Rótulo acessível incorreto', 'Existe rótulo, mas ele não comunica corretamente o propósito do componente.'],
  ['SEM-03', 'Papel semântico ausente', 'Componente customizado não expõe o papel adequado (botão, link, checkbox…).'],
  ['SEM-04', 'Estado não exposto', 'Estado relevante (selecionado, marcado, expandido, habilitado) não é exposto pela semântica.'],
  ['SEM-05', 'Controle customizado inacessível', 'Controle interativo customizado não fornece informação semântica equivalente à de um controle nativo.'],
  ['INT-01', 'Alvo de toque insuficiente', 'Área interativa menor que o limiar adotado (ADR-R003).'],
  ['INT-02', 'Gesto customizado sem alternativa', 'Gesto customizado (toque duplo, pressionar longo, arrastar, pinçar) sem equivalente acessível.'],
  ['INT-03', 'Interação não exposta', 'O comportamento interativo não chega aos mecanismos de acessibilidade (ex.: ação de toque ausente na árvore semântica).'],
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Revisão do piloto')
    .addItem('Abrir classificador', 'abrirClassificador')
    .addToUi();
}

function abrirClassificador() {
  const html = HtmlService.createHtmlOutputFromFile('Classificador')
    .setWidth(1280)
    .setHeight(820);
  SpreadsheetApp.getUi().showModalDialog(html, 'Classificador do piloto');
}

/** Ponto de entrada do app da Web. */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Classificador')
    .setTitle('Classificador do piloto')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function planilha_() {
  if (PLANILHA_ID) return SpreadsheetApp.openById(PLANILHA_ID);
  const ativa = SpreadsheetApp.getActive();
  if (ativa) return ativa;
  throw new Error('Preencha PLANILHA_ID no início do Code.gs com o ID da planilha e crie uma nova versão da implantação.');
}

/* ---------- Revisor ---------- */

/** E-mail da conta que está usando o classificador ou, se o Google não informar, o nome digitado. */
function revisor_() {
  const email = Session.getActiveUser().getEmail();
  if (email) return email;
  return PropertiesService.getUserProperties().getProperty('REVISOR') || '';
}

/** Usado só quando o Google não informa o e-mail de quem acessa. */
function definirRevisor(nome) {
  const limpo = String(nome || '').trim();
  if (limpo.length < 2) throw new Error('Digite um nome com pelo menos 2 letras.');
  PropertiesService.getUserProperties().setProperty('REVISOR', limpo);
  return carregarDados();
}

function apelido_(revisor) {
  return revisor.split('@')[0].replace(/[\[\]\*\?\/\\:']/g, '').slice(0, 60);
}

function abasDoRevisor_(revisor) {
  return { itens: 'Revisão – ' + apelido_(revisor) };
}

/* ---------- Leitura ---------- */

function lerAba_(nome) {
  const sheet = planilha_().getSheetByName(nome);
  if (!sheet) throw new Error('Aba não encontrada: "' + nome + '". Confira se a planilha foi importada sem renomear as abas.');
  const values = sheet.getDataRange().getDisplayValues();
  const header = values[0].map(String);
  const rows = values.slice(1).map((linha, i) => {
    const obj = { _row: i + 2 };
    header.forEach((h, j) => { obj[h] = linha[j]; });
    return obj;
  });
  return { sheet, header, rows };
}

function chave_(sampleId, variant) {
  return sampleId + '|' + variant;
}

function itemId_(sampleId, variant, resposta, nViolacao) {
  return [sampleId, variant, resposta, nViolacao || '-'].join('|');
}

/** Alertas de falso positivo, lidos da aba de origem (iguais para todos os revisores). */
function itensDeOrigem_() {
  const itens = [];
  lerAba_(ABAS.fp).rows.filter((r) => r.sample_id).forEach((r) => itens.push({
    aba: 'fp', sample_id: r.sample_id, variant: r.variant, resposta: r.resposta, n_violacao: r.n_violacao,
    tipo_modelo: r.tipo_modelo, trecho_afetado: r.trecho_afetado, explicacao: r.explicacao, confianca_modelo: r.confianca_modelo,
  }));
  itens.forEach((it) => { it.item_id = itemId_(it.sample_id, it.variant, it.resposta, it.n_violacao); });
  return itens;
}

/** Cria a aba do revisor na primeira vez, já com uma linha por item. */
function garantirAbasDoRevisor_(revisor, itens) {
  const nomes = abasDoRevisor_(revisor);
  const ss = planilha_();
  const lock = LockService.getDocumentLock();
  lock.waitLock(20000);
  try {
    if (!ss.getSheetByName(nomes.itens)) {
      const sheet = ss.insertSheet(nomes.itens);
      const linhas = itens.map((it) => [it.item_id, it.sample_id, it.variant, it.aba.toUpperCase(), it.resposta, it.n_violacao, '', '', '', '', '', '']);
      sheet.getRange(1, 1, 1, CABECALHO_ITENS.length).setValues([CABECALHO_ITENS]).setFontWeight('bold');
      if (linhas.length) sheet.getRange(2, 1, linhas.length, CABECALHO_ITENS.length).setNumberFormat('@').setValues(linhas);
      sheet.setFrozenRows(1);
    }
  } finally {
    lock.releaseLock();
  }
  return nomes;
}

/** Devolve tudo o que a interface precisa, agrupado por variante, com as classificações do revisor atual. */
function carregarDados() {
  const revisor = revisor_();
  if (!revisor) return { precisaNome: true };

  const resumo = lerAba_(ABAS.resumo);
  const codigo = lerAba_(ABAS.codigo);
  const itens = itensDeOrigem_();
  const nomes = garantirAbasDoRevisor_(revisor, itens);

  const meus = {};
  lerAba_(nomes.itens).rows.forEach((r) => { meus[r.item_id] = r; });

  const codigos = {};
  codigo.rows.forEach((r) => { codigos[chave_(r.sample_id, r.variant)] = r; });

  const porVariante = {};
  itens.forEach((it) => {
    const mine = meus[it.item_id] || {};
    it.classificacao = mine.classificacao || '';
    it.subcategoria = mine['subcategoria_se_FP-GT'] || '';
    it.evidencia = mine.evidencia || '';
    it.justificativa = mine.justificativa || '';
    const k = chave_(it.sample_id, it.variant);
    (porVariante[k] = porVariante[k] || []).push(it);
  });

  const variantes = resumo.rows
    .filter((r) => r.sample_id && r.tipo_erro === 'FP')
    .map((r) => {
      const k = chave_(r.sample_id, r.variant);
      const lista = (porVariante[k] || []).sort((a, b) =>
        a.resposta.localeCompare(b.resposta) || Number(a.n_violacao || 0) - Number(b.n_violacao || 0));
      return {
        sample_id: r.sample_id,
        variant: r.variant,
        tipo_erro: r.tipo_erro,
        respostas_com_erro: r.respostas_com_erro,
        codigo: codigos[k] || {},
        itens: lista,
      };
    });

  return {
    revisor,
    abas: nomes,
    variantes,
    classes: CLASSES,
    evidencias: EVIDENCIAS,
    subcategorias: SUBCATEGORIAS,
  };
}

/* ---------- Gravação ---------- */

function colunas_(header, nomes) {
  return nomes.map((nome) => {
    const idx = header.indexOf(nome);
    if (idx < 0) throw new Error('Coluna não encontrada: "' + nome + '".');
    return idx + 1;
  });
}

function localizar_(tabela, filtro) {
  const linha = tabela.rows.find((r) => Object.keys(filtro).every((k) => String(r[k]) === String(filtro[k])));
  if (!linha) throw new Error('Linha não encontrada para ' + JSON.stringify(filtro) + '.');
  return linha._row;
}

function revisorObrigatorio_() {
  const revisor = revisor_();
  if (!revisor) throw new Error('Não consegui identificar quem está revisando. Feche e abra o classificador de novo.');
  return revisor;
}

/** Grava a classificação de um item na aba do revisor atual. */
function salvarItem(sampleId, variant, item) {
  const aba = item.aba;
  if (!CLASSES[aba]) throw new Error('Aba inválida.');
  if (item.classificacao && CLASSES[aba].indexOf(item.classificacao) < 0) throw new Error('Classe inválida.');
  if (item.evidencia && EVIDENCIAS.indexOf(item.evidencia) < 0) throw new Error('Evidência inválida.');

  const revisor = revisorObrigatorio_();
  const tabela = lerAba_(abasDoRevisor_(revisor).itens);
  const row = localizar_(tabela, { item_id: itemId_(sampleId, variant, item.resposta, item.n_violacao) });
  const nomes = ['classificacao', 'subcategoria_se_FP-GT', 'evidencia', 'justificativa', 'revisor', 'revisado_em'];
  const valores = [
    item.classificacao || '',
    aba === 'fp' && item.classificacao === 'FP-GT' ? (item.subcategoria || '') : '',
    item.evidencia || '',
    item.justificativa || '',
    revisor,
    new Date(),
  ];
  const cols = colunas_(tabela.header, nomes);
  cols.forEach((col, i) => { tabela.sheet.getRange(row, col).setValue(valores[i]); });
  return true;
}
