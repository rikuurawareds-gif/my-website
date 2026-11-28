"""X（@afimakase）のアイコンとヘッダーを、ixs-llc.com のデザイン（濃紺・青→水色のグラデーション・Noto Sans JP）で作る。
使い方: python make_x_images.py <出力フォルダ>
フォントは Windows の Noto Sans JP（可変フォント C:\\Windows\\Fonts\\NotoSansJP-VF.ttf）を使う。"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
FONT = r"C:\Windows\Fonts\NotoSansJP-VF.ttf"
NAVY, NAVY3 = (7, 11, 24), (20, 29, 56)
BLUE, CYAN = (51, 102, 255), (34, 211, 238)
INV, INV_SUB = (232, 236, 247), (154, 164, 191)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def grad(w, h, c1=BLUE, c2=CYAN, angle_x=1.0, angle_y=0.55):
    """120度ぐらいの斜めのグラデーション"""
    g = Image.new("RGB", (w, h))
    px = g.load()
    tot = angle_x * w + angle_y * h
    for y in range(h):
        for x in range(w):
            t = (angle_x * x + angle_y * y) / tot
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return g


def glow(base, center, radius, color, alpha):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.6))
    base.alpha_composite(layer)


def brand_mark(size):
    """角丸の正方形（グラデーション）に、白い線の菱形。サイトのロゴと同じ形"""
    s = size * 4  # 縮小して滑らかにする
    g = grad(s, s).convert("RGBA")
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.3), fill=255)
    g.putalpha(mask)
    d = ImageDraw.Draw(g)
    c, r, wdt = s / 2, s * 0.24, int(s * 0.085)
    d.line([(c, c - r), (c + r, c), (c, c + r), (c - r, c), (c, c - r)], fill="white", width=wdt, joint="curve")
    for p in [(c, c - r), (c + r, c), (c, c + r), (c - r, c)]:
        d.ellipse([p[0] - wdt / 2, p[1] - wdt / 2, p[0] + wdt / 2, p[1] + wdt / 2], fill="white")
    return g.resize((size, size), Image.LANCZOS)


def text_grad(img, xy, text, f):
    """グラデーションの文字"""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = d.textbbox(xy, text, font=f)
    w, h = x1 - x0, y1 - y0
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).text(xy, text, font=f, fill=255)
    g = grad(w + 2, h + 2)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(g, (x0, y0))
    layer.putalpha(m)
    img.alpha_composite(layer)


def grid(img, step, alpha_top=18):
    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, alpha_top))
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(255, 255, 255, alpha_top))
    fade = Image.linear_gradient("L").resize(img.size).point(lambda v: 255 - v)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", img.size, 0), fade))
    img.alpha_composite(layer)


# ---- アイコン 400x400（X では丸く切り抜かれる）----
icon = Image.new("RGBA", (400, 400), NAVY + (255,))
glow(icon, (330, 60), 170, BLUE, 120)
glow(icon, (60, 360), 140, CYAN, 60)
m = brand_mark(150)
icon.alpha_composite(m, (125, 78))
d = ImageDraw.Draw(icon)
f = font(52, 900)
t = "アフィまかせ"
tw = d.textlength(t, font=f)
d.text(((400 - tw) / 2, 248), t, font=f, fill=INV)
f2 = font(20, 700)
t2 = "by IXS"
tw2 = d.textlength(t2, font=f2)
d.text(((400 - tw2) / 2, 320), t2, font=f2, fill=INV_SUB)
icon.convert("RGB").save(OUT / "x-icon-400-ixs.png", optimize=True)

# ---- ヘッダー 1500x500（左下はアイコンで隠れるので、文字は上寄せ・右寄せ気味）----
hd = Image.new("RGBA", (1500, 500), NAVY + (255,))
glow(hd, (1300, 40), 380, BLUE, 140)
glow(hd, (200, 520), 260, CYAN, 55)
grid(hd, 56)
d = ImageDraw.Draw(hd)
X0 = 430
# 小さな見出し（ピル）
fp = font(19, 700)
pill = "AFFILIATE OPERATIONS"
pw = d.textlength(pill, font=fp)
pl = Image.new("RGBA", hd.size, (0, 0, 0, 0))
ImageDraw.Draw(pl).rounded_rectangle([X0, 70, X0 + pw + 64, 112], radius=21, outline=CYAN + (110,), width=2, fill=CYAN + (18,))
hd.alpha_composite(pl)
d = ImageDraw.Draw(hd)
d.ellipse([X0 + 20, 86, X0 + 30, 96], fill=CYAN)
d.text((X0 + 42, 77), pill, font=fp, fill=CYAN)
# 見出し
fh = font(66, 900)
d.text((X0, 140), "アフィリエイトの運用を、", font=fh, fill=(255, 255, 255))
text_grad(hd, (X0, 228), "まるごと手離れ。", fh)
# 説明
fs = font(25, 500)
d.text((X0, 338), "ASP・メディア対応 ／ 成果承認 ／ 表記チェック ／ レポート", font=fs, fill=INV_SUB)
# 運営
fo = font(21, 700)
mk = brand_mark(34)
hd.alpha_composite(mk, (X0, 410))
d.text((X0 + 48, 414), "運営: 合同会社IXS　afimakase.ixs-llc.com", font=fo, fill=INV)
hd.convert("RGB").save(OUT / "x-header-1500x500-ixs.png", optimize=True)
print("ok", OUT)
