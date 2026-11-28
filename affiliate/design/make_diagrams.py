"""コラム記事の図解（SVG）を書き出す。出力先は引数のフォルダ（site/assets/img/diagrams）。
記事の原稿では `![説明](/assets/img/diagrams/<名前>.svg)` の1行で差し込む（build.py が図として表示する）。
幅 560 の viewBox に、文字 15px 以上で描く（スマホ幅でも 9px 前後で読める）。数字は記事の本文と同じものだけを使う。"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
INK, SUB, KNOT, LINE, BG, BLUE, CYAN, WARN = "#0f1424", "#5b6378", "#9aa4bf", "#e4e7ef", "#f4f6fb", "#3366ff", "#22d3ee", "#b54708"
FT = 'font-family="Noto Sans JP,Hiragino Kaku Gothic ProN,sans-serif"'


def svg(title, w, h, body):
    g = (f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0">'
         f'<stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{title}</title>{g}<g {FT}>{body}</g></svg>\n'


def t(x, y, s, size=15, fill=INK, w=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, fill="#fff", stroke=LINE, r=10, extra="", sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def arrow_down(x, y1, y2, color=KNOT):
    return (f'<path d="M{x} {y1}V{y2 - 6}" stroke="{color}" stroke-width="2" fill="none"/>'
            f'<path d="M{x - 6} {y2 - 9}L{x} {y2}L{x + 6} {y2 - 9}" stroke="{color}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


# 1. 作業ごとの時間（kosu-sakugen の表。運用が重めの広告主の一例、月80時間）
HOURS = [("ASP担当者とのやり取り", 15), ("成果の承認・否認の判定", 10), ("広告素材・LPの準備", 10), ("媒体ごとの効果分析", 6),
         ("社内報告", 6), ("新規メディア・ASPの開拓", 5), ("新規提携の手続き", 5), ("掲載記事の表記の確認", 4),
         ("請求・予算・着地見込み", 4), ("単価・特単の交渉", 3), ("その他", 12)]


def kosu_hours():
    rows, y, sc = "", 18, 17
    for i, (k, v) in enumerate(HOURS):
        top = i < 7
        rows += t(196, y + 15, k, 14, INK if top else SUB, 700 if top else 400, "end")
        rows += f'<rect x="206" y="{y + 3}" width="{v * sc}" height="16" rx="4" fill="{"url(#g)" if top else KNOT}"/>'
        rows += t(214 + v * sc, y + 16, f"{v}時間", 14, INK if top else SUB, 700 if top else 400)
        y += 32
    y += 8
    legend = (f'<rect x="206" y="{y}" width="18" height="12" rx="3" fill="url(#g)"/>' + t(230, y + 11, "上位7つの作業（計57時間・約7割）", 14, INK, 700) +
              f'<rect x="206" y="{y + 24}" width="18" height="12" rx="3" fill="{KNOT}"/>' + t(230, y + 35, "そのほかの作業（計23時間）", 14, SUB))
    return svg("運用が重めの広告主の一例で、月80時間の作業ごとの内訳。上位7つの作業で全体の約7割", 560, y + 50, rows + legend)


# 2. なくす → 自動化する → 任せる（スマホでも読めるように縦に3段）
def kosu_3steps():
    rows = [
        ("1", "なくす", "作業そのものを見直す", ["全件承認の契約、取引先の整理、", "報告の型を固定"]),
        ("2", "自動化する", "決まった手順を機械に", ["データの突き合わせ、複数ASPの集計、", "記事の読み込み"]),
        ("3", "任せる", "判断がいる作業を外へ", ["ASPとの交渉、新規メディアの開拓、", "分析と改善の提案"]),
    ]
    body, rh, gap, iw = "", 112, 22, 150
    for i, (n, head, lead, ex) in enumerate(rows):
        y = i * (rh + gap)
        last = i == 2
        body += box(0, y, 560, rh, "#fff", BLUE if last else LINE, 14, sw=2 if last else 1.5)
        # 左: 線の扱いで3段階を描く
        ix, iy = 22, y + 32
        if i == 0:
            pic = "".join(f'<path d="M{ix} {iy + k * 12}h{iw if k in (0, 2) else 52}" stroke="{KNOT if k in (0, 2) else LINE}" stroke-width="2" stroke-linecap="round"/>' for k in range(5))
            pic += "".join(f'<path d="M{ix + 60} {iy + k * 12 - 5}l10 10M{ix + 70} {iy + k * 12 - 5}l-10 10" stroke="{WARN}" stroke-width="2" stroke-linecap="round"/>' for k in (1, 3, 4))
        elif i == 1:
            pic = "".join(f'<path d="M{ix} {iy + k * 12}h58" stroke="{KNOT}" stroke-width="2" stroke-linecap="round"/>' for k in range(5))
            pic += box(ix + 58, iy - 10, 40, 68, "#fff", INK, 8) + f'<circle cx="{ix + 78}" cy="{iy + 24}" r="9" fill="none" stroke="{INK}" stroke-width="2"/>'
            pic += "".join(f'<path d="M{ix + 98} {iy + k * 12}h{iw - 98}" stroke="url(#g)" stroke-width="2" stroke-linecap="round"/>' for k in range(5))
        else:
            pic = "".join(f'<path d="M{ix} {iy + k * 12}C{ix + 44} {iy + k * 12} {ix + 44} {iy + 24} {ix + 76} {iy + 24}" stroke="{KNOT}" stroke-width="2" fill="none"/>' for k in range(5))
            pic += box(ix + 76, iy + 12, 26, 24, "#fff", BLUE, 6) + f'<path d="M{ix + 102} {iy + 24}h{iw - 102}" stroke="url(#g)" stroke-width="3" stroke-linecap="round"/>'
        body += pic
        tx = 206
        body += f'<circle cx="{tx + 12}" cy="{y + 34}" r="12" fill="{"url(#g)" if last else INK}"/>' + t(tx + 12, y + 39, n, 13, "#fff", 900, "middle")
        body += t(tx + 32, y + 41, head, 21, INK, 900) + t(tx + 32 + len(head) * 21 + 12, y + 40, lead, 15, SUB, 700)
        body += t(tx, y + 74, "例: " + ex[0], 14, INK) + t(tx + 28, y + 96, ex[1], 14, INK)
        if not last:
            body += arrow_down(97, y + rh + 2, y + rh + gap - 2, SUB)
    return svg("工数を減らす順番。1 なくす（作業そのものを見直す）、2 自動化する（決まった手順を機械に）、3 任せる（判断がいる作業を外へ）", 560, 3 * rh + 2 * gap + 2, body)


# 3. 成果承認の流れ（seika-shonin の手順 1〜5）
def shonin_flow():
    b = ""
    b += box(20, 10, 230, 58, BG) + t(135, 36, "ASPの成果一覧（CSV）", 15, INK, 700, "middle") + t(135, 56, "承認待ちの成果", 13, SUB, 400, "middle")
    b += box(310, 10, 230, 58, BG) + t(425, 36, "自社の注文・申込データ", 15, INK, 700, "middle") + t(425, 56, "注文番号・申込ID", 13, SUB, 400, "middle")
    b += f'<path d="M135 68C135 96 280 86 280 110M425 68C425 96 280 86 280 110" stroke="{KNOT}" stroke-width="2" fill="none"/>'
    b += box(150, 110, 260, 50, "#fff", INK) + t(280, 141, "突き合わせて、基準で判定", 16, INK, 700, "middle")
    b += f'<path d="M280 160V176M120 176H440M120 176V190M280 176V190M440 176V190" stroke="{KNOT}" stroke-width="2" fill="none"/>'
    b += box(50, 190, 140, 44, "#eef3ff", BLUE) + t(120, 218, "承認", 16, BLUE, 900, "middle")
    b += box(210, 190, 140, 44, "#fff6ea", WARN) + t(280, 218, "否認", 16, WARN, 900, "middle")
    b += box(370, 190, 140, 44, "#fff", KNOT, 10, 'stroke-dasharray="5 4"') + t(440, 212, "要確認", 15, INK, 700, "middle") + t(440, 228, "人が判断", 12, SUB, 400, "middle")
    b += f'<path d="M120 234V250H440V234M280 234V250" stroke="{KNOT}" stroke-width="2" fill="none"/>' + arrow_down(280, 250, 274)
    b += box(150, 274, 260, 46, "#fff", INK) + t(280, 302, "ASPの管理画面に反映", 16, INK, 700, "middle")
    b += arrow_down(280, 320, 344)
    b += box(150, 344, 260, 46, BG) + t(280, 372, "メディアからの問い合わせに答える", 14, INK, 400, "middle")
    b += (f'<path d="M150 297H10V39H14" stroke="{BLUE}" stroke-width="2" fill="none" stroke-dasharray="5 5"/>'
          f'<path d="M12 33l7 6-7 6" stroke="{BLUE}" stroke-width="2" fill="none" stroke-linecap="round"/>'
          + t(18, 262, "ASPの数だけくり返す", 13, BLUE, 700))
    return svg("成果承認の流れ。ASPの成果一覧と自社の注文データを突き合わせ、承認・否認・要確認に分け、管理画面に反映し、問い合わせに答える。ASPの数だけくり返す", 560, 400, b)


# 4. 連絡の入口を1つにまとめる（asp-media-renraku）
def madoguchi():
    b = t(0, 22, "入口がばらばら", 16, INK, 900)
    src = ["メール", "チャット", "管理画面", "電話", "メール"]
    for i, s in enumerate(src):
        y = 44 + i * 40
        b += box(0, y, 104, 30, "#fff", LINE, 15) + t(52, y + 20, s, 13, SUB, 700, "middle")
    for i in range(5):
        y = 59 + i * 40
        for dy in (-40, 40):
            b += f'<path d="M104 {y}C190 {y + dy} 170 {150 - dy} 250 150" stroke="{KNOT}" stroke-width="1.4" fill="none" opacity=".7"/>'
    b += (f'<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"><circle cx="272" cy="134" r="12"/><path d="M252 172c1-15 8-22 20-22s19 7 20 22"/></g>'
          + t(272, 196, "確認と返事の漏れ", 13, WARN, 700, "middle"))
    ox = 320
    b += t(ox, 22, "入口を1つにして、分けて並べる", 16, INK, 900)
    for i in range(5):
        y = 59 + i * 40
        b += f'<path d="M{ox} {y}C{ox + 40} {y} {ox + 30} 154 {ox + 70} 154" stroke="{KNOT}" stroke-width="1.6" fill="none"/>'
    b += box(ox + 70, 132, 50, 44, "#fff", BLUE, 10, sw=2) + t(ox + 95, 159, "入口", 13, BLUE, 900, "middle")
    trays = [("返事が必要", BLUE), ("確認だけ", SUB), ("判断が必要", WARN)]
    for i, (s, c) in enumerate(trays):
        y = 64 + i * 70
        b += f'<path d="M{ox + 120} 154C{ox + 140} 154 {ox + 130} {y + 22} {ox + 150} {y + 22}" stroke="url(#g)" stroke-width="2" fill="none"/>'
        b += box(ox + 150, y, 90, 44, "#fff", c, 10) + t(ox + 195, y + 27, s, 13, c, 700, "middle")
    return svg("連絡の入口がばらばらだと確認と返事の漏れが起きる。入口を1つにまとめ、返事が必要・確認だけ・判断が必要に分けて並べる", 560, 280, b)


FILES = {"kosu-hours": kosu_hours, "kosu-3steps": kosu_3steps, "shonin-flow": shonin_flow, "madoguchi-ichihon": madoguchi}
OUT.mkdir(parents=True, exist_ok=True)
for name, fn in FILES.items():
    (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
print(len(FILES), "diagrams written")
