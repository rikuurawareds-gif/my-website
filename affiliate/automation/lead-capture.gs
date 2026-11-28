/**
 * サービスLPの相談フォーム → Drive「09_集客/リード管理」シートに追記する Apps Script。
 *
 * 設定手順（1回だけ・オーナー作業 約5分）:
 *  1. リード管理シートを開く → 拡張機能 → Apps Script → この中身を貼る
 *  2. デプロイ → 新しいデプロイ → 種類「ウェブアプリ」
 *     実行ユーザー: 自分 ／ アクセスできるユーザー: 全員 → デプロイ → 権限を許可
 *  3. 表示されたURLを PM に伝える（site/assets/config.js の leadEndpoint に入れる）
 *  通知: 申込のたびに、このスクリプトの持ち主（デプロイした Google アカウント）にメールが届く。
 *  宛先を変えたいときはスクリプト プロパティ NOTIFY_EMAIL に入れる。止めたいときは NOTIFY_EMAIL を off にする。
 *  （公開リポジトリなので、アドレスはコードに書かない）
 */
function notifyTo_() {
  const p = PropertiesService.getScriptProperties().getProperty('NOTIFY_EMAIL');
  if (p === 'off') return '';
  return p || Session.getEffectiveUser().getEmail();
}

function doPost(e) {
  const d = JSON.parse(e.postData.contents || '{}');
  const a = (d.diagnosis && d.diagnosis.answers) || {};
  const label = {
    asp: ['1社', '2〜3社', '4〜6社', '7社以上'], media: ['〜20', '21〜100', '101〜300', '301以上'],
    cv: ['〜50件', '51〜200件', '201〜500件', '501件以上']
  };
  const clean = v => String(v == null ? '' : v).slice(0, 2000).replace(/^[=+\-@]/, "'$&"); // 数式の注入を防ぐ
  const row = [
    new Date(), d.source, d.company, d.name, d.email, '', d.spend,
    label.asp[a.asp] || '', label.media[a.media] || '', label.cv[a.cv] || '',
    a.approve || '', a.check || '', a.dev || '', a.report || '',
    d.diagnosis ? d.diagnosis.hours : '', d.diagnosis ? d.diagnosis.yen : '',
    '［' + (d.type || '') + '］' + (d.freecheck ? '【無料表記チェック希望: ' + (d.product || '商品名未記入') + '】' : '') + (d.message || ''),
    '新規', '', ''
  ].map(clean);
  row[0] = new Date(); // 日時は日付型のまま入れる
  SpreadsheetApp.getActiveSpreadsheet().getSheets()[0].appendRow(row);
  const to = notifyTo_();
  if (to) {
    const body = ['日時', '流入元', '会社名', 'お名前', 'メール', '', '媒体費', 'ASP数', 'メディア数', '成果件数', '承認', '表記チェック', '開拓', 'レポート', '診断の工数(h)', '診断の金額', '内容']
      .map((k, i) => k ? k + ': ' + row[i] : '').filter(Boolean).join('\n');
    MailApp.sendEmail(to, '【アフィまかせ 新規の相談】' + clean(d.company), body + '\n\nリード管理シートにも記録しました。');
  }
  return ContentService.createTextOutput('ok');
}
