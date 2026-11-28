"""有料note の表紙（1280×670）を、サイトと同じ線のモチーフで作る。
使い方: python make_note_cover.py <出力ファイル.png> [タイトル（行は | で区切る） 小見出し [幅x高さ]]
例（サイトの OGP 画像）: python make_note_cover.py ../site/assets/img/og.png "アフィリエイトの|連絡窓口を、|まるごと代行。" "ASP・メディアとのやり取りを代行。窓口代行は月3万円から（税別）" 1200x630
フォントは Windows の Noto Sans JP（可変フォント C:\\Windows\\Fonts\\NotoSansJP-VF.ttf）。2倍で描いて縮小し、線をなめらかにする。"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
W, H, K = 1280, 670, 2
FONT = r"C:\Windows\Fonts\NotoSansJP-VF.ttf"
NAVY, NAVY2 = (7, 11, 24), (13, 20, 40)
BLUE, CYAN = (51, 102, 255), (34, 211, 238)
INV, INV_SUB, KNOT = (232, 236, 247), (154, 164, 191), (58, 69, 102)

TITLE = ["アフィリエイト広告の", "担当者になったら", "最初に読む運用ノート"]
SUB = "元代理店の運用担当が、件数と質を両立させる考え方"
FINAL = (W, H)
if len(sys.argv) >= 4:
    TITLE, SUB = sys.argv[2].split("|"), sys.argv[3]
if len(sys.argv) >= 5:
    FINAL = tuple(int(v) for v in sys.argv[4].split("x"))


def font(size, weight):
    f = ImageFont.truetype(FONT, size * K)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def bezier(p0, p1, p2, p3, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def s(v):
    return v * K


img = Image.new("RGB", (s(W), s(H)), NAVY)

# 右上と左下のにじみ（サイトのヒーローと同じ）
glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
g.ellipse([s(820), s(-260), s(1500), s(360)], fill=BLUE + (95,))
g.ellipse([s(-200), s(470), s(300), s(900)], fill=CYAN + (40,))
glow = glow.filter(ImageFilter.GaussianBlur(s(110)))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img)

# 線のモチーフ: 左から来る何本もの線が、1点でまとまり、1本の青→水色の線になる
hub = (s(1040), s(335))
for i, y in enumerate(range(150, 540, 48)):
    pts = bezier((s(800), s(y)), (s(930), s(y)), (s(930), hub[1]), hub)
    d.line(pts, fill=KNOT, width=s(2))
    d.ellipse([s(794), s(y) - s(6), s(806), s(y) + s(6)], outline=INV_SUB, width=s(2))
one = bezier(hub, (s(1100), hub[1]), (s(1150), s(335)), (s(1210), s(335)), 40)
for j in range(len(one) - 1):
    d.line([one[j], one[j + 1]], fill=mix(BLUE, CYAN, j / (len(one) - 1)), width=s(5))
d.ellipse([hub[0] - s(9), hub[1] - s(9), hub[0] + s(9), hub[1] + s(9)], fill=BLUE)
d.ellipse([s(1210) - s(7), s(335) - s(7), s(1210) + s(7), s(335) + s(7)], fill=CYAN)

# 文字
ft, fs, fb, fsm = font(62, 900), font(24, 500), font(22, 900), font(14, 700)
x, y = s(80), s(150)
for line in TITLE:
    d.text((x, y), line, font=ft, fill=(255, 255, 255))
    y += s(88)
y += s(18)
d.rectangle([x, y, x + s(56), y + s(5)], fill=CYAN)
d.text((x, y + s(24)), SUB, font=fs, fill=INV_SUB)

# 小さくブランド（左上）
bx, by = s(80), s(64)
mark = Image.new("RGB", (s(30), s(30)))
md = ImageDraw.Draw(mark)
for i in range(s(30)):
    md.line([(i, 0), (i, s(30))], fill=mix(BLUE, CYAN, i / s(30)))
m = Image.new("L", mark.size, 0)
ImageDraw.Draw(m).rounded_rectangle([0, 0, s(30) - 1, s(30) - 1], radius=s(9), fill=255)
img.paste(mark, (bx, by), m)
d.text((bx + s(42), by + s(1)), "アフィまかせ", font=fb, fill=(255, 255, 255))
d.text((bx + s(42) + d.textlength("アフィまかせ", font=fb) + s(10), by + s(8)), "by IXS", font=fsm, fill=INV_SUB)

img.resize(FINAL, Image.LANCZOS).save(OUT, optimize=True)
print("saved", OUT)
