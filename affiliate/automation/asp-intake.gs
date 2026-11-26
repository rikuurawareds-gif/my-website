/**
 * ASP のレポートメール → 顧客ごとの Drive フォルダへ自動で振り分ける Apps Script。
 *
 * 仕組み:
 *  - ASP の担当者に、レポート（CSV）を専用アドレスへ定期送付してもらう（データの集め方 ②）
 *  - 専用アドレスはオーナーの Gmail の「+」付きアドレス（例: 名前+asp@gmail.com）。どこにも公開しない
 *  - 毎時、そのアドレス宛ての未処理メールを探し、添付の CSV / Excel を
 *    「ASP振り分け設定」シートのルールで顧客を判定して、顧客の 01_ASP成果CSV フォルダに保存する
 *  - 判定できなかったものは「未振り分け」フォルダへ。処理済みのメールにはラベルを付ける
 *
 * スクリプトのプロパティ:
 *   INTAKE_ADDRESS   … 専用アドレス（例: 名前+asp@gmail.com）
 *   UNSORTED_FOLDER  … 未振り分けフォルダのID
 *   RULES_FOLDER     … 振り分けルールの CSV（「ASP振り分け_」で始まる名前）を置くフォルダのID（PM が顧客ごとに追加する）
 *
 * 「ASP振り分け設定」シート（このスクリプトを入れるスプレッドシートの1枚目）の列:
 *   顧客ID | 顧客名 | ASP名 | 送信元に含まれる文字（メールアドレスやドメイン） | 件名に含まれる文字 | 保存先フォルダID
 *
 * 初回: setup() を実行（毎時の実行を登録）。
 */

const LABEL_DONE = 'asp-intake/処理済み';
const LABEL_UNSORTED = 'asp-intake/未振り分け';

function setup() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'intake')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('intake').timeBased().everyHours(1).create();
  intake();
}

function intake() {
  const p = PropertiesService.getScriptProperties();
  const address = p.getProperty('INTAKE_ADDRESS');
  if (!address) throw new Error('INTAKE_ADDRESS が未設定');
  const done = GmailApp.getUserLabelByName(LABEL_DONE) || GmailApp.createLabel(LABEL_DONE);
  const unsortedLabel = GmailApp.getUserLabelByName(LABEL_UNSORTED) || GmailApp.createLabel(LABEL_UNSORTED);
  const rules = loadRules_();
  const unsortedFolderId = p.getProperty('UNSORTED_FOLDER');

  const threads = GmailApp.search('to:' + address + ' has:attachment -label:"' + LABEL_DONE + '" newer_than:60d', 0, 50);
  threads.forEach(th => {
    let allSorted = true;
    th.getMessages().forEach(msg => {
      const from = msg.getFrom().toLowerCase();
      const subject = msg.getSubject();
      const rule = rules.find(r =>
        (!r.from || from.indexOf(r.from) !== -1) &&
        (!r.subject || subject.indexOf(r.subject) !== -1) &&
        (r.from || r.subject));
      msg.getAttachments().forEach(att => {
        const name = att.getName();
        if (!/\.(csv|tsv|xlsx?|zip)$/i.test(name)) return;
        const stamp = Utilities.formatDate(msg.getDate(), 'Asia/Tokyo', 'yyyyMMdd_HHmm');
        if (rule) {
          DriveApp.getFolderById(rule.folderId)
            .createFile(att.copyBlob().setName(stamp + '_' + rule.asp + '_' + name));
        } else {
          allSorted = false;
          if (unsortedFolderId) {
            DriveApp.getFolderById(unsortedFolderId)
              .createFile(att.copyBlob().setName(stamp + '_' + sanitize_(from) + '_' + name));
          }
        }
      });
    });
    th.addLabel(done);
    if (!allSorted) th.addLabel(unsortedLabel);
  });
}

function loadRules_() {
  let values = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0].getDataRange().getValues().slice(1);
  const folderId = PropertiesService.getScriptProperties().getProperty('RULES_FOLDER');
  if (folderId) {
    const files = DriveApp.getFolderById(folderId).getFiles();
    while (files.hasNext()) {
      const f = files.next();
      if (f.getName().indexOf('ASP振り分け_') !== 0) continue;
      values = values.concat(Utilities.parseCsv(f.getBlob().getDataAsString('UTF-8')).slice(1));
    }
  }
  return values
    .filter(v => v[5])
    .map(v => ({
      clientId: String(v[0]), client: String(v[1]), asp: String(v[2]) || 'ASP',
      from: String(v[3] || '').toLowerCase().trim(), subject: String(v[4] || '').trim(), folderId: String(v[5]).trim()
    }));
}

function sanitize_(s) {
  return s.replace(/[^a-z0-9@._-]/gi, '_').slice(0, 40);
}
