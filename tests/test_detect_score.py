import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src/predict"))
import src.predict.detect_score as detect_score


class TestDetectScore(unittest.TestCase):
    def setUp(self):  # 設定
        self.ds = detect_score.DetectScore()

    def test_fix_text(self):
        # bugfix
        text = "3 6 10 6 3 4 15"  # 10を1 0 に分解したい
        text = self.ds.fix_text(text)
        self.assertEqual("3 6 1 0 6 3 4 15", text)

    def test_fix_in_ad(self):
        print("text_fix_in_ad")
        text_array = ["3", "6", "Ad"]
        text_array = self.ds.fix_in_ad(text_array)
        self.assertEqual(["3", "40", "6", "Ad"], text_array)

        text_array = ["3", "Ad", "6"]
        text_array = self.ds.fix_in_ad(text_array)
        self.assertEqual(["3", "Ad", "6", "40"], text_array)

        text_array = ["3", "6", "1", "6", "3", "4", "Ad"]
        text_array = self.ds.fix_in_ad(text_array)
        self.assertEqual(["3", "6", "1", "40", "6", "3", "4", "Ad"], text_array)

        text_array = ["3", "6", "1", "Ad", "6", "3", "4"]
        text_array = self.ds.fix_in_ad(text_array)
        self.assertEqual(["3", "6", "1", "Ad", "6", "3", "4", "40"], text_array)

    def test_fix_zero_zero(self):
        text_array = ["3", "6"]
        text_array = self.ds.fix_zero_zero(text_array)
        self.assertEqual(["3", "0", "6", "0"], text_array)

        text_array = ["3", "6", "6", "3"]
        text_array = self.ds.fix_zero_zero(text_array)
        self.assertEqual(["3", "6", "0", "6", "3", "0"], text_array)

        text_array = ["3", "6", "1", "6", "3", "4"]
        text_array = self.ds.fix_zero_zero(text_array)
        self.assertEqual(["3", "6", "1", "0", "6", "3", "4", "0"], text_array)

    def test_text2score(self):
        text = "A 40"
        set_num = self.ds.get_set_text_num(text)
        self.assertEqual(2, set_num)

        text = "4 1 15\n6 1 15"
        set_num = self.ds.get_set_text_num(text)
        self.assertEqual(6, set_num)

        text = "1 15 \n0\n0"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("1", game_a)
        self.assertEqual("0", game_b)
        self.assertEqual("15", score_a)
        self.assertEqual("0", score_b)

        text = "1 A \n5\n40"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("1", game_a)
        self.assertEqual("5", game_b)
        self.assertEqual("A", score_a)
        self.assertEqual("40", score_b)

        text = "30 15"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("0", game_a)
        self.assertEqual("0", game_b)
        self.assertEqual("30", score_a)
        self.assertEqual("15", score_b)

        text = "A 40"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("0", game_a)
        self.assertEqual("0", game_b)
        self.assertEqual("A", score_a)
        self.assertEqual("40", score_b)

        text = "15 "
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("0", game_a)
        self.assertEqual("0", game_b)
        self.assertEqual("15", score_a)
        self.assertEqual("", score_b)

        text = ""
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("", game_a)
        self.assertEqual("", game_b)
        self.assertEqual("", score_a)
        self.assertEqual("", score_b)

        text = "4 1 15\n6 2 30"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("1", game_a)
        self.assertEqual("15", score_a)
        self.assertEqual("2", game_b)
        self.assertEqual("30", score_b)

        text = "4 6 4 15\n6 2 2 30"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("4", game_a)
        self.assertEqual("15", score_a)
        self.assertEqual("2", game_b)
        self.assertEqual("30", score_b)

        text = "6 4 6 4 15\n4 6 2 2 30"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("4", game_a)
        self.assertEqual("15", score_a)
        self.assertEqual("2", game_b)
        self.assertEqual("30", score_b)

        text = "5 6 4 6 4 15\n7 4 6 2 2 30"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("4", game_a)
        self.assertEqual("15", score_a)
        self.assertEqual("2", game_b)
        self.assertEqual("30", score_b)

        text = "3 6 1\n6 3 4 Ad"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("1", game_a)
        self.assertEqual("4", game_b)
        self.assertEqual("40", score_a)
        self.assertEqual("Ad", score_b)

        text = "3 6 1\n6 3 4"
        game_a, game_b, score_a, score_b = self.ds.text2score(text)
        self.assertEqual("1", game_a)
        self.assertEqual("4", game_b)
        self.assertEqual("0", score_a)
        self.assertEqual("0", score_b)
