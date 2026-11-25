/**
 * X（旧Twitter）の自動投稿（公式API経由）。Drive の「X投稿キュー.csv」を読み、
 * 「X投稿ログ」シートで状態を管理しながら、予定時刻になった投稿を1本ずつ投稿する。
 *
 * - 投稿文は PM（Claude Code）が X投稿キュー.csv に追記する。オーナーは何もしなくてよい
 * - 止めたい投稿は、ログシートの「状態」を「停止」に変える（その投稿だけ止まる）
 * - 全部止めたいときは、スクリプトのプロパティ PAUSED を true にする
 *
 * スクリプトのプロパティ（「プロジェクトの設定」→「スクリプト プロパティ」）:
 *   X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET … X Developer のキー（ここ以外に書かない）
 *   QUEUE_FILE_ID … X投稿キュー.csv のファイルID
 *   LP_URL        … 本文中の {LP_URL} を置き換えるURL
 *   DRY_RUN       … true の間は投稿せず、ログに「テスト」と書くだけ
 *   PAUSED        … true の間は何もしない
 *
 * 初回: setup() を実行（毎時の実行を登録し、キューを取り込む）。
 */

const COL = { id: 1, at: 2, text: 3, status: 4, url: 5, postedAt: 6, error: 7, memo: 8 };
const MAX_LATE_HOURS = 24; // 予定から24時間以上過ぎたものは投稿しない（まとめて連投しないため）

function props_() { return PropertiesService.getScriptProperties(); }
function sheet_() { return SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]; }

function setup() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'run')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('run').timeBased().everyHours(1).create();
  importQueue();
}

/** 毎時の実行。キューを取り込み、予定時刻を過ぎた投稿を最大1本投稿する */
function run() {
  const p = props_();
  if (String(p.getProperty('PAUSED')).toLowerCase() === 'true') return;
  importQueue();
  const sh = sheet_();
  const last = sh.getLastRow();
  if (last < 2) return;
  const rows = sh.getRange(2, 1, last - 1, 8).getValues();
  const now = new Date();
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    if (r[COL.status - 1] !== '予約') continue;
    const v = r[COL.at - 1];
    const at = Object.prototype.toString.call(v) === '[object Date]' ? v : parseJst_(String(v));
    if (!at || at > now) continue;
    const rowNo = i + 2;
    if ((now - at) / 3600000 > MAX_LATE_HOURS) {
      sh.getRange(rowNo, COL.status).setValue('期限切れ');
      continue;
    }
    postRow_(sh, rowNo, String(r[COL.text - 1]));
    return; // 1回の実行で1本だけ
  }
}

/** キューCSVから、まだログにないIDを「予約」として追加する */
function importQueue() {
  const id = props_().getProperty('QUEUE_FILE_ID');
  if (!id) return;
  const csv = Utilities.parseCsv(DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8'));
  const sh = sheet_();
  const last = sh.getLastRow();
  const known = new Set(last > 1 ? sh.getRange(2, 1, last - 1, 1).getValues().flat().map(String) : []);
  const add = [];
  csv.slice(1).forEach(c => {
    const [qid, at, text, memo] = c;
    if (!qid || known.has(qid) || !text) return;
    add.push([qid, parseJst_(at) || at, text, '予約', '', '', '', memo || '']);
  });
  if (add.length) sh.getRange(last + 1, 1, add.length, 8).setValues(add);
}

function postRow_(sh, rowNo, rawText) {
  const p = props_();
  const text = rawText.replace(/\{LP_URL\}/g, p.getProperty('LP_URL') || '');
  if (/\{LP_URL\}/.test(rawText) && !p.getProperty('LP_URL')) {
    return fail_(sh, rowNo, 'LP_URL が未設定');
  }
  if (weightedLength_(text) > 280) return fail_(sh, rowNo, '文字数オーバー（' + weightedLength_(text) + '/280）');

  if (String(p.getProperty('DRY_RUN')).toLowerCase() !== 'false') {
    sh.getRange(rowNo, COL.status).setValue('テスト');
    sh.getRange(rowNo, COL.postedAt).setValue(new Date());
    sh.getRange(rowNo, COL.error).setValue('DRY_RUN のため投稿していない: ' + text.slice(0, 40));
    return;
  }
  const url = 'https://api.x.com/2/tweets';
  const res = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ text: text }),
    headers: { Authorization: oauthHeader_('POST', url) },
    muteHttpExceptions: true
  });
  const code = res.getResponseCode();
  const body = res.getContentText();
  if (code === 201 || code === 200) {
    const tid = JSON.parse(body).data.id;
    sh.getRange(rowNo, COL.status).setValue('投稿済');
    sh.getRange(rowNo, COL.url).setValue('https://x.com/i/web/status/' + tid);
    sh.getRange(rowNo, COL.postedAt).setValue(new Date());
  } else {
    fail_(sh, rowNo, 'HTTP ' + code + ': ' + body.slice(0, 300));
  }
}

function fail_(sh, rowNo, msg) {
  sh.getRange(rowNo, COL.status).setValue('失敗');
  sh.getRange(rowNo, COL.error).setValue(msg);
}

/** 動作確認用: 次に投稿される予定の1本を、投稿せずに表示する */
function preview() {
  importQueue();
  const rows = sheet_().getDataRange().getValues().slice(1).filter(r => r[COL.status - 1] === '予約');
  Logger.log(rows.length ? rows[0].slice(0, 3).join(' | ') : '予約なし');
}

// ---- 共通 ----

function parseJst_(s) {
  if (!s) return null;
  try { return Utilities.parseDate(String(s).trim(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm'); } catch (e) { return null; }
}

/** X の文字数（日本語などは2、URLは23として数える） */
function weightedLength_(t) {
  t = t.replace(/https?:\/\/\S+/g, 'x'.repeat(23));
  let n = 0;
  for (const ch of t) {
    const o = ch.codePointAt(0);
    n += (o <= 0x10FF || (o >= 0x2000 && o <= 0x200D) || (o >= 0x2010 && o <= 0x201F) || (o >= 0x2032 && o <= 0x2037)) ? 1 : 2;
  }
  return n;
}

function enc_(s) {
  return encodeURIComponent(s).replace(/[!*'()]/g, c => '%' + c.charCodeAt(0).toString(16).toUpperCase());
}

/** OAuth 1.0a の Authorization ヘッダー（JSON本文は署名に含めない） */
function oauthHeader_(method, url, fixed) {
  const p = props_();
  const o = {
    oauth_consumer_key: p.getProperty('X_API_KEY'),
    oauth_nonce: fixed ? fixed.nonce : Utilities.getUuid().replace(/-/g, ''),
    oauth_signature_method: 'HMAC-SHA1',
    oauth_timestamp: fixed ? fixed.timestamp : String(Math.floor(Date.now() / 1000)),
    oauth_token: p.getProperty('X_ACCESS_TOKEN'),
    oauth_version: '1.0'
  };
  return buildOauthHeader_(method, url, o, p.getProperty('X_API_SECRET'), p.getProperty('X_ACCESS_SECRET'), fixed && fixed.extra);
}

function buildOauthHeader_(method, url, o, consumerSecret, tokenSecret, extraParams) {
  const all = Object.assign({}, o, extraParams || {});
  const paramStr = Object.keys(all).sort().map(k => enc_(k) + '=' + enc_(all[k])).join('&');
  const base = method.toUpperCase() + '&' + enc_(url) + '&' + enc_(paramStr);
  const key = enc_(consumerSecret) + '&' + enc_(tokenSecret);
  const sig = Utilities.base64Encode(Utilities.computeHmacSignature(Utilities.MacAlgorithm.HMAC_SHA_1, base, key));
  const h = Object.assign({}, o, { oauth_signature: sig });
  return 'OAuth ' + Object.keys(h).sort().map(k => enc_(k) + '="' + enc_(h[k]) + '"').join(', ');
}
