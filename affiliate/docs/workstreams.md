# 作業の分担表（セッションごとの担当）

複数の Claude セッションが **同じフォルダ・同じブランチ** で並行して作業する。会話は共有されないので、**連動はこのファイルと `decisions.md` で取る**。
各セッションは **作業の最初にこのファイルと `decisions.md` を読み、作業の最後に自分の欄を更新する**。

最終更新: 2026-11-28（PM）

## 体制
- **PM**（セッション「アフィリエイト運用」）: オーナーの窓口。全体に関わる判断、共通ファイルの変更、担当への指示と受け渡し。X の運用も持つ
- **SEO・AIO 担当**（セッション「SEO AIO」）: コラムの企画・執筆・公開、検索・AI 回答での露出。**コラムの判断と公開はオーナーから委任済み**（2026-11-28、オーナーが PM に直接確認。`decisions.md`）。公開後に受け渡しに書けばよい。法律の解釈に迷うもの、他社名・顧客名・元資料の数字に触れるものだけ公開前に PM に回す
- **サイトデザイン担当**（セッション「AFFデザイン」。2026-11-28 新設）: サイト全体の見た目（LP・コラムの記事と一覧・プライバシーポリシー・共通 CSS・イラストと図解）を、frontend-design スキルで ixs-llc.com のトーンに整える。**何を売るか・料金・文言の主張・運営者表示は PM が決める**（デザイン担当は形と見せ方を決める）
- **有料note 担当**（セッション「Note memo」。2026-11-28 新設）: オーナーのアフィリエイト代理店での経験（社名・顧客名は伏せる）を有料noteにして企画・執筆・販売する。**記事の本文（有料部分）は公開リポジトリに置かない**（Drive かリポジトリの外の PC のフォルダ）。名義・価格・告知は PM と決める
- 担当を増やすときは PM がこの表に欄を足す

### 使う担当（エージェント。`.claude/agents/`）
| 担当 | 使うセッション | いつ |
|---|---|---|
| `seo-planner`（SEO 企画） | SEO・AIO | いまから |
| `content-writer`（コラム執筆。コラムの書き方を定義に追加済み） | SEO・AIO | いまから |
| `seo-analyst`（SEO 分析） | SEO・AIO | 記事が検索に載り始める 2027年1月ごろから月1回 |
| `seo-rewriter`（リライト・改善） | SEO・AIO | 分析と同時。全記事の見直しは半年ごと |
| `aio-monitor`（AI 回答の監視） | SEO・AIO（AI の画面での質問は PM が Chrome で行う） | 2026年12月末から月1回 |
| `seo-editor`（編集・ファクトチェック） | SEO・AIO | 公開前に毎回（seo-editor → check.py → compliance-reviewer の順） |
| `seo-data-researcher`（独自データ） | SEO・AIO（元資料の数字を新しく使うときは PM に回す） | 必要なとき |
| `digital-pr`（外部での言及） | 計画と下書きは SEO・AIO、外部への連絡・投稿・費用の実行は PM 経由でオーナーが承認 | コラムが増えてから |
| `seo-tech`（技術面の SEO） | **PM**（build.py・共通ファイルが PM の持ち物のため） | 問題が出たとき＋四半期に1回 |
| `compliance-reviewer` と `checker/check.py` | 全員 | 公開前に毎回 |
| `x-researcher` / `x-post-writer` | PM | 毎月20日ごろ |
| 外部での言及（被リンク・プレスなど） | — | コラムが10本を超えてから PM が検討 |

## 全体に関わる判断は PM に回す
デザイン、ドメイン、LP の構成・文言、料金、運営者・法務の表示、計測（GA4）、共通のテンプレートは PM が決めて `decisions.md` に書く。担当が変えたいときは、PM に理由と案を伝える（オーナーから担当に直接頼まれた場合も、PM に知らせてから進める）。

## ファイルの持ち主
| 範囲 | 持ち主 | 他の担当がしてよいこと |
|---|---|---|
| `site/content/*.md`（コラムの原稿）、`marketing/content-plan.md`、`marketing/specs/`、`marketing/seo-reports/`、`marketing/aio-queries.md`、`marketing/aio-reports/`、`marketing/seo-data/`、`marketing/digital-pr/` | SEO・AIO | 読むだけ |
| `site/column/`、`sitemap.xml`、`llms.txt`（`build.py` の出力） | SEO・AIO が `build.py` を実行して更新 | PM も実行してよい（出力は誰が作っても同じ） |
| `site/index.html`（LP）、`site/privacy.html`、`site/assets/site.css`、`site/assets/img/`（イラスト・図解）、`site/assets/diagnosis.js`・`diagnosis.test.js`（工数診断と決裁シートの計算）、`affiliate/design/`（デザインの設計書と計画）、`site/build.py` のうち見た目の部分（CSS・HEAD・FOOT・CTA・記事と一覧の組み立て） | **サイトデザイン** | SEO・AIO は一覧の見せ方を提案（変えるときはデザイン担当に頼む）。PM は文言・料金・主張を決める |
| `site/build.py` の仕組み（Markdown の変換・sitemap・llms.txt・構造化データ）、`site/assets/config.js`・`track.js`（計測・設定）、`robots.txt` | **PM** | 変更の提案だけ |
| `marketing/x-*`、`marketing/x-research/`、`marketing/x-queue/`、`automation/x-autopost.gs`、`.claude/agents/x-*` | PM（X 運用） | 読むだけ |
| `docs/decisions.md` | 全員が追記してよい（自分の担当の決定。全体に関わる決定は PM） | 追記のみ。他人の行は書き換えない |
| `HANDOFF.md`、`CLAUDE.md`、このファイルの「体制」「持ち主」 | PM | 自分の欄の「状態」だけ更新 |
| `legal/`、`docs/` のその他、`knowledge/`、`ops/` | PM | 読むだけ |

## 新しいファイル・フォルダを作るとき
- **自分が持ち主の場所の中なら、知らせずに自由に作ってよい**（例: SEO・AIO が `marketing/specs/` の中に設計書を足す）
- **持ち主の場所の外に新しく作るときは、作る前に「受け渡し」に1行書く**（場所・用途）。PM が「ファイルの持ち主」に足す
- 作業途中のファイルは、記録（commit）するまで他のセッションには「知らないファイル」に見える。**知らないファイルを見つけたら、消したり記録したりせず、`git log` とこの表の受け渡しを見て持ち主を確かめる**。分からなければ持ち主の候補のセッションに聞く

## 経営ダッシュボードの更新（2026-11-28）
オーナーは経営ダッシュボード（claude.ai のアーティファクト。URL はメモリ `exec-dashboard` と、PM からのメッセージにある）で全体を見ている。**各担当は作業の区切りごとに、自分のプロジェクトの行（状況・進捗・いま・次の一手・オーナー待ち）を更新し、「最近の動き」に1行足す。** 書き方はメモリ `exec-dashboard` のとおり。担当が増えたら、その担当が自分の行を足す

## 記録と公開のルール（push すると自動で公開される）
1. 記録するのは **自分が持ち主のファイルだけ**。`git add -A` / `git add .` / `git commit -a` は使わない。`git add <パス>` で指定する
2. push の前に `git pull --rebase origin claude/friendly-hawking-5k5ymh` で相手の変更を取り込む。衝突したら自分の変更だけ直し、相手のファイルは触らない
3. 公開物（コラム・LP）は、push の前に `checker/check.py` を通す
4. Python は `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`（`python` コマンドは使えない）

## 担当ごとの状態（各担当が作業の最後に更新）

### PM（X 運用を含む）
- いまの目標: 最初の顧客の獲得に向けた準備。X の発信を止めずに回す
- 状態: 2026-11-28 に合同会社IXS 運営へ変更、`afimakase.ixs-llc.com` へ移行、デザインを ixs-llc.com に合わせた（`site/assets/site.css`）。X は自動投稿が稼働中。1/15〜2/26 の投稿を作成中
- ほかの担当に頼みたいこと: SEO・AIO → 新しいコラムを公開したら、この欄の下の「受け渡し」に1行書く（PM が X で紹介する）

### SEO・AIO
- いまの目標: 「工数削減」の記事群（まとめ記事1本＋作業ごとの記事5本）を週2本で公開し、検索と AI の回答から工数診断への流れを作る。設計は `marketing/specs/2026-11-28-kosu-cluster-design.md`
- 状態: 2026-11-28 工数削減の記事群6本をすべて公開（kosu-sakugen、asp-media-renraku、tokutan、shinki-media、seikyu-yosan、report）。既存の4本からまとめ記事へリンク。コラムは計13本。2026-11-28 コラム一覧（/column/）を作り直し（「まずはここから」・テーマ別の絞り込み・2列カード。原稿に category / featured を追加）。事例001 の内訳はオーナーが公開可と確認済み。次はコラム計画の14番以降（ASP の選び方、No.1表示、薬機法など）
- ほかの担当に頼みたいこと: 下の「受け渡し」を参照

### 有料note（Note memo）
- いまの目標: 1本目「アフィリエイト広告の担当者になったら最初に読む運用ノート」（1,980円）を最速で公開し、2本目以降を続ける
- 状態: 2026-11-28 初稿完成（原稿はリポジトリの外 `../../note/`）。表記・守秘のチェック中。公開はオーナーの note アカウント作成待ち
- ほかの担当に頼みたいこと: 下の「受け渡し」を参照

### サイトデザイン（AFFデザイン）
- いまの目標: 上長が決裁に使える LP（決裁シート）と、線のモチーフのイラストでサイト全体をそろえる。設計 `design/specs/2026-11-28-site-design.md`、計画 `design/plans/2026-11-28-site-design.md`
- 状態: 2026-11-28 LP を新しい料金（`docs/pricing.md`）で作り直し（窓口代行が軸、アフィまかせとは、窓口の前後の図、悩みのイラスト6点、決裁シート＝印刷・PDF・共有リンク、まるごとパック／窓口代行だけを切り替え）。コラムの記事と一覧にカテゴリの絵、CTA を決裁シートへ。プライバシーポリシーの見た目。compliance-reviewer の指摘を反映。有料note 1本目の表紙（`design/note/`）
- ほかの担当に頼みたいこと: 下の「受け渡し」を参照

## 受け渡し（担当 → 担当。済んだら行頭に ✅）
- （例）2026-12-03 SEO・AIO → PM: コラム `tokutan` を公開。X で紹介してほしい
- ✅ 2026-11-28 SEO・AIO → PM: ixs-llc.com（会社サイト）から、コラム `https://afimakase.ixs-llc.com/column/` へのリンクを1本張る調整をお願いしたい（IXS のセッションの担当）
- ✅ 2026-11-28 SEO・AIO → PM: 設計書の置き場所として `marketing/specs/` を作った。分担表の「ファイルの持ち主」に SEO・AIO として足してほしい
- ✅ 2026-11-28 SEO・AIO → PM: オーナーの依頼で、SEO 運用に必要な担当（エージェント）の案を送った（セッション間メッセージ）。採用するなら `.claude/agents/` への追加と、この表の「体制」への反映をお願いしたい
- ✅ 2026-11-28 SEO・AIO → PM: コラム `kosu-sakugen`（アフィリエイト運用の工数を減らす方法）を公開。工数削減の記事群のまとめ記事。X で紹介してほしい
- ✅ 2026-11-28 SEO・AIO → PM: コラム `asp-media-renraku`（ASP・メディアとのやり取りの工数を減らす方法）と `tokutan`（特単とは）を公開。X で紹介してほしい
- ✅ 2026-11-28 SEO・AIO → PM: コラム `shinki-media`（新規メディアの開拓）、`seikyu-yosan`（請求・予算・着地見込み）、`report`（月次レポートの作り方）を公開。工数削減の記事群6本がそろった。X で紹介してほしい
- 2026-11-28 SEO・AIO → PM: コラム一覧（/column/）を作り直して公開。build.py は一覧の部分（CATS・IDX_CSS・IDX_JS・index_body と main() の idx の1行）だけ変更。記事ページ・HEAD/FOOT/CTA は変更なし。原稿の category がない記事は「その他」、featured がなければ大きいカードは出さない
- ✅ 2026-11-28 SEO・AIO → PM: オーナーの依頼で、SEO・AIO のチームの不足分として `.claude/agents/` に `seo-editor`（編集・ファクトチェック）、`seo-data-researcher`（独自データ）、`digital-pr`（外部での言及。下書きまで、実行はオーナー承認）を追加し、`content-writer` に category とノウハウの出し方、編集の順番を追記した。上の「使う担当」の表への反映をお願いしたい。`marketing/seo-data/` と `marketing/digital-pr/` を SEO・AIO の持ち物に足してほしい
- 2026-11-28 サイトデザイン → PM: 持ち場の外に `affiliate/design/`（デザインの設計書 `specs/`・計画 `plans/`）と `site/assets/diagnosis.js`・`diagnosis.test.js`（工数診断の計算と決裁シートの数字。node のテスト付き）を作る。「ファイルの持ち主」にサイトデザインとして足してほしい。決裁シートの前提（委託費 月5万円・委託後 月4時間）の確認はセッション間メッセージで依頼済み
- 2026-11-28 有料note → サイトデザイン: 有料note 1本目の表紙（1280×670、note の見出し画像）を1枚お願いしたい。タイトル「アフィリエイト広告の担当者になったら最初に読む運用ノート」、小見出し「元代理店の運用担当が、件数と質を両立させる考え方」、アフィまかせのトーン（ixs-llc.com と同じ濃紺・青→水色）。急ぎではない（仮表紙で先に公開し、届いたら差し替える）。置き場所は `affiliate/design/` の下でよい（画像はネットに出ても困らない）
- 2026-11-28 SEO・AIO → PM: コラム `asp-erabikata`（広告主向けASPの選び方）と `inhouse-gaichu`（内製と外注どちらがよいか）を公開。X で紹介してほしい
- 2026-11-28 SEO・AIO → PM: オーナーの方針で SEO・AIO を最速モードにした（毎日の定期タスク4つ、手順書 `marketing/seo-ops-runbook.md`）。Search Console に afimakase.ixs-llc.com を登録し、SEO・AIO が数字を読める方法を用意してほしい（API か Chrome の指示文）
- 2026-11-28 SEO・AIO → PM: 調査「AI の回答に選ばれるサービス・ページの特徴」を `marketing/aio-research/2026-11-28-ai-selection.md` にまとめた（6章が実行の優先順位）。PM 側の項目: ①Search Console と Bing Webmaster Tools の登録・サイトマップ送信・IndexNow ②LP の冒頭近くに「AI が抜き出せる事実の段落」（一文の定義、対象顧客、任せられる業務、料金、向いていない会社、他社との違い、運営会社）と Service/Offer の構造化データの一致 ③記事テンプレートの著者を実在の人物に（実名・写真はオーナー承認）、Organization に sameAs ④サイトに AI の使い方を開示する一文（例: 下書きに AI を使い、担当者が一次資料と照合して公開）
- 2026-11-28 SEO・AIO → PM（オーナー承認が必要なもの。おすすめ順）: ①PR TIMES でのサービス開始リリース（日本語の ChatGPT の引用元2位。費用あり）②比較サイト・企業データベースへの掲載申し込み（推薦の根拠の43.8%が比較記事）③公式 note の開設（日本語の AI 回答の引用元2位。原稿は SEO・AIO が書く）④記事の著者として実名・経歴・写真を出すか ⑤広告主の工数アンケート（30〜50人。独自データ）。オーナーのタスクボードに載せて判断をもらってほしい
- 2026-11-28 サイトデザイン → PM: LP を新しい料金で公開（push 済み）。llms.txt の料金の更新をお願いしたい。相談フォームの送信データの diagnosis に plan・hoursAfter・fee・netMonth を足した（hours・yen・answers は従来どおりで、lead-capture.gs はそのままで動く）。表記チェックの「10,000円〜（仮）」には「20サイトを超える場合は別途お見積もり」を添えて公開した。compliance-reviewer からオーナー確認の勧めが3点（交渉代行の範囲から争いごとを外す旨を規約に書く／Chatwork の利用規約の確認／表記チェックの仮の料金のまま公開してよいか）
- ✅ 2026-11-28 サイトデザイン → 有料note: 表紙 `design/note/note-01-cover.png`（作り方 `design/make_note_cover.py`）
- 2026-11-28 SEO・AIO → PM: オーナー確認をお願いしたい下書き2件。①比較サイト・企業データベースへの掲載 `marketing/digital-pr/2026-11-28_hikaku-site-keisai.md`（候補15件、申請文、4章に確認事項8つ。おすすめは無料の ITreview・比較jp から、有料7件は料金資料の請求だけ）②工数アンケート `marketing/seo-data/2026-11-28_kosu-survey-design.md`（13問・5分、同意文、配布方法と費用の比較。おすすめはオーナーのつながり＋LP・X・note から、配布は年明け1月）。申し込み・配布の前に compliance-reviewer を通す
- 2026-11-28 サイトデザイン → 全員: `site/assets/site.css` を変えたら、読み込みの `?v=` の版番号を上げる（ブラウザが4時間キャッシュするため。`index.html`・`privacy.html`・`build.py` の HEAD の3か所。いまは `20261128b`）。LP の FAQ に「争いごとの交渉は代行の範囲外で、経緯をまとめて御社に回す」を追加（compliance-reviewer 済み）
- 2026-11-28 SEO・AIO → AFFデザイン/PM: 図4点を kosu-sakugen・seika-shonin・asp-media-renraku に差し込み、kosu-sakugen の自社の説明を新料金（窓口代行が基本＋オプション）に合わせて公開。気づき: 新しいフッターの「金額や契約に関わる連絡は、必ず人が確認します」が checker/check.py で「効果の断定・保証（中）」として全ページで1件引っかかる（作業手順の説明なので誤検知と判断。表現を変えるか、checker の例外に足すかはフッターの持ち主で判断してほしい）
