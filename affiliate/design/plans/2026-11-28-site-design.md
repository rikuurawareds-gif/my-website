# サイト全体のデザイン 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 工数診断を「決裁シート」に作り直し、線のモチーフの SVG イラストで LP・コラム・プライバシーポリシーの見た目をそろえる。

**Architecture:** 静的サイト（`affiliate/site`）。共通の見た目は `assets/site.css`、イラストは `assets/img/*.svg`（ヒーローと窓口の図はインライン SVG）。診断の計算は `assets/diagnosis.js`（ブラウザと node の両方で読める純粋関数）に切り出し、node のテストで確かめる。コラムは `build.py` の見た目の部分（CSS・HEAD・FOOT・CTA・記事と一覧の組み立て）を変えて再生成する。

**Tech Stack:** HTML / CSS / 素の JavaScript、Python 3.12（build.py）、node（テストだけ）

**Spec:** `affiliate/design/specs/2026-11-28-site-design.md`

## Global Constraints
- トーン: 濃紺 #070b18・`--grad`（#3366ff → #22d3ee）・Noto Sans JP。既存トークン名は変えない。足すのは `--paper:#fbfcff`、`--knot:#9aa4bf`
- LP の文言と料金表はいまのものから変えない（見た目・図・決裁シートの部品だけ）。英字の大文字の見出し飾り `.en` と英単語の帯 `.band` は外す
- 委託費と委託後の工数は `diagnosis.js` の `ASSUMPTIONS` 1か所。PM 確認までは `{ fee: 50000, remainHours: 4 }`（週1回の確認 × 約1時間）
- 375px で横にはみ出さない。キーボード操作・`:focus-visible`・`prefers-reduced-motion` を守る
- 触らない: `site/content/*.md`、`config.js`、`track.js`、build.py の `md_to_html`・`parse`・sitemap・llms.txt・構造化データ
- 記録は `git add <パス>` だけ。push の前に `git pull --rebase origin claude/friendly-hawking-5k5ymh`、`checker/check.py` を通す
- Python: `$LOCALAPPDATA/Programs/Python/Python312/python.exe`

## Review Focus
1. 共有リンクの # が壊れている・古い形式・値が範囲外 → 黙って無視し、空の診断を出す（落ちない）
2. 差し引きがマイナス（工数が小さい） → マイナスのまま正直に出し、一部だけ任せる案内を出す
3. 印刷で紙が2枚に分かれる・机の地や操作ボタンが印刷される → 紙だけが A4 1枚に収まる
4. 宛名に `<script>` などを入れる → 文字として表示される（innerHTML を使わない）
5. 動きを減らす設定 → ヒーローの線はほどけ終わった形で止まる

---

### Task 1: 診断の計算を切り出す（決裁シートの数字）

**Files:**
- Create: `site/assets/diagnosis.js`
- Create: `site/assets/diagnosis.test.js`

**Interfaces:**
- Produces（`window.AffDiag` と `module.exports` の両方）:
  - `calc(answers) -> { tasks: {名前: 時間}, total: number, alerts: string[] }` — いまの index.html の calc をそのまま移す（係数は変えない）
  - `roi(total, wage, a = ASSUMPTIONS) -> { hoursNow, hoursAfter, hoursSaved, laborSaved, fee, netMonth, netYear }`（円。hoursAfter = min(remainHours, total)）
  - `encode(answers) -> string`（例 `"a1m2c1pmcrdsrfw4000"` のような短い形）／ `decode(str) -> answers | null`（不正なら null）
  - `ASSUMPTIONS = { fee: 50000, remainHours: 4 }`

- [ ] **Step 1: テストを書く**（`node:test` と `assert`）
  - `roi(48, 4000)` → `hoursSaved 44, laborSaved 176000, netMonth 126000, netYear 1512000`
  - `roi(3, 4000)` → `hoursAfter 3, hoursSaved 0, netMonth -50000`
  - `decode(encode(x))` が x と同じ（8問すべて）
  - `decode("zzz")`・`decode("")`・`decode("a9m0c0pmcrdsrfw4000")` → `null`
  - `calc` の既存の答え1組で、移す前と同じ total（移す前に index.html で手計算した値を固定）
- [ ] **Step 2:** `node --test site/assets/diagnosis.test.js` → 失敗を確認
- [ ] **Step 3:** 実装（UMD の小さな包み。DOM には触らない）
- [ ] **Step 4:** テストが通ることを確認
- [ ] **Step 5:** commit（`site/assets/diagnosis.js` `site/assets/diagnosis.test.js`）

### Task 2: 共通 CSS とイラスト

**Files:**
- Modify: `site/assets/site.css`（トークン2つ追加、`.en`・`.band` の削除、イラスト・決裁シート・記事・印刷のスタイル）
- Create: `site/assets/img/pain-renraku.svg` `pain-shonin.svg` `pain-hyoki.svg` `pain-kaitaku.svg` `pain-sozai.svg` `pain-report.svg` `remain-weekly.svg` `cat-kosu.svg` `cat-jitsumu.svg` `cat-hourei.svg` `cat-hajime.svg` `cat-etc.svg`

- [ ] **Step 1:** SVG を描く。`viewBox` を持ち、線 2px・`stroke-linecap:round`、色は `#0f1424`（線）・`#9aa4bf`（絡まった線）・グラデーション（まとまった線だけ）。`role="img"` と `<title>` を付ける
- [ ] **Step 2:** `python -m http.server` で `affiliate/site` を配信し、各 SVG を開いて見た目を確認（スクリーンショット）
- [ ] **Step 3:** commit

### Task 3: LP の見た目と決裁シート

**Files:**
- Modify: `site/index.html`（ヒーローにインライン SVG の線の図、悩みの節をイラスト付きに、窓口の前後の図を追加、残る作業に絵、診断の結果を決裁シートに、`.en`・`.band` を外す。文言・料金は変えない）

**Interfaces:**
- Consumes: Task 1 の `AffDiag.calc / roi / encode / decode / ASSUMPTIONS`、Task 2 のクラスと SVG

- [ ] **Step 1:** 決裁シートの HTML（紙 `.sheet`、操作の帯 `.sheet-tools`: 宛名入力・「印刷・PDF保存」・「リンクをコピー」）
- [ ] **Step 2:** 結果の描画を `textContent` で書く。表示のときに `location.hash = '#r=' + encode(a)`、読み込み時に `#r=` があれば `decode` して結果を出す（null なら何もしない）
- [ ] **Step 3:** `@media print` で `.sheet` 以外を隠し、A4 1枚（`@page { size: A4; margin: 12mm }`）
- [ ] **Step 4:** ブラウザで確かめる: 8問回答 → シート表示、リンクをコピーして新しいタブで開く → 同じ数字、壊れた # → 落ちない、宛名に `<b>x</b>` → 文字のまま、375px で横スクロールなし、Tab で全部操作できる、印刷プレビューが1枚
- [ ] **Step 5:** `checker/check.py site/index.html` を通す → commit

### Task 4: コラムの記事と一覧（build.py の見た目の部分）

**Files:**
- Modify: `site/build.py` の `CSS`・`HEAD`・`FOOT`・`CTA`・`article_page` の見出し帯・`index_body` のカード（カテゴリの絵を足すだけ。並びと絞り込みはそのまま）
- 再生成: `site/column/**`（`build.py` を実行）

- [ ] **Step 1:** 記事の見出し帯にカテゴリの絵、本文 42em・17px・行間 1.9、CTA の文言は「あなたの運用で決裁シートを作る」に（宣伝文の変更なので compliance-reviewer に回す）
- [ ] **Step 2:** `python build.py` → `13 articles built`、sitemap・llms.txt に差分がないこと（`git diff --stat site/sitemap.xml site/llms.txt` が日付以外空）
- [ ] **Step 3:** 記事1本と一覧を 375px と 1280px で確認 → commit

### Task 5: プライバシーポリシー

**Files:**
- Modify: `site/privacy.html`（見た目だけ。本文は変えない。`.en` を外し、目次と読みやすい本文幅）

- [ ] **Step 1:** 変更 → 375px で確認 → commit

### Task 6: 公開と連絡
- [ ] `git pull --rebase` → push → 本番で LP・記事・一覧・プライバシーを確認
- [ ] PM に連絡（決裁シートの前提 `ASSUMPTIONS` と注記の文言の確認、CTA 文言の確認）、workstreams.md の自分の欄と受け渡し、経営ダッシュボードの行を更新
