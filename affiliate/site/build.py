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
BASE = "https://afimakase.pages.dev"
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
:root{--bg:#fff;--surface:#f5f7fa;--ink:#14181f;--muted:#5a6271;--line:#e2e6ec;--brand:#0f5bd8;--accent:#e8590c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.9 system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif}
header,footer{border-bottom:1px solid var(--line)}footer{border-top:1px solid var(--line);border-bottom:0;margin-top:64px;font-size:13px;color:var(--muted)}
.w{max-width:760px;margin:0 auto;padding:0 16px}header .w{display:flex;justify-content:space-between;align-items:center;height:56px}
header a{color:var(--ink);text-decoration:none;font-weight:800}header nav a{font-weight:600;font-size:14px;margin-left:16px}
.crumb{font-size:13px;color:var(--muted);margin:16px 0}.crumb a{color:var(--muted)}
h1{font-size:clamp(26px,4.5vw,34px);line-height:1.4;margin:8px 0 12px}h2{font-size:23px;line-height:1.5;margin:48px 0 12px;padding-top:8px;border-top:2px solid var(--ink)}h3{font-size:19px;margin:28px 0 8px}
.meta{font-size:13px;color:var(--muted)}.lead{background:var(--surface);border-left:4px solid var(--brand);padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0}
.lead strong:first-child{display:block;font-size:14px;color:var(--brand);margin-bottom:4px}
.toc{border:1px solid var(--line);border-radius:10px;padding:12px 20px;margin:24px 0;font-size:15px}.toc ol{margin:6px 0;padding-left:20px}.toc a{color:var(--ink)}
a{color:var(--brand)}.tbl{overflow-x:auto;margin:16px 0}table{border-collapse:collapse;width:100%;font-size:15px}th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}th{background:var(--surface)}
blockquote{margin:16px 0;padding:12px 16px;background:#fff8f0;border-radius:8px;font-size:15px}
.cta{margin:48px 0;padding:24px;border-radius:14px;background:var(--surface);text-align:center}.cta a.btn{display:inline-block;margin:8px 6px;padding:12px 22px;border-radius:999px;background:var(--accent);color:#fff;font-weight:700;text-decoration:none}
.cta a.ghost{background:transparent;color:var(--brand);border:1.5px solid var(--brand)}
.list a{display:block;padding:16px 0;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none}.list a strong{display:block;font-size:18px}.list a span{font-size:14px;color:var(--muted)}
.note{font-size:13px;color:var(--muted)}
"""

HEAD = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="アフィまかせ"><meta name="twitter:card" content="summary">
<style>{css}</style>
{jsonld}
<script src="/assets/config.js"></script>
</head><body data-page-id="{pageid}">
<header><div class="w"><a href="/">アフィまかせ</a><nav><a href="/column/">コラム</a><a href="/#price">料金</a><a href="/#diagnosis">無料診断</a></nav></div></header>
<main class="w">
"""
FOOT = """</main>
<footer><div class="w"><p>運営: アフィまかせ ／ <a href="/privacy.html">プライバシーポリシー</a> ／ <a href="/column/">コラム一覧</a></p><p>本サイトの記事は一般的な情報の提供を目的としたもので、個別の事案についての法的な助言ではありません。</p></div></footer>
<script src="/assets/track.js"></script>
</body></html>"""
CTA = """<div class="cta"><p><strong>アフィリエイトの運用、月にどれくらいの時間がかかっていますか？</strong><br>8問・1分の無料診断で、工数と手離れできる時間の目安が分かります。</p>
<a class="btn" href="/#diagnosis">無料で工数を診断する</a><a class="btn ghost" href="/#contact">無料の伸びしろ診断・表記チェック</a></div>"""

ORG = {"@type": "Organization", "name": SITE, "url": BASE + "/", "description": "広告主・広告代理店向けのアフィリエイト運用支援サービス"}


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
    page += f'<div class="crumb"><a href="/">ホーム</a> › <a href="/column/">コラム</a></div>\n<h1>{html.escape(a["title"])}</h1>\n'
    page += f'<p class="meta">公開: {a["date"]}　更新: {a.get("updated", a["date"])}　運営: アフィまかせ</p>\n'
    page += body_html + CTA + FOOT
    return page


def main():
    arts = sorted((parse(p) for p in (ROOT / "content").glob("*.md")), key=lambda a: a["date"], reverse=True)
    for a in arts:
        d = ROOT / "column" / a["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(article_page(a), encoding="utf-8")
    # 一覧
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "アフィリエイト運用コラム", "url": BASE + "/column/", "publisher": ORG}
    idx = HEAD.format(title="アフィリエイト運用コラム｜アフィまかせ", desc="広告主・代理店のためのアフィリエイト運用の実務、ステマ規制・表記の注意点、工数を減らす方法を解説します。",
                      url=BASE + "/column/", ogtype="website", css=CSS, jsonld=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>', pageid="col-index")
    idx += '<h1>アフィリエイト運用コラム</h1><p class="meta">広告主・代理店のための、アフィリエイト運用の実務と表記の注意点。</p><div class="list">'
    idx += "".join(f'<a href="/column/{a["slug"]}/"><strong>{html.escape(a["title"])}</strong><span>{html.escape(a["description"])}</span></a>' for a in arts)
    idx += "</div>" + CTA + FOOT
    (ROOT / "column" / "index.html").write_text(idx, encoding="utf-8")
    # sitemap
    today = datetime.date.today().isoformat()
    urls = [(BASE + "/", today), (BASE + "/column/", today), (BASE + "/privacy.html", today)] + [(f"{BASE}/column/{a['slug']}/", a.get("updated", a["date"])) for a in arts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    # llms.txt（AI 向けのサイト案内）
    llms = ["# アフィまかせ", "", "> 広告主・アフィリエイト代理店向けのアフィリエイト運用支援サービス。ASP・メディア対応、成果承認、記事の表記チェック（ステマ規制・景品表示法・薬機法の一次チェック）、月次レポートまでを、AIと担当者で引き受ける。料金は月5万円（税別）から。", "",
            "## サービス", f"- [サービス概要・料金・無料診断]({BASE}/): 運用プラン月5万円、大規模プラン月15万円〜、代理店プラン1アカウント月5万円、表記チェックのみ月3万円（いずれも税別・初期費用0円・最低3か月）", f"- [プライバシーポリシー]({BASE}/privacy.html)", "", "## コラム"]
    llms += [f"- [{a['title']}]({BASE}/column/{a['slug']}/): {a['description']}" for a in arts]
    (ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    print(f"{len(arts)} articles built")


if __name__ == "__main__":
    main()
