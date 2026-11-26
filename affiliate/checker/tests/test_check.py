import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import check

R = check.load_rules()
def run(name, brand=None):
    return check.check_page((Path(__file__).parent / name).read_text(encoding="utf-8"), name, R, brand)
ids = lambda res: {f["id"] for f in res["findings"]}

class T(unittest.TestCase):
    def test_bad_page_flags_expected_rules(self):
        r = run("sample_bad.html", "サンプルサプリ")
        for rid in ["S01", "K01", "K02", "K04", "K06", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06"]:
            self.assertIn(rid, ids(r), rid)
        self.assertTrue(r["brand_hit"])
    def test_script_text_is_ignored(self):
        r = run("sample_bad.html")
        self.assertFalse(any("var x" in f["excerpt"] for f in r["findings"]))
    def test_ok_page_has_no_high(self):
        r = run("sample_ok.html")
        self.assertNotIn("S01", ids(r)); self.assertNotIn("S02", ids(r))
        self.assertFalse([f for f in r["findings"] if f["severity"] == "高"])
        k01 = [f for f in r["findings"] if f["id"] == "K01"]
        self.assertTrue(k01 and k01[0]["severity"] == "低")  # 根拠の注記があるので下がる
    def test_late_pr_and_finance(self):
        r = run("sample_late_pr.html")
        self.assertIn("S02", ids(r)); self.assertIn("F02", ids(r))
    def test_brand_missing(self):
        self.assertFalse(run("sample_ok.html", "存在しない商品")["brand_hit"])

if __name__ == "__main__":
    unittest.main()
