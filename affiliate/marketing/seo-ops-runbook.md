# SEO・AIO 毎日の運用手順書（最速モード）

作成: 2026-11-28（SEO・AIO 担当）。オーナーの方針「スピードを最高レベルに。ほぼ毎日、データ分析・コラム追加・市場調査・リライト・FAQ の改善を行い、AI に選ばれるサービスを調べて質を上げ続ける」による。
定期実行のタスクは、毎回このファイルを最初に読んで動く。

## 0. 毎回最初にやること
1. 作業フォルダ: `C:\Users\rikuu\OneDrive\デスクトップ\Claude\アフィリエイト運用\my-website`
2. `git pull --rebase origin claude/friendly-hawking-5k5ymh`（他のセッションの変更を取り込む。未記録の変更があって失敗したら `git stash` → pull → `git stash pop`）
3. 読む: `affiliate/CLAUDE.md`、`affiliate/docs/workstreams.md`（自分は「SEO・AIO 担当」）、`affiliate/docs/decisions.md` の最新の行、`affiliate/marketing/content-plan.md`、このファイル、最新の `affiliate/marketing/seo-reports/daily/*.md`、`affiliate/marketing/aio-research/*.md`
4. Python は `"$LOCALAPPDATA/Programs/Python/Python312/python.exe"`（以下 PY）

## 1. 1日の流れ
| 時刻（目安） | タスク | やること | 出力 |
|---|---|---|---|
| 毎朝 | 朝の調査と分析 | 市場調査、AI 回答の確認、数字の確認、今日の作業リストを決める | `seo-reports/daily/<日付>.md` |
| 午前 | 記事の追加 | 新しい記事を2本 | 公開 |
| 午後 | リライトと FAQ の改善 | 既存記事1〜2本の改善＋（質を保てるときだけ）新しい記事1本 | 公開 |
| 毎週月曜 | 週次の見直し | AI 回答の詳しい確認、競合の確認、記事の候補を30本以上先まで補充、計画と手順の見直し | `seo-reports/weekly/<日付>.md`、content-plan の更新 |

新しい記事は **1日2本が基本、最大3本**。3本目は、その日の候補に独自の数字や知見があるときだけ書く。

## 2. 朝の調査と分析
1. **市場調査**（WebSearch。30分以内）: 消費者庁（ステマ規制・景品表示法）、主要 ASP のお知らせ、アフィリエイト業界のニュースの直近の動き。記事にすべき変化があれば、今日の候補の先頭に入れる
2. **AI 回答の確認**: `marketing/aio-queries.md`（なければ作る。狙う質問を20〜30個）から毎日5問を順番に選び、WebSearch で検索結果の上位と AI による概要に出るサイトを観察する。アフィまかせが出るか、出るのはどんなサイトか、を記録する。ChatGPT・Perplexity の画面での確認は月1回 PM に頼む（`aio-monitor`）
3. **数字の確認**: Search Console・GA4 が読めるようになっていれば、前日までの表示回数・クリック・順位・記事から工数診断への流れ。読めなければ「未接続」と書く（PM に接続を頼んである）
4. **今日の作業リスト**: 新しい記事2〜3本（content-plan の一覧の上から、朝の調査で優先が変わったものは入れ替える）と、リライト1〜2本（理由つき: 古い情報、FAQ が弱い、AI に引用されにくい形、内部リンク不足、数字で順位が5〜20位など）
5. 日報に書く: 調べたこと、気づき、今日の作業リスト、PM・オーナーへの依頼

## 3. 記事の追加（1本ごと）
1. `seo-planner` の考え方で、狙う言葉と検索意図、上位の記事との差（自社だけが出せる数字・知見）を決める。差が作れない題材は書かずに後ろへ回す
2. `content-writer` の定義に従って `affiliate/site/content/<slug>.md` を書く（category を必ず入れる）
3. `seo-editor` の定義に従って自分で点検・修正する（正確さ、言い切り、事例と自社の区別、AIO の形、ノウハウの出し方、内部リンク）
4. `PY affiliate/site/build.py` → リンク検査（下）→ `PY affiliate/checker/check.py --html affiliate/site/column/<slug>/index.html --out <scratch>/r.md` で指摘0件
5. `compliance-reviewer` をサブエージェントで呼んで「要修正」を直す
6. 関連する既存の記事・まとめ記事から、新しい記事へのリンクを足す
7. `git add <自分のファイルだけ>` → commit → pull --rebase → push（自動で公開）
8. `docs/workstreams.md` の「受け渡し」に1行（PM が X で紹介する）

リンク検査:
```
PY -c "import re,pathlib as p;c=p.Path('affiliate/site/content');s={f.stem for f in c.glob('*.md')};ng=[(f.name,m) for f in c.glob('*.md') for m in re.findall(r'\]\(/column/([^/)]+)/\)',f.read_text(encoding='utf-8')) if m not in s];print('NG',len(ng),ng)"
```

## 4. リライトと FAQ の改善
- 対象は朝の作業リストのとおり。`seo-rewriter` の定義に従う
- **FAQ の質**: 各記事の「よくある質問」を、実際に AI に聞かれる質問の形にそろえ、回答の1文目で答えを言い切る。回答は1段落で完結させる。重複する質問は記事ごとに角度を変える
- 直したら `updated` を今日にする。同じ点検（build、リンク検査、check.py、法令に触れる変更は compliance-reviewer）を通して公開
- LP（`site/index.html`）の FAQ やサービス説明の改善案は、PM の持ち物なので `workstreams.md` の受け渡しに案として書く

## 5. 週次の見直し（毎週月曜）
- AI 回答の確認を全質問で行い、先週との変化を書く
- 競合（運用代行・代理店・比較サイト）の新しいページ、AI に引用されているページの共通点を調べ、`aio-research/` に追記する
- `seo-data-researcher` の考え方で、独自データを1つ増やす（`marketing/seo-data/`）
- content-plan の記事候補を **30本以上先まで** 補充し、優先順を付け直す
- この手順書の改善点を反映する

## 6. 質を守るための決まり（スピードより優先）
- Google は、検索順位を操作する目的で価値の低いページを大量に作ることをスパムとしている。**本数は目的ではない。** 毎記事に「自社だけが出せる数字・知見・判断の基準」を最低1つ入れる。入れられないなら書かない
- 似た記事を増やさない。既存の記事と狙う言葉が重なるなら、新しく書かずに既存の記事を直す
- 顧客名・媒体名・元資料の新しい数字は使わない（使うなら PM に回す）。法律の解釈に迷うものも PM に回す
- 点検（build・リンク・check.py・compliance-reviewer）を1つでも通らない記事は公開しない
- 公開した記事が検索・AI に悪い影響を出している兆し（インデックスから外れる、表示回数の急な減少）があれば、新しい記事を止めて日報と PM に報告する

## 7. 記録と報告
- 日報: `affiliate/marketing/seo-reports/daily/<YYYY-MM-DD>.md`（その日の全タスクが追記する）
- 作業の区切りで、経営ダッシュボードの `data/ops/projects/aff-seo`（get → if_version で update: phase / next / progress / updatedAt）と `data/ops/events`（`e-<YYYYMMDDHHmm>-seo`）、公開したら `data/ops/kpis/columns` の value を更新する。ダッシュボードの URL はメモリ `exec-dashboard` にある（リポジトリには書かない）
- 1日の最後のタスクは、`workstreams.md` の SEO・AIO 欄の「状態」を更新する
- 記録は `git add <パス>` だけ。`git add -A` は使わない
