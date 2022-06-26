import unittest
from pathlib import Path
import sys
import tkinter
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.score as score
import src.database as database
import src.const as const


class TestDatabase(unittest.TestCase):
    def setUp(self):  # 設定 save_temp_db
        print("setUp")
        self.pattern = const.PATTERN
        self.db_name = "./data/test.db"
        self.score = score.Score(0)
        self.db = database.Database(self.db_name, self.score)

    def create_temp_data_score(self):
        # 2ポイントのscoreデータ
        self.db.arrayFrameStart = [0, 100, 200]
        self.db.arrayFrameEnd = [10, 150, 230]
        self.db.arraySet = ["1", "1", "1"]
        self.db.arrayGame = ["0-0", "0-0", "0-0"]
        self.db.arrayScore = ["0-0", "15-0", "15-0"]
        self.db.arrayScoreResult = ["15-0", "15-15", "15-15"]
        self.db.arrayFirstSecond = [0, 1, 2]
        self.db.arrayServer = ["A", "B", "B"]
        self.db.arrayPointWinner = ["A", "B", "B"]
        self.db.pointWin = [[0, 1, 1], [1, 0, 0]]  # pointwin [[0], [0]] [[A],[B]]
        self.db.arrayFault = [0, 1, 1]
        self.db.arrayPointPattern = [self.pattern[0], self.pattern[1], self.pattern[3]]
        self.db.arrayForeBack = ["Fore", "Back", "Back"]
        self.db.arrayContactServe = [[0, 0], [0, 0], [0, 0]]  # 使っている？使っていなければ消す
        self.db.arrayCourt = [
            [[0, 1], [2, 3], [2, 3]],
            [[4, 5], [6, 7], [2, 3]],
            [[8, 9], [10, 11], [2, 3]],
            [[12, 13], [14, 15], [2, 3]],
        ]

    def create_temp_data_shot(self):
        self.db.shot_frame = [1296, 1730, 1742]
        self.db.array_ball_position_shot_x = ["5.42", "9.26", "13.96"]
        self.db.array_ball_position_shot_y = ["17.15", "16.21", "24.5"]
        self.db.arrayPlayerAPosition_x = ["4.57", "4.57", "4.57"]
        self.db.arrayPlayerAPosition_y = ["-1.97", "-1.97", "-1.97"]
        self.db.arrayPlayerBPosition_x = ["1.27", "1.27", "1.27"]
        self.db.arrayPlayerBPosition_y = ["-8.95", "-8.95", "-8.95"]
        self.db.arrayHitPlayer = ["Nishioka", "Nishioka", "Nishioka"]
        self.db.arrayBounceHit = ["Bounce", "Hit", "Bounce"]
        self.db.arrayForeBack = ["", "Fore", ""]
        self.db.arrayDirection = ["Cross", "Cross", "Cross"]
        self.db.array_x1 = [2, 3, 4]
        self.db.array_y1 = [2, 3, 4]
        self.db.array_x2 = [2, 3, 4]
        self.db.array_y2 = [2, 3, 4]
        self.db.array_x3 = [2, 3, 4]
        self.db.array_y3 = [2, 3, 4]
        self.db.array_x4 = [2, 3, 4]
        self.db.array_y4 = [2, 3, 4]

        # shotデータ
        # self.db.array_ball_position_shot = [
        #     [],
        #     [[1, 1296.0, "5.42", "17.15"]],
        #     [[2, 1730.0, "9.26", "16.21"], [2, 1742.0, "13.96", "24.5"]],
        # ]  # point frame bx by
        # self.db.arrayPlayerAPosition = [
        #     [],
        #     [[1, 861.0, "4.57", "-1.97"]],
        #     [[2, 861.0, "4.57", "-1.97"], [2, 861.0, "4.57", "-1.97"]],
        # ]
        # self.db.arrayPlayerBPosition = [
        #     [],
        #     [[1, 1016.0, "1.27", "-8.95"]],
        #     [[2, 1016.0, "1.27", "-8.95"], [2, 1016.0, "1.27", "-8.95"]],
        # ]  #
        # self.db.arrayHitPlayer = [
        #     [],
        #     ["Nishioka"],
        #     ["Nishioka", "Nishioka", "Nishioka"],
        # ]
        # self.db.arrayBounceHit = [[], ["Hit"], ["Bounce", "Hit", "Bounce"]]
        # self.db.arrayForeBack = [[], ["Fore"], ["", "Fore", ""]]
        # self.db.arrayDirection = [[], ["Cross"], ["Cross", "Cross", "Cross"]]
        # self.db.array_x1 = [[], [1], [2, 3, 4]]
        # self.db.array_y1 = [[], [1], [2, 3, 4]]
        # self.db.array_x2 = [[], [1], [2, 3, 4]]
        # self.db.array_y2 = [[], [1], [2, 3, 4]]
        # self.db.array_x3 = [[], [1], [2, 3, 4]]
        # self.db.array_y3 = [[], [1], [2, 3, 4]]
        # self.db.array_x4 = [[], [1], [2, 3, 4]]
        # self.db.array_y4 = [[], [1], [2, 3, 4]]

    def create_temp_data_basic(self):
        self.db.playerA = "player_A"
        self.db.playerB = "player_B"
        self.db.number = 2
        self.db.totalGame = 5
        self.db.faultFlug = 1

    def test_save_database_score(self):
        """3ポイントのスコアデータをデータベースに保存したときの保存数が合っているか"""
        self.assertEqual(1, self.db.save_database_score(self.db_name))
        self.create_temp_data_score()
        self.assertEqual(3, self.db.save_database_score(self.db_name))

    def test_save_database_shot(self):
        """calc length of saved dataframe"""
        self.assertEqual(0, self.db.save_database_shot(self.db_name))  # 初期データ　0
        self.create_temp_data_shot()
        self.assertEqual(3, self.db.save_database_shot(self.db_name))  # 仮データ 3

    def test_save_database_basic(self):
        """basicデータ"""
        self.assertEqual(1, self.db.save_database_basic(self.db_name))
        self.create_temp_data_basic()
        self.assertEqual(1, self.db.save_database_basic(self.db_name))

    def test_array2arrays(self):
        """frame ballx ballyの3つの配列を1つの配列にする"""
        frame, ballx, bally = [], [], []
        self.assertEqual([], self.db.array2arrays(frame, ballx, bally))

        # point = [1, 2, 3, 4]
        frame = [861, 1296, 1730, 1742]
        ballx = [12.2, 5.42, 9.26, 13.96]
        bally = [23.47, 17.15, 16.21, 24.5]

        self.assertEqual(
            [
                [861, 12.2, 23.47],
                [1296, 5.42, 17.15],
                [1730, 9.26, 16.21],
                [1742, 13.96, 24.5],
            ],
            self.db.array2arrays(frame, ballx, bally),
        )

    def test_array2arrays2(self):
        point = [1, 2, 3, 3, 4, 4, 4, 4]
        hit = ["A", "B", "A", "B", "A", "B", "A", "B"]
        bh = ["Hit", "Hit", "Hit", "Bounce", "Hit", "Bounce", "Hit", "Bounce"]
        fb = ["", "", "Fore", "", "", "Back", "", ""]
        d = ["Cross", "Cross", "Cross", "Cross", "Cross", "Cross", "Cross", "Cross"]
        x1 = [1, 2, 3, 4, 5, 6, 7, 8]
        y1 = [1, 2, 3, 4, 5, 6, 7, 8]
        x2 = [1, 2, 3, 4, 5, 6, 7, 8]
        y2 = [1, 2, 3, 4, 5, 6, 7, 8]
        x3 = [1, 2, 3, 4, 5, 6, 7, 8]
        y3 = [1, 2, 3, 4, 5, 6, 7, 8]
        x4 = [1, 2, 3, 4, 5, 6, 7, 8]
        y4 = [1, 2, 3, 4, 5, 6, 7, 8]
        (
            array_hit,
            array_bouncehit,
            array_foreback,
            array_direction,
            array_x1,
            array_y1,
            array_x2,
            array_y2,
            array_x3,
            array_y3,
            array_x4,
            array_y4,
        ) = self.db.array2arrays2(point, hit, bh, fb, d, x1, y1, x2, y2, x3, y3, x4, y4)
        self.assertEqual(
            [[], ["A"], ["B"], ["A", "B"], ["A", "B", "A", "B"]], array_hit
        )
        self.assertEqual(
            [
                [],
                ["Hit"],
                ["Hit"],
                ["Hit", "Bounce"],
                ["Hit", "Bounce", "Hit", "Bounce"],
            ],
            array_bouncehit,
        )
        self.assertEqual(
            [[], [""], [""], ["Fore", ""], ["", "Back", "", ""]], array_foreback
        )
        self.assertEqual(
            [
                [],
                ["Cross"],
                ["Cross"],
                ["Cross", "Cross"],
                ["Cross", "Cross", "Cross", "Cross"],
            ],
            array_direction,
        )
        self.assertEqual([[], [1], [2], [3, 4], [5, 6, 7, 8]], array_x1)

    def test_load_database_score_init(self):
        sc = score.Score(0)
        db_name = "./tests/temp.db"
        db = database.Database(db_name, sc)
        db.save_database_score(db_name)
        self.assertEqual(1, db.load_database_score(db_name))  # 初期scoreテーブル

    def test_load_database_score(self):
        self.create_temp_data_score()
        self.assertEqual(3, self.db.load_database_score(self.db_name))

    def test_load_database_shot_init(self):
        sc = score.Score(0)
        db_name = "./tests/temp.db"
        db = database.Database(db_name, sc)
        db.save_database_shot(db_name)
        self.assertEqual(0, db.load_database_shot(db_name))

    def test_load_database_shot(self):
        # レコード数3つのデータ
        # self.create_temp_data_score()
        self.create_temp_data_shot()
        self.assertEqual(3, self.db.load_database_shot(self.db_name))

    def test_load_database_basic(self):
        sc = score.Score(0)
        db_name = "./data/test.db"
        db = database.Database(db_name, sc)
        db.save_database_basic(db_name)
        self.assertEqual(1, self.db.load_database_basic(db_name))  # 初期basicテーブル

    def test_pop_array_from_df(self):
        df = pd.DataFrame({"x1": [1, 2, 3]})
        x1 = self.db.pop_array_from_df(df, "x1")
        self.assertEqual([1, 2, 3], x1)

        x2 = self.db.pop_array_from_df(df, "x2")
        self.assertEqual([[], [], []], x2)

    def test_check_size_return_array(self):
        array_frame_start = [0, 100, 200]
        array_x1 = [[], [1], [2, 3, 4]]
        score_array_x1 = self.db.check_size_return_array(
            array_x1, len(array_frame_start)
        )
        self.assertEqual(array_x1, score_array_x1)

        # データが少ない場合
        array_x1 = [[], [1]]
        score_array_x1 = self.db.check_size_return_array(
            array_x1, len(array_frame_start)
        )
        self.assertEqual([[], [1], []], score_array_x1)

        array_frame_start = [0, 100, 200, 300, 400, 500]
        array_x1 = [[], [1], [2, 3, 4]]
        score_array_x1 = self.db.check_size_return_array(
            array_x1, len(array_frame_start)
        )
        self.assertEqual([[], [1], [2, 3, 4], [], [], []], score_array_x1)

    # def test_index_shot(self):

    def test_db2score(self):
        self.create_temp_data_score()
        self.create_temp_data_shot()
        self.db.db2score()
        self.assertEqual(
            self.db.array_ball_position_shot_x, self.db.score.array_ball_position_shot_x
        )
        self.assertEqual(
            self.db.arrayPlayerAPosition_x, self.db.score.arrayPlayerAPosition_x
        )
        self.assertEqual(
            self.db.arrayPlayerBPosition_x, self.db.score.arrayPlayerBPosition_x
        )
        self.assertEqual(self.db.arrayHitPlayer, self.db.score.arrayHitPlayer)
        self.assertEqual(self.db.arrayBounceHit, self.db.score.arrayBounceHit)
        self.assertEqual(self.db.arrayForeBack, self.db.score.arrayForeBack)
        self.assertEqual(self.db.arrayDirection, self.db.score.arrayDirection)
        self.assertEqual(self.db.array_x1, self.db.score.array_x1)
        self.assertEqual(self.db.array_y1, self.db.score.array_y1)
        self.assertEqual(self.db.array_x2, self.db.score.array_x2)
        self.assertEqual(self.db.array_y2, self.db.score.array_y2)
        self.assertEqual(self.db.array_x3, self.db.score.array_x3)
        self.assertEqual(self.db.array_y3, self.db.score.array_y3)
        self.assertEqual(self.db.array_x4, self.db.score.array_x4)
        self.assertEqual(self.db.array_y4, self.db.score.array_y4)
        self.assertEqual([2,2,2],self.db.score.shot_index)


