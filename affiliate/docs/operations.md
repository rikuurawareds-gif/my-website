# 運用フロー

## A. オーナーからの依頼
オーナー → PM → 担当（並列）→ compliance-reviewer → PM → PR → オーナー承認 → 公開

## B. 週次サイクル（毎週月曜、自動）
1. Apps Script が GA4 の前週分を `KPI_週次` に追記（朝6時台）
2. 週次タスクで PM セッションが起動し、`analyst` に週次レポートを作らせる
3. `kpi.md` の発動条件に当たる指標があれば、PM が該当担当に改善案と実装を振り、ブランチと PR まで進める
4. PM がオーナーに「今週の数字 / やったこと / 承認してほしいPR」を短く報告

## C. 新しいページを作る
1. business-strategist: 案件とキーワードの選定
2. service-architect: 仕様書（導線・フォーム・計測）
3. content-writer: 原稿
4. designer: 実装（テンプレートから）
5. analyst: 計測の抜け確認
6. compliance-reviewer: 公開前チェック
7. オーナー承認 → 公開

## D. CVR 改善（A/Bテスト）
cro-specialist が計画書を書く → 実装 → 最低2週間・各バリアント100CV以上（少ない場合は期間延長）→ 結果判定 → 勝ちを本採用
