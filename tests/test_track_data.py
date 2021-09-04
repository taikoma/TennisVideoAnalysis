import unittest

# import pandas as pd
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.score as score
import src.track_data as track_data


class TestTrackData(unittest.TestCase):
    def setUp(self):
        # print("setup")
        self.track_data = track_data.TrackData()
        self.score = score.Score(0)

    def test_load_ball_data(self):
        filename = "./data/ball-pos.csv"
        self.track_data.load_ball_data(filename)
        self.assertEqual(
            [5, 819, 448],
            [
                self.track_data.frame_array[0],
                self.track_data.all_track_ball_x[0],
                self.track_data.all_track_ball_y[0],
            ],
        )

    def test_df2data(self):
        frame = [100, 200, 300, 400, 500]
        x_ball = [np.NaN] * 5
        y_ball = [np.NaN] * 5
        x_a = [""] * 5
        y_a = [""] * 5
        x_b = [""] * 5
        y_b = [""] * 5
        hb = [""] * 5
        x1, y1, x2, y2, x3, y3, x4, y4 = (
            [""] * 5,
            [""] * 5,
            [""] * 5,
            [""] * 5,
            [""] * 5,
            [""] * 5,
            [""] * 5,
            [""] * 5,
        )
        df = pd.DataFrame(
            {
                "Frame": frame,
                "X_Ball_onC": x_ball,
                "Y_Ball_onC": y_ball,
                "X_A_onC": x_a,
                "Y_A_onC": y_a,
                "X_B_onC": x_b,
                "Y_B_onC": y_b,
                "HitBounce": hb,
                "X1": x1,
                "Y1": y1,
                "X2": x2,
                "Y2": y2,
                "X3": x3,
                "Y3": y3,
                "X4": x4,
                "Y4": y4,
            }
        )
        self.track_data.df2data(df)
        self.assertEqual(
            len(self.track_data.track_frame_array), len(self.track_data.track_x1)
        )

    @unittest.skip("test")
    def test_load_track_data(self):
        filename = "./data/track-data.csv"
        self.track_data.load_track_data(filename)
        self.assertEqual(1.46, self.track_data.track_ball_x[0])

    def test_load_track_to_score(self):
        start_track = [0, 15, 450, 1000]
        self.score.array_frame_start = start_track
        self.score.array_ball_position_shot = [[], [], [], []]
        self.score.arrayPlayerAPosition = [[], [], [], []]
        self.score.arrayPlayerBPosition = [[], [], [], []]
        self.score.arrayHitPlayer = [[], [], [], []]
        self.score.arrayBounceHit = [[], [], [], []]
        self.score.arrayForeBack = [[], [], [], []]
        self.score.arrayDirection = [[], [], [], []]
        self.score.arrayBounceHit = [[], [], [], []]
        self.score.array_x1 = [[], [], [], []]
        self.score.array_y1 = [[], [], [], []]
        self.score.array_x2 = [[], [], [], []]
        self.score.array_y2 = [[], [], [], []]
        self.score.array_x3 = [[], [], [], []]
        self.score.array_y3 = [[], [], [], []]
        self.score.array_x4 = [[], [], [], []]
        self.score.array_y4 = [[], [], [], []]

        frame = [100, 200, 300, 400, 500]
        x_ball = [np.NaN] * 5
        y_ball = [np.NaN] * 5
        x_a = [""] * 5
        y_a = [""] * 5
        x_b = [""] * 5
        y_b = [""] * 5
        hb = [""] * 5
        x1 = [1, 2, 3, 4, 5]
        y1 = [1, 2, 3, 4, 5]
        x2 = [1, 2, 3, 4, 5]
        y2 = [1, 2, 3, 4, 5]
        x3 = [1, 2, 3, 4, 5]
        y3 = [1, 2, 3, 4, 5]
        x4 = [1, 2, 3, 4, 5]
        y4 = [1, 2, 3, 4, 5]
        # x1,y1,x2,y2,x3,y3,x4,y4=[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5
        df = pd.DataFrame(
            {
                "Frame": frame,
                "X_Ball_onC": x_ball,
                "Y_Ball_onC": y_ball,
                "X_A_onC": x_a,
                "Y_A_onC": y_a,
                "X_B_onC": x_b,
                "Y_B_onC": y_b,
                "HitBounce": hb,
                "X1": x1,
                "Y1": y1,
                "X2": x2,
                "Y2": y2,
                "X3": x3,
                "Y3": y3,
                "X4": x4,
                "Y4": y4,
            }
        )
        self.track_data.df2data(df)  # df->track_data

        self.track_data.load_track_to_score(self.score)  # track_data->score
        self.assertEqual([[], [1, 2, 3, 4], [5], []], self.score.array_x1)

    def test_detect_front_hit_frame(self):
        NET_LINE = 340
        THRESH = 30
        frame = np.array([10, 11, 12, 113, 114, 115, 216, 217, 218, 219])
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([540, 550, 540, 610, 620, 610, 740, 750, 740, 730])
        (
            front_hit_array,
            x_front_hit_array,
            y_front_hit_array,
        ) = self.track_data.detect_front_hit_frame(frame, x, y, NET_LINE, THRESH)
        self.assertEqual([11, 114, 217], front_hit_array)
        self.assertEqual([1, 4, 7], x_front_hit_array)
        self.assertEqual([550, 620, 750], y_front_hit_array)

    def test_detect_back_hit_frame(self):
        NET_LINE = 340
        THRESH = 30
        frame = np.array([10, 11, 12, 113, 114, 115, 216, 217, 218, 219])
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([60, 50, 70, 130, 120, 110, 260, 250, 270, 270])
        (
            back_hit_array,
            x_back_hit_array,
            y_back_hit_array,
        ) = self.track_data.detect_back_hit_frame(frame, x, y, NET_LINE, THRESH)
        self.assertEqual([11, 114, 217], back_hit_array)
        self.assertEqual([1, 4, 7], x_back_hit_array)
        self.assertEqual([50, 120, 250], y_back_hit_array)

    def test_detect_front_bounce_frame(self):
        NET_LINE = 340
        THRESH = 30
        frame = np.array([10, 11, 12, 50, 113, 114, 115, 216, 217, 218, 219])
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([540, 550, 540, 570, 610, 620, 610, 740, 750, 740, 730])
        front_hit_array = [11, 114, 217]
        (
            front_bounce_array,
            x_front_bounce_array,
            y_front_bounce_array,
        ) = self.track_data.detect_front_bounce_frame(
            frame, x, y, NET_LINE, THRESH, front_hit_array
        )
        print(front_bounce_array)
        self.assertEqual(
            [10, 11, 12, 113, 114, 115, 216, 217, 218, 219], front_bounce_array
        )
        self.assertEqual([0, 1, 2, 4, 5, 6, 7, 8, 9, 10], x_front_bounce_array)
        self.assertEqual(
            [540, 550, 540, 610, 620, 610, 740, 750, 740, 730], y_front_bounce_array
        )

    def test_detect_back_bounce_frame(self):
        NET_LINE = 340
        THRESH = 30
        frame = np.array([10, 11, 12, 113, 114, 115, 216, 217, 218, 219])
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([60, 50, 70, 130, 120, 110, 260, 250, 270, 270])
        back_hit_array = [11, 114, 217]
        (
            back_bounce_array,
            x_back_bounce_array,
            y_back_bounce_array,
        ) = self.track_data.detect_back_bounce_frame(
            frame, x, y, NET_LINE, THRESH, back_hit_array
        )
        print(back_bounce_array)
        self.assertEqual(
            [10, 11, 12, 113, 114, 115, 216, 217, 218, 219], back_bounce_array
        )
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], x_back_bounce_array)
        self.assertEqual(
            [60, 50, 70, 130, 120, 110, 260, 250, 270, 270], y_back_bounce_array
        )

    def test_delete_overlap_ball_pos_df(self):
        frame = np.array([10, 11, 11, 11, 114, 115, 216, 217, 218, 219])
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([60, 50, 70, 130, 120, 110, 260, 250, 270, 270])
        df = pd.DataFrame(
            {
                "Frame": frame,
                "X": x,
                "Y": y,
            }
        )
        df = self.track_data.delete_overlap_ball_pos_df(df)
        self.assertEqual(
            [10, 11, 114, 115, 216, 217, 218, 219],
            df["Frame"].astype(np.int64).values.tolist(),
        )
