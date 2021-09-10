import unittest
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.score as score
import src.const as const


class TestScore(unittest.TestCase):
    def setUp(self):  # 設定 save_temp_db
        self.score = score.Score(0)

    def test_convert_set(self):
        game_a, game_b = 6, 4
        set_a, set_b = 0, 0
        self.assertEqual(
            (0, 0, 1, 0), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

        game_a, game_b = 4, 6
        set_a, set_b = 0, 0
        self.assertEqual(
            (0, 0, 0, 1), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

        game_a, game_b = 7, 6
        set_a, set_b = 0, 0
        self.assertEqual(
            (0, 0, 1, 0), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

        game_a, game_b = 6, 7
        set_a, set_b = 0, 0
        self.assertEqual(
            (0, 0, 0, 1), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

        game_a, game_b = 6, 5
        set_a, set_b = 0, 0
        self.assertEqual(
            (6, 5, 0, 0), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

        game_a, game_b = 5, 6
        set_a, set_b = 0, 0
        self.assertEqual(
            (5, 6, 0, 0), self.score.convert_set(game_a, game_b, set_a, set_b)
        )

    def test_convert_score(
        self,
    ):  # score計算にエラーがないかテスト total_gameの変化が含まれていてステートレスになっていない
        # ゲームに変化がない場合
        g = [0, 0]
        s = [0, 0]
        for i in range(0, 1):
            s[0] = i
            for j in range(0, 1):
                s[1] = j
                for k in range(0, 6):
                    g[0] = k
                    for l in range(0, 6):
                        g[1] = l

                        ps = [
                            [0, 0],
                            [1, 0],
                            [2, 0],
                            [3, 0],
                            [0, 1],
                            [1, 1],
                            [2, 1],
                            [3, 1],  # ,[4,0],[4,1]
                            [0, 2],
                            [1, 2],
                            [2, 2],
                            [3, 2],
                            [0, 3],
                            [1, 3],
                            [2, 3],
                            [3, 3],  # ,[4,2] Ad
                            [4, 3],
                            [4, 4],
                            [5, 4],
                            [5, 5],
                            [6, 5],
                            [6, 6],
                            [7, 6],
                            [7, 7],
                        ]
                        # g_temp=g
                        for m, p in enumerate(ps):
                            correct_score = [
                                ["0", "0"],
                                ["15", "0"],
                                ["30", "0"],
                                ["40", "0"],
                                ["0", "15"],
                                ["15", "15"],
                                ["30", "15"],
                                ["40", "15"],  # ,['0','0'],['0','0']
                                ["0", "30"],
                                ["15", "30"],
                                ["30", "30"],
                                ["40", "30"],
                                ["0", "40"],
                                ["15", "40"],
                                ["30", "40"],
                                ["40", "40"],  # ,['0','0'],['0','0']
                                ["Ad", "40"],
                                ["40", "40"],
                                ["Ad", "40"],
                                ["40", "40"],
                                ["Ad", "40"],
                                ["40", "40"],
                                ["Ad", "40"],
                                ["40", "40"],
                            ]
                            (
                                scoreA,
                                scoreB,
                                gamePointA,
                                gamePointB,
                                gameA,
                                gameB,
                                setA,
                                setB,
                            ) = self.score.convert_score(
                                p[0], p[1], g[0], g[1], s[0], s[1]
                            )
                            self.assertEqual([scoreA, scoreB], correct_score[m])
                            self.assertEqual([gamePointA, gamePointB], p)
                            self.assertEqual([gameA, gameB], g)
                            self.assertEqual([setA, setB], s)
        # ゲームに変化がある場合
        for i in range(0, 1):
            s[0] = i
            for j in range(0, 1):
                s[1] = j
                for k in range(0, 5):
                    g[0] = k
                    for l in range(0, 5):
                        g[1] = l

                        ps = [
                            [4, 0],
                            [4, 1],
                            [4, 2],
                            [5, 3],
                            [6, 4],
                            [7, 5],
                            [9, 7],
                            [10, 8],
                            [11, 9],
                            [12, 10],
                        ]
                        for m, p in enumerate(ps):
                            (
                                scoreA,
                                scoreB,
                                gamePointA,
                                gamePointB,
                                gameA,
                                gameB,
                                setA,
                                setB,
                            ) = self.score.convert_score(
                                p[0], p[1], g[0], g[1], s[0], s[1]
                            )
                            self.assertEqual([scoreA, scoreB], ["0", "0"])
                            self.assertEqual([gamePointA, gamePointB], [0, 0])
                            self.assertEqual([gameA, gameB], [g[0] + 1, g[1]])
                            self.assertEqual([setA, setB], s)

                        ps = [
                            [0, 4],
                            [1, 4],
                            [2, 4],
                            [3, 5],
                            [4, 6],
                            [5, 7],
                            [7, 9],
                            [8, 10],
                            [9, 11],
                            [10, 12],
                        ]
                        for m, p in enumerate(ps):
                            (
                                scoreA,
                                scoreB,
                                gamePointA,
                                gamePointB,
                                gameA,
                                gameB,
                                setA,
                                setB,
                            ) = self.score.convert_score(
                                p[0], p[1], g[0], g[1], s[0], s[1]
                            )
                            self.assertEqual([scoreA, scoreB], ["0", "0"])
                            self.assertEqual([gamePointA, gamePointB], [0, 0])
                            self.assertEqual([gameA, gameB], [g[0], g[1] + 1])
                            self.assertEqual([setA, setB], s)
        # セットに変化がある場合
        for k in range(0, 1):
            s[0] = k
            for l in range(0, 1):
                s[1] = l

                gs = [[5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [6, 5]]
                p = [4, 0]
                for m, g in enumerate(gs):
                    (
                        scoreA,
                        scoreB,
                        gamePointA,
                        gamePointB,
                        gameA,
                        gameB,
                        setA,
                        setB,
                    ) = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                    self.assertEqual([scoreA, scoreB], ["0", "0"])
                    self.assertEqual([gamePointA, gamePointB], [0, 0])
                    self.assertEqual([gameA, gameB], [0, 0])
                    self.assertEqual([setA, setB], [s[0] + 1, s[1]])

                gs = [[0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 6]]
                p = [0, 4]
                for m, g in enumerate(gs):
                    (
                        scoreA,
                        scoreB,
                        gamePointA,
                        gamePointB,
                        gameA,
                        gameB,
                        setA,
                        setB,
                    ) = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                    self.assertEqual([scoreA, scoreB], ["0", "0"])
                    self.assertEqual([gamePointA, gamePointB], [0, 0])
                    self.assertEqual([gameA, gameB], [0, 0])
                    self.assertEqual([setA, setB], [s[0], s[1] + 1])

    def test_devide_left_right(self):
        text_score = "15-30"
        l, r = self.score.divide_left_right(text_score)
        self.assertEqual("15", l)
        self.assertEqual("30", r)

        text_score = ""
        l, r = self.score.divide_left_right(text_score)
        self.assertEqual("", l)
        self.assertEqual("", r)

    def test_get_winner(self):
        winner = self.score.get_winner(0, 0, 0, 0)
        self.assertEqual(2, winner)
        winner = self.score.get_winner(0, 1, 0, 0)
        self.assertEqual(0, winner)

    def test_get_winner_list(self):
        array_score = [
            "0-0",
            "0-15",
            "0-15",
            "15-15",
            "15-30",
            "15-40",
            "30-40",
            "40-40",
            "40-A",
            "40-40",
        ]
        winner_array = self.score.get_winner_list(array_score)
        self.assertEqual([1, 2, 0, 1, 1, 0, 0, 1, 0, 3], winner_array)

        array_score = [
            "0-0",
            "0-15",
            "0-15",
            "",
            "15-15",
            "15-30",
            "15-40",
            "30-40",
            "40-40",
            "40-A",
            "40-40",
        ]
        winner_array = self.score.get_winner_list(array_score)
        self.assertEqual([1, 2, 3, 0, 1, 1, 0, 0, 1, 0, 3], winner_array)

        array_score = [
            "0-0",
            "0-15",
            "0-15",
            "",
            "",
            "15-15",
            "15-30",
            "15-40",
            "30-40",
            "40-40",
            "40-A",
            "40-40",
        ]
        winner_array = self.score.get_winner_list(array_score)
        self.assertEqual([1, 2, 3, 3, 0, 1, 1, 0, 0, 1, 0, 3], winner_array)

        array_score = [
            "0-0",
            "0-15",
            "0-15",
            "",
            "",
            "0-15",
            "15-15",
            "15-30",
            "15-40",
            "30-40",
            "40-40",
            "40-A",
            "40-40",
        ]
        winner_array = self.score.get_winner_list(array_score)
        self.assertEqual([1, 2, 3, 3, 2, 0, 1, 1, 0, 0, 1, 0, 3], winner_array)

    def test_score2count(self):
        score = "0"
        self.assertEqual(0, self.score.score2count(score))
        score = "15"
        self.assertEqual(1, self.score.score2count(score))
        score = "30"
        self.assertEqual(2, self.score.score2count(score))
        score = "40"
        self.assertEqual(3, self.score.score2count(score))
        score = "A"
        self.assertEqual(4, self.score.score2count(score))
        score = "fasdf"
        self.assertEqual(-1, self.score.score2count(score))

    def test_winner2player_fault(self):
        player_name = ["a", "b"]
        winner_array = [0, 1, 1, 2, 2, 3, 0, 2]
        point_pattern = ["", "", "", "", "", "", "", ""]
        (
            point_winner_array,
            first_second_array,
            point_pattern,
        ) = self.score.winner2player_fault(winner_array, player_name, point_pattern)
        self.assertEqual(["a", "b", "b", "", "", "", "a", ""], point_winner_array)
        self.assertEqual(
            [1, 1, 1, 1, 2, 0, 1, 1], first_second_array
        )  # 0:not point 1:1st 2:2nd
        self.assertEqual(
            ["", "", "", const.PATTERN[6], const.PATTERN[7], "", "", const.PATTERN[6]],
            point_pattern,
        )  # 0:not point 1:1st 2:2nd

    def test_position_data2array(self):
        # test when add num=2 data to array
        self.score.playerName = ["A", "B"]
        self.score.firstServer = 0
        self.score.totalGame = 1

        self.score.array_ball_position_shot = [[], [], [], []]
        self.score.arrayPlayerAPosition = [[], [], [], []]
        self.score.arrayPlayerBPosition = [[], [], [], []]
        self.score.arrayHitPlayer = [[], [], [], []]
        self.score.arrayBounceHit = [[], [], [], []]
        self.score.arrayForeBack = [[], [], [], []]
        self.score.arrayDirection = [[], [], [], []]
        self.score.array_x1 = [[], [], [], []]
        self.score.array_y1 = [[], [], [], []]
        self.score.array_x2 = [[], [], [], []]
        self.score.array_y2 = [[], [], [], []]
        self.score.array_x3 = [[], [], [], []]
        self.score.array_y3 = [[], [], [], []]
        self.score.array_x4 = [[], [], [], []]
        self.score.array_y4 = [[], [], [], []]

        num = 2
        self.score.number = num
        pos_seek = 100
        xball = 10
        yball = 20
        x1, y1, x2, y2, x3, y3, x4, y4 = 0, 1, 2, 3, 4, 5, 6, 7
        self.score.position_data2array(
            xball,
            yball,
            3,
            4,
            5,
            6,
            0,
            "Hit",
            "Fore",
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            pos_seek,
        )
        self.assertEqual(
            [[], [], [[num, pos_seek, xball, yball]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], ["B"], []], self.score.arrayHitPlayer)
        self.assertEqual([[], [], [0], []], self.score.array_x1)
        self.assertEqual([[], [], [7], []], self.score.array_y4)

    def test_position_data2array_fix(self):
        #
        self.score.playerName = ["A", "B"]
        self.score.firstServer = 0
        self.score.totalGame = 1

        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2], []]
        self.score.array_y1 = [[], [], [3, 4], []]
        self.score.array_x2 = [[], [], [5, 6], []]
        self.score.array_y2 = [[], [], [7, 8], []]
        self.score.array_x3 = [[], [], [9, 10], []]
        self.score.array_y3 = [[], [], [11, 12], []]
        self.score.array_x4 = [[], [], [13, 14], []]
        self.score.array_y4 = [[], [], [15, 16], []]

        num = 2
        self.score.number = num
        rally = 2
        self.score.rally = rally
        pos_seek = 100
        xball = 10
        yball = 20
        x1, y1, x2, y2, x3, y3, x4, y4 = 0, 1, 2, 3, 4, 5, 6, 7
        self.score.position_data2array_fix(
            xball,
            yball,
            3,
            4,
            5,
            6,
            0,
            "Hit",
            "Fore",
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            pos_seek,
        )
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [rally, pos_seek, xball, yball]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], ["A", "B"], []], self.score.arrayHitPlayer)
        self.assertEqual([[], [], [1, 0], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 7], []], self.score.array_y4)

    def test_delete_position_data(self):
        # delete middle
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3], []]
        self.score.array_y1 = [[], [], [3, 4, 5], []]
        self.score.array_x2 = [[], [], [5, 6, 7], []]
        self.score.array_y2 = [[], [], [7, 8, 9], []]
        self.score.array_x3 = [[], [], [9, 10, 11], []]
        self.score.array_y3 = [[], [], [11, 12, 13], []]
        self.score.array_x4 = [[], [], [13, 14, 15], []]
        self.score.array_y4 = [[], [], [15, 16, 17], []]
        num = 2
        self.score.number = num
        i = 1
        self.score.delete_position_data(i)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 101, 5, 6]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual(
            [[], [], [[1, 11, 11, 12], [2, 101, 15, 16]], []],
            self.score.arrayPlayerAPosition,
        )
        self.assertEqual([[], [], [1, 3], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 17], []], self.score.array_y4)

        # delete last
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3], []]
        self.score.array_y1 = [[], [], [3, 4, 5], []]
        self.score.array_x2 = [[], [], [5, 6, 7], []]
        self.score.array_y2 = [[], [], [7, 8, 9], []]
        self.score.array_x3 = [[], [], [9, 10, 11], []]
        self.score.array_y3 = [[], [], [11, 12, 13], []]
        self.score.array_x4 = [[], [], [13, 14, 15], []]
        self.score.array_y4 = [[], [], [15, 16, 17], []]
        num = 2
        self.score.number = num
        i = 2
        self.score.delete_position_data(i)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 51, 3, 4]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual(
            [[], [], [[1, 11, 11, 12], [2, 51, 13, 14]], []],
            self.score.arrayPlayerAPosition,
        )
        self.assertEqual([[], [], [1, 2], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 16], []], self.score.array_y4)

        # delete first
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3], []]
        self.score.array_y1 = [[], [], [3, 4, 5], []]
        self.score.array_x2 = [[], [], [5, 6, 7], []]
        self.score.array_y2 = [[], [], [7, 8, 9], []]
        self.score.array_x3 = [[], [], [9, 10, 11], []]
        self.score.array_y3 = [[], [], [11, 12, 13], []]
        self.score.array_x4 = [[], [], [13, 14, 15], []]
        self.score.array_y4 = [[], [], [15, 16, 17], []]
        num = 2
        self.score.number = num
        i = 0
        self.score.delete_position_data(i)
        self.assertEqual(
            [[], [], [[1, 51, 3, 4], [2, 101, 5, 6]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual(
            [[], [], [[1, 51, 13, 14], [2, 101, 15, 16]], []],
            self.score.arrayPlayerAPosition,
        )
        self.assertEqual([[], [], [2, 3], []], self.score.array_x1)
        self.assertEqual([[], [], [16, 17], []], self.score.array_y4)

    def test_delete_point_shift(self):
        # middle
        print("test_delete_point_shift")
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        num = 2
        self.score.number = num
        start_shot = 1
        end_shot = 2
        self.score.delete_tree_shot_shift(start_shot, end_shot)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 201, 7, 8]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], [1, 4], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 18], []], self.score.array_y4)

        # all
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        num = 2
        self.score.number = num
        start_shot = 0
        end_shot = 3
        self.score.delete_tree_shot_shift(start_shot, end_shot)
        self.assertEqual([[], [], [], []], self.score.array_ball_position_shot)
        self.assertEqual([[], [], [], []], self.score.array_x1)
        self.assertEqual([[], [], [], []], self.score.array_y4)

        # last2
        print("test_delete_point_shift")
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        num = 2
        self.score.number = num
        start_shot = 2
        end_shot = 3
        self.score.delete_tree_shot_shift(start_shot, end_shot)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 51, 3, 4]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], [1, 2], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 16], []], self.score.array_y4)

        # last1
        print("test_delete_point_shift")
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        num = 2
        self.score.number = num
        start_shot = 3
        end_shot = 3
        self.score.delete_tree_shot_shift(start_shot, end_shot)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], [1, 2, 3], []], self.score.array_x1)
        self.assertEqual([[], [], [15, 16, 17], []], self.score.array_y4)

        # 1st1
        print("test_delete_point_shift")
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        num = 2
        self.score.number = num
        start_shot = 0
        end_shot = 0
        self.score.delete_tree_shot_shift(start_shot, end_shot)
        self.assertEqual(
            [[], [], [[1, 51, 3, 4], [2, 101, 5, 6], [3, 201, 7, 8]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[], [], [2, 3, 4], []], self.score.array_x1)
        self.assertEqual([[], [], [16, 17, 18], []], self.score.array_y4)

    def test_divide_track_data(self):
        self.score.array_ball_position_shot = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayHitPlayer = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayBounceHit = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayForeBack = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayDirection = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.arrayBounceHit = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]  # num12
        self.score.array_x1 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_y1 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_x2 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_y2 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_x3 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_y3 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_x4 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12
        self.score.array_y4 = [[], [], [], [], [], [], [], [], [], [], [], []]  # num12

        start_frame = [0, 40, 70, 120, 1000]
        track_frame = [15, 20, 30, 50, 100, 115, 120, 130, 150, 200]
        bx = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        by = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
        xa = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        ya = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
        xb = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        yb = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
        x1 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y1 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        x2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        x3 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y3 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        x4 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y4 = [81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
        hit_bounce = [
            "Front_Hit",
            "Front_Bounce",
            "Back_Hit",
            "Back_Bounce",
            "Front_Hit",
            "Front_Bounce",
            "Back_Hit",
            "Back_Bounce",
            "Front_Hit",
            "Front_Bounce",
        ]
        self.score.divide_track_data(
            start_frame,
            track_frame,
            bx,
            by,
            xa,
            ya,
            xb,
            yb,
            hit_bounce,
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
        )
        # print(self.score.array_ball_position_shot)
        self.assertEqual(
            [
                [[0, 15, 1.0, 11.0], [0, 20, 2.0, 12.0], [0, 30, 3.0, 13.0]],
                [[1, 50, 4.0, 14.0]],
                [[2, 100, 5.0, 15.0], [2, 115, 6.0, 16.0]],
                [
                    [3, 120, 7.0, 17.0],
                    [3, 130, 8.0, 18.0],
                    [3, 150, 9.0, 19.0],
                    [3, 200, 10.0, 20.0],
                ],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
            self.score.array_ball_position_shot,
        )
        self.assertEqual(
            [
                [[0, 15, 1.0, 11.0], [0, 20, 2.0, 12.0], [0, 30, 3.0, 13.0]],
                [[1, 50, 4.0, 14.0]],
                [[2, 100, 5.0, 15.0], [2, 115, 6.0, 16.0]],
                [
                    [3, 120, 7.0, 17.0],
                    [3, 130, 8.0, 18.0],
                    [3, 150, 9.0, 19.0],
                    [3, 200, 10.0, 20.0],
                ],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
            self.score.arrayPlayerAPosition,
        )
        self.assertEqual(
            [
                ["Hit", "Bounce", "Hit"],
                ["Bounce"],
                ["Hit", "Bounce"],
                ["Hit", "Bounce", "Hit", "Bounce"],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
            self.score.arrayBounceHit,
        )
        self.assertEqual(
            [
                [11, 12, 13],
                [14],
                [15, 16],
                [17, 18, 19, 20],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
            self.score.array_x1,
        )
        self.assertEqual(
            [
                [81, 82, 83],
                [84],
                [85, 86],
                [87, 88, 89, 90],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
            self.score.array_y4,
        )

    def test_delete_after_end(self):
        self.score.array_ball_position_shot = [
            [],
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], [], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [[], [], ["Bounce", "Hit", "Bounce", "Hit"], []]
        self.score.arrayForeBack = [[], [], ["Fore", "Back", "Back", "Back"], []]
        self.score.arrayDirection = [[], [], ["Cross", "Cross", "Cross", "Cross"], []]
        self.score.array_x1 = [[], [], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [], [15, 16, 17, 18], []]
        self.score.number = 2
        end = 100
        self.score.delete_after_end(self.score.number, end)
        self.assertEqual(
            [[], [], [[1, 11, 1, 2], [2, 51, 3, 4]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual(
            [[], [], [[1, 11, 11, 12], [2, 51, 13, 14]], []],
            self.score.arrayPlayerAPosition,
        )

    def test_delete_tree_point(self):
        self.score.array_frame_start = [100, 200, 300, 400]
        self.score.array_frame_end = [100, 200, 300, 400]
        self.score.arraySet = [100, 200, 300, 400]
        self.score.arrayGame = [100, 200, 300, 400]
        self.score.arrayScore = [100, 200, 300, 400]
        self.score.arrayScoreResult = [100, 200, 300, 400]
        self.score.arrayFirstSecond = [100, 200, 300, 400]
        self.score.arrayServer = [100, 200, 300, 400]
        self.score.arrayPointWinner = [100, 200, 300, 400]

        self.score.pointWin[0] = [0, 1, 1, 2]
        self.score.pointWin[1] = [0, 1, 1, 2]

        self.score.arrayPointPattern = [100, 200, 300, 400]
        self.score.arrayFault = [0, 0, 1, 0]

        # "Court1X": list(np.array(self.arrayCourt)[0][:, 0]),#[[0, 0], [0, 0], [0, 0], [0, 0],[0, 0], [0, 0], [0, 0], [0, 0]]
        ##[[0, 0],[0, 0],[0, 0]]

        self.score.arrayContactServe = [[0, 0], [1, 1], [2, 2], [3, 3]]

        self.score.arrayCourt = [
            [[0, 0], [1, 1], [2, 2], [3, 3]],
            [[10, 0], [11, 11], [12, 12], [13, 13]],
            [[20, 20], [21, 21], [22, 22], [23, 23]],
            [[30, 30], [31, 31], [32, 32], [33, 33]],
        ]

        self.score.array_ball_position_shot = [
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4]],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14]],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24]],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], ["A", "A"], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [
            [],
            ["Bounce", "Hit"],
            ["Bounce", "Hit", "Bounce", "Hit"],
            [],
        ]
        self.score.arrayForeBack = [
            [],
            ["Fore", "Back"],
            ["Fore", "Back", "Back", "Back"],
            [],
        ]
        self.score.arrayDirection = [
            [],
            ["Cross", "Cross"],
            ["Cross", "Cross", "Cross", "Cross"],
            [],
        ]
        self.score.array_x1 = [[], [1, 2], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [3, 4], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [5, 6], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [7, 8], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [9, 10], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [11, 12], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [13, 14], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [15, 16], [15, 16, 17, 18], []]

        self.score.number = 1  # delete 1th row

        self.score.delete_tree_point()
        self.assertEqual([100, 300, 400], self.score.array_frame_start)
        self.assertEqual([0, 1, 2], self.score.pointWin[0])
        self.assertEqual([0, 1, 2], self.score.pointWin[1])
        self.assertEqual(
            [[], [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]], []],
            self.score.array_ball_position_shot,
        )
        self.assertEqual([[0, 0], [2, 2], [3, 3]], self.score.arrayContactServe)
        self.assertEqual(
            [
                [[0, 0], [2, 2], [3, 3]],
                [[10, 0], [12, 12], [13, 13]],
                [[20, 20], [22, 22], [23, 23]],
                [[30, 30], [32, 32], [33, 33]],
            ],
            self.score.arrayCourt,
        )

    def test_position_data2array_insert(self):
        self.score.array_ball_position_shot = [
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4]],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [[1, 11, 11, 12], [2, 51, 13, 14]],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 717, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [[1, 11, 21, 22], [2, 51, 23, 24]],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 717, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [[], ["A", "A"], ["A", "A", "B", "A"], []]
        self.score.arrayBounceHit = [
            [],
            ["Bounce", "Hit"],
            ["Bounce", "Hit", "Bounce", "Hit"],
            [],
        ]
        self.score.arrayForeBack = [
            [],
            ["Fore", "Back"],
            ["Fore", "Back", "Back", "Back"],
            [],
        ]
        self.score.arrayDirection = [
            [],
            ["Cross", "Cross"],
            ["Cross", "Cross", "Cross", "Cross"],
            [],
        ]
        self.score.array_x1 = [[], [1, 2], [1, 2, 3, 4], []]
        self.score.array_y1 = [[], [3, 4], [3, 4, 5, 6], []]
        self.score.array_x2 = [[], [5, 6], [5, 6, 7, 8], []]
        self.score.array_y2 = [[], [7, 8], [7, 8, 9, 10], []]
        self.score.array_x3 = [[], [9, 10], [9, 10, 11, 12], []]
        self.score.array_y3 = [[], [11, 12], [11, 12, 13, 14], []]
        self.score.array_x4 = [[], [13, 14], [13, 14, 15, 16], []]
        self.score.array_y4 = [[], [15, 16], [15, 16, 17, 18], []]
        self.score.number = 2
        pos_seek = 100
        xball = 10
        yball = 20
        x1, y1, x2, y2, x3, y3, x4, y4 = 0, 1, 2, 3, 4, 5, 6, 7
        self.score.position_data2array_insert(
            xball,
            yball,
            3,
            4,
            5,
            6,
            0,
            "Hit",
            "Fore",
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            pos_seek,
        )
        self.assertEqual(
            self.score.array_ball_position_shot,
            [
                [],
                [[1, 11, 1, 2], [2, 51, 3, 4]],
                [
                    [1, 11, 1, 2],
                    [2, 51, 3, 4],
                    [3, 100, 10, 20],
                    [4, 101, 5, 6],
                    [5, 201, 7, 8],
                ],
                [],
            ],
        )

    def test_convert_bally2playery(self):
        self.score.array_ball_position_shot = [
            [],
            [[1, 11, 1, 2], [2, 51, 3, 4]],
            [[1, 11, 1, 2], [2, 51, 3, 4], [3, 101, 5, 6], [4, 201, 7, 8]],
            [],
        ]
        self.score.arrayPlayerAPosition = [
            [],
            [[1, 11, 11, 12], [2, 51, 313, 14]],
            [[1, 11, 11, 12], [2, 51, 13, 14], [3, 101, 15, 16], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayPlayerBPosition = [
            [],
            [[1, 11, 21, 22], [2, 51, 323, 24]],
            [[1, 11, 21, 22], [2, 51, 23, 24], [3, 101, 25, 26], [4, 201, 17, 18]],
            [],
        ]
        self.score.arrayHitPlayer = [
            [],
            ["Up", "Down"],
            ["Up", "Down", "Up", "Down"],
            [],
        ]
        self.score.convert_bally2playery()
        self.assertEqual(
            [
                [],
                [[1, 11, 1, 12], [2, 51, 3, 24]],
                [[1, 11, 1, 12], [2, 51, 3, 24], [3, 101, 5, 16], [4, 201, 7, 18]],
                [],
            ],
            self.score.array_ball_position_shot,
        )
