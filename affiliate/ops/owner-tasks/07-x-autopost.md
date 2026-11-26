# 07 X の自動投稿の設定（X API ＋ Apps Script）

- 実行者: **Claude in Chrome**
- あなたがやること: 開発者規約への同意（数秒）、API の利用料のチャージ（カード入力・1分）、Google の権限の「許可」（30秒）
- 依存: 01（公開URL）、04（アフィまかせのアカウント）
- 費用の目安: 投稿1本あたり約2円（リンク付きは約30円）。平日1本でも月数十〜100円程度（第三者の情報。チャージ画面の金額で確認する）

仕組み: PM が投稿文を Drive の 09_集客 フォルダに「X投稿キュー_YYYYMM.csv」として置く → オーナーの Google 上で動くスクリプトが毎時確認し、予定時刻になった投稿を公式 API で1本ずつ投稿する。止めたい投稿は「X投稿ログ」シートの状態を「停止」に変えるだけ。

```
あなたは X（旧Twitter）の自動投稿の設定担当です。オーナーのブラウザで作業します。
作業番号: 07　作業名: X の自動投稿の設定

# 目的
サービスアカウント「アフィまかせ」で、公式APIを使った予約投稿が自動で動く状態にする。

# 前提
- 公開URL（01）と X のユーザー名（04）は、次のドキュメントにある: https://docs.google.com/document/d/1h3CYlzcAakR8DB2nmBx2qvGakh9Z7z5Zahi3_SNWSzM/edit
- 投稿ログのシート: https://docs.google.com/spreadsheets/d/1lQUPoyUg1vfRzL703pkYMAC1MSh1LD0KQ7YWj6mGNd0/edit
- 貼るコード: https://raw.githubusercontent.com/rikuurawareds-gif/my-website/claude/friendly-hawking-5k5ymh/affiliate/automation/x-autopost.gs
- 投稿キューのフォルダID: 1A-qNkwfsgXpchzldo6oy63Has1Dmw1O5

# 守ること
- X の開発者ポータルには、必ず「アフィまかせ」のアカウントでログインする。オーナーの個人アカウントで作業しない（違うアカウントのキーになってしまう）。
- APIキー・シークレット・アクセストークンは、Apps Script の「スクリプト プロパティ」にだけ貼る。受け渡しドキュメントやチャットなど、ほかの場所には絶対に書かない・読み上げない。
- 開発者規約への同意、支払い（チャージ）、Google の権限の許可は、止まってオーナーに頼む。チャージは画面で選べる最小の金額にする。
- このスクリプト以外の方法（ブラウザ操作など）で投稿しない。手順の中で投稿ボタンは押さない。
- 有料の定額プランや Premium の申込はしない。

# 手順
## A. 開発者アカウントとアプリ
1. 受け渡しドキュメントで、01 の公開URL と 04 のユーザー名を確認する。どちらかがなければ止まってオーナーに伝える。
2. x.com で「アフィまかせ」のアカウントにログインしていることを確認する（違えば、オーナーに切り替えを頼む）。
3. https://developer.x.com/ を開き、開発者ポータルに登録する。利用目的の説明を求められたら、次の文をそのまま使う:
   「自社サービス（アフィリエイト運用支援）の公式アカウントで、自社が作成したお知らせと運用ノウハウの投稿を、予約した時刻に自動で投稿するために使います。投稿の作成のみに使い、他のユーザーのデータの収集・分析・転売や、フォロー・いいね・返信の自動化は行いません。」
   規約への同意はオーナーに頼む。
4. 料金プランは「従量課金（pay-per-use／クレジット）」を選ぶ。クレジットのチャージ（支払い）はオーナーに頼む。
5. プロジェクトとアプリを作る（名前: afimakase-autopost。使えなければ末尾に数字）。
6. アプリの「User authentication settings」（ユーザー認証の設定）を開き、次のとおり設定して保存する:
   - App permissions: Read and write
   - Type of App: Web App, Automated App or Bot
   - Callback URI / Redirect URL: 01 の公開URL
   - Website URL: 01 の公開URL
7. 「Keys and tokens」で、API Key と API Key Secret を生成（または再生成）し、Access Token と Access Token Secret を生成する。Access Token の権限表示が「Read and Write」になっていることを確認する（Read only なら、6 を確認してから Access Token を再生成）。
   ※ この画面は開いたままにし、値は B の手順で直接貼る。

## B. スクリプトの設定
8. コードの URL を新しいタブで開き、内容をすべてコピーする。
9. 投稿ログのシートを開き、メニュー「拡張機能」→「Apps Script」を開く。Code.gs（コード.gs）の中身をすべて消してコードを貼り、プロジェクト名を「X自動投稿」にして保存する。
10. 左の「プロジェクトの設定」（歯車）で、タイムゾーンを「(GMT+09:00) 日本標準時 - 東京」にする。
11. 同じ画面の「スクリプト プロパティ」に、次の9つを追加して保存する:
    - X_API_KEY: 手順7の API Key
    - X_API_SECRET: 手順7の API Key Secret
    - X_ACCESS_TOKEN: 手順7の Access Token
    - X_ACCESS_SECRET: 手順7の Access Token Secret
    - QUEUE_FOLDER_ID: 1A-qNkwfsgXpchzldo6oy63Has1Dmw1O5
    - LP_URL: 01 の公開URL の末尾に ?utm_source=x&utm_medium=social&utm_campaign=post を付けたもの
    - DRY_RUN: true
    - PAUSED: false
12. エディタに戻り、関数の選択で「setup」を選んで「実行」する。権限の承認を求められたら、オーナーに許可を頼む。
13. シートに戻り、2行目以降に29件の投稿が「予約」で並んでいることを確認する。
14. エディタで関数「preview」を実行し、実行ログに最初の投稿（無料診断の案内）が表示されることを確認する。
15. スクリプト プロパティの DRY_RUN を false に変えて保存する（これで予定時刻から本番の投稿が始まる）。
16. 開発者ポータルのタブを閉じる。

# 終わったら
1. 次の Google ドキュメントの一番下に追記する: https://docs.google.com/document/d/1h3CYlzcAakR8DB2nmBx2qvGakh9Z7z5Zahi3_SNWSzM/edit
   ## 07 X の自動投稿の設定（YYYY-MM-DD HH:MM）
   - 状態: 完了 / 途中で停止（理由）
   - 結果: アプリ名=、トークンの権限=Read and Write、予約件数=、最初の投稿予定=2026-12-01 12:13、DRY_RUN=false
   - オーナーの対応が必要なこと: （なければ「なし」）
   ※ キー・シークレット・トークンの値は書かない。
2. オーナーに、終わったことを短く伝える。
```
