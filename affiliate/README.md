# アフィリエイト運用支援サービス

事業計画は [docs/business-plan.md](docs/business-plan.md)、運営ルールは [CLAUDE.md](CLAUDE.md)、進め方は [docs/roadmap.md](docs/roadmap.md)。

## オーナーにしかできないこと

**作業は貼るだけの指示文にしてある → [`ops/owner-tasks/`](ops/owner-tasks/README.md)。新しい作業が出たら `/sagyo-bunsyo` で指示文を作る。**

本人確認・契約・お金・外部アカウントに関わるものだけが残っています。

| # | やること | いつ | 所要 |
|---|---|---|---|
| 1 | 商品の順番と価格の方向性を決める（PMが調査結果つきで案を出す） | 今 | 判断のみ |
| 2 | 事業の名前（屋号・サービス名）を決める | フェーズ1 | 判断のみ |
| 3 | Claude API のキーを発行し、環境の認証情報に登録する（PMが登録画面を出す） | フェーズ1 | 5分 |
| 4 | 利用規約・業務委託契約・NDA のたたき台を弁護士に見てもらう | 最初の顧客の前 | 外注 |
| 5 | 運用担当用の Chatwork アカウントを作り、APIトークンを登録する | フェーズ3 | 10分 |
| 6 | Google Cloud のプロジェクトと請求先を作る | フェーズ3 | 10分 |
| 7 | 最初の顧客への営業（知り合いの広告主など） | フェーズ1〜 | — |
| 8 | PM が出す PR・顧客向け文面の承認 | 随時 | — |

自社サービスLPの集客計測（GA4）を始めるときは、`automation/ga4-to-sheet.gs` の手順を使います。

## 構成
```
affiliate/
  CLAUDE.md          運営ルール（全担当が読む）
  docs/
    business-plan.md 事業計画（顧客・商品・価格仮説・順番・前提）
    services/        4つの商品の仕様
    architecture.md  システム構成（Claude Code と Claude API の役割分担）
    roadmap.md       フェーズごとのやること
    …                計測・KPI・ASPナレッジ・Drive構成・運用フロー
  lp/                自社サービスLP（テンプレート、計測、A/Bテスト）
  automation/        GA4 → スプレッドシート取込
.claude/agents/      担当の定義（11）
```
