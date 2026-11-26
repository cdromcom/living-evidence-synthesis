/**
 * LIVES sheet style macros (JP, 2026-11-26): the same look as pipeline/scripts/sheet_style.py, for any Google Sheet.
 * Butterick's Practical Typography for the text, Stephen Few's Show Me the Numbers (chapter 8) for the table.
 *
 * Install: in the sheet choose Extensions > Apps Script, delete the sample code, paste this file, Save, reload the sheet.
 * A "LIVES style" menu appears. To make them macros too: Extensions > Macros > Import macro, then pick the functions
 * (applyLivesStyle is the one most people want). Nothing here changes values, only formatting.
 *
 * Rules: Spectral bold for column names, Google Sans 11 for data; no gridlines; one dark rule under the header; faint grey
 * zebra stripe; yellow fill for columns whose header starts with "JP"; numbers and brief words or phrases (up to 22
 * characters) centered; longer text left aligned and wrapped; each header aligned like its data; columns sized
 * to their data (wrapped text stops at about 460 pixels); one number format per column.
 */
var LIVES = {
  HEAD_FONT: 'Spectral',
  BODY_FONT: 'Google Sans',
  SIZE: 11,
  INK: '#222222',
  STRIPE: '#f4f4f4',
  JP_FILL: '#fff6d6',
  BRIEF: 22,            // characters: at most this many counts as a brief word or phrase
  TEXT_MAX_PX: 460,
  MIN_PX: 56,
  HEADER_ROWS: 1
};

function onOpen() {
  SpreadsheetApp.getUi().createMenu('LIVES style')
    .addItem('Apply to this sheet', 'applyLivesStyle')
    .addItem('Apply to every sheet', 'applyLivesStyleAllSheets')
    .addSeparator()
    .addItem('Fonts and header only', 'styleFontsAndHeader')
    .addItem('Align by content (centered or left)', 'alignByContent')
    .addItem('Fit column widths', 'fitColumnWidths')
    .addItem('Fit row heights', 'fitRowHeights')
    .addItem('Zebra stripes', 'addZebraStripes')
    .addItem('Mark JP columns yellow', 'markJpColumns')
    .addToUi();
}

/** The one to use: everything below, in order, on the active sheet. */
function applyLivesStyle() {
  var sheet = SpreadsheetApp.getActiveSheet();
  styleSheet_(sheet);
}

function applyLivesStyleAllSheets() {
  SpreadsheetApp.getActive().getSheets().forEach(styleSheet_);
}

function styleSheet_(sheet) {
  if (sheet.getLastRow() < 1 || sheet.getLastColumn() < 1) return;
  sheet.setHiddenGridlines(true);
  fontsAndHeader_(sheet);
  alignByContent_(sheet);
  markJpColumns_(sheet);
  zebra_(sheet);
  fitColumnWidths_(sheet);
  fitRowHeights_(sheet);
  sheet.setFrozenRows(LIVES.HEADER_ROWS);
}

/* ---------- individual macros (each works on the active sheet) ---------- */
function styleFontsAndHeader() { fontsAndHeader_(SpreadsheetApp.getActiveSheet()); }
function alignByContent() { alignByContent_(SpreadsheetApp.getActiveSheet()); }
function fitColumnWidths() { fitColumnWidths_(SpreadsheetApp.getActiveSheet()); }
function fitRowHeights() { fitRowHeights_(SpreadsheetApp.getActiveSheet()); }
function addZebraStripes() { zebra_(SpreadsheetApp.getActiveSheet()); }
function markJpColumns() { markJpColumns_(SpreadsheetApp.getActiveSheet()); }

/* ---------- implementation ---------- */
function fontsAndHeader_(sheet) {
  var rows = sheet.getLastRow(), cols = sheet.getLastColumn(), h = LIVES.HEADER_ROWS;
  var all = sheet.getRange(1, 1, rows, cols);
  all.setFontFamily(LIVES.BODY_FONT).setFontSize(LIVES.SIZE).setFontColor(LIVES.INK)
     .setFontWeight('normal').setFontStyle('normal').setFontLine('none').setVerticalAlignment('top');
  var head = sheet.getRange(1, 1, h, cols);
  head.setFontFamily(LIVES.HEAD_FONT).setFontWeight('bold').setBackground('#ffffff')
      .setWrap(true).setVerticalAlignment('bottom');
  head.setBorder(null, null, true, null, null, null, LIVES.INK, SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
}

function columnKind_(values) {
  var vals = values.filter(function (v) { return v !== '' && v !== null; });
  if (!vals.length) return 'brief';
  var numeric = vals.every(function (v) {
    return typeof v === 'number' || (typeof v === 'string' && /^[-+]?\$?\d[\d,]*(\.\d+)?%?$/.test(v.trim()));
  });
  if (numeric) return 'number';
  var longest = vals.reduce(function (m, v) { return Math.max(m, String(v).length); }, 0);
  return longest <= LIVES.BRIEF ? 'brief' : 'text';
}

function alignByContent_(sheet) {
  var h = LIVES.HEADER_ROWS, rows = sheet.getLastRow(), cols = sheet.getLastColumn();
  if (rows <= h) return;
  var data = sheet.getRange(h + 1, 1, rows - h, cols).getValues();
  for (var c = 0; c < cols; c++) {
    var kind = columnKind_(data.map(function (r) { return r[c]; }));
    var align = (kind === 'text') ? 'left' : 'center';
    var body = sheet.getRange(h + 1, c + 1, rows - h, 1);
    var head = sheet.getRange(1, c + 1, h, 1);
    body.setHorizontalAlignment(align).setWrap(kind !== 'number');
    head.setHorizontalAlignment(align).setWrap(true);
    if (kind === 'number') {
      var decimals = 0;
      data.forEach(function (r) {
        var v = r[c];
        if (typeof v === 'number' && v % 1 !== 0) decimals = Math.max(decimals, Math.min(3, String(v).split('.')[1].length));
      });
      var title = String(sheet.getRange(1, c + 1).getValue()).toLowerCase();
      var fmt = /usd|cost|\$/.test(title) ? '$#,##0.00' : (decimals ? '0.' + new Array(decimals + 1).join('0') : '0');
      body.setNumberFormat(fmt);
    }
  }
}

function markJpColumns_(sheet) {
  var h = LIVES.HEADER_ROWS, rows = sheet.getLastRow(), cols = sheet.getLastColumn();
  var headers = sheet.getRange(1, 1, 1, cols).getValues()[0];
  headers.forEach(function (name, i) {
    if (String(name).indexOf('JP') === 0) sheet.getRange(1, i + 1, Math.max(rows, 1), 1).setBackground(LIVES.JP_FILL);
  });
}

function zebra_(sheet) {
  var h = LIVES.HEADER_ROWS, rows = sheet.getLastRow(), cols = sheet.getLastColumn();
  if (rows <= h) return;
  var range = sheet.getRange(h + 1, 1, rows - h, cols);
  var rules = sheet.getConditionalFormatRules().filter(function (r) {   // replace an earlier stripe rule, keep any other rules
    var c = r.getBooleanCondition();
    return !(c && c.getCriteriaType() === SpreadsheetApp.BooleanCriteria.CUSTOM_FORMULA && c.getCriteriaValues()[0] === '=ISEVEN(ROW())');
  });
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=ISEVEN(ROW())').setBackground(LIVES.STRIPE).setRanges([range]).build());
  sheet.setConditionalFormatRules(rules);
}

function fitColumnWidths_(sheet) {
  var cols = sheet.getLastColumn(), h = LIVES.HEADER_ROWS, rows = sheet.getLastRow();
  if (rows <= h) return;
  var data = sheet.getRange(h + 1, 1, rows - h, cols).getValues();
  for (var c = 1; c <= cols; c++) {
    var kind = columnKind_(data.map(function (r) { return r[c - 1]; }));
    sheet.autoResizeColumn(c);
    var w = sheet.getColumnWidth(c);
    if (kind === 'text') w = Math.min(w, LIVES.TEXT_MAX_PX);
    sheet.setColumnWidth(c, Math.max(LIVES.MIN_PX, w + 12));
  }
}

function fitRowHeights_(sheet) {
  var rows = sheet.getLastRow();
  if (rows < 1) return;
  sheet.autoResizeRows(1, rows);   // wrapped text grows the row; rows that hold pictures keep their own height if you set it after this
}
