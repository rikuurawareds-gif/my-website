# AI の回答に選ばれ・引用されるページとサービスの特徴（アフィまかせ向け実行指針）

- 作成日: 2026-11-28
- 対象: ChatGPT 検索、Perplexity、Google の AI による概要 / AI モード、Gemini、Claude、Copilot
- 用途: 「アフィまかせ」（afimakase.ixs-llc.com）が AI の回答で引用・推薦されるようにするための実行指針
- 情報源の扱い: Google・OpenAI・Perplexity・Anthropic の公式文書を一次情報とし、Ahrefs・SE Ranking・Seer Interactive・Profound などの実データ研究で補った。SEO ツール会社の研究には「自社ツールを売る立場」というバイアスがあり、ほぼすべてが相関分析で因果は示していない。根拠が弱いもの・推測は **［推測］** と書いた。
- 現状の確認: サイトのファイル（`site/robots.txt`、`site/llms.txt`、コラムの JSON-LD）を読んだだけで、変更はしていない。

---

## 0. 結論（先に要点）

1. **Google の AI による概要 / AI モードは「普通の検索順位の延長」です。** 引用 URL の約76%は通常検索の上位10位から選ばれます（Ahrefs）。Google も公式に「特別な対策は要らない、通常の SEO で足りる」と書いています。つまり、まず検索で上位に入ることが必要です。
2. **ChatGPT・Gemini・Copilot は、検索順位と重なる部分が小さいです。** 引用 URL のうち、同じ質問の Google 上位10位に入っていたのは約12%だけでした（Ahrefs、2025年7月時点のデータ）。AI は質問を言い換えた複数の検索（クエリファンアウト）を同時に行うため、関連する質問の多くで「そこそこ上位」にいるページが選ばれやすくなります。
3. **「どのサービスが推薦されるか」には、自社サイトの外での言及が最も強く関係します。** 7.5万ブランドの分析では、Web 上のブランド言及数（相関 0.66〜0.71）と YouTube での言及（約 0.74）が上位で、被リンク数や DR（0.27〜0.33）より強い結果でした（Ahrefs、2025年12月）。
4. **「おすすめ○選」型の比較記事が、推薦の材料として最も多く引用されています。** ChatGPT がサービスを推薦するときに引用したページの43.8%が「best X」型のまとめ記事でした。ただし、**自社を1位に置く比較記事は2026年1月以降に検索順位を落とす事例が多く、AI による概要は自社比較記事を引用しても、その会社自体は推薦しないことが69%ありました**（Lily Ray）。
5. **日本語で引用されやすいドメインは YouTube、note、Wikipedia、アメブロ、Yahoo!知恵袋、PR TIMES、Reddit、価格.com などです**（Ahrefs 2026年6月版）。ChatGPT では PR TIMES が2位でした。新しいサブドメインにとっては「自社サイトの外に、事実ベースの一次情報を置く」ことが近道です。
6. **llms.txt は効果が確認されていません**（Google は使わないと明言しており、30万ドメインの分析でも効果なし）。**構造化データも、引用を増やす効果は確認されていません**（Ahrefs の追加前後比較で上昇なし）。どちらも害はないので、今あるものは残して構いませんが、優先度は低くしてください。
7. **1日に何本も記事を出すこと自体は違反ではありませんが、「量産・自社を1位にする比較・年号だけの更新」が重なると危険です。** Google のポリシーは作り方（AI か人か）を問わず、「価値を加えない大量のページ」を対象にしています。

---

## 1. AI の回答がどのページを引用するか（分かっている事実と実データ）

### 1-1. 公式に分かっていること

| 項目 | 内容 | 出典（時点） |
|---|---|---|
| Google の AI による概要 / AI モードの選び方 | Google の通常の検索ランキングシステムが、インデックスから関連する新しいページを取り出し、それをもとに AI が回答を書いて根拠のページへリンクする（グラウンディング）。質問を関連する複数の検索に分けて同時に実行する「クエリファンアウト」を使う | [Google: Optimizing your website for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)（ページに日付の記載なし、2026-11-28 閲覧） |
| Google の AI 機能に表示される条件 | インデックスされていて、スニペット付きで表示できること。Search Console で「Search generative AI features」に含まれていることも条件とされる | 同上 |
| Google の AI 機能に特別な対策は要るか | 不要。「通常の検索の SEO のベストプラクティスがそのまま当てはまる」 | [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)（2026-11-28 閲覧） |
| Google が勧めること | 独自で価値のある「コモディティでない」コンテンツ、ページの使いやすさ、クロールできる状態、見えている内容と一致する構造化データ、画像・動画、Merchant Center / ビジネス プロフィールの更新 | [Google 検索セントラル ブログ「Top ways to ensure your content performs well in Google's AI experiences」](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search)（2025-05-21、John Mueller） |
| 細かく分けた文章は必要か | 不要。1ページに複数の話題があっても処理できる。理想の文字数もない | Google 最適化ガイド（上記） |
| 外部での言及 | AI 機能も、ブログ・動画・フォーラムで人々がその商品やサービスについて何を言っているかを示すことがある。ただし「本物でない言及を集めても、思うほど役に立たない」 | Google 最適化ガイド（上記） |
| ChatGPT 検索に載る条件 | robots.txt で OAI-SearchBot を許可すること（GPTBot は学習用で、検索への表示とは別）。変更の反映には約24時間かかる | [OpenAI: Overview of OpenAI Crawlers](https://developers.openai.com/api/docs/bots)（2026-11-28 閲覧） |
| Perplexity に載る条件 | PerplexityBot を許可すること（検索表示用で、学習用ではない）。Perplexity-User はユーザーの質問に応じてページを取得するもので、robots.txt を基本的に無視する | [Perplexity: Perplexity Crawlers](https://docs.perplexity.ai/guides/bots)（2026-11-28 閲覧） |
| Claude | ClaudeBot（学習用）、Claude-User（ユーザーの質問時の取得）、Claude-SearchBot（検索結果の質の向上用）の3つ。Claude-SearchBot をブロックすると Claude の検索回答での露出が減る可能性がある | [Anthropic ヘルプ記事 8896518](https://support.claude.com/en/articles/8896518)（2026年2月ごろ更新と報道） |

### 1-2. 実データ研究で分かっていること

| 論点 | 分かったこと | 出典（時点） |
|---|---|---|
| 検索順位との関係 | 1.5万プロンプトで調べると、ChatGPT・Gemini・Copilot の引用 URL のうち Google 上位10位に入っていたのは約12%。Perplexity は28.6%。AI による概要は76%が上位10位から | [Ahrefs: Only 12% of AI Cited URLs Rank in Google's Top 10](https://ahrefs.com/blog/ai-search-overlap/)（2025-08-11公開、データは2025年7月） |
| ブランドの推薦に関係する要素 | 7.5万ブランドの相関（スピアマン）。YouTube での言及 約0.737、Web 上のブランド言及 0.664（ChatGPT）/ 0.709（AI モード）/ 0.656（AI による概要）、ブランド名を使ったアンカーテキスト 0.51〜0.63、指名検索数 0.35〜0.47、DR 0.27〜0.33。被リンク数とページ数（約0.19）はほぼ関係なし | [Ahrefs: Top Brand Visibility Factors in ChatGPT, AI Mode, and AI Overviews](https://ahrefs.com/de/blog/ai-brand-visibility-correlations/)（2025-12-12） / 前回版 [AI Overview Brand Correlation](https://ahrefs.com/blog/ai-overview-brand-correlation/)（2025年5月） |
| 勝者総取り | 言及数が上位25%のブランドは AI による概要に平均169回登場し、次の25%（平均14回）の10倍以上。26%のブランドは一度も登場しない | Ahrefs（2025年5月、上記） |
| 鮮度 | 約1,700万件の引用を分析。AI が引用するページは、通常検索の結果より平均25.7%新しい（公開からの日数で1,064日と1,432日）。最終更新日で見ると差は13.1%に縮む。最も新しいページを好むのは ChatGPT。AI による概要はむしろやや古いページを引用する | [Ahrefs: AI Assistants Prefer to Cite "Fresher" Content](https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/)（2025年夏） |
| 推薦の材料になるページの種類 | ChatGPT がソフトウェア・商品・代理店を推薦するとき、引用されたページの43.8%が「best X」型のまとめ記事。比較記事の上位に載っているブランドほど推薦されやすい。引用されたまとめ記事の79.1%は2025年に更新されていた。代理店の推薦で自社ページが引用される場合、30.4%は汎用の LP（トップページ） | [Ahrefs: Do Self-Promotional "Best" Lists Boost ChatGPT Visibility?](https://ahrefs.com/blog/best-lists-research/)（2025-12-04） |
| まとめ記事の衰え | ChatGPT での「best / top」型 URL の引用は、2025年12月から2026年1月に30%減。伸びたのは Wikipedia、Reddit、LinkedIn、G2・Capterra などのレビューサイト。伸びた比較記事には、候補が10〜20件と多い、外部データ（評価や公的データ）を引用している、選定方法を開示している、番号付きで機能・長所短所・料金・「こんな人向け」を書いている、という共通点があった。AI による概要では横ばいか増加 | [Seer Interactive: The Listicle Window Is Closing in AI Search](https://www.seerinteractive.com/insights/the-listicle-window-is-closing-in-ai-search-30-decline-mom)（2026-02-25、200万件超の引用） |
| 自社を1位にする比較記事 | 2026年1月20日ごろから、自社を1位にした「best」記事を多く持つ SaaS 企業の検索での露出が29〜49%落ちた（Google は特定のアップデートを認めていない）。2026年5月のコアアップデートで影響がサイト全体に広がった例もある。B2B の「best software」系100クエリで、AI による概要は自社比較記事を引用しつつ、その会社自体は推薦しないことが69% | [Lily Ray: Is Google Finally Cracking Down on Self-Promotional Listicles?](https://lilyraynyc.substack.com/p/is-google-finally-cracking-down-on)（2026年2月） / [Search Engine Land: AI Overviews cite self-serving listicles, recommend competitors 69% of the time](https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573)（2026年） |
| プラットフォームごとの引用元（英語圏） | 2024年8月〜2025年6月の約3,000万件の引用。ChatGPT は Wikipedia が首位、Perplexity と AI による概要は Reddit が首位、AI による概要では YouTube・Quora・LinkedIn も上位 | [Profound: AI Platform Citation Patterns](https://www.tryprofound.com/blog/ai-platform-citation-patterns)（2025年）※Semrush は ChatGPT の Reddit 引用が2025年8〜9月に急減したと報告しており、比率は大きく変わり続けている |
| 日本語での引用元 | 総合1位 YouTube、2位 note、3位 日本語版 Wikipedia、4位 アメブロ、5位 Yahoo!知恵袋。6位以下に PR TIMES、Reddit、マイベスト、楽天市場、英語版 Wikipedia。ChatGPT では Reddit が1位、PR TIMES が2位。Copilot では価格.com が5位 | [Ahrefs 日本語ブログ: AI が最も信頼するドメイン TOP10（2026年6月版）](https://ahrefs.com/blog/ja/brand-radar-top-10-cited-domains-2026-june/)（2026-06-23） / 2025年11月の [AI による概要 vs AI モード 日本のトップ1000引用ドメイン](https://ahrefs.com/ja/blog/ai-overviews-vs-ai-mode/) |
| 統計・引用・出典の追加 | 文章に統計、引用、出典を足すと、生成 AI の回答での露出が最大40%程度上がったという実験結果がある。ただし2023年の研究用の環境での結果で、実際の商用 AI での再現は確認していない | Aggarwal ほか「GEO: Generative Engine Optimization」（KDD 2024、arXiv:2311.09735）※**根拠は中程度** |

### 1-3. 引用されやすいページの形式（まとめ）

上の研究から言えることを、確度で分けて整理します。

**確度が高い（複数の公式文書や研究が一致している）**
- 検索インデックスに入っていて、クロールでき、スニペットが表示できること（Google・OpenAI・Perplexity の公式文書）
- 独自の一次情報があること：自社の体験、実データ、事例、手順（Google の「コモディティでない」コンテンツ）
- 見出しと段落がはっきりしていること（Google）
- 第三者のサイトでブランドが言及されていること（Ahrefs の相関研究、Google の「何を言われているか」の記述）

**確度は中程度（実データでは関係が見られるが、因果は証明されていない）**
- 最終更新が新しいこと。特に ChatGPT（Ahrefs、Seer）
- 比較記事・まとめ記事への掲載と、その中での順位（Ahrefs、Seer）
- 番号付きのリスト、料金、「こんな人向け」、長所と短所、選定方法の開示（Seer）
- 統計や出典の明記（GEO 論文）

**効果が確認されていない（第4章を参照）**
- llms.txt
- 構造化データの追加（FAQPage を含む）
- AI 向けに文章を細かく分けること（Google は不要と明言）

**著者情報について**: Google の helpful content の自己評価では「誰が書いたかが明らかか」「署名から著者の経歴に飛べるか」を問われ、架空の著者や偽の経歴は欺瞞とされています（[Google: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)、2026-11-28 閲覧）。ただし、著者情報が AI の引用を増やすことを直接示した実データ研究は見つかりませんでした。**［推測］** 実在する担当者の署名と経歴を載せると、信頼の評価と第三者からの指名言及の両方に効きます。

---

## 2. 「おすすめのサービスは？」で AI が特定のサービスを推薦する条件

研究と公式文書から言えることを整理します。

1. **第三者の比較記事・まとめ記事に載っていること。上位に載っていればなお良いです。** 推薦の根拠として引用されたページの43.8%は「best X」型でした（Ahrefs 2025-12）。日本語の「アフィリエイト 代理店 おすすめ」でも、上位はほぼすべて比較・まとめ記事です（第5章）。
2. **Web と YouTube でのブランド言及が多いこと。** 相関が最も強い要素です（Ahrefs 2025-12）。言及数で上位25%に入るかどうかで、AI による概要への登場回数が10倍以上違いました。
3. **口コミ・Q&A・UGC（ユーザー投稿）で話題にされていること。** 英語圏では Reddit・G2・Capterra、日本語では Yahoo!知恵袋・note・アメブロが伸びています（Seer 2026-02、Ahrefs 2026-06）。ただし Google は「本物でない言及は役に立たない」と書いているので、自作自演の投稿は逆効果になりえます。
4. **公式サイトで、事実が分かりやすく書かれていること。** 代理店を推薦するとき、自社ページから引用されるのは汎用の LP が30.4%でした（Ahrefs 2025-12）。**［推測］** AI は「何をする会社か」「料金」「誰向けか」「どこが違うか」を LP から抜き出して回答に使います。料金を「要問い合わせ」にしている競合が多いので、料金を公開していること自体が違いになります。
5. **エンティティ（会社・サービスとしての実体）の情報が一貫していること。** **［推測（公式の直接の根拠は薄い）］** サービス名、運営会社、所在地、料金、提供範囲が自社サイト・PR TIMES・note・SNS・比較サイトで同じ書き方になっていると、AI が同じサービスとして結びつけやすくなります。ブランド名を使ったアンカーテキストとの相関（0.51〜0.63）は、このことの間接的な根拠です。
6. **自社を1位にした比較記事は推薦につながりにくいです。** AI による概要は自社比較記事を引用しても、その会社自体は推薦しないことが69%ありました（Lily Ray）。同じ種類の記事を量産したサイトは、検索順位を落とす事例も出ています。

---

## 3. Google の公式な立場と、記事を多く出すときのリスク

### 3-1. 公式の立場

- **AI による概要と SEO**: 特別な対策は不要で、Google 検索の基本事項（Search Essentials）と通常の SEO に従えばよいとされています（[AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)）。
- **AI で作ったコンテンツ**: AI の使用自体は認められています。条件は Search Essentials とスパムポリシーを守ることです。AI を使って価値を加えないページを大量に作ると、スケールされたコンテンツの不正使用にあたる可能性があります。公開前に事実確認（タイトル、メタディスクリプション、構造化データ、alt 属性も含む）が必要で、自動化をどう使ったかを読者に説明することも勧められています（[Google: Using generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content)、2026-11-28 閲覧）。
- **スケールされたコンテンツの不正使用（scaled content abuse）**: 「主に検索順位を操作する目的で多くのページを生成すること」と定義され、作り方は問いません（AI でも人でも、その組み合わせでも対象）。例として、AI で価値のないページを大量に作る、他サイトの内容を言い換え・翻訳して並べる、価値を加えずにつなぎ合わせる、複数のサイトに分けて規模を隠す、が挙げられています（[Google: Spam policies](https://developers.google.com/search/docs/essentials/spam-policies)、2026-11-28 閲覧）。Google の AI 最適化ガイドも「検索順位や AI の回答を操作するために大量のページを作ることは、このポリシー違反」と明記しています。
- **helpful content の警告サイン**: 多くの話題を大量に作って何かが当たるのを待っている、多くの話題を広く自動化で作っている、他人の情報を要約しているだけ、専門性のない分野にトラフィック目当てで参入している、決まった文字数で書いている、内容をほとんど変えずに日付だけ新しくしている、読者がもう一度検索し直す必要がある（[Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)）。

### 3-2. 1日に何本も出すときのリスクと、それを避ける条件

公開の頻度そのものを禁じる記述は、Google の文書にはありません。リスクが高くなるのは次の条件が重なるときです。

| リスクの高い状態 | 避ける条件 |
|---|---|
| 同じ型の記事を、キーワードだけ替えて量産している（例：「○○ 代行 おすすめ」を地域や業種別に大量に作る） | 1本ごとに、その記事にしかない一次情報（自社の作業時間の実測、テンプレート、チェックリスト、事例、計算例）を入れる。似た記事は1本にまとめる |
| 自社を1位にした比較記事を何本も作る | 比較記事は1本だけにし、選定方法を開示し、自社は「こういう会社に向いている」という書き方にとどめる（他社を正しく扱う） |
| 中身を直さず日付と年号だけ更新する | 更新するときは中身（数字、法令、事例）を実際に直し、更新履歴を記事に残す |
| 専門外の話題に広げる | 「広告主のアフィリエイト運用」の範囲から出ない |
| 事実確認をしない AI の出力をそのまま出す | 法令（景品表示法・ステマ規制・薬機法）の記述は一次資料と照合する。AI をどう使ったかを開示する |
| 新しいサブドメインで、短期間に大量の記事を出す | **［推測］** 立ち上げ期は、1日の本数よりも、1本の深さとインデックス登録の状況（Search Console）を見ながら増やす。インデックスされない記事が増えるなら、出すペースを落とすサインと考える |

**［推測］** 現在のコラム13本は、いずれも広告主の実務に絞ったテーマで、範囲としては問題ありません。リスクは、今後「似たタイトルの工数削減記事」を毎日出し続けて、記事どうしの違いが薄くなった場合に生じます。

---

## 4. llms.txt・構造化データ・robots.txt の実際の効果

| 施策 | 効果が確認されているか | 根拠 |
|---|---|---|
| robots.txt で検索用の AI クローラーを許可する（OAI-SearchBot、PerplexityBot、Claude-SearchBot、Googlebot） | **確認されている（前提条件）**。ブロックすると表示されない。許可しただけで引用が増えるわけではない | OpenAI・Perplexity・Anthropic の公式文書。Google は通常の Googlebot でクロールし、Google-Extended は検索の AI 機能への表示には関係しない |
| 学習用クローラーの許可（GPTBot、ClaudeBot、Google-Extended） | **検索での表示との関係は確認されていない**。公式には検索表示とは別の扱い。**［推測］** モデルの知識にブランドが入る可能性はあるが、測れない | OpenAI 公式（GPTBot と OAI-SearchBot は別々に設定できる） |
| llms.txt | **効果は確認されていない**。Google は「無視するので、良くも悪くもならない」と明言。SE Ranking の約30万ドメインの分析では引用数との関係が見られず、モデルから外すと精度が上がった。AI のクローラーはほとんど取りに来ないという報告もある | [Google 最適化ガイド](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) / [SE Ranking: Does LLMs.txt impact your AI visibility?](https://seranking.com/blog/llms-txt/)（2025年） / [Optimizely: Does llms.txt work?](https://www.optimizely.com/field-notes/articles/does-llms-txt-work/) |
| 構造化データ（Organization / Service / FAQPage / Article） | **引用を増やす効果は確認されていない**。JSON-LD を追加した1,885ページと対照群4,000ページの比較では、どのプラットフォームでも目立った上昇はなかった（すでに引用されているページが対象。まだ引用されていないページへの効果は未検証）。リアルタイムでページを取りに行く AI 5種は、JSON-LD を読まずに見えている HTML だけを抽出していたという実験もある。Google は「AI 機能のための特別なマークアップは不要。リッチリザルトの対象になるので使い続ける価値はある」という立場。なお FAQ のリッチリザルトは、2023年から行政・医療の権威あるサイトに限定されている | [Ahrefs: schema AI citations](https://ahrefs.com/blog/schema-ai-citations/)（2026年5月） / [Search Atlas: The Limits of Schema Markup for AI Search](https://searchatlas.com/research/the-limits-of-schema-markup-for-ai-search/)（2025年12月） / Google 最適化ガイド |
| 見えている文章としての FAQ（質問と回答の段落） | **［推測］** 構造化データとしてではなく、本文の「よくある質問」として、AI の言い換えた検索（クエリファンアウト）と一致する短い答えを置くことには意味がありそう。直接の実データは見つからなかった | Google のクエリファンアウトの説明、searchVIU の「見えている HTML だけを抽出する」という結果からの推測 |

**アフィまかせの現状（ファイルで確認）**
- `site/robots.txt`: `User-agent: *` で全体を許可し、GPTBot・OAI-SearchBot・ClaudeBot・PerplexityBot・Google-Extended も明示的に許可しています。Claude-SearchBot・Claude-User・Perplexity-User は個別には書かれていませんが、`*` の許可でカバーされているため、**直す必要はありません**。
- `site/llms.txt`: すでにあります。効果は未確認ですが害もないので、残して構いません。新しい記事を追加するたびに更新する作業は、優先度を下げてください。
- 構造化データ: Article、FAQPage、BreadcrumbList、Organization、Service、Offer が入っています。ただし、記事の `author` が組織（合同会社IXS）だけで、個人の著者がいません。`sameAs`（SNS や会社ページなどの外部プロフィールへのリンク）もありません。

---

## 5. 日本の B2B マーケティング支援・運用代行分野で、上位や AI 回答に出るサイト

### 5-1. 観察した検索（2026-11-28、WebSearch で実施）

注意: 使った WebSearch は米国から実行される検索 API で、表示されたのは Google の日本語の通常検索や AI による概要そのものではありません。傾向をつかむための参考と考えてください。

| 検索語 | 上位に出たサイト | サイトの種類 |
|---|---|---|
| アフィリエイト 運用代行 おすすめ | stock-sun.com（自社の StockSun を前に出した比較記事）、shopowner-support.net（「PR」表記のある比較記事）、kigyolog.com（企業比較のデータベース）、aspicjapan.org（ASPIC のクラウドサービス比較） | 比較メディア、自社運営の比較記事、比較データベース |
| アフィリエイト 代理店 比較 | kigyolog.com、boxil.jp（BOXIL Magazine）、stock-sun.com（2026年版、26社を5分類）、shopowner-support.net、biz.ne.jp（ビジネス＋IT 系の比較まとめ）、aspicjapan.org | 比較メディア、SaaS 比較サイト |
| アフィリエイト 工数 削減 広告主 | PR TIMES のリリース（日刊工業新聞のサイトに転載）、ecnomikata.com（EC のミカタ）、netshop.impress.co.jp（ネットショップ担当者フォーラム）、shopowner-support.net、消費者庁（内閣府 消費者委員会）の資料 PDF | プレスリリース、業界メディア、公的資料 |

比較記事に名前が挙がっていた代理店の例: シード、エムフロ、ADrim、SQOOPY、フォースリーなど。料金を「要問い合わせ」にしている会社が多いことも分かりました。

### 5-2. 共通点

1. **「おすすめ」「比較」の検索では、比較メディアとまとめ記事が上位を占めます。** 個別の代理店の公式サイトはほとんど出ません。AI もこれらを材料にして推薦するので、**比較記事に載ること＝推薦の候補に入ること**です（Ahrefs 2025-12 の43.8%と一致）。
2. **「工数削減」などの悩みの検索では、PR TIMES と業界メディア（EC のミカタ、ネットショップ担当者フォーラム）が出ます。** 数字の入った事例（「工数50%削減」「広告費20%削減」）が引用されています。ChatGPT の日本語回答で PR TIMES が2位という Ahrefs のデータとも一致します。
3. **比較記事の多くは、料金相場（月20〜50万円）、料金体系（月額固定型・月額＋成果報酬型）、選び方の観点（媒体開拓、成果の質、表記・法務のリスク管理、レポートの透明性）を書いています。** AI の回答はこれらの観点で候補を並べるので、**公式 LP でこの観点ごとに自社の答えを書いておく**と、比較記事にも AI にも拾われやすくなります。**［推測］**
4. **料金を公開している会社は少ないです。** アフィまかせの「月5万円から・初期費用0円」は比較記事で目立つ材料になります。**［推測］**
5. 企業比較データベース（kigyolog、BOXIL、ASPIC）は、掲載を申し込める（無料・有料の）仕組みがあることが多いです。**［推測：各サイトの掲載条件は未確認］**

---

## 6. アフィまかせが今すぐやるべきこと（優先度順の10項目）

担当の区分: **SEO担当**＝コラム原稿、**PM**＝LP・テンプレート、**要オーナー承認**＝外部での言及

### 1. Google Search Console と Bing Webmaster Tools への登録とインデックスの確認
- **なぜ**: Google の AI 機能は「インデックスされていてスニペットを表示できる」ことが条件で、AI による概要の引用の76%は上位10位から選ばれます（Google 最適化ガイド、Ahrefs 2025-08）。ChatGPT 検索は Bing を含む外部の検索プロバイダーも使うとされています。**［Bing の比重は推測］**
- **何をするか**: サブドメインをドメインプロパティか URL プレフィックスで登録し、sitemap.xml を送信します。13本すべてのインデックス状況と、「Search generative AI features」の設定を確認します。Bing Webmaster Tools にも登録し、IndexNow を有効にします。
- **担当**: PM（アカウントの作成・所有権の確認は要オーナー承認）

### 2. LP に「AI が抜き出せる事実の段落」を置く
- **なぜ**: 代理店の推薦で自社ページから引用されるのは汎用 LP が30.4%（Ahrefs 2025-12）。比較記事は料金・体制・範囲・リスク管理の観点で並べています（第5章）。
- **何をするか**: LP の冒頭近くに、本文として見える形で次の内容を書きます。「アフィまかせは、合同会社IXSが運営する、広告主・代理店向けのアフィリエイト運用代行です」という一文の定義、対象顧客（例：ASP を2〜3社使っている広告主、担当者が兼務の会社）、任せられる業務の一覧、料金表（月5万円〜、初期費用0円、最低3か月）、向いていない会社、他社との違い（料金公開・表記チェックの込み・AI と担当者の分担）、運営会社の情報。構造化データの Service / Offer も、本文と同じ内容にそろえます。
- **担当**: PM

### 3. 実在する担当者の署名と経歴ページを作る
- **なぜ**: Google の helpful content の自己評価で「誰が書いたか」が問われ、架空の著者は欺瞞とされています（Google、helpful content）。今は全記事の author が組織だけです。
- **何をするか**: 実在する責任者か担当者の名前、経歴（運用の経験年数・担当してきた業種）、顔写真（実物）を載せたプロフィールページを作ります。各記事に署名を入れ、JSON-LD の author に Person を追加します。Organization には `sameAs`（会社サイト、X、note など）を入れます。架空の人物は使いません。
- **担当**: PM（テンプレート）、**要オーナー承認**（実名・写真の公開）

### 4. PR TIMES でサービス開始のリリースを出す
- **なぜ**: 日本語の ChatGPT の回答で、PR TIMES は引用ドメインの2位です（Ahrefs 2026-06）。「工数削減」の検索で PR TIMES のリリースが上位に出ています（第5章）。外部での言及はブランドの推薦との相関が最も強い要素です（Ahrefs 2025-12）。
- **何をするか**: 「月5万円からのアフィリエイト運用代行を開始」という事実のリリースに、料金、対象、提供範囲、運営会社を LP と同じ書き方で入れます。可能なら独自の数字（例：広告主のアフィリエイト業務の作業時間の調査結果）を付けます。
- **担当**: **要オーナー承認**（費用・公開内容）

### 5. 独自データを1本作り、コラムとリリースで使う
- **なぜ**: Google は「コモディティでない」一次情報を求めています（Google 最適化ガイド）。統計や出典を加えると AI の回答での露出が上がった実験があります（GEO 論文、**根拠は中程度**）。伸びている比較記事は外部データを引用しています（Seer 2026-02）。
- **何をするか**: 例として「広告主のアフィリエイト運用の作業時間（作業別）」の実測値か、小規模なアンケート（担当者30〜50人）の結果を出します。既存の `kosu-sakugen` 記事の「作業別の時間の目安」を、出典のある数字に置き換えます。調査方法・人数・時期も書きます。
- **担当**: SEO担当（記事化）、**要オーナー承認**（アンケートの実施・費用）

### 6. 比較記事サイト・企業データベースへの掲載を申し込む
- **なぜ**: 推薦の根拠ページの43.8%は「best X」型のまとめ記事で、上位に載るほど推薦されやすくなります（Ahrefs 2025-12）。日本語の「アフィリエイト 代理店 おすすめ／比較」の上位は、kigyolog、BOXIL、ASPIC、shopowner-support、stock-sun などの比較記事でした（第5章）。
- **何をするか**: 掲載の申し込み窓口がある比較メディアとデータベースを一覧にし、料金・対象・提供範囲を同じ書き方で申請します。有料掲載の場合は「PR」表記が付くことを前提にします。
- **担当**: **要オーナー承認**（申し込み・費用・各サイトの規約への同意）

### 7. 比較・選び方の記事を「自社を1位にしない」形にそろえる
- **なぜ**: 自社を1位にした比較記事を持つサイトは2026年1月以降に露出を落としており、AI による概要は自社比較記事を引用しても、その会社自体は推薦しないことが69%でした（Lily Ray 2026）。伸びている比較記事は選定方法を開示し、「こんな人向け」を書いています（Seer 2026-02）。
- **何をするか**: 既存の `dairiten-erabikata`（選び方8項目）と `affiliate-unyo-daiko`（費用相場）を、「判断基準と、自社運用・専業代理店・総合代理店・アフィまかせのような小さな代行のそれぞれが向いている会社」という書き方に保ちます。他社のランキング記事は作りません。自社の紹介は「向いている会社・向いていない会社」として最後に置きます。
- **担当**: SEO担当

### 8. 各記事に「よくある質問」と「短い答え」を本文として置く
- **なぜ**: AI は質問を言い換えた複数の検索を同時に行い、見えている HTML から文章を抜き出します（Google のクエリファンアウトの説明、Ahrefs 2025-08、searchVIU）。FAQPage の構造化データだけでは効果は確認されていません（Ahrefs 2026-05）。
- **何をするか**: 記事の冒頭に2〜3文の結論を置きます。末尾の FAQ は「アフィリエイトの運用代行の費用はいくら？」「成果報酬型と固定型のどちらがいい？」のように、実際に聞かれる質問の文にします。答えの最初の一文で数字や結論を言い切ります。数字には出典と時点を付けます。構造化データは本文と一致する範囲で今のまま残します。
- **担当**: SEO担当（原稿）、PM（テンプレートの冒頭要約欄）

### 9. note・YouTube（または X）で、自社サイトと同じ事実を一次情報として出す
- **なぜ**: 日本語の AI 回答で引用されるドメインの1位は YouTube、2位は note でした（Ahrefs 2026-06）。YouTube での言及はブランドの推薦との相関が最も強い要素です（約0.737、Ahrefs 2025-12）。
- **何をするか**: 公式の note アカウントで、コラムの要点版や「実務の失敗談」など自社サイトにない切り口の記事を出し、LP へリンクします。サービス名・運営会社・料金の書き方は統一します。余裕があれば、3〜5分の解説動画（成果承認の手順など）を YouTube に出します。**［推測：新しいアカウントの記事がすぐ引用されるかは未確認］**
- **担当**: **要オーナー承認**（外部アカウントの作成・運用）、SEO担当（原稿）

### 10. 公開ペースのルールと更新ルールを決める（量産のリスクを避ける）
- **なぜ**: スケールされたコンテンツの不正使用は作り方を問いません。helpful content は、日付だけの更新や広い範囲の自動化を警告サインとしています（Google スパムポリシー、helpful content）。自社比較記事の量産と年号だけの更新が重なったサイトが露出を落としています（Lily Ray 2026）。一方で ChatGPT は新しいページを好みます（Ahrefs、Seer）。
- **何をするか**: (a) 新しい記事は「その記事にしかない一次情報（実測、テンプレート、事例、計算例）が1つ以上あるもの」に限る。(b) 既存の記事と検索意図が重なる場合は、新しく書かずに既存の記事に追記する。(c) 更新するときは中身を直し、更新日と変更点を記事に残す（日付だけの更新はしない）。(d) AI の使い方を開示する一文をサイトに置く（例：「下書きに AI を使い、担当者が一次資料と照合して公開しています」）。(e) Search Console でインデックスされない記事が増えたら、公開ペースを落とす。**［(e) の基準は推測］**
- **担当**: SEO担当（運用ルール）、PM（更新履歴の表示欄）

### やらなくてよいこと（優先度を下げる）
- llms.txt の作り込みと頻繁な更新（効果未確認。今あるものは残してよい）
- 構造化データの種類を増やすこと（引用の増加は確認されていない。本文との一致の確認だけで十分）
- robots.txt の書き換え（今の設定で、検索用の AI クローラーはすべて許可されている）
- 口コミや Q&A サイトへの自作自演の投稿（Google は「本物でない言及は役に立たない」と明言。ステマ規制にも関わる）

---

## 7. 測り方（任意）

- **［推測］** 月に1回、ChatGPT（検索あり）・Perplexity・Gemini・Google の AI モードに、決まった質問を10個ほど投げ、アフィまかせが引用・推薦されたかを記録します。質問の例：「アフィリエイト 運用代行 おすすめ」「アフィリエイトの工数を減らしたい広告主向けのサービス」「月5万円くらいで頼めるアフィリエイト代行」「アフィリエイトの成果承認を外注したい」。回答は毎回変わるため、1回の結果ではなく傾向で判断します。
- Search Console の検索パフォーマンス（AI 機能のクリックも通常の検索結果に含めて集計されます）と、GA4 の参照元（chatgpt.com、perplexity.ai など）を合わせて見ます。

---

## 出典一覧（閲覧日 2026-11-28）

**公式文書**
- Google 検索セントラル「Optimizing your website for generative AI features on Google Search」 https://developers.google.com/search/docs/fundamentals/ai-optimization-guide （日付の記載なし）
- Google 検索セントラル「AI features and your website」 https://developers.google.com/search/docs/appearance/ai-features
- Google 検索セントラル ブログ「Top ways to ensure your content performs well in Google's AI experiences on Search」 https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search （2025-05-21）
- Google 検索セントラル「Spam policies for Google web search」 https://developers.google.com/search/docs/essentials/spam-policies
- Google 検索セントラル「Using generative AI content」 https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Google 検索セントラル「Creating helpful, reliable, people-first content」 https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Japan ブログ「Google 検索における『AI モード』を日本語で提供開始」 https://blog.google/intl/ja-jp/products/explore-get-answers/ai-mode-search/ （2025-09-09）
- OpenAI「Overview of OpenAI Crawlers」 https://developers.openai.com/api/docs/bots
- Perplexity「Perplexity Crawlers」 https://docs.perplexity.ai/guides/bots
- Anthropic ヘルプ「ClaudeBot / robots.txt controls」 https://support.claude.com/en/articles/8896518

**実データ研究**
- Ahrefs「Only 12% of AI Cited URLs Rank in Google's Top 10」 https://ahrefs.com/blog/ai-search-overlap/ （2025-08-11）
- Ahrefs「An Analysis of AI Overview Brand Visibility Factors (75K Brands)」 https://ahrefs.com/blog/ai-overview-brand-correlation/ （2025年5月）
- Ahrefs「Top Brand Visibility Factors in ChatGPT, AI Mode, and AI Overviews」 https://ahrefs.com/de/blog/ai-brand-visibility-correlations/ （2025-12-12）
- Ahrefs「AI Assistants Prefer to Cite "Fresher" Content」 https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/ （2025年）
- Ahrefs「Do Self-Promotional "Best" Lists Boost ChatGPT Visibility?」 https://ahrefs.com/blog/best-lists-research/ （2025-12-04）
- Ahrefs「schema AI citations」 https://ahrefs.com/blog/schema-ai-citations/ （2026年5月）
- Ahrefs 日本語「AI が最も信頼するドメイン TOP10（2026年6月版）」 https://ahrefs.com/blog/ja/brand-radar-top-10-cited-domains-2026-june/ （2026-06-23）
- Ahrefs 日本語「AI による概要 vs AI モード 日本のトップ1000引用ドメイン」 https://ahrefs.com/ja/blog/ai-overviews-vs-ai-mode/ （2025-11-18）
- Seer Interactive「The Listicle Window Is Closing in AI Search」 https://www.seerinteractive.com/insights/the-listicle-window-is-closing-in-ai-search-30-decline-mom （2026-02-25）
- Lily Ray「Is Google Finally Cracking Down on Self-Promotional Listicles?」 https://lilyraynyc.substack.com/p/is-google-finally-cracking-down-on （2026年2月）
- Search Engine Land「Google AI Overviews cite self-serving listicles, recommend competitors」 https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573 （2026年）
- SE Ranking「Does LLMs.txt impact your AI visibility and citations?」 https://seranking.com/blog/llms-txt/ （2025年）
- Optimizely「Does llms.txt work?」 https://www.optimizely.com/field-notes/articles/does-llms-txt-work/
- Search Atlas「The Limits of Schema Markup for AI Search」 https://searchatlas.com/research/the-limits-of-schema-markup-for-ai-search/ （2025年12月）
- Profound「AI Platform Citation Patterns」 https://www.tryprofound.com/blog/ai-platform-citation-patterns （2025年）
- Aggarwal ほか「GEO: Generative Engine Optimization」 KDD 2024, arXiv:2311.09735

**日本の検索の観察（2026-11-28）**
- https://stock-sun.com/column/affiliate-advertising-agency/
- https://www.shopowner-support.net/customer_attraction_information/web/affiliate/operation-agency/
- https://www.shopowner-support.net/customer_attraction_information/online/affiliate/affiliate-ad-agency/
- https://kigyolog.com/service.php?id=462
- https://boxil.jp/mag/a8629/
- https://www.aspicjapan.org/asu/article/37336
- https://www.biz.ne.jp/matome/2010197/
- https://www.nikkan.co.jp/releases/view/9892 （PR TIMES の転載）
- https://ecnomikata.com/knowhow/24116/
- https://netshop.impress.co.jp/node/3409
