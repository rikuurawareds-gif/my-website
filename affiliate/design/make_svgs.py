"""アフィまかせのイラスト（線のモチーフ）を書き出す。出力先は引数のフォルダ。"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
G = '<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="240" y2="120"><stop offset="0" stop-color="#3366ff"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs>'
S = 'fill="none" stroke="#0f1424" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
FT = 'font-family="Noto Sans JP,sans-serif"'


def svg(title, body, vb="0 0 240 160"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img"><title>{title}</title>{G}{body}</svg>\n'


def person(x, y, s=1.0, stroke="#0f1424"):
    # 丸い頭と胴だけの人物（顔は描かない）
    return (f'<g fill="none" stroke="{stroke}" stroke-width="2" stroke-linecap="round" transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-26" r="11"/><path d="M-19 8c1-14 8-21 19-21s18 7 19 21"/></g>')


cal_cells = ""
for r, y in enumerate([50, 74, 98, 122]):
    for c, x in enumerate([30, 56, 82, 108, 134, 160, 186]):
        if c == 2:
            cal_cells += f'<rect x="{x}" y="{y}" width="20" height="18" rx="4" fill="url(#g)"/><path d="M{x+5} {y+9}l4 4 7-8" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        else:
            cal_cells += f'<rect x="{x}" y="{y}" width="20" height="18" rx="4" fill="#eef1f8"/>'
days = "".join(f'<text x="{40 + i * 26}" y="33">{d}</text>' for i, d in enumerate("月火水木金土日"))

FILES = {
    "pain-renraku": svg("返信待ちの連絡が積み上がる", f'''
<g {S}><path d="M14 148h100"/><rect x="34" y="116" width="54" height="30" rx="4"/></g>{person(61, 108, 1.1)}
<g fill="#fff" stroke="#9aa4bf" stroke-width="2" stroke-linejoin="round">
<path d="M112 104h56a8 8 0 0 1 8 8v10a8 8 0 0 1-8 8h-44l-10 8v-8h-2a8 8 0 0 1-8-8v-10a8 8 0 0 1 8-8z"/>
<path d="M128 72h62a8 8 0 0 1 8 8v10a8 8 0 0 1-8 8h-48l-10 8v-8h-4a8 8 0 0 1-8-8v-10a8 8 0 0 1 8-8z"/>
<path d="M148 40h62a8 8 0 0 1 8 8v10a8 8 0 0 1-8 8h-48l-10 8v-8h-4a8 8 0 0 1-8-8v-10a8 8 0 0 1 8-8z"/>
<path d="M164 10h52a8 8 0 0 1 8 8v6a8 8 0 0 1-8 8h-52a8 8 0 0 1-8-8v-6a8 8 0 0 1 8-8z"/></g>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M120 117h34M138 85h40M158 53h40M170 21h30"/></g>
<circle cx="222" cy="12" r="11" fill="#b54708"/><text x="222" y="16" {FT} font-size="11" font-weight="700" fill="#fff" text-anchor="middle">12</text>'''),

    "pain-shonin": svg("ASPの成果と注文データを1件ずつ突き合わせる", f'''
<g {S}><rect x="12" y="20" width="90" height="120" rx="6"/><rect x="138" y="20" width="90" height="120" rx="6"/><path d="M12 42h90M138 42h90"/></g>
<g {FT} font-size="10" font-weight="700" fill="#5b6378" text-anchor="middle"><text x="57" y="35">ASPの成果</text><text x="183" y="35">注文データ</text></g>
<rect x="18" y="86" width="204" height="18" rx="4" fill="#b54708" fill-opacity=".1"/>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M24 58h62M24 76h52M24 95h62M24 116h46M150 58h62M150 76h52M150 95h62M150 116h46"/></g>
<g stroke="#9aa4bf" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 6"><path d="M106 58h28M106 76h28M106 116h28"/></g>
<g stroke="#b54708" stroke-width="2.4" stroke-linecap="round"><path d="M114 90l10 10M124 90l-10 10"/></g>'''),

    "pain-hyoki": svg("外部の記事に広告の表記が欠けていないかを探す", f'''
<g {S}><rect x="26" y="12" width="128" height="138" rx="6"/></g>
<path d="M40 30h66" stroke="#0f1424" stroke-width="3" stroke-linecap="round"/>
<rect x="116" y="21" width="28" height="17" rx="3" fill="#fff" stroke="#b54708" stroke-width="2" stroke-dasharray="4 3"/>
<text x="130" y="33.5" {FT} font-size="9" font-weight="700" fill="#b54708" text-anchor="middle">PR?</text>
<rect x="40" y="48" width="100" height="34" rx="3" fill="#eef1f8"/>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M40 96h98M40 108h84M40 120h98M40 132h60"/></g>
<circle cx="174" cy="78" r="30" fill="#fff" fill-opacity=".75" stroke="#0f1424" stroke-width="2"/>
<path d="M196 100l26 26" stroke="#0f1424" stroke-width="6" stroke-linecap="round"/>
<g stroke="#b54708" stroke-width="2.4" stroke-linecap="round"><path d="M160 72h28M160 84h16"/></g>'''),

    "pain-kaitaku": svg("比較記事に競合は載っていて、自社だけ載っていない", f'''
<g {S}><rect x="38" y="8" width="164" height="146" rx="6"/></g>
<path d="M52 26h96" stroke="#0f1424" stroke-width="3" stroke-linecap="round"/>
<g {FT} font-size="11" font-weight="700" fill="#5b6378"><text x="54" y="57">1</text><text x="54" y="87">2</text><text x="54" y="117">3</text><text x="54" y="144">4</text></g>
<g fill="#eef1f8"><rect x="68" y="42" width="26" height="20" rx="3"/><rect x="68" y="72" width="26" height="20" rx="3"/><rect x="68" y="102" width="26" height="20" rx="3"/></g>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M102 48h76M102 57h50M102 78h76M102 87h44M102 108h76M102 117h56"/></g>
<rect x="68" y="130" width="120" height="19" rx="4" fill="#eef3ff" stroke="#3366ff" stroke-width="2" stroke-dasharray="4 4"/>
<text x="128" y="143.5" {FT} font-size="10" font-weight="700" fill="#3366ff" text-anchor="middle">御社はまだ載っていない</text>'''),

    "pain-sozai": svg("価格やキャンペーンが変わるたびに素材を差し替えて周知する", f'''
<g fill="#fff" stroke="#9aa4bf" stroke-width="2" stroke-linejoin="round"><rect x="16" y="76" width="112" height="62" rx="6"/><rect x="28" y="60" width="112" height="62" rx="6"/></g>
<rect x="40" y="44" width="112" height="62" rx="6" fill="#fff" stroke="#0f1424" stroke-width="2"/>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M52 58h52M52 68h34"/></g>
<text x="54" y="94" {FT} font-size="13" font-weight="700" fill="#9aa4bf">¥3,980</text><path d="M52 90h48" stroke="#b54708" stroke-width="2"/>
<text x="106" y="94" {FT} font-size="13" font-weight="900" fill="#0f1424">¥2,980</text>
<g fill="none" stroke="#0f1424" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M184 46a28 28 0 1 1-24 36"/></g><path d="M192 44l-12-8v15z" fill="#0f1424"/>
<g stroke="#9aa4bf" stroke-width="2" stroke-linecap="round"><path d="M176 116l-14 10M196 116v12M216 116l14 10"/></g>
<g fill="#fff" stroke="#9aa4bf" stroke-width="2"><circle cx="158" cy="134" r="6"/><circle cx="196" cy="140" r="6"/><circle cx="234" cy="134" r="5"/></g>'''),

    "pain-report": svg("ASPごとに形の違う数字を集めて社内の資料にまとめる", f'''
<g fill="#fff" stroke="#9aa4bf" stroke-width="2"><rect x="10" y="12" width="62" height="36" rx="4"/><rect x="20" y="62" width="58" height="38" rx="14"/><rect x="8" y="114" width="68" height="32" rx="1"/></g>
<g {FT} font-size="10" fill="#5b6378"><text x="18" y="35">CV 128</text><text x="30" y="85">成果 97</text><text x="16" y="134">件数:112</text></g>
<g fill="none" stroke="#9aa4bf" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 6"><path d="M76 30c30 0 40 28 64 38M82 81h56M80 130c30 0 40-28 60-38"/></g>
<g {S}><path d="M144 16h60l18 18v112h-78z" fill="#fff"/><path d="M204 16v18h18"/></g>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M156 46h36M156 56h50"/></g>
<g fill="url(#g)"><rect x="158" y="104" width="11" height="28" rx="2"/><rect x="175" y="90" width="11" height="42" rx="2"/><rect x="192" y="76" width="11" height="56" rx="2"/></g>'''),

    "remain-weekly": svg("御社に残るのは週1回の確認だけ", f'''
<g {S}><rect x="20" y="16" width="200" height="134" rx="10"/><path d="M20 40h200M60 8v14M180 8v14"/></g>
<g {FT} font-size="10" font-weight="700" fill="#5b6378" text-anchor="middle">{days}</g>{cal_cells}'''),

    # コラムのカテゴリの絵（小さめ、横長）
    "cat-kosu": svg("工数を減らす", f'''
<g {S}><circle cx="44" cy="40" r="22"/><path d="M44 28v12l8 6"/></g>
<path d="M78 26h96" stroke="#9aa4bf" stroke-width="2" stroke-linecap="round"/><path d="M78 40h70" stroke="#9aa4bf" stroke-width="2" stroke-linecap="round" opacity=".7"/>
<path d="M78 54h30" stroke="url(#g)" stroke-width="4" stroke-linecap="round"/>''', "0 0 200 80"),
    "cat-jitsumu": svg("運用の実務", f'''
<g fill="#fff" stroke="#0f1424" stroke-width="2" stroke-linejoin="round"><path d="M30 18h52a8 8 0 0 1 8 8v12a8 8 0 0 1-8 8h-36l-10 8v-8h-6a8 8 0 0 1-8-8v-12a8 8 0 0 1 8-8z"/></g>
<g fill="#fff" stroke="url(#g)" stroke-width="2.5" stroke-linejoin="round"><path d="M170 34h-52a8 8 0 0 0-8 8v12a8 8 0 0 0 8 8h36l10 8v-8h6a8 8 0 0 0 8-8v-12a8 8 0 0 0-8-8z"/></g>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M34 32h40M122 48h40"/></g>''', "0 0 200 80"),
    "cat-hourei": svg("表記・法令", f'''
<g {S}><rect x="40" y="8" width="58" height="66" rx="4"/></g>
<g stroke="#c5ccdd" stroke-width="2" stroke-linecap="round"><path d="M50 36h38M50 46h38M50 56h26"/></g>
<rect x="50" y="16" width="22" height="13" rx="3" fill="url(#g)"/><text x="61" y="26" {FT} font-size="9" font-weight="900" fill="#fff" text-anchor="middle">PR</text>
<g {S}><path d="M120 30l12 12 26-26"/></g><path d="M120 58h50" stroke="#9aa4bf" stroke-width="2" stroke-linecap="round"/>''', "0 0 200 80"),
    "cat-hajime": svg("始め方", f'''
<circle cx="34" cy="40" r="7" fill="#0f1424"/>
<path d="M42 40c30 0 34-22 62-22s34 22 62 22" fill="none" stroke="url(#g)" stroke-width="4" stroke-linecap="round"/>
<circle cx="168" cy="40" r="9" fill="none" stroke="#0f1424" stroke-width="2"/>''', "0 0 200 80"),
    "cat-etc": svg("その他", f'''
<g {S}><rect x="60" y="14" width="80" height="54" rx="6"/></g>
<g fill="#9aa4bf"><circle cx="84" cy="41" r="4"/><circle cx="100" cy="41" r="4"/></g><circle cx="116" cy="41" r="4" fill="url(#g)"/>''', "0 0 200 80"),
}

OUT.mkdir(parents=True, exist_ok=True)
for name, s in FILES.items():
    (OUT / f"{name}.svg").write_text(s.strip() + "\n", encoding="utf-8")
print(len(FILES), "svg written")
