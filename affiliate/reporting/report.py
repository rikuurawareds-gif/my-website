#!/usr/bin/env python3
"""
アフィまかせ 月次レポート v0（M8）

ASP ごとに形の違う成果 CSV を共通の形にそろえ、ASP × メディア × 月で集計し、
レポートの下書き（Markdown）と共通形式の CSV を出す。

使い方:
  python3 report.py --in 顧客フォルダ/01_ASP成果CSV --month 2026-11 --client 顧客名 --out report.md --csv unified.csv

- 列名は、よくある日本語の列名から自動で判定する（ALIASES）。ASP ごとの正確な対応は
  ../automation/asp-formats/<ASP名>.md ができたら FORMATS に足す
- 文字コードは UTF-8 / Shift_JIS(CP932) を自動判定
- 成果1件ごとの CSV（明細）と、メディア別に集計済みの CSV（集計）の両方に対応
- 分析コメントと翌月の打ち手は、ここでは数字の変化だけを書く。文章はコワーク等の AI が
  knowledge/report-playbook.md の型で仕上げ、人が確認する
"""
import argparse, csv, io, re, sys
from collections import defaultdict
from pathlib import Path

# 共通の列 → よくある列名（部分一致。上から順に優先）
ALIASES = {
    "date":          ["成果発生日", "発生日時", "発生日", "成果日", "注文日", "日付", "対象日", "年月日", "対象月", "年月"],
    "confirm_date":  ["確定日", "承認日", "確定日時"],
    "media":         ["メディア名", "サイト名", "パートナー名", "媒体名", "メディア", "サイト", "パートナー"],
    "media_id":      ["メディアID", "サイトID", "パートナーID", "媒体ID"],
    "program":       ["プログラム名", "案件名", "広告名", "プロモーション名"],
    "clicks":        ["クリック数", "クリック"],
    "occurred":      ["発生件数", "成果件数", "発生数", "成果数", "件数"],
    "occurred_rw":   ["発生報酬", "発生金額", "成果報酬額", "報酬額", "報酬", "成果報酬", "金額"],
    "approved":      ["承認件数", "確定件数", "承認数", "確定数"],
    "approved_rw":   ["承認報酬", "確定報酬", "承認金額", "確定金額"],
    "rejected":      ["否認件数", "非承認件数", "キャンセル件数", "否認数"],
    "status":        ["ステータス", "状態", "承認状況", "成果ステータス"],
}
APPROVED_WORDS = ["承認", "確定", "approved"]
REJECTED_WORDS = ["否認", "非承認", "キャンセル", "取消", "却下", "rejected"]
NUM_FIELDS = ["clicks", "occurred", "occurred_rw", "approved", "approved_rw", "rejected"]


def read_csv(path):
    raw = Path(path).read_bytes()
    for enc in ("utf-8-sig", "cp932"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    delim = "\t" if text.count("\t") > text.count(",") else ","
    rows = list(csv.reader(io.StringIO(text), delimiter=delim))
    # 見出し行を探す（上の数行に説明が入っている CSV がある）
    for i, r in enumerate(rows[:10]):
        joined = "".join(r)
        hits = sum(1 for names in ALIASES.values() if any(n in joined for n in names))
        if hits >= 2:
            return rows[i], rows[i + 1:]
    return rows[0], rows[1:]


def map_columns(header):
    mapping, used = {}, set()
    for field, names in ALIASES.items():
        for n in names:
            for idx, h in enumerate(header):
                if idx in used:
                    continue
                if n in h.strip():
                    mapping[field] = idx
                    used.add(idx)
                    break
            if field in mapping:
                break
    return mapping


def num(s):
    s = (s or "").replace(",", "").replace("¥", "").replace("円", "").replace("件", "").strip()
    try:
        return float(s) if s else 0.0
    except ValueError:
        return 0.0


def month_of(s):
    m = re.search(r"(20\d\d)[/\-年.]?\s?(\d{1,2})", s or "")
    return f"{m.group(1)}-{int(m.group(2)):02d}" if m else ""


def guess_asp(path):
    name = Path(path).name
    m = re.match(r"\d{8}_\d{4}_([^_]+)_", name)  # asp-intake.gs の保存名
    if m:
        return m.group(1)
    for k in ["A8", "バリューコマース", "afb", "アクセストレード", "もしも", "felmat", "レントラックス", "プレスコ", "JANet", "TG"]:
        if k.lower() in name.lower():
            return k
    return Path(path).stem


def normalize(path):
    header, rows = read_csv(path)
    m = map_columns(header)
    asp = guess_asp(path)
    is_detail = "status" in m and not any(f in m for f in ("occurred", "approved"))
    out = []
    for r in rows:
        if not any(c.strip() for c in r):
            continue
        g = lambda f: r[m[f]] if f in m and m[f] < len(r) else ""
        rec = dict(asp=asp, month=month_of(g("date") or g("confirm_date")), media=g("media").strip() or "(不明)",
                   media_id=g("media_id"), program=g("program"))
        if is_detail:  # 明細: 1行1成果
            st = g("status")
            rw = num(g("occurred_rw"))
            rec.update(clicks=0, occurred=1, occurred_rw=rw,
                       approved=1 if any(w in st for w in APPROVED_WORDS) else 0,
                       approved_rw=rw if any(w in st for w in APPROVED_WORDS) else 0,
                       rejected=1 if any(w in st for w in REJECTED_WORDS) else 0)
        else:
            for f in NUM_FIELDS:
                rec[f] = num(g(f))
        if rec["media"] in ("合計", "総計", "小計"):
            continue
        out.append(rec)
    return out, m, header


def aggregate(records, month=None):
    agg = defaultdict(lambda: defaultdict(float))
    for r in records:
        if month and r["month"] and r["month"] != month:
            continue
        key = (r["asp"], r["media"])
        for f in NUM_FIELDS:
            agg[key][f] += r[f]
    return agg


def pct(a, b):
    return f"{a / b * 100:.1f}%" if b else "-"


def yen(v):
    return f"¥{v:,.0f}"


def render(client, month, agg, prev, unmapped):
    tot = defaultdict(float)
    for v in agg.values():
        for f in NUM_FIELDS:
            tot[f] += v[f]
    ptot = defaultdict(float)
    for v in prev.values():
        for f in NUM_FIELDS:
            ptot[f] += v[f]
    lines = [f"# {client} アフィリエイト月次レポート（{month}）下書き", "",
             "> 数字は ASP の CSV から自動で集計したもの。分析コメントと翌月の打ち手は、`knowledge/report-playbook.md` の型で AI が書き、担当者が確認してから送る。", "",
             "## 1. 全体", "", "| 指標 | 今月 | 前月 | 前月比 |", "|---|---|---|---|"]
    for label, f, fmt in [("クリック", "clicks", lambda v: f"{v:,.0f}"), ("発生件数", "occurred", lambda v: f"{v:,.0f}"),
                          ("発生報酬", "occurred_rw", yen), ("承認件数", "approved", lambda v: f"{v:,.0f}"),
                          ("承認報酬", "approved_rw", yen), ("否認件数", "rejected", lambda v: f"{v:,.0f}")]:
        lines.append(f"| {label} | {fmt(tot[f])} | {fmt(ptot[f]) if prev else '-'} | {pct(tot[f], ptot[f]) if prev else '-'} |")
    lines += [f"| 承認率 | {pct(tot['approved'], tot['occurred'])} | {pct(ptot['approved'], ptot['occurred']) if prev else '-'} | |",
              f"| CVR（発生÷クリック） | {pct(tot['occurred'], tot['clicks'])} | {pct(ptot['occurred'], ptot['clicks']) if prev else '-'} | |", ""]
    by_asp = defaultdict(lambda: defaultdict(float))
    for (asp, _), v in agg.items():
        for f in NUM_FIELDS:
            by_asp[asp][f] += v[f]
    lines += ["## 2. ASP 別", "", "| ASP | 発生 | 承認 | 承認率 | 承認報酬 |", "|---|---|---|---|---|"]
    for asp, v in sorted(by_asp.items(), key=lambda x: -x[1]["approved_rw"]):
        lines.append(f"| {asp} | {v['occurred']:,.0f} | {v['approved']:,.0f} | {pct(v['approved'], v['occurred'])} | {yen(v['approved_rw'])} |")
    lines += ["", "## 3. メディア別（承認報酬の多い順・上位20）", "", "| ASP | メディア | クリック | 発生 | CVR | 承認 | 承認率 | 承認報酬 | 前月比（発生） |", "|---|---|---|---|---|---|---|---|---|"]
    for (asp, media), v in sorted(agg.items(), key=lambda x: -x[1]["approved_rw"])[:20]:
        pv = prev.get((asp, media))
        chg = pct(v["occurred"], pv["occurred"]) if pv and pv["occurred"] else ("新規" if prev else "-")
        lines.append(f"| {asp} | {media} | {v['clicks']:,.0f} | {v['occurred']:,.0f} | {pct(v['occurred'], v['clicks'])} | {v['approved']:,.0f} | {pct(v['approved'], v['occurred'])} | {yen(v['approved_rw'])} | {chg} |")
    # 変化の大きいメディア
    if prev:
        moves = []
        for k in set(agg) | set(prev):
            a, b = agg.get(k, {}).get("occurred", 0), prev.get(k, {}).get("occurred", 0)
            if max(a, b) >= 5:
                moves.append((a - b, k, a, b))
        moves.sort()
        lines += ["", "## 4. 変化の大きいメディア（発生件数）", ""]
        for d, (asp, media), a, b in moves[:3]:
            if d < 0:
                lines.append(f"- 減少: {asp} / {media}: {b:,.0f} → {a:,.0f}")
        for d, (asp, media), a, b in reversed(moves[-3:]):
            if d > 0:
                lines.append(f"- 増加: {asp} / {media}: {b:,.0f} → {a:,.0f}")
    lines += ["", "## 5. 分析コメントと翌月の打ち手", "", "（AI が下書きし、担当者が確認する）", ""]
    if unmapped:
        lines += ["## 取り込みの注意", ""] + [f"- {u}" for u in unmapped]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--client", default="顧客")
    ap.add_argument("--out", default="report.md")
    ap.add_argument("--csv")
    a = ap.parse_args()
    y, mth = map(int, a.month.split("-"))
    prev_month = f"{y - 1}-12" if mth == 1 else f"{y}-{mth - 1:02d}"
    records, notes = [], []
    files = [p for p in Path(a.indir).glob("*") if p.suffix.lower() in (".csv", ".tsv", ".txt")]
    for p in sorted(files):
        recs, m, header = normalize(p)
        missing = [f for f in ("media", "occurred", "approved") if f not in m and not ("status" in m)]
        if missing:
            notes.append(f"{p.name}: 列を判定できなかった項目 {missing}（見出し: {header[:8]}…）→ asp-formats に対応表を追加")
        if not any(r["month"] for r in recs):
            notes.append(f"{p.name}: 月が判定できないため、全行を {a.month} として扱った")
            for r in recs:
                r["month"] = a.month
        records += recs
    cur = aggregate(records, a.month)
    prev = aggregate(records, prev_month)
    Path(a.out).write_text(render(a.client, a.month, cur, prev, notes), encoding="utf-8")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as fp:
            w = csv.DictWriter(fp, fieldnames=["asp", "month", "media", "media_id", "program"] + NUM_FIELDS)
            w.writeheader()
            w.writerows(records)
    print(f"{len(files)} ファイル、{len(records)} 行 → {a.out}" + (f"（注意 {len(notes)} 件）" if notes else ""))


if __name__ == "__main__":
    main()
