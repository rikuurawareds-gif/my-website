# 工数削減の記事群 実行計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 工数削減のまとめ記事1本と作業ごとの記事5本を公開し、既存記事とリンクでつなぐ。
**Architecture:** 原稿は `site/content/<slug>.md`。`site/build.py` で `site/column/`・`sitemap.xml`・`llms.txt` を作る。push すると Cloudflare Pages が自動で公開する。
**Tech Stack:** Markdown（build.py の簡易記法）、Python 3.12（標準ライブラリ）、git
**Spec:** `marketing/specs/2026-11-28-kosu-cluster-design.md`

## Global Constraints
- Python: `"$LOCALAPPDATA/Programs/Python/Python312/python.exe"`（以下 `PY`）。`python` コマンドは使わない
- 書いてよいファイル: `site/content/*.md`、`marketing/content-plan.md`、`marketing/specs/*`。`build.py` は実行だけ
- 記録は `git add <パス>` だけ。push の前に `git pull --rebase origin claude/friendly-hawking-5k5ymh`
- 顧客名・媒体名・業種と結びつく個別の数字は出さない。事例001 は「ASP・メディア約20社と取引する、運用が重めの広告主の一例」。移管後 約10時間は「人の代理店に任せた場合の例。アフィまかせの実績ではない」と書く
- 「多くの広告主はもっと少なく、月20時間ほど」を必ず併記する
- ノウハウは考え方まで。作業ごとの時間の数字ははっきり出す。連絡の型・調査手順・要因分解のテンプレートそのものは出さない
- 料金の比較は本文に書かない。自社への誘導はテンプレートの CTA と、「任せる」の節の最後の1文だけ
- 根拠のない言い切り（「必ず」「半分になる」など）を書かない。法律の最終判断を書かない
- 冒頭の段落で結論を言い切る。見出しは検索・質問の言葉。表を使う。「## よくある質問」に3〜5問
- ペース: 品質チェックを通ったものから公開する（コラム計画の週2本は下限）

## Review Focus
1. 公開後のリンク切れ: 本文の `/column/<slug>/` が実在しない → 公開前の検査（各タスクの「検証」）で 0 件
2. まだ公開していない記事へのリンク: ハブから未公開の子記事へリンクしない → 子記事を公開するたびにハブへリンクを足す（タスク 3〜7）
3. 事例の数字が自社の実績に読める → compliance-reviewer の確認項目に入れる
4. FAQ の構造化データが出ない（「### 質問」の直後が段落でない） → 検証でビルド結果に `FAQPage` があることを確認
5. 同じ言葉の食い合い（「アフィリエイト 代理店 料金」）→ 新しい記事のタイトルに入れない。`affiliate-unyo-daiko` で受ける（タスク 2）

## 各タスク共通の「検証」と「公開」
- **検証**
  1. `PY site/build.py` がエラーなく終わる
  2. `PY checker/check.py --html site/column/<slug>/index.html` で、自社の表現に要修正の指摘がない（法令の解説で例として挙げた表現は誤検知）
  3. リンク検査で「NG 0」:
     ```
     PY -c "import re,pathlib as p;c=p.Path('site/content');s={f.stem for f in c.glob('*.md')};ng=[(f.name,m) for f in c.glob('*.md') for m in re.findall(r'\]\(/column/([^/)]+)/\)',f.read_text(encoding='utf-8')) if m not in s];print('NG',len(ng),ng)"
     ```
  4. `grep -c FAQPage site/column/<slug>/index.html` が 1 以上
  5. compliance-reviewer（サブエージェント）が、原稿に「要修正」なし。見る点: 誇大な表示、事例の数字が自社の実績に読めないか、法律の断定、顧客・媒体が特定できないか
- **公開**: `git add site/content/<slug>.md site/column/ site/sitemap.xml site/llms.txt [ほかに直した原稿]` → commit → pull --rebase → push。`docs/workstreams.md` の「受け渡し」に「SEO・AIO → PM: コラム `<slug>` を公開。X で紹介してほしい」を1行足して、それも記録する

---

### Task 1: コラム計画の更新
**Files:** Modify: `marketing/content-plan.md`
- [ ] 「書き方の手順」の「PM が書き」を「SEO・AIO 担当が書き」に、ペースの節を「品質チェックを通ったものから公開（週2本は下限）」に直す
- [ ] 記事の一覧の未公開分を、設計書 7 章の順（kosu-sakugen、asp-media-renraku、tokutan、shinki-media、seikyu-yosan、report）を先頭にして並べ替え、`asp-media-renraku` を新規の行として足す。13・9・14・25・12 の行は移す（重複させない）
- [ ] 公開の流れに compliance-reviewer を足し、設計書へのリンクを書く
- [ ] commit（`git add marketing/content-plan.md`）

### Task 2: まとめ記事 `kosu-sakugen`
**Files:** Create: `site/content/kosu-sakugen.md`／Modify: `site/content/affiliate-unyo-daiko.md`, `seika-shonin.md`, `pr-hyoki.md`, `stema-affiliate.md`
- タイトル案: 「アフィリエイト運用の工数を減らす方法：作業別の時間と『なくす・自動化・任せる』の判断」
- 中身は設計書 8 章のとおり。表は「作業／月の時間の目安／減らし方／詳しい記事」。数字は `knowledge/workload-benchmarks.md` の事例001 と `docs/workload-inventory.md`（幅で）
- リンクは公開済みの記事だけ: seika-shonin、pr-hyoki、stema-affiliate、affiliate-unyo-daiko、epc
- 既存の4本に、ハブへのリンクを1文ずつ足す（成果承認・表記・運用代行の文脈で）
- `affiliate-unyo-daiko` の見出しかよくある質問に「アフィリエイト代理店の料金」の言葉を足す
- [ ] 原稿を書く → [ ] 検証 → [ ] 公開

### Task 3: `asp-media-renraku`（ASP・メディアとのやりとりの工数を減らす）
- 作業番号 B4・B5。実データでは最大の作業（月15時間の例）。減らし方は考え方まで（窓口の一本化、よくある質問の資料化、定例の議題の固定、返事の下書きの自動化）
- ハブの表の該当行にリンクを足す
- [ ] 原稿 → [ ] 検証 → [ ] 公開

### Task 4: `tokutan`（特単とは？出し方・期限の管理・やめどき）
- 作業番号 B7。EPC 記事（`epc`）へリンク。単価管理の言葉を含める。計算例は架空の数字
- ハブにリンクを足す
- [ ] 原稿 → [ ] 検証 → [ ] 公開

### Task 5: `shinki-media`（新規メディアの開拓方法）
- 作業番号 B6。考え方は `knowledge/report-playbook.md` の媒体調査（狙う言葉で上位の面を調べ、未掲載で競合が載っている面から当たる、順位を上げない判断）。具体的な比率・社名は出さない
- ハブにリンクを足す
- [ ] 原稿 → [ ] 検証 → [ ] 公開

### Task 6: `seikyu-yosan`（請求・予算・着地見込みの管理）
- 作業番号 C5。請求額と承認額の照合、予算の消化と CPA 上限の監視、月末の着地見込みの出し方（計算例は架空）
- ハブにリンクを足す
- [ ] 原稿 → [ ] 検証 → [ ] 公開

### Task 7: `report`（月次レポートの作り方）
- 作業番号 C2〜C4。考え方は `knowledge/report-playbook.md`（数字が動いた理由を分けて書く、外部環境、着地見込みとのずれ）。テンプレートそのものは出さない
- ハブにリンクを足す
- [ ] 原稿 → [ ] 検証 → [ ] 公開

### Task 8: 仕上げ
- [ ] `docs/workstreams.md` の SEO・AIO 欄の状態を更新して記録
- [ ] PM にセッション間メッセージで公開した記事の一覧を送る
