import csv
import tempfile
import unittest
from pathlib import Path

from notebook.validate_summary import FIELDS, load_summary, parse_p_value, significance_label


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_summary()

    def check_invalid(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "summary.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ValueError):
                load_summary(path)

    def test_published_summary_has_six_comparisons(self):
        self.assertEqual(len(self.rows), 6)

    def test_missing_comparison_rejected(self):
        self.check_invalid(self.rows[:-1])

    def test_duplicate_comparison_rejected(self):
        self.check_invalid(self.rows + [self.rows[0]])

    def test_nonfinite_effect_rejected(self):
        for value in ("NaN", "inf", "-inf", "not-a-number"):
            with self.subTest(value=value):
                self.check_invalid([{**self.rows[0], "cohens_d": value}] + self.rows[1:])

    def test_invalid_p_value_rejected(self):
        for value in ("NaN", "0", "1.1", "-0.1", "missing", "<"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_p_value(value)

    def test_very_small_p_value_is_preserved(self):
        operator, value = parse_p_value("2.10e-195")
        self.assertEqual(operator, "=")
        self.assertGreater(value, 0)

    def test_bound_preserved(self):
        self.assertEqual(parse_p_value("<1e-58")[0], "<")

    def test_threshold_labels_respect_exact_values_and_upper_bounds(self):
        for value in ("0.049", "<0.05", "<1e-58"):
            self.assertEqual(significance_label(value), "reported p < 0.05")
        for value in ("0.05", "0.390", "1"):
            self.assertEqual(significance_label(value), "reported p >= 0.05")
        self.assertIn("does not establish", significance_label("<0.5"))

    def test_empty_field_rejected(self):
        self.check_invalid([{**self.rows[0], "protocol": ""}] + self.rows[1:])

    def test_wrong_schema_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "summary.csv"
            path.write_text("wrong,columns\n1,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_summary(path)


if __name__ == "__main__":
    unittest.main()
