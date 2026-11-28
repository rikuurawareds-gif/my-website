# 作業の分担表（セッションごとの担当）

複数の Claude セッションが **同じフォルダ・同じブランチ** で並行して作業する。会話は共有されないので、**連動はこのファイルと `decisions.md` で取る**。
各セッションは **作業の最初にこのファイルと `decisions.md` を読み、作業の最後に自分の欄を更新する**。

最終更新: 2026-11-28（PM）

## 体制
- **PM**（セッション「アフィリエイト運用」）: オーナーの窓口。全体に関わる判断、共通ファイルの変更、担当への指示と受け渡し。X の運用も持つ
- **SEO・AIO 担当**（セッション「SEO AIO」）: コラムの企画・執筆・公開、検索・AI 回答での露出
- 担当を増やすときは PM がこの表に欄を足す

## 全体に関わる判断は PM に回す
デザイン、ドメイン、LP の構成・文言、料金、運営者・法務の表示、計測（GA4）、共通のテンプレートは PM が決めて `decisions.md` に書く。担当が変えたいときは、PM に理由と案を伝える（オーナーから担当に直接頼まれた場合も、PM に知らせてから進める）。

## ファイルの持ち主
| 範囲 | 持ち主 | 他の担当がしてよいこと |
|---|---|---|
| `site/content/*.md`（コラムの原稿）、`marketing/content-plan.md` | SEO・AIO | 読むだけ |
| `site/column/`、`sitemap.xml`、`llms.txt`（`build.py` の出力） | SEO・AIO が `build.py` を実行して更新 | PM も実行してよい（出力は誰が作っても同じ） |
| `site/build.py`、`site/assets/*`（共通 CSS・計測・設定）、`site/index.html`（LP）、`site/privacy.html`、`robots.txt` | **PM** | 変更の提案だけ |
| `marketing/x-*`、`marketing/x-research/`、`marketing/x-queue/`、`automation/x-autopost.gs`、`.claude/agents/x-*` | PM（X 運用） | 読むだけ |
| `docs/decisions.md` | 全員が追記してよい（自分の担当の決定。全体に関わる決定は PM） | 追記のみ。他人の行は書き換えない |
| `HANDOFF.md`、`CLAUDE.md`、このファイルの「体制」「持ち主」 | PM | 自分の欄の「状態」だけ更新 |
| `legal/`、`docs/` のその他、`knowledge/`、`ops/` | PM | 読むだけ |

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
- いまの目標: （SEO・AIO 担当が記入）
- 状態: （記入）
- ほかの担当に頼みたいこと: （記入）

## 受け渡し（担当 → 担当。済んだら行頭に ✅）
- （例）2026-12-03 SEO・AIO → PM: コラム `tokutan` を公開。X で紹介してほしい
