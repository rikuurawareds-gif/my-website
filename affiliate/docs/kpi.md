# KPI 定義と改善の発動条件

## ファネル
セッション → LP到達 → フォーム開始 → フォーム完了 → 広告クリック → ASP発生 → ASP承認

| 指標 | 計算式 | 初期の目安（仮） | 下回ったら |
|---|---|---|---|
| フォーム開始率 | form_start ÷ page_view | 20% | `designer`（ファーストビュー）+ `content-writer`（見出し） |
| フォーム完了率 | generate_lead ÷ form_start | 50% | `cro-specialist`（設問数・ステップ離脱） |
| 広告CTR | affiliate_click ÷ page_view | 10% | `cro-specialist` + `content-writer`（CTA・比較表） |
| ASP発生率 | ASP発生件数 ÷ affiliate_click | 案件ごと | `business-strategist`（案件の見直し） |
| 承認率 | 承認件数 ÷ 発生件数 | 案件ごと | `business-strategist`（流入の質・案件変更） |
| EPC | 承認報酬 ÷ affiliate_click | 案件ごと | ページ・案件の優先順位づけに使う |

- 目安はジャンル決定後に `business-strategist` が実データに合わせて更新する。
- 週のセッションが100未満のページは判定しない（データ不足）。

## 判定のしかた
- 2週連続で目安を下回ったら、PM が該当担当に改善を振る。
- 前週比で50%以上落ちたら、まず計測の故障を疑い `analyst` に確認させる。
