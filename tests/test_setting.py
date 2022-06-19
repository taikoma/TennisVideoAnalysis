import unittest
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.setting as setting


class TestSetting(unittest.TestCase):
    def setUp(self):
        self.filaname = "./tests/settings.json"
        self.setting = setting.Setting(self.filaname)

    def tearDown(self):
        os.remove(self.filaname)

    def test_save_data(self):
        print("test_save_data")
        playerA = "A"
        playerB = ""
        firstServer = ""
        dataFile = ""
        videoFile = ""
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        self.setting.save_data(
            playerA, playerB, firstServer, dataFile, videoFile, x1, y1, x2, y2
        )
        self.assertEqual(playerA, self.setting.playerA)
        self.assertEqual(playerB, self.setting.playerB)
        self.assertEqual(firstServer, self.setting.firstServer)
        self.assertEqual(dataFile, self.setting.dataFile)
        self.assertEqual(videoFile, self.setting.videoFile)
        self.assertEqual(x1, self.setting.sx1)
        self.assertEqual(x2, self.setting.sx2)
        self.assertEqual(y1, self.setting.sy1)
        self.assertEqual(y2, self.setting.sy2)
