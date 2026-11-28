# 10 ASPレポートの自動取り込みの設定（Apps Script）

- 実行者: **Claude in Chrome**
- あなたがやること: Google の権限の「許可」（30秒）
- 依存: なし

```
あなたは Google スプレッドシートの設定担当です。オーナーのブラウザ（Googleにログイン済み）で作業します。
作業番号: 10　作業名: ASPレポートの自動取り込みの設定

# 目的
ASP の担当者から専用アドレスに届くレポートの添付ファイルを、毎時、顧客ごとの Drive フォルダに自動で振り分けるようにする。

# 前提
- 設定シート: https://docs.google.com/spreadsheets/d/18SuZA-lVYTPnatkTRLMRYoCisLgY0pkrC6FZ1_VoN-8/edit
- 貼るコード: https://raw.githubusercontent.com/rikuurawareds-gif/my-website/claude/friendly-hawking-5k5ymh/affiliate/automation/asp-intake.gs
- 専用アドレス: {{INTAKE_ADDRESS}}
- 未振り分けフォルダのID: 1Ta0AZWO52XMS8AugJ63dsSkdWd-SVidm

# 守ること
- 指示にない設定・購入・削除・送信はしない。迷ったら止まって確認する。
- パスワード、認証コード、CAPTCHA、アクセス許可の画面、支払い、本人確認、ファイル選択は、止まってオーナーに頼む。オーナーが終えたら続きから再開する。
- パスワード・APIキー・認証コードを、どこにも書き写さない。
- シートの見出し行は変更しない。

# 手順
1. コードの URL を開き、内容をすべてコピーする。
2. 設定シートを開き、「拡張機能」→「Apps Script」。Code.gs の中身を消してコードを貼り、プロジェクト名を「ASPレポート取り込み」にして保存する。
3. 「プロジェクトの設定」でタイムゾーンを「(GMT+09:00) 日本標準時 - 東京」にし、スクリプト プロパティに次の3つを追加して保存する:
   - INTAKE_ADDRESS: 前提の専用アドレス
   - UNSORTED_FOLDER: 1Ta0AZWO52XMS8AugJ63dsSkdWd-SVidm
   - RULES_FOLDER: 1XESUcnk2cU6h6PN0AX-H2JZUSjtXBfyW
4. エディタで関数「setup」を実行する。権限の承認はオーナーに頼む。
5. エラーなく終わったことを確認する（顧客がまだいないので、何も振り分けられなくて正常）。

# 終わったら
1. 次の Google ドキュメントの一番下に追記する: https://docs.google.com/document/d/1h3CYlzcAakR8DB2nmBx2qvGakh9Z7z5Zahi3_SNWSzM/edit
   ## 10 ASPレポートの自動取り込みの設定（YYYY-MM-DD HH:MM）
   - 状態: 完了 / 途中で停止（理由）
   - 結果: setup 実行=成功、毎時のトリガー=登録済み
   - オーナーの対応が必要なこと: （なければ「なし」）
2. オーナーに、終わったことを短く伝える。
```
