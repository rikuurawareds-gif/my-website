#!/usr/bin/env python3
"""
コラム（SEO・AIO）記事のビルド。content/*.md → column/<slug>/index.html、column/index.html、
sitemap.xml、llms.txt を作る。標準ライブラリのみ。

記事の書き方（content/<slug>.md）:
---
title: 記事タイトル
description: 120字前後の説明（検索結果・AIの要約に使われる）
date: 2026-11-27
updated: 2026-11-27
---
本文（Markdown の簡易記法: ## 見出し、### 小見出し、- 箇条書き、1. 番号、| 表 |、**太字**、[リンク](URL)、> 引用）

- 「## よくある質問」の下の「### 質問」と、その直後の段落は、FAQ の構造化データ（FAQPage）にもなる
- 冒頭の段落は「結論」として目立たせる（AI が引用しやすい形）
"""
import html, json, re, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://afimakase.ixs-llc.com"
SITE = "アフィまかせ"


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}"' + (' rel="noopener" target="_blank"' if m.group(2).startswith("http") else "") + f">{m.group(1)}</a>", s)
    return s


def md_to_html(md):
    out, lines, i = [], md.strip("\n").split("\n"), 0
    toc = []
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        if l.startswith("## "):
            t = l[3:].strip(); aid = f"s{len(toc) + 1}"; toc.append((aid, t))
            out.append(f'<h2 id="{aid}">{inline(t)}</h2>'); i += 1; continue
        if l.startswith("### "):
            out.append(f"<h3>{inline(l[4:].strip())}</h3>"); i += 1; continue
        if l.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(inline(lines[i][2:])); i += 1
            out.append('<blockquote>' + "<br>".join(buf) + "</blockquote>"); continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'); continue
        if re.match(r"^(- |\d+\. )", l):
            ordered = bool(re.match(r"^\d+\. ", l)); tag = "ol" if ordered else "ul"; items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                items.append(inline(re.sub(r"^(- |\d+\. )", "", lines[i]))); i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||- |\d+\. )", lines[i]):
            buf.append(inline(lines[i])); i += 1
        out.append("<p>" + "".join(buf) + "</p>")
    return "\n".join(out), toc


def parse(path):
    t = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    meta["slug"] = path.stem
    meta["body"] = m.group(2)
    faq = []
    fm = re.search(r"^## よくある質問\n(.*?)(?=^## |\Z)", meta["body"], re.S | re.M)
    if fm:
        for q, a in re.findall(r"^### (.+?)\n+(.+?)(?=\n### |\n## |\Z)", fm.group(1), re.S | re.M):
            faq.append((q.strip(), re.sub(r"\s+", " ", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.replace("**", ""))).strip()))
    meta["faq"] = faq
    return meta


CSS = """
.col-hero{background:var(--navy);color:var(--text-inv);padding:40px 0 44px;position:relative;overflow:hidden}
.col-hero:before{content:"";position:absolute;inset:0;background:radial-gradient(50% 80% at 90% 0%,rgba(51,102,255,.35),transparent 70%)}
.col-hero .w{position:relative;display:grid;grid-template-columns:1fr 150px;gap:24px;align-items:end}
.col-hero .w>div{min-width:0}.col-hero .art{width:150px;background:#fff;border-radius:14px;padding:6px;margin-bottom:4px}
@media (max-width:640px){.col-hero .w{grid-template-columns:1fr}.col-hero .art{display:none}}
.w{max-width:800px;margin:0 auto;padding:0 20px}
.crumb{font-size:13px;color:var(--text-inv-sub);margin:0 0 14px}.crumb a{color:var(--text-inv-sub);text-decoration:none}.crumb a:hover{color:#fff}
.col-hero h1{font-weight:900;font-size:clamp(26px,4.4vw,38px);line-height:1.45;margin:6px 0 14px;color:#fff;text-wrap:balance}
.meta{font-size:13px;color:var(--text-inv-sub);margin:0}
article.w{padding-top:36px;padding-bottom:24px;font-size:17px;line-height:1.9}
article.w>p,article.w>ul,article.w>ol{max-width:42em}
article h2{font-size:clamp(22px,3vw,26px);line-height:1.5;margin:56px 0 14px;padding-left:16px;border-left:5px solid;border-image:var(--grad) 1}
article h3{font-size:19px;margin:30px 0 8px}
.lead{background:var(--bg-sub);border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin:0 0 8px}
.lead strong:first-child{display:inline-block;font-size:12px;letter-spacing:.14em;color:#fff;background:var(--grad);border-radius:999px;padding:2px 12px;margin-bottom:8px}
.toc{border:1px solid var(--line);border-radius:16px;padding:16px 24px;margin:24px 0;font-size:15px;background:#fff}.toc ol{margin:6px 0;padding-left:20px}.toc a{color:var(--text);text-decoration:none}.toc a:hover{color:var(--blue)}
.tbl{overflow-x:auto;margin:18px 0}table{border-collapse:collapse;width:100%;font-size:15px}th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}th{background:var(--bg-sub)}
blockquote{margin:18px 0;padding:14px 18px;background:#f7f9ff;border-left:4px solid var(--blue);border-radius:0 12px 12px 0;font-size:15px}
.cta-box{margin:48px 0;padding:32px 24px;border-radius:20px;background:var(--navy);color:var(--text-inv);text-align:center;position:relative;overflow:hidden}
.cta-box:before{content:"";position:absolute;inset:0;background:radial-gradient(60% 90% at 100% 0%,rgba(51,102,255,.35),transparent 70%)}
.cta-box>*{position:relative}.cta-box p{margin:0 0 16px}.cta-box strong{color:#fff;font-size:18px}
.cta-box .btn{margin:6px}
.list{display:grid;gap:14px;padding:32px 0}
.list a{display:block;padding:22px 24px;border:1px solid var(--line);border-radius:16px;color:var(--text);text-decoration:none;background:#fff;transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.list a:hover{transform:translateY(-2px);box-shadow:0 18px 36px -24px rgba(15,20,36,.3)}
.list a strong{display:block;font-size:18px;line-height:1.5;margin-bottom:6px}.list a span{font-size:14px;color:var(--text-sub)}
"""

# site.css を変えたら ?v= の版番号を上げる（ブラウザが4時間キャッシュするため）。index.html・privacy.html も同じ番号に
HEAD = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="アフィまかせ"><meta property="og:image" content="https://afimakase.ixs-llc.com/assets/img/og-column.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#070b18">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="/assets/site.css?v=20261128b">
<style>{css}</style>
{jsonld}
<script src="/assets/config.js"></script>
</head><body data-page-id="{pageid}">
<header class="site-header"><div class="wrap"><a class="brand" href="/"><span class="brand-mark" aria-hidden="true"></span><span>アフィまかせ</span><small>by IXS</small></a><nav class="nav" aria-label="メイン"><a class="hide-sm" href="/#service">サービス</a><a class="hide-sm" href="/#price">料金</a><a href="/column/">コラム</a><a class="btn sm" href="/#diagnosis">無料で診断</a></nav></div></header>
"""
FOOT = """<footer class="site-footer"><div class="wrap">
<div class="top"><a class="brand" href="/"><span class="brand-mark" aria-hidden="true"></span><span>アフィまかせ</span></a><nav aria-label="フッター"><a href="/#service">サービス</a><a href="/#price">料金</a><a href="/column/">コラム</a><a href="/#contact">お問い合わせ</a><a href="/privacy.html">プライバシーポリシー</a></nav></div>
<p class="op">アフィまかせは、合同会社IXS（イクス）が運営するアフィリエイト運用支援サービスです。運営会社: <a href="https://ixs-llc.com/" rel="noopener">合同会社IXS</a><br>本サイトの記事は一般的な情報の提供を目的としたもので、個別の事案についての法的な助言ではありません。<br>アフィまかせは、連絡の下書きやデータの判定に AI を使っています。はじめはすべて担当者が確認してから送り、自動にするのは御社と合意した定型の連絡だけです。金額や契約に関わる連絡は、必ず人が確認します。</p>
<p class="copy">© IXS LLC.</p>
</div></footer>
<script src="/assets/track.js"></script>
</body></html>"""
CTA = """<div class="cta-box"><p><strong>任せた場合の費用対効果を、上長に見せられる1枚に</strong><br>8問・1分の無料の工数診断で、いまの工数と、委託費を差し引いた効果の目安（決裁用の試算）が出ます。</p>
<a class="btn" href="/#diagnosis">工数を診断して試算を作る</a><a class="btn ghost" href="/#contact">無料の伸びしろ診断・表記チェック</a></div>"""

ORG = {"@type": "Organization", "name": "合同会社IXS", "alternateName": "IXS LLC", "url": "https://ixs-llc.com/", "description": "Webマーケティングのコンサルティング、アフィリエイト・広告の運用支援"}


def article_page(a):
    body_html, toc = md_to_html(a["body"])
    # 冒頭の段落を「結論」ボックスに
    body_html = re.sub(r"^<p>(.*?)</p>", r'<div class="lead"><strong>結論</strong>\1</div>', body_html, count=1, flags=re.S)
    url = f"{BASE}/column/{a['slug']}/"
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"],
           "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "inLanguage": "ja",
           "author": ORG, "publisher": ORG, "mainEntityOfPage": url},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "コラム", "item": BASE + "/column/"},
              {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]}]
    if a["faq"]:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]})
    jsonld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    toc_html = '<nav class="toc"><strong>目次</strong><ol>' + "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc) + "</ol></nav>"
    # 目次は結論の直後に
    body_html = body_html.replace("</div>", "</div>\n" + toc_html, 1)
    # 本文の途中（3つ目の見出しの前）と末尾に CTA
    parts = body_html.split("<h2", 3)
    if len(parts) == 4:
        body_html = "<h2".join(parts[:3]) + CTA + "<h2" + parts[3]
    page = HEAD.format(title=html.escape(a["title"]) + "｜アフィまかせ", desc=html.escape(a["description"]), url=url, ogtype="article",
                       css=CSS, jsonld=jsonld, pageid="col-" + a["slug"])
    cat = a.get("category") if a.get("category") in dict(CATS) else "etc"
    page += f'<div class="col-hero"><div class="w"><div><div class="crumb"><a href="/">ホーム</a> › <a href="/column/">コラム</a></div>\n<h1>{html.escape(a["title"])}</h1>\n'
    page += f'<p class="meta">公開: {a["date"]}　更新: {a.get("updated", a["date"])}　運営: アフィまかせ（合同会社IXS）</p></div>'
    page += f'<img class="art" src="/assets/img/cat-{cat}.svg" alt="" width="150" height="60"></div></div>\n'
    page += '<main><article class="w">' + body_html + CTA + '</article></main>' + FOOT
    return page


# ---- コラム一覧（2026-11-28 SEO・AIO がオーナーの依頼で作り直し。持ち主は PM） ----
# 記事の category（下の CATS のキー）でテーマ別に並べる。category がない・未知の記事は "etc"（その他）。
# featured: true の記事は「まずはここから」に大きく出す（なければ出さない）。
CATS = [("kosu", "工数を減らす"), ("jitsumu", "運用の実務"), ("hourei", "表記・法令"), ("hajime", "始め方"), ("etc", "その他")]

IDX_CSS = """
.col-hero .wrap{position:relative}.col-hero h1{font-size:clamp(28px,5vw,40px);line-height:1.3;margin:6px 0 8px}
.col-hero .count{display:inline-block;margin-top:14px;font-size:13px;color:var(--text-inv-sub);border:1px solid var(--line-inv);border-radius:999px;padding:3px 12px}
.col-main{padding-bottom:16px}
.col-feat{position:relative;display:grid;gap:10px;margin:32px 0 0;padding:32px clamp(20px,4vw,40px);border-radius:20px;background:var(--navy-2);color:var(--text-inv);text-decoration:none;overflow:hidden;transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.col-feat:before{content:"";position:absolute;inset:0;background:radial-gradient(55% 90% at 100% 0%,rgba(51,102,255,.45),transparent 70%),radial-gradient(40% 70% at 0% 100%,rgba(34,211,238,.18),transparent 70%)}
.col-feat>*{position:relative}.col-feat:hover{transform:translateY(-2px);box-shadow:0 24px 48px -28px rgba(15,20,36,.6)}
.col-feat .tag{justify-self:start;background:var(--grad);color:#fff}
.col-feat strong{font-size:clamp(21px,3.2vw,28px);line-height:1.45;color:#fff}
.col-feat .sub{color:var(--text-inv);font-weight:700}
.col-feat .desc{color:var(--text-inv-sub);font-size:15px;max-width:760px}
.col-feat .more{font-weight:700;color:var(--cyan);font-size:15px}
.col-filter{display:flex;flex-wrap:wrap;gap:8px;margin:36px 0 4px}
.col-filter button{font:inherit;font-size:14px;font-weight:700;border:1px solid var(--line);background:#fff;color:var(--text);border-radius:999px;padding:6px 16px;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.col-filter button span{font-weight:400;color:var(--text-sub);margin-left:4px}
.col-filter button:hover{border-color:#c5cbdc}
.col-filter button[aria-pressed="true"]{background:var(--navy);border-color:var(--navy);color:#fff}.col-filter button[aria-pressed="true"] span{color:var(--text-inv-sub)}
.col-main .col-sec{padding:0}
@media (max-width:640px){.col-feat{padding:26px 20px}.col-feat .desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.col-sec h2{display:flex;align-items:center;gap:12px;font-size:20px;margin:36px 0 14px}
.col-sec h2:before{content:"";width:6px;height:22px;border-radius:3px;background:var(--grad)}
.col-sec h2 small{font-size:13px;font-weight:400;color:var(--text-sub)}
.col-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:16px}
.col-card{display:flex;flex-direction:column;gap:8px;min-width:0;padding:22px 22px 18px;border:1px solid var(--line);border-radius:16px;background:#fff;color:var(--text);text-decoration:none;transition:transform .2s var(--ease),box-shadow .2s var(--ease),border-color .2s}
.col-card:hover{transform:translateY(-2px);border-color:#d3d8e6;box-shadow:0 18px 36px -24px rgba(15,20,36,.3)}
.col-card strong{font-size:17px;line-height:1.5;overflow-wrap:anywhere}
.col-card .sub{font-size:14px;line-height:1.6;color:var(--text-sub);font-weight:700;overflow-wrap:anywhere}
.col-card .desc{font-size:14px;line-height:1.75;color:var(--text-sub);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.col-card time{margin-top:auto;padding-top:6px;font-size:12px;color:var(--text-sub)}
.tag{align-self:flex-start;display:inline-block;font-size:12px;font-weight:700;line-height:1.6;padding:2px 10px;border-radius:999px;background:#eef2ff;color:#2952cc}
.t-jitsumu{background:#e6f7fb;color:#0e6f86}.t-hourei{background:#fff4e5;color:var(--warn)}.t-hajime{background:#e7f6ef;color:var(--ok)}.t-etc{background:var(--bg-sub);color:var(--text-sub)}
.col-sec[hidden]{display:none}
.card-top{display:flex;justify-content:space-between;align-items:center;gap:8px}.card-top img{width:70px;height:auto}
.col-card:focus-visible,.col-feat:focus-visible{outline:2px solid var(--blue);outline-offset:3px}
"""

IDX_JS = """<script>
(function(){var b=document.querySelectorAll('.col-filter button'),s=document.querySelectorAll('.col-sec');
b.forEach(function(x){x.addEventListener('click',function(){var f=x.getAttribute('data-f');
b.forEach(function(y){y.setAttribute('aria-pressed',y===x?'true':'false')});
s.forEach(function(z){z.hidden=!(f==='all'||z.getAttribute('data-cat')===f)});});});})();
</script>"""


def split_title(t):
    """「主題：副題」を2つに分ける。区切りがなければ副題は空。"""
    main, sep, sub = t.partition("：")
    return (main, sub) if sep else (t, "")


def fmt_date(d):
    return d.replace("-", ".")


def index_body(arts):
    labels = dict(CATS)
    for a in arts:
        if a.get("category") not in labels:
            a["category"] = "etc"

    def card(a):
        m, s = split_title(a["title"])
        d = a.get("updated", a["date"])
        return (f'<a class="col-card" href="/column/{a["slug"]}/"><span class="card-top"><span class="tag t-{a["category"]}">{labels[a["category"]]}</span><img src="/assets/img/cat-{a["category"]}.svg" alt="" width="70" height="28" loading="lazy"></span>'
                f'<strong>{html.escape(m)}</strong>' + (f'<span class="sub">{html.escape(s)}</span>' if s else "") +
                f'<span class="desc">{html.escape(a["description"])}</span><time datetime="{d}">{fmt_date(d)} 更新</time></a>')

    out = ('<div class="col-hero"><div class="wrap"><h1>アフィリエイト運用コラム</h1>'
           '<p class="meta">広告主・代理店のための、アフィリエイト運用の実務と表記の注意点。</p>'
           f'<span class="count">全{len(arts)}本</span></div></div><main class="wrap col-main">')
    feat = next((a for a in arts if str(a.get("featured", "")).lower() == "true"), None)
    if feat:
        m, s = split_title(feat["title"])
        out += (f'<a class="col-feat" href="/column/{feat["slug"]}/"><span class="tag">まずはここから</span><strong>{html.escape(m)}</strong>'
                + (f'<span class="sub">{html.escape(s)}</span>' if s else "") +
                f'<span class="desc">{html.escape(feat["description"])}</span><span class="more">記事を読む</span></a>')
    used = [(k, v, [a for a in arts if a["category"] == k]) for k, v in CATS]
    used = [u for u in used if u[2]]
    out += '<nav class="col-filter" aria-label="テーマで絞り込む"><button type="button" data-f="all" aria-pressed="true">すべて<span>' + str(len(arts)) + "</span></button>"
    out += "".join(f'<button type="button" data-f="{k}" aria-pressed="false">{v}<span>{len(lst)}</span></button>' for k, v, lst in used) + "</nav>"
    out += "".join(f'<section class="col-sec" data-cat="{k}"><h2>{v}<small>{len(lst)}本</small></h2><div class="col-grid">' + "".join(card(a) for a in lst) + "</div></section>" for k, v, lst in used)
    return out + IDX_JS


def main():
    arts = sorted((parse(p) for p in (ROOT / "content").glob("*.md")), key=lambda a: a["date"], reverse=True)
    for a in arts:
        d = ROOT / "column" / a["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(article_page(a), encoding="utf-8")
    # 一覧
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "アフィリエイト運用コラム", "url": BASE + "/column/", "publisher": ORG}
    idx = HEAD.format(title="アフィリエイト運用コラム｜アフィまかせ", desc="広告主・代理店のためのアフィリエイト運用の実務、ステマ規制・表記の注意点、工数を減らす方法を解説します。",
                      url=BASE + "/column/", ogtype="website", css=CSS + IDX_CSS, jsonld=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>', pageid="col-index")
    idx += index_body(arts) + CTA + "</main>" + FOOT
    (ROOT / "column" / "index.html").write_text(idx, encoding="utf-8")
    # sitemap
    today = datetime.date.today().isoformat()
    urls = [(BASE + "/", today), (BASE + "/column/", today), (BASE + "/privacy.html", today)] + [(f"{BASE}/column/{a['slug']}/", a.get("updated", a["date"])) for a in arts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    # llms.txt（AI 向けのサイト案内）
    # 料金は docs/pricing.md が正。変えたらここも合わせる
    llms = ["# アフィまかせ", "", "> 広告主・アフィリエイト代理店向けのアフィリエイト運用支援サービス。主力は、ASP・メディアとの日々のやり取りを「アフィまかせの担当者」として代わりに受けて返す窓口代行（Chatwork に同席し、任された範囲はその場で返答）。成果承認、記事の表記チェック（ステマ規制・景品表示法などの一次チェックで、法的な判断ではない）、月次レポート、新規メディアの調査・開拓はオプションで追加できる。運営は合同会社IXS（https://ixs-llc.com/）。", "",
            "## サービス", f"- [サービス概要・料金・工数の試算]({BASE}/): 窓口代行 月3万円（ASP3社まで。4社目から1社につき+1万円）／オプション: 成果承認 ASP1社3,000円（5社目から2,000円）、表記チェック 月20サイトまで1万円〜、月次レポート1万円、新規メディアの調査・開拓4万円／まるごとパック 月9万円／表記チェックのみ 月2万円（いずれも税別・初期費用0円・最低3か月。媒体費が月100万円を超える場合は見積もり）", f"- [プライバシーポリシー]({BASE}/privacy.html)", "", "## コラム"]
    llms += [f"- [{a['title']}]({BASE}/column/{a['slug']}/): {a['description']}" for a in arts]
    (ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    print(f"{len(arts)} articles built")


if __name__ == "__main__":
    main()
