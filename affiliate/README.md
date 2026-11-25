# アフィリエイト事業

運営ルールは [CLAUDE.md](CLAUDE.md)、運用フローは [docs/operations.md](docs/operations.md)。

## オーナーにしかできないこと（最初の1回だけ）

本人確認・ログイン・お金が絡むものだけが残っています。それ以外は PM と各担当が進めます。

| # | やること | 所要 | 終わったら PM に伝えること |
|---|---|---|---|
| 1 | ジャンルを決める（または「候補を出して」と PM に頼む） | — | ジャンル or 依頼 |
| 2 | GA4 でプロパティとウェブストリームを作る（[analytics.google.com](https://analytics.google.com)） | 5分 | 測定ID（G-…）とプロパティID（数字） |
| 3 | KPI_週次 シートに Apps Script を入れる（手順は `automation/ga4-to-sheet.gs` の先頭） | 5分 | 「入れた」 |
| 4 | ASP に登録する（まず A8.net。サイトURLは公開後のURL） | 15分/社 | 登録したASP名 |
| 5 | 週1回、ASPの成果CSVを `ASP管理画面_日次取込` に貼る（後で自動化予定） | 5分/週 | — |
| 6 | PM が出す PR を確認して承認する | 随時 | — |

2〜3 は GA4 の管理画面で PM が手順を案内しながら進めることもできます。

## 構成
```
affiliate/
  CLAUDE.md            運営ルール（全担当が読む）
  docs/                設計書（計測・KPI・ASP・法務・デザイン・Drive）
  lp/                  公開するページ
    _template/         LPテンプレート（3ステップ診断 + 結果 + 広告リンク）
    assets/            計測(track.js)・A/Bテスト(ab.js)・共通CSS・設定
  automation/          GA4 → スプレッドシート自動取込
  reports/             週次レポート
.claude/agents/        各担当の定義
```
