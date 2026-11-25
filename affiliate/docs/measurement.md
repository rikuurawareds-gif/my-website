# 計測設計（GA4）

## 1. GA4 の基本設定
| 項目 | 設定 |
|---|---|
| プロパティ | 事業で1つ。ウェブデータストリームを1つ（サイトのドメイン） |
| 拡張計測機能 | ページビュー・スクロール・離脱クリックをON。**フォーム操作はOFF**（独自イベントと二重になるため） |
| データ保持期間 | 14か月 |
| 内部トラフィック | オーナーと開発時のアクセスを除外（`?internal=1` で訪問すると `track.js` が以後 `traffic_type=internal` を付ける） |
| キーイベント | `generate_lead`、`affiliate_click` |
| BigQuery リンク | 月間1万セッションを超えたら設定（無料枠で足りる） |

## 2. イベント仕様（実装: `affiliate/lp/assets/track.js`）
| イベント | いつ | パラメータ |
|---|---|---|
| `page_view` | 自動 | `page_id` |
| `form_start` | フォームの最初の入力 | `page_id`, `form_id` |
| `form_step` | 設問ステップを進んだ | `page_id`, `form_id`, `step`（数値）, `step_name` |
| `generate_lead` | フォーム送信完了 | `page_id`, `form_id` |
| `affiliate_click` | 広告リンクのクリック | `page_id`, `aff_id`, `asp`, `program_id`, `position` |
| `experiment_view` | A/Bテスト対象を表示 | `page_id`, `experiment_id`, `variant` |

### HTML 側の書き方
```html
<body data-page-id="lp-001">
<form data-form-id="survey-001"> ... <div data-step="2" data-step-name="予算"> ... </form>
<a href="(ASPのリンク)" data-aff-id="a8-xxx-01" data-asp="a8" data-program-id="xxx" data-position="fv">申し込む</a>
```

## 3. カスタムディメンション（GA4管理画面で登録、すべてイベントスコープ）
`page_id`, `form_id`, `step`, `step_name`, `aff_id`, `asp`, `program_id`, `position`, `experiment_id`, `variant`, `traffic_type`

## 4. 流入元（UTM）ルール
- `utm_source`: x / instagram / tiktok / google / line など小文字
- `utm_medium`: social / cpc / email / referral
- `utm_campaign`: `<YYYYMM>-<施策名>`
- 自然検索には付けない。

## 5. ASP との突き合わせ
- GA4 の `affiliate_click` と ASP 管理画面のクリック数を週次で比較する。ずれが20%を超えたら analyst が原因を調べる（広告ブロッカー、リンクの貼り間違い、ボット）。
- ASPがサブID（任意パラメータ）に対応している場合は、`page_id` と `position` を渡して成果をページ単位で追う。対応可否はASPごとに異なるので `ASP案件管理` に記録する。

## 6. 自動集計
`affiliate/automation/ga4-to-sheet.gs` を KPI_週次 シートの Apps Script に入れると、毎週月曜に前週分が自動で追記される。
