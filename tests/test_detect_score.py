import unittest
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.detect_score as detect_score

class TestDetectScore(unittest.TestCase):
    def setUp(self):#設定
        print("setup")
        self.ds=detect_score.DetectScore()

    def test_text2score(self):
        print("test")
        text="1 15 \n0\n0"
        game_a,game_b,score_a,score_b=self.ds.detect_score(text)
        self.assertEqual("1",game_a)
        self.assertEqual("0",game_b)
        self.assertEqual("15",score_a)
        self.assertEqual("0",score_b)

# if __name__ == "__main__":
#     unittest.main()
        
