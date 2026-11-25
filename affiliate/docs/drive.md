# Google Drive 構成

ルート: [アフィリエイト事業](https://drive.google.com/drive/folders/15YjEuSvXCW638BGOe-8edyTtuCaG46Oi)（`15YjEuSvXCW638BGOe-8edyTtuCaG46Oi`）

| フォルダ | ID | 入れるもの |
|---|---|---|
| 00_PM・経営 | `11jQh5lBY3wKICruwEr5-bOiCOIZ8Meph` | 意思決定ログ、オーナー向け月次まとめ |
| 01_事業設計・リサーチ | `1JhNyNmoSBmf10zUSu32rWstn28e0J_sR` | ジャンル比較、競合調査（Markdownの写し） |
| 02_サービス設計 | `1eMXAwwhWqsb68n4WELDQY43d4yoQzIbO` | 導線図、仕様書の写し |
| 03_デザイン素材 | `1oBIi8JiHHRrUranb0c2wDawGAf5EUYQN` | 画像、ロゴ、スクリーンショット |
| 04_コンテンツ・LP原稿 | `1TyBWptKUUQJv6eYlteyuAnmizRTnu-M9` | 原稿のレビュー用コピー |
| 05_計測・KPI | `1r9pA_aKF-uaTz2FnvDU5_DxjO9RD3SBG` | KPIシート、ASP取込シート |
| 06_ASP・契約 | `1t5WDha4TuU0WKoUYQyDW_Ph0smhRDJrw` | ASP案件管理、規約PDF |
| 07_法務・コンプライアンス | `1a89nDptuN9cyUnbdxE8b64iZznEh-gIu` | 法令メモ、レビュー記録 |
| 08_顧客 | `1XESUcnk2cU6h6PN0AX-H2JZUSjtXBfyW` | 顧客ごとのフォルダと顧客管理シート |
| 99_アーカイブ | `16cMyE6nvX-F7An5Pm0-DIyCnqhGO9Lik` | 終了した案件・ページ |

## スプレッドシート

| シート | ID | 更新者 |
|---|---|---|
| [KPI_週次](https://docs.google.com/spreadsheets/d/1ElKlECNYHWdqrCTFxZe0xgoBzXEi6ZVf-ZfWvP903E8/edit) | `1ElKlECNYHWdqrCTFxZe0xgoBzXEi6ZVf-ZfWvP903E8` | Apps Script が GA4 から毎週自動取込（`affiliate/automation/ga4-to-sheet.gs`） |
| [ASP管理画面_日次取込](https://docs.google.com/spreadsheets/d/1-0RVdWvSOMapYX1GI95C4094d9gQdDU55nZs2gnFyxs/edit) | `1-0RVdWvSOMapYX1GI95C4094d9gQdDU55nZs2gnFyxs` | ASPのCSVを貼る（→ `asp.md`） |
| [ASP案件管理（自社メディアを運営する場合用。今は使わない）](https://docs.google.com/spreadsheets/d/1gT57CpD6iyJ8RSFrVb4sZkXD9N_RvOWBax530lc_VfY/edit) | `1gT57CpD6iyJ8RSFrVb4sZkXD9N_RvOWBax530lc_VfY` | business-strategist / PM |
| [意思決定ログ](https://docs.google.com/spreadsheets/d/1SRn6rCWL8J-nMbMl-Z4dotP4EhER40Opdnas1XxWMFA/edit) | `1SRn6rCWL8J-nMbMl-Z4dotP4EhER40Opdnas1XxWMFA` | PM |

## 顧客フォルダ
新しい顧客が決まったら、`08_顧客/_顧客テンプレート（複製して使う）`（`1pmy5Vp5TryuUXqYxRQEnrCqq_wlDnRcD`）と同じ構成で `<顧客ID>_<社名>` フォルダを作り、顧客の担当者と共有する。
- `01_ASP成果CSV（顧客がここに置く）`
- `02_月次レポート`
- `03_表記チェックレポート`
- `04_契約・レギュレーション`
- `提携メディア台帳`（スプレッドシート）

顧客管理シート: [顧客管理](https://docs.google.com/spreadsheets/d/1w4G0OlehBrubnMqX3sb6XtJF-hJcR0b9dGm_PwnOtJk/edit)（`1w4G0OlehBrubnMqX3sb6XtJF-hJcR0b9dGm_PwnOtJk`）

## ルール
- 正本は GitHub。Drive はオーナーが読むための写しと、スプレッドシート・契約書類の置き場。
- 個人情報を含むファイルは Drive にも置かない（フォーム回答はフォームサービス側に保存し、集計値だけ持ってくる）。
