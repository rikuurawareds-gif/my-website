# 月次レポート（M8）v0

ASP ごとに形の違う成果 CSV を共通の形にそろえ、ASP × メディア × 月で集計してレポートの下書きを作る。

## データの流れ（顧客の手間ゼロ）
1. ASP のデータは、代理店権限 → ASP 担当者からの定期送付 → 専用ログインの順で集める（`../docs/decisions.md`）。顧客に CSV を送ってもらう方式は使わない
2. ASP 担当者からのメールは、専用アドレス（オーナーの Gmail の「+asp」付きアドレス）に届く → `../automation/asp-intake.gs` が毎時、顧客の `01_ASP成果CSV` フォルダに振り分ける（設定は Drive `08_顧客/ASP振り分け設定`）
3. 月初に `report.py` で集計し、AI（コワーク）が `knowledge/report-playbook.md` の型で分析コメントと打ち手を書き、担当者が確認して送る

## 使い方
```
python3 report.py --in <顧客の01_ASP成果CSVフォルダ> --month 2026-11 --client 顧客名 --out report.md --csv unified.csv
```
- 文字コード（UTF-8 / Shift_JIS）、区切り（カンマ / タブ）、見出しの上の説明行、「合計」行を自動で扱う
- 列名はよくある日本語名から自動判定。判定できない列はレポートの末尾に「取り込みの注意」として出る → `../automation/asp-formats/` に対応表を足す
- 成果1件ごとの明細 CSV（ステータス列で承認・否認を判定）と、メディア別の集計 CSV の両方に対応
- テスト: `python3 tests/test_report.py`（架空のデータ3種類）
