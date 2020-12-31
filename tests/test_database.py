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
        self.db_name="./data/test.db"
        self.score = score.Score(0)
        self.db = database.Database(self.db_name, self.score)

    def create_temp_data_score(self):
        #2ポイントのscoreデータ
        self.db.arrayFrameStart = [0,100,200]
        self.db.arrayFrameEnd = [10,150,230]
        self.db.arraySet = ["1","1","1"]
        self.db.arrayGame = ["0-0","0-0","0-0"]
        self.db.arrayScore = ["0-0","15-0","15-0"]
        self.db.arrayScoreResult = ["15-0","15-15","15-15"]
        self.db.arrayFirstSecond = [0,1,2]
        self.db.arrayServer = ["A","B","B"]
        self.db.arrayPointWinner = ["A","B","B"]
        self.db.pointWin = [[0,1,1], [1,0,0]]#pointwin [[0], [0]] [[A],[B]]
        self.db.arrayFault=[0,1,1]
        self.db.arrayPointPattern = [self.pattern[0],self.pattern[1],self.pattern[3]]
        self.db.arrayForeBack = ["Fore","Back","Back"]
        self.db.arrayContactServe = [[0, 0], [0, 0], [0, 0]]#使っている？使っていなければ消す
        self.db.arrayCourt = [[[0, 1],[2, 3],[2, 3]], [[4, 5],[6, 7],[2, 3]], [[8, 9],[10, 11],[2, 3]], [[12, 13],[14, 15],[2, 3]]]

    def create_temp_data_shot(self):#3
        self.db.arrayBallPosition=[[],[[1, 1296.0, '5.42', '17.15']],[[2, 1730.0, '9.26', '16.21'], [2, 1742.0, '13.96', '24.5']]]#point frame bx by
        self.db.arrayPlayerAPosition=[[],[[1, 861.0, '4.57', '-1.97']],[[2, 861.0, '4.57', '-1.97'],[2, 861.0, '4.57', '-1.97']]]
        self.db.arrayPlayerBPosition=[[],[[1, 1016.0, '1.27', '-8.95']],[[2, 1016.0, '1.27', '-8.95'],[2, 1016.0, '1.27', '-8.95']]]#
        self.db.arrayHitPlayer=[[], ['Nishioka'],['Nishioka', 'Nishioka', 'Nishioka']]
        self.db.arrayBounceHit=[[], ['Hit'], ['Bounce','Hit', 'Bounce']]
        self.db.arrayForeBack=[[], ['Fore'],['', 'Fore','']]
        self.db.arrayDirection=[[], ['Cross'], ['Cross','Cross','Cross']]
    
    def create_temp_data_basic(self):
        self.db.playerA = "player_A"
        self.db.playerB = "player_B"
        self.db.number = 2
        self.db.totalGame = 5
        self.db.faultFlug = 1

    def test_save_database_score(self):
        self.assertEqual(1,self.db.save_database_score(self.db_name))#初期データ　1

        self.create_temp_data_score()
        self.assertEqual(3,self.db.save_database_score(self.db_name))#仮データ 3

    def test_save_database_shot(self):
        self.assertEqual(0,self.db.save_database_shot(self.db_name))#初期データ　0

        self.create_temp_data_shot()
        self.assertEqual(3,self.db.save_database_shot(self.db_name))#仮データ 3

    def test_save_database_basic(self):
        self.assertEqual(1,self.db.save_database_basic(self.db_name))#初期データ　1

        self.create_temp_data_basic()
        self.assertEqual(1,self.db.save_database_basic(self.db_name))#仮データ 1

    def test_array2arrays(self):
        print("test_array2arrays")
        point,frame,ballx,bally=[],[],[],[]
        self.assertEqual([],self.db.array2arrays(point,frame,ballx,bally))#初期データ

        point=[1,2,3,4]
        frame=[861,1296,1730,1742]
        ballx=[12.2,5.42,9.26,13.96]
        bally=[23.47,17.15,16.21,24.5]
        r=self.db.array2arrays(point,frame,ballx,bally)
        for i in range(len(point)):
            self.assertEqual([[point[i],frame[i],ballx[i],bally[i]]],r[i+1])#仮データ

    def test_array2arrays2(self):
        point=[1,2,3,3,4,4,4,4]
        hit=["A","B","A","B","A","B","A","B"]
        bh=["Hit","Hit","Hit","Bounce","Hit","Bounce","Hit","Bounce"]
        fb=["","","Fore","","","Back","",""]
        d=["Cross","Cross","Cross","Cross","Cross","Cross","Cross","Cross"]
        array_hit,array_bouncehit,array_foreback,array_direction=self.db.array2arrays2(point,hit,bh,fb,d)
        self.assertEqual([[], ['A'], ['B'], ['A', 'B'], ['A', 'B', 'A', 'B']],array_hit)
        self.assertEqual([[], ['Hit'], ['Hit'], ['Hit', 'Bounce'], ['Hit', 'Bounce', 'Hit', 'Bounce']],array_bouncehit)
        self.assertEqual([[], [''], [''], ['Fore', ''], ['', 'Back', '', '']],array_foreback)
        self.assertEqual([[], ['Cross'], ['Cross'], ['Cross', 'Cross'], ['Cross', 'Cross', 'Cross', 'Cross']],array_direction)

    def test_load_database_score(self):
        sc = score.Score(0)
        db_name="./data/test.db"
        db = database.Database(db_name, sc)
        db.save_database_score(db_name)
        self.assertEqual(1,self.db.load_database_score(db_name))#初期scoreテーブル

    def test_load_database_shot(self):
        sc = score.Score(0)
        db_name="./data/test.db"
        db = database.Database(db_name, sc)
        db.save_database_shot(db_name)
        self.assertEqual(0,self.db.load_database_shot(db_name))#初期shotテーブル

    def test_load_database_basic(self):
        sc = score.Score(0)
        db_name="./data/test.db"
        db = database.Database(db_name, sc)
        db.save_database_basic(db_name)
        self.assertEqual(1,self.db.load_database_basic(db_name))#初期basicテーブル
        
        
