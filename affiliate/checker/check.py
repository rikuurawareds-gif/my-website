#!/usr/bin/env python3
"""
アフィまかせ 表記チェック v0（ルール辞書による一次チェック）

使い方:
  python3 check.py --url https://example.com/article [--url ...] [--brand 商品名] --out report.md
  python3 check.py --urls-file urls.txt --brand 商品名 --out report.md --csv findings.csv
  python3 check.py --html tests/sample_bad.html --out report.md      # 手元のHTMLで試す

- 公開ページだけを取得する。robots.txt に従い、同じサイトへは間隔を空ける
- 法的な判断はしない。確認すべき箇所の候補を拾うだけ（レポートの冒頭に明記）
- 標準ライブラリのみで動く（Python 3.9 以上）
"""
import argparse, csv, datetime, html, json, re, sys, time, urllib.parse, urllib.request, urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

UA = "AfimakaseChecker/0.1 (+https://afimakase.pages.dev/)"
HERE = Path(__file__).resolve().parent
DISCLAIMER = ("本レポートは、表現上のリスクを機械的に抽出した一次チェックであり、法的な判断を示すものではありません。"
              "最終的な判断は、広告主様（必要に応じて弁護士等の専門家）にてお願いいたします。")
CONTEXT = 25          # 抜粋の前後の文字数
SOFTEN_WINDOW = 80    # 根拠の注記を探す範囲（前後の文字数）
PR_HEAD_RATIO = 0.25  # 記事の冒頭とみなす範囲（本文の先頭から何割か）


class TextExtractor(HTMLParser):
    """表示される本文テキストと、リンク先を取り出す"""
    SKIP = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self._skip, self.title = [], [], 0, ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)
        if tag in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "section", "article"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.parts.append(data)

    def text(self):
        t = "".join(self.parts)
        t = re.sub(r"[ \t　]+", " ", t)
        return re.sub(r"\n\s*\n+", "\n", t).strip()


def load_rules():
    return json.loads((HERE / "rules.json").read_text(encoding="utf-8"))


_last_access = {}


def fetch(url, delay=3.0):
    """robots.txt を守って公開ページを取得する"""
    p = urllib.parse.urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
    try:
        rp.read()
        if not rp.can_fetch(UA, url):
            raise PermissionError("robots.txt で取得が許可されていない")
    except PermissionError:
        raise
    except Exception:
        pass  # robots.txt が読めない場合は通常のアクセスとして扱う
    wait = delay - (time.time() - _last_access.get(p.netloc, 0))
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read()
        charset = r.headers.get_content_charset() or "utf-8"
    _last_access[p.netloc] = time.time()
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def excerpt(text, start, end):
    a, b = max(0, start - CONTEXT), min(len(text), end + CONTEXT)
    s = text[a:b].replace("\n", " ")
    return ("…" if a > 0 else "") + s + ("…" if b < len(text) else "")


def check_page(page_html, url, rules, brand=None):
    ex = TextExtractor()
    ex.feed(page_html)
    text = ex.text()
    findings = []

    # 広告リンクの有無
    hosts = rules["affiliate_link_hosts"]
    aff_links = [l for l in ex.links if any(h in l for h in hosts)]
    brand_hit = (brand in text) if brand else None

    # PR表記（ステマ告示）
    label_re = re.compile("|".join(re.escape(x) for x in rules["pr_labels"]))
    head = text[: max(300, int(len(text) * PR_HEAD_RATIO))]
    in_head = label_re.search(head)
    anywhere = label_re.search(text)
    if aff_links and not anywhere:
        findings.append(dict(id="S01", category="景品表示法（ステマ告示）", severity="高", name="広告であることの表示（PR表記）が見当たらない",
                             excerpt=f"広告リンク {len(aff_links)} 件あり／PR・広告の表記なし",
                             basis="景品表示法 第5条第3号の指定告示（いわゆるステマ告示、2023年10月施行）。広告主が表示内容の決定に関与したアフィリエイト記事は広告主の表示とされ、広告であることが分かりにくい場合は不当表示となるおそれがある",
                             fix="記事の冒頭など分かりやすい位置に「広告」「PR」等の表記を入れる"))
    elif aff_links and not in_head:
        pos = anywhere.start()
        findings.append(dict(id="S02", category="景品表示法（ステマ告示）", severity="中", name="PR表記が冒頭にない",
                             excerpt=excerpt(text, pos, anywhere.end()),
                             basis="ステマ告示の運用基準では、広告であることが一般消費者に明瞭に分かる表示が求められる。末尾のみの表記などは不明瞭と判断されるおそれがある",
                             fix="PR表記を記事の冒頭（タイトル付近）に移す、または追加する"))

    # 辞書のルール
    for r in rules["rules"]:
        soft = re.compile(r["softener"]) if r.get("softener") else None
        seen, last_end = 0, -1000
        for m in re.finditer(r["pattern"], text):
            if m.start() < last_end + 15:  # 近すぎる同じルールの一致は1件にまとめる
                continue
            last_end = m.end()
            win = text[max(0, m.start() - SOFTEN_WINDOW): m.end() + SOFTEN_WINDOW]
            softened = bool(soft and soft.search(win))
            sev = r["severity"]
            if softened:
                sev = {"高": "中", "中": "低", "低": "低"}[sev]
            findings.append(dict(id=r["id"], category=r["category"], severity=sev, name=r["name"],
                                 excerpt=excerpt(text, m.start(), m.end()),
                                 basis=r["basis"] + ("（近くに根拠・注記らしき記載あり。内容を確認）" if softened else ""),
                                 fix=r["fix"]))
            seen += 1
            if seen >= 5:  # 同じルールは1ページ5件まで
                break

    order = {"高": 0, "中": 1, "低": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["id"]))
    return dict(url=url, title=ex.title.strip(), chars=len(text), aff_links=len(aff_links),
                brand_hit=brand_hit, findings=findings)


def request_text(f, url):
    """メディアにそのまま送れる修正依頼文（定型）"""
    return (f"記事「{url}」の「{f['excerpt'].strip('…')[:60]}」の箇所について、{f['name']}に当たるおそれがあるため、"
            f"{f['fix']}よう修正をお願いできますでしょうか。")


def render_markdown(results, brand):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(len(r["findings"]) for r in results if "findings" in r)
    hi = sum(1 for r in results if "findings" in r for f in r["findings"] if f["severity"] == "高")
    out = [f"# 表記チェック レポート（一次チェック）", "",
           f"- 実施日時: {now}", f"- 対象: {brand or '指定なし'}",
           f"- 確認した記事: {len(results)} 本 ／ 指摘: {total} 件（うち重要度「高」{hi} 件）", "",
           f"> {DISCLAIMER}", ""]
    out += ["## 記事ごとの結果", "", "| 記事 | 広告リンク | 指摘（高/中/低） |", "|---|---|---|"]
    for r in results:
        if "error" in r:
            out.append(f"| {r['url']} | - | 取得できず（{r['error']}） |")
            continue
        c = {s: sum(1 for f in r["findings"] if f["severity"] == s) for s in "高中低"}
        out.append(f"| [{html.escape(r['title'][:40]) or r['url']}]({r['url']}) | {r['aff_links']} | {c['高']}/{c['中']}/{c['低']} |")
    out.append("")
    for r in results:
        if "error" in r or not r["findings"]:
            continue
        out += [f"## {r['title'] or r['url']}", f"{r['url']}", ""]
        if r["brand_hit"] is False:
            out += [f"※ 本文に「{brand}」の記載が見つかりませんでした。対象の記事か確認してください。", ""]
        out += ["| 重要度 | 該当箇所 | 何が問題か | 根拠 | 修正の方向 |", "|---|---|---|---|---|"]
        for f in r["findings"]:
            cell = lambda s: s.replace("|", "｜").replace("\n", " ")
            out.append(f"| {f['severity']} | {cell(f['excerpt'])} | {cell(f['name'])} | {cell(f['basis'])} | {cell(f['fix'])} |")
        out += ["", "**メディアへの修正依頼文（案）**", ""]
        for f in r["findings"]:
            if f["severity"] in ("高", "中"):
                out.append(f"- {request_text(f, r['url'])}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="アフィまかせ 表記チェック v0")
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--urls-file")
    ap.add_argument("--html", action="append", default=[], help="手元のHTMLファイル（テスト用）")
    ap.add_argument("--brand")
    ap.add_argument("--out", default="report.md")
    ap.add_argument("--csv")
    ap.add_argument("--delay", type=float, default=3.0)
    a = ap.parse_args()

    rules = load_rules()
    urls = list(a.url)
    if a.urls_file:
        urls += [l.strip() for l in Path(a.urls_file).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    results = []
    for path in a.html:
        results.append(check_page(Path(path).read_text(encoding="utf-8"), path, rules, a.brand))
    for u in urls:
        try:
            results.append(check_page(fetch(u, a.delay), u, rules, a.brand))
        except Exception as e:
            results.append(dict(url=u, error=str(e)[:80]))
    if not results:
        ap.error("--url / --urls-file / --html のいずれかを指定してください")

    Path(a.out).write_text(render_markdown(results, a.brand), encoding="utf-8")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as fp:
            w = csv.writer(fp)
            w.writerow(["記事URL", "ルール", "重要度", "問題", "該当箇所", "根拠", "修正の方向", "修正依頼文"])
            for r in results:
                for f in r.get("findings", []):
                    w.writerow([r["url"], f["id"], f["severity"], f["name"], f["excerpt"], f["basis"], f["fix"], request_text(f, r["url"])])
    n = sum(len(r.get("findings", [])) for r in results)
    print(f"{len(results)} 記事、指摘 {n} 件 → {a.out}")


if __name__ == "__main__":
    main()
