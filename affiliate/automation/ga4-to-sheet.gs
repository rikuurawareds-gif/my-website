/**
 * GA4 → KPI_週次 シートへ前週分を自動追記する Apps Script。
 *
 * 設定手順（1回だけ・オーナー作業 約5分）:
 *  1. KPI_週次 シートを開く → 拡張機能 → Apps Script
 *  2. このファイルの中身を貼り付ける。GA4_PROPERTY_ID を自分の数字に変える
 *     （GA4 管理 → プロパティの詳細 に出る「プロパティID」。G-から始まるIDではない）
 *  3. 左の「サービス」+ → 「Google Analytics Data API」を追加
 *  4. 関数 setupWeeklyTrigger を選んで実行 → 権限を許可
 *  以後、毎週月曜6時台に前週（月〜日）の数字が自動で追記される。
 */
const GA4_PROPERTY_ID = '000000000';
const SHEET_NAME = null; // null なら先頭シート

const EVENTS = ['page_view', 'form_start', 'generate_lead', 'affiliate_click'];

function setupWeeklyTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'importLastWeek')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('importLastWeek')
    .timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(6).create();
  importLastWeek();
}

function importLastWeek() {
  const tz = Session.getScriptTimeZone();
  const today = new Date();
  const dow = (today.getDay() + 6) % 7; // 月曜=0
  const thisMonday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - dow);
  const start = new Date(thisMonday.getTime() - 7 * 86400000);
  const end = new Date(thisMonday.getTime() - 86400000);
  const fmt = d => Utilities.formatDate(d, tz, 'yyyy-MM-dd');
  const range = [{ startDate: fmt(start), endDate: fmt(end) }];
  const prop = 'properties/' + GA4_PROPERTY_ID;
  const notInternal = {
    notExpression: { filter: { fieldName: 'customEvent:traffic_type',
      stringFilter: { value: 'internal' } } }
  };

  // ページ別のイベント数
  const ev = AnalyticsData.Properties.runReport({
    dateRanges: range,
    dimensions: [{ name: 'customEvent:page_id' }, { name: 'eventName' }],
    metrics: [{ name: 'eventCount' }],
    dimensionFilter: { andGroup: { expressions: [
      { filter: { fieldName: 'eventName', inListFilter: { values: EVENTS } } },
      notInternal
    ] } },
    limit: 10000
  }, prop);

  // ページ別のセッション数
  const ss = AnalyticsData.Properties.runReport({
    dateRanges: range,
    dimensions: [{ name: 'customEvent:page_id' }],
    metrics: [{ name: 'sessions' }],
    dimensionFilter: notInternal,
    limit: 10000
  }, prop);

  const pages = {};
  const get = id => (pages[id] = pages[id] || { sessions: 0, page_view: 0, form_start: 0, generate_lead: 0, affiliate_click: 0 });
  (ev.rows || []).forEach(r => {
    get(r.dimensionValues[0].value)[r.dimensionValues[1].value] = Number(r.metricValues[0].value);
  });
  (ss.rows || []).forEach(r => {
    get(r.dimensionValues[0].value).sessions = Number(r.metricValues[0].value);
  });

  const ssheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = SHEET_NAME ? ssheet.getSheetByName(SHEET_NAME) : ssheet.getSheets()[0];

  // 同じ週を二重に入れない
  const existing = sheet.getRange(1, 1, Math.max(sheet.getLastRow(), 1), 1).getDisplayValues().flat();
  if (existing.indexOf(fmt(start)) !== -1) return;

  const pct = (a, b) => (b ? Math.round((a / b) * 1000) / 10 : '');
  const rows = Object.keys(pages)
    .filter(id => id && id !== '(not set)')
    .map(id => {
      const p = pages[id];
      // 列はシートの見出しと同じ順。ASP系の列は空欄（ASP取込シートから別途埋める）
      return [fmt(start), id, '全体', p.sessions, p.page_view, p.form_start, p.generate_lead,
        pct(p.generate_lead, p.form_start), p.affiliate_click, pct(p.affiliate_click, p.page_view),
        '', '', '', '', '', '', '', 'Apps Script', ''];
    });
  if (rows.length) {
    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
}
