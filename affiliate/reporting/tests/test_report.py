import sys, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import report

class T(unittest.TestCase):
    def setUp(self):
        self.recs = []
        for p in sorted(HERE.glob("*.[ct]sv")):
            self.recs += report.normalize(p)[0]
    def tot(self, month, f, asp=None):
        return sum(v[f] for (a, _), v in report.aggregate(self.recs, month).items() if asp in (None, a))
    def test_summary_csv_cp932_and_total_row_skipped(self):
        self.assertEqual(self.tot("2026-11", "occurred", "ASP甲"), 38)
        self.assertEqual(self.tot("2026-11", "approved_rw", "ASP甲"), 320000)
    def test_detail_csv_status(self):
        self.assertEqual(self.tot("2026-11", "occurred", "ASP乙"), 3)
        self.assertEqual(self.tot("2026-11", "approved", "ASP乙"), 2)
        self.assertEqual(self.tot("2026-11", "rejected", "ASP乙"), 1)
    def test_tsv_with_preamble(self):
        self.assertEqual(self.tot("2026-11", "approved", "ASP丙"), 8)
    def test_overall(self):
        self.assertEqual(self.tot("2026-11", "occurred"), 51)
        self.assertEqual(self.tot("2026-10", "occurred"), 35)

if __name__ == "__main__":
    unittest.main()
