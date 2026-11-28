# 作業の分担表（セッションごとの担当）

複数の Claude セッションが **同じフォルダ・同じブランチ** で並行して作業する。会話は共有されないので、**連動はこのファイルと `decisions.md` で取る**。
各セッションは **作業の最初にこのファイルと `decisions.md` を読み、作業の最後に自分の欄を更新する**。

最終更新: 2026-11-28（PM）

## 体制
- **PM**（セッション「アフィリエイト運用」）: オーナーの窓口。全体に関わる判断、共通ファイルの変更、担当への指示と受け渡し。X の運用も持つ
- **SEO・AIO 担当**（セッション「SEO AIO」）: コラムの企画・執筆・公開、検索・AI 回答での露出。**コラムの判断と公開はオーナーから委任済み**（2026-11-28、オーナーが PM に直接確認。`decisions.md`）。公開後に受け渡しに書けばよい。法律の解釈に迷うもの、他社名・顧客名・元資料の数字に触れるものだけ公開前に PM に回す
- 担当を増やすときは PM がこの表に欄を足す

### 使う担当（エージェント。`.claude/agents/`）
| 担当 | 使うセッション | いつ |
|---|---|---|
| `seo-planner`（SEO 企画） | SEO・AIO | いまから |
| `content-writer`（コラム執筆。コラムの書き方を定義に追加済み） | SEO・AIO | いまから |
| `seo-analyst`（SEO 分析） | SEO・AIO | 記事が検索に載り始める 2027年1月ごろから月1回 |
| `seo-rewriter`（リライト・改善） | SEO・AIO | 分析と同時。全記事の見直しは半年ごと |
| `aio-monitor`（AI 回答の監視） | SEO・AIO（AI の画面での質問は PM が Chrome で行う） | 2026年12月末から月1回 |
| `seo-tech`（技術面の SEO） | **PM**（build.py・共通ファイルが PM の持ち物のため） | 問題が出たとき＋四半期に1回 |
| `compliance-reviewer` と `checker/check.py` | 全員 | 公開前に毎回 |
| `x-researcher` / `x-post-writer` | PM | 毎月20日ごろ |
| 外部での言及（被リンク・プレスなど） | — | コラムが10本を超えてから PM が検討 |

## 全体に関わる判断は PM に回す
デザイン、ドメイン、LP の構成・文言、料金、運営者・法務の表示、計測（GA4）、共通のテンプレートは PM が決めて `decisions.md` に書く。担当が変えたいときは、PM に理由と案を伝える（オーナーから担当に直接頼まれた場合も、PM に知らせてから進める）。

## ファイルの持ち主
| 範囲 | 持ち主 | 他の担当がしてよいこと |
|---|---|---|
| `site/content/*.md`（コラムの原稿）、`marketing/content-plan.md`、`marketing/specs/`、`marketing/seo-reports/`、`marketing/aio-queries.md`、`marketing/aio-reports/` | SEO・AIO | 読むだけ |
| `site/column/`、`sitemap.xml`、`llms.txt`（`build.py` の出力） | SEO・AIO が `build.py` を実行して更新 | PM も実行してよい（出力は誰が作っても同じ） |
| `site/build.py`、`site/assets/*`（共通 CSS・計測・設定）、`site/index.html`（LP）、`site/privacy.html`、`robots.txt` | **PM** | 変更の提案だけ |
| `marketing/x-*`、`marketing/x-research/`、`marketing/x-queue/`、`automation/x-autopost.gs`、`.claude/agents/x-*` | PM（X 運用） | 読むだけ |
| `docs/decisions.md` | 全員が追記してよい（自分の担当の決定。全体に関わる決定は PM） | 追記のみ。他人の行は書き換えない |
| `HANDOFF.md`、`CLAUDE.md`、このファイルの「体制」「持ち主」 | PM | 自分の欄の「状態」だけ更新 |
| `legal/`、`docs/` のその他、`knowledge/`、`ops/` | PM | 読むだけ |

## 新しいファイル・フォルダを作るとき
- **自分が持ち主の場所の中なら、知らせずに自由に作ってよい**（例: SEO・AIO が `marketing/specs/` の中に設計書を足す）
- **持ち主の場所の外に新しく作るときは、作る前に「受け渡し」に1行書く**（場所・用途）。PM が「ファイルの持ち主」に足す
- 作業途中のファイルは、記録（commit）するまで他のセッションには「知らないファイル」に見える。**知らないファイルを見つけたら、消したり記録したりせず、`git log` とこの表の受け渡しを見て持ち主を確かめる**。分からなければ持ち主の候補のセッションに聞く

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
- 状態: 2026-11-28 設計が確定（オーナーが SEO・AIO の判断を担当に委任。公開ごとの確認なし）。次は実行計画 → まとめ記事 `kosu-sakugen` の執筆
- ほかの担当に頼みたいこと: 下の「受け渡し」を参照

## 受け渡し（担当 → 担当。済んだら行頭に ✅）
- （例）2026-12-03 SEO・AIO → PM: コラム `tokutan` を公開。X で紹介してほしい
- ✅ 2026-11-28 SEO・AIO → PM: ixs-llc.com（会社サイト）から、コラム `https://afimakase.ixs-llc.com/column/` へのリンクを1本張る調整をお願いしたい（IXS のセッションの担当）
- ✅ 2026-11-28 SEO・AIO → PM: 設計書の置き場所として `marketing/specs/` を作った。分担表の「ファイルの持ち主」に SEO・AIO として足してほしい
- ✅ 2026-11-28 SEO・AIO → PM: オーナーの依頼で、SEO 運用に必要な担当（エージェント）の案を送った（セッション間メッセージ）。採用するなら `.claude/agents/` への追加と、この表の「体制」への反映をお願いしたい
- 2026-11-28 SEO・AIO → PM: コラム `kosu-sakugen`（アフィリエイト運用の工数を減らす方法）を公開。工数削減の記事群のまとめ記事。X で紹介してほしい
- 2026-11-28 SEO・AIO → PM: コラム `asp-media-renraku`（ASP・メディアとのやり取りの工数を減らす方法）と `tokutan`（特単とは）を公開。X で紹介してほしい
