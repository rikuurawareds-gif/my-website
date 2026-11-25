# 03 相談フォームの送信先（Apps Script）

- 実行者: **Claude in Chrome**
- あなたがやること: Google の権限の「許可」画面（「詳細」→「安全ではないページに移動」→「許可」・30秒）
- 依存: なし

```
あなたは Google スプレッドシートの設定担当です。オーナーのブラウザ（Googleにログイン済み）で作業します。
作業番号: 03　作業名: 相談フォームの送信先（Apps Script）

# 目的
サービスLPの相談フォームから送られた内容が、スプレッドシート「リード管理」に自動で追記されるようにし、送信先のURLを PM に渡す。

# 前提
- リード管理シート: https://docs.google.com/spreadsheets/d/1bBkDmB2BL_lVZYOh1NkUsFBVvNNSO1VmXdvH0r3HJ1w/edit
- 貼るコード: https://raw.githubusercontent.com/rikuurawareds-gif/my-website/claude/friendly-hawking-5k5ymh/affiliate/automation/lead-capture.gs

# 守ること
- コードは上のURLの内容をそのまま使い、書き換えない（NOTIFY_EMAIL も空のまま）。
- 権限の許可画面（「このアプリは Google で確認されていません」を含む）は、止まってオーナーに頼む。オーナーが許可したら続きから再開する。
- シートの既存の見出し行は変更しない。

# 手順
1. コードのURLを新しいタブで開き、内容をすべてコピーする。
2. リード管理シートを開き、メニュー「拡張機能」→「Apps Script」を開く。
3. エディタの Code.gs（コード.gs）の中身をすべて消して、コピーしたコードを貼り付け、プロジェクト名を「リード受付」にして保存する。
4. 右上「デプロイ」→「新しいデプロイ」→ 種類の歯車で「ウェブアプリ」を選ぶ:
   - 説明: LP相談フォーム
   - 次のユーザーとして実行: 自分
   - アクセスできるユーザー: 全員
5. 「デプロイ」を押す。権限の承認を求められたら、オーナーに許可を頼む。
6. 表示された「ウェブアプリ」の URL（https://script.google.com/macros/s/.../exec）を控える。

# 終わったら
1. 次の Google ドキュメントの一番下に追記する: https://docs.google.com/document/d/1h3CYlzcAakR8DB2nmBx2qvGakh9Z7z5Zahi3_SNWSzM/edit
   ## 03 相談フォームの送信先（YYYY-MM-DD HH:MM）
   - 状態: 完了 / 途中で停止（理由）
   - 結果: ウェブアプリURL=
   - オーナーの対応が必要なこと: （なければ「なし」）
2. オーナーに、終わったことを短く伝える。
```
