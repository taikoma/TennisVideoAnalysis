import unittest
from pathlib import Path
import sys
import tkinter
import numpy as np
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
# import src.TennisVideoAnalysis as TennisVideoAnalysis
# import src.video as video
import src.score as score
import src.database as database
import src.const as const

class TestDatabase(unittest.TestCase):
    def setUp(self):#設定 save_temp_db
        print("setUp")
        self.pattern = const.PATTERN
        db_name="./data/test.db"
        self.score = score.Score(0)
        self.db = database.Database(db_name, self.score)

    def create_temp_data(self):
        #2ポイントのscoreデータ
        self.db.arrayFrameStart = [0,100]
        self.db.arrayFrameEnd = [10,150]
        self.db.arraySet = ["1","1"]
        self.db.arrayGame = ["0-0","0-0"]
        self.db.arrayScore = ["0-0","15-0"]
        self.db.arrayScoreResult = ["15-0","15-15"]
        self.db.arrayFirstSecond = [0,1]
        self.db.arrayServer = ["A","B"]
        self.db.arrayPointWinner = ["A","B"]
        self.db.pointWin = [[0,1], [1,0]]#pointwin [[0], [0]]
        self.db.arrayFault=[0,1]
        self.db.arrayPointPattern = [self.pattern[0],self.pattern[1]]
        self.db.arrayForeBack = ["Fore","Back"]
        self.db.arrayContactServe = [[0, 0], [0, 0]]#使っている？使っていなければ消す
        self.db.arrayCourt = [[[0, 1],[2, 3]], [[4, 5],[6, 7]], [[8, 9],[10, 11]], [[12, 13],[14, 15]]]

        # self.playerA = score.playerA
        # self.playerB = score.playerB
        # print("self.playerA,self.playerB",self.playerA,self.playerB)

        # self.number = score.number
        # self.totalGame = score.totalGame
        # self.faultFlug = score.faultFlug
        # # self.arrayContactBalls = score.arrayContactBalls
        # self.arrayFault = score.arrayFault

        # self.arrayBallPosition=score.arrayBallPosition
        # self.arrayPlayerAPosition=score.arrayPlayerAPosition
        # self.arrayPlayerBPosition=score.arrayPlayerBPosition
        # self.arrayHitPlayer=score.arrayHitPlayer
        # self.arrayBounceHit=score.arrayBounceHit
        # self.arrayForeBack=score.arrayForeBack
        # self.arrayDirection=score.arrayDirection

    def test_save_database(self):
        #空データ
        self.db.save_database()

        #仮のデータを保存
        self.create_temp_data()
        self.db.save_database()

    def test_load_database(self):
        print("test_database")
        self.db.save_temp_db()
        self.db.load_database()