import tkinter
import cv2
from PIL import Image, ImageTk
import numpy as np
import sqlite3
import pandas as pd
from tkinter import ttk
from tkinter import Menu
import tkinter.messagebox
import csv
import threading
from tkinter import filedialog

import const


class Database:
    def __init__(self, dbName, score):
        self.dbName = dbName
        self.score = score

        self.patternString = const.PATTERN
        self.firstSecondString = ["", "1st", "2nd"]

        self.arrayFrameStart = score.array_frame_start
        self.arrayFrameEnd = score.array_frame_end
        self.arraySet = score.arraySet

        self.arrayGame = score.arrayGame

        self.arrayScore = score.arrayScore

        self.arrayScoreResult = score.arrayScoreResult
        self.arrayFirstSecond = score.arrayFirstSecond
        self.arrayServer = score.arrayServer

        self.arrayPointWinner = score.arrayPointWinner
        self.pointWin = score.pointWin
        self.arrayPointPattern = score.arrayPointPattern

        self.arrayContactServe = score.arrayContactServe
        self.arrayCourt = score.arrayCourt  # [[0, 0], [0, 0], [0, 0], [0, 0]]

        self.playerA = score.playerA
        self.playerB = score.playerB

        self.number = score.number
        self.totalGame = score.totalGame
        self.faultFlug = score.faultFlug
        self.arrayFault = score.arrayFault

        self.shot_frame = score.shot_frame
        self.array_ball_position_shot_x = score.array_ball_position_shot_x
        self.array_ball_position_shot_y = score.array_ball_position_shot_y
        self.arrayPlayerAPosition_x = score.arrayPlayerAPosition_x
        self.arrayPlayerAPosition_y = score.arrayPlayerAPosition_y
        self.arrayPlayerBPosition_x = score.arrayPlayerBPosition_x
        self.arrayPlayerBPosition_y = score.arrayPlayerBPosition_y
        self.arrayHitPlayer = score.arrayHitPlayer
        self.arrayBounceHit = score.arrayBounceHit
        self.arrayForeBack = score.arrayForeBack
        self.arrayDirection = score.arrayDirection

        self.array_x1 = score.array_x1
        self.array_y1 = score.array_y1
        self.array_x2 = score.array_x2
        self.array_y2 = score.array_y2
        self.array_x3 = score.array_x3
        self.array_y3 = score.array_y3
        self.array_x4 = score.array_x4
        self.array_y4 = score.array_y4

    def save_temp_db(self):  #
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        df = pd.DataFrame(
            {
                "StartFrame": self.arrayFrameStart,
                "EndFrame": self.arrayFrameEnd,
                "Set": self.arraySet,
                "Game": self.arrayGame,
                "Score": self.arrayScore,
                "ScoreResult": self.arrayScoreResult,
                "FirstSecond": self.arrayFirstSecond,
                "Server": self.arrayServer,
                "PointWinner": self.arrayPointWinner,
                "PointWinA": self.pointWin[0],
                "PointWinB": self.pointWin[1],
                "PointPattern": self.arrayPointPattern,
                "Fault": self.arrayFault,
                "ContactServeX": list(np.array(self.arrayContactServe)[:, 0]),
                "ContactServeY": list(np.array(self.arrayContactServe)[:, 1]),
                "Court1X": list(np.array(self.arrayCourt)[0][:, 0]),
                "Court1Y": list(np.array(self.arrayCourt)[0][:, 1]),
                "Court2X": list(np.array(self.arrayCourt)[1][:, 0]),
                "Court2Y": list(np.array(self.arrayCourt)[1][:, 1]),
                "Court3X": list(np.array(self.arrayCourt)[2][:, 0]),
                "Court3Y": list(np.array(self.arrayCourt)[2][:, 1]),
                "Court4X": list(np.array(self.arrayCourt)[3][:, 0]),
                "Court4Y": list(np.array(self.arrayCourt)[3][:, 1]),
            }
        )
        df.to_sql("score", conn, if_exists="replace")
        conn.close()

    def save_database_score(self, db_name):
        print(self.dbName)
        r = 0
        conn = sqlite3.connect(self.dbName)
        try:
            df = pd.DataFrame(
                {
                    "StartFrame": self.arrayFrameStart,
                    "EndFrame": self.arrayFrameEnd,
                    "Set": self.arraySet,
                    "Game": self.arrayGame,
                    "Score": self.arrayScore,
                    "ScoreResult": self.arrayScoreResult,
                    "FirstSecond": self.arrayFirstSecond,
                    "Server": self.arrayServer,
                    "PointWinner": self.arrayPointWinner,
                    "PointWinA": self.pointWin[0],
                    "PointWinB": self.pointWin[1],
                    "PointPattern": self.arrayPointPattern,
                    "Fault": self.arrayFault,
                    "ContactServeX": list(np.array(self.arrayContactServe)[:, 0]),
                    "ContactServeY": list(np.array(self.arrayContactServe)[:, 1]),
                    "Court1X": list(np.array(self.arrayCourt)[0][:, 0]),
                    "Court1Y": list(np.array(self.arrayCourt)[0][:, 1]),
                    "Court2X": list(np.array(self.arrayCourt)[1][:, 0]),
                    "Court2Y": list(np.array(self.arrayCourt)[1][:, 1]),
                    "Court3X": list(np.array(self.arrayCourt)[2][:, 0]),
                    "Court3Y": list(np.array(self.arrayCourt)[2][:, 1]),
                    "Court4X": list(np.array(self.arrayCourt)[3][:, 0]),
                    "Court4Y": list(np.array(self.arrayCourt)[3][:, 1]),
                }
            )
            r = len(df)
        except ValueError as e:
            print("Error Score", e)
        else:
            try:
                df.to_sql("score", conn, if_exists="replace")
            except pd.io.sql.DatabaseError as e:
                print("Error Score", e)
        finally:
            conn.close()
        return r

    def save_database_shot(self, db_name):  #
        """shotテーブルにshotデータを保存
        array_ball_position_shot:[num,pos_seek,xball,yball]

        """
        r = 0
        conn = sqlite3.connect(self.dbName)

        # point = []
        # frame = []
        # bx = []
        # by = []
        # pax = []
        # pay = []
        # pbx = []
        # pby = []
        # h = []
        # bh = []
        # fb = []
        # d = []
        # x1 = []
        # y1 = []
        # x2 = []
        # y2 = []
        # x3 = []
        # y3 = []
        # x4 = []
        # y4 = []
        # try:
        #     for i in range(len(self.array_ball_position_shot)):
        #         for j in range(len(self.array_ball_position_shot[i])):
        #             # print(i, j)
        #             point.append(self.array_ball_position_shot[i][j][0])#num
        #             frame.append(self.array_ball_position_shot[i][j][1])#pos_seek
        #             bx.append(self.array_ball_position_shot[i][j][2])
        #             by.append(self.array_ball_position_shot[i][j][3])
        #             pax.append(self.arrayPlayerAPosition[i][j][2])
        #             pay.append(self.arrayPlayerAPosition[i][j][3])
        #             pbx.append(self.arrayPlayerBPosition[i][j][2])
        #             pby.append(self.arrayPlayerBPosition[i][j][3])
        #             h.append(self.arrayHitPlayer[i][j])
        #             bh.append(self.arrayBounceHit[i][j])
        #             fb.append(self.arrayForeBack[i][j])  # arrayDirection
        #             d.append(self.arrayDirection[i][j])
        #             x1.append(self.array_x1[i][j])
        #             y1.append(self.array_y1[i][j])
        #             x2.append(self.array_x2[i][j])
        #             y2.append(self.array_y2[i][j])
        #             x3.append(self.array_x3[i][j])
        #             y3.append(self.array_y3[i][j])
        #             x4.append(self.array_x4[i][j])
        #             y4.append(self.array_y4[i][j])

        # except IndexError as e:
        #     print("Error Shot", e)
        print(self.shot_frame)
        try:
            if len(self.shot_frame) > 0:
                df_shot = pd.DataFrame(
                    {
                        "point": self.shot_frame,
                        "frame": self.shot_frame,
                        "ballx": self.array_ball_position_shot_x,
                        "bally": self.array_ball_position_shot_y,
                        "playerAx": self.arrayPlayerAPosition_x,
                        "playerAy": self.arrayPlayerAPosition_y,
                        "playerBx": self.arrayPlayerBPosition_x,
                        "playerBy": self.arrayPlayerBPosition_y,
                        "hitplayer": self.arrayHitPlayer,
                        "bouncehit": self.arrayBounceHit,
                        "foreback": self.arrayForeBack,
                        "direction": self.arrayDirection,
                        "x1": self.array_x1,
                        "y1": self.array_y1,
                        "x2": self.array_x2,
                        "y2": self.array_y2,
                        "x3": self.array_x3,
                        "y3": self.array_y3,
                        "x4": self.array_x4,
                        "y4": self.array_y4,
                    }
                )
            else:
                df_shot = pd.DataFrame(
                    {
                        "point": [],
                        "frame": [],
                        "ballx": [],
                        "bally": [],
                        "playerAx": [],
                        "playerAy": [],
                        "playerBx": [],
                        "playerBy": [],
                        "hitplayer": [],
                        "bouncehit": [],
                        "foreback": [],
                        "direction": [],
                        "x1": [],
                        "y1": [],
                        "x2": [],
                        "y2": [],
                        "x3": [],
                        "y3": [],
                        "x4": [],
                        "y4": [],
                    }
                )
        except ValueError as e:
            print("Error Shot", e)
        else:
            df_shot.to_sql("shot", conn, if_exists="replace")
            r = len(df_shot)
            df_shot.to_csv("test.csv")
        finally:
            conn.close()
        return r

    def save_database_basic(self, db_name):
        r = 0
        conn = sqlite3.connect(self.dbName)
        try:
            df_basic = pd.DataFrame(
                {
                    "playerA": self.playerA,
                    "playerB": self.playerB,
                    "number": self.number,
                    "totalGame": self.totalGame,
                    "faultFlug": self.faultFlug,
                },
                index=[0],
            )
        except ValueError as e:
            print("Error Basic", e)
        else:
            df_basic.to_sql("match", conn, if_exists="replace")
            r = len(df_basic)
        finally:
            conn.close()
        return r

    def save_database(self):
        print("saveDatabase", self.dbName)
        self.save_database_score(self.dbName)
        self.save_database_shot(self.dbName)
        self.save_database_basic(self.dbName)

    def clear_array(self):
        self.arrayFrameStart.clear()
        self.arrayFrameEnd.clear()
        self.arraySet.clear()
        self.arrayGame.clear()
        self.arrayScore.clear()
        self.arrayScoreResult.clear()
        self.arrayFirstSecond.clear()
        self.arrayServer.clear()
        self.arrayPointWinner.clear()
        self.arrayPointPattern.clear()
        self.arrayForeBack.clear()
        self.pointWin[0].clear()
        self.pointWin[1].clear()
        self.arrayContactServe.clear()
        self.arrayCourt.clear()
        self.arrayContactServe.clear()
        self.arrayFault.clear()
        self.array_ball_position_shot_x.clear()
        self.array_ball_position_shot_y.clear()
        self.arrayPlayerAPosition_x.clear()
        self.arrayPlayerAPosition_y.clear()
        self.arrayPlayerBPosition_x.clear()
        self.arrayPlayerBPosition_y.clear()
        self.arrayHitPlayer.clear()
        self.arrayBounceHit.clear()
        self.arrayForeBack.clear()
        self.arrayDirection.clear()

        self.array_x1.clear()
        self.array_y1.clear()
        self.array_x2.clear()
        self.array_y2.clear()
        self.array_x3.clear()
        self.array_y3.clear()
        self.array_x4.clear()
        self.array_y4.clear()

    def load_database_score(self, db_name):
        """
        scoreテーブル
        """
        r = 0
        conn = sqlite3.connect(self.dbName)
        try:
            df = pd.read_sql("select * from score", conn)
        except pd.io.sql.DatabaseError as e:
            print(e)
            return 0
        else:
            df = df.fillna("")

            self.arrayFrameStart.extend(df["StartFrame"].values.tolist())
            self.arrayFrameEnd.extend(df["EndFrame"].values.tolist())
            self.arraySet.extend(df["Set"].values.tolist())
            self.arrayGame.extend(df["Game"].values.tolist())
            self.arrayScore.extend(df["Score"].values.tolist())
            self.arrayScoreResult.extend(df["ScoreResult"].values.tolist())
            self.arrayFirstSecond.extend(df["FirstSecond"].values.tolist())
            self.arrayServer.extend(df["Server"].values.tolist())
            self.arrayPointWinner.extend(df["PointWinner"].values.tolist())
            self.arrayPointPattern.extend(df["PointPattern"].values.tolist())
            self.arrayFault.extend(df["Fault"].values.tolist())

            self.pointWin[0].extend(df["PointWinA"].values.tolist())
            self.pointWin[1].extend(df["PointWinB"].values.tolist())

            for i in range(len(df["ContactServeX"].values.tolist())):
                self.arrayContactServe.append(
                    [
                        df["ContactServeX"].values.tolist()[i],
                        df["ContactServeY"].values.tolist()[i],
                    ]
                )
            self.arrayCourt.append([])
            self.arrayCourt.append([])
            self.arrayCourt.append([])
            self.arrayCourt.append([])
            for i in range(len(df["Court1X"].values.tolist())):
                self.arrayCourt[0].insert(
                    i,
                    [
                        df["Court1X"].values.tolist()[i],
                        df["Court1Y"].values.tolist()[i],
                    ],
                )
                self.arrayCourt[1].insert(
                    i,
                    [
                        df["Court2X"].values.tolist()[i],
                        df["Court2Y"].values.tolist()[i],
                    ],
                )
                self.arrayCourt[2].insert(
                    i,
                    [
                        df["Court3X"].values.tolist()[i],
                        df["Court3Y"].values.tolist()[i],
                    ],
                )
                self.arrayCourt[3].insert(
                    i,
                    [
                        df["Court4X"].values.tolist()[i],
                        df["Court4Y"].values.tolist()[i],
                    ],
                )
            self.number = len(df) - 1
        r = len(df)
        conn.close()
        return r

    def load_database_basic(self, db_name):
        r = 0
        conn = sqlite3.connect(db_name)
        # c = conn.cursor()
        # df_basic
        df_basic = pd.read_sql("select * from match", conn)
        self.playerA = df_basic["playerA"].values[0]
        self.playerB = df_basic["playerB"].values[0]
        self.totalGame = df_basic["totalGame"].values[0]
        self.faultFlug = df_basic["faultFlug"].values[0]
        # print(df_basic)
        conn.close()
        r = len(df_basic)
        return r

    def load_database_shot(self, db_name):
        r = 0
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        # df_shot
        df_shot = pd.read_sql("select * from shot", conn)
        # point = df_shot["point"].values.tolist()
        frame = df_shot["frame"].values.tolist()
        ballx = self.df_float2fillna(df_shot["ballx"]).values.tolist()
        bally = self.df_float2fillna(df_shot["bally"]).values.tolist()
        pax = self.df_float2fillna(df_shot["playerAx"]).values.tolist()
        pay = self.df_float2fillna(df_shot["playerAy"]).values.tolist()
        pbx = self.df_float2fillna(df_shot["playerBx"]).values.tolist()
        pby = self.df_float2fillna(df_shot["playerBy"]).values.tolist()

        hit = df_shot["hitplayer"].values.tolist()
        bh = df_shot["bouncehit"].values.tolist()
        fb = df_shot["foreback"].values.tolist()
        d = df_shot["direction"].values.tolist()

        x1 = self.pop_array_from_df(df_shot, "x1")
        y1 = self.pop_array_from_df(df_shot, "y1")
        x2 = self.pop_array_from_df(df_shot, "x2")
        y2 = self.pop_array_from_df(df_shot, "y2")
        x3 = self.pop_array_from_df(df_shot, "x3")
        y3 = self.pop_array_from_df(df_shot, "y3")
        x4 = self.pop_array_from_df(df_shot, "x4")
        y4 = self.pop_array_from_df(df_shot, "y4")

        self.shot_frame.extend(frame)
        self.array_ball_position_shot_x.extend(ballx)
        self.array_ball_position_shot_y.extend(bally)
        self.arrayPlayerAPosition_x.extend(pax)
        self.arrayPlayerAPosition_y.extend(pay)
        self.arrayPlayerBPosition_x.extend(pbx)
        self.arrayPlayerBPosition_y.extend(pby)

        # self.array_ball_position_shot.extend(
        #     self.array2arrays(frame, ballx, bally)
        # )
        # self.arrayPlayerAPosition.extend(self.array2arrays(frame, pax, pax))
        # self.arrayPlayerBPosition.extend(self.array2arrays(frame, pbx, pby))

        # print(x1)

        # (
        #     array_hit,
        #     array_bouncehit,
        #     array_foreback,
        #     array_direction,
        #     array_x1,
        #     array_y1,
        #     array_x2,
        #     array_y2,
        #     array_x3,
        #     array_y3,
        #     array_x4,
        #     array_y4,
        # ) = self.array2arrays2(point, hit, bh, fb, d, x1, y1, x2, y2, x3, y3, x4, y4)

        self.arrayHitPlayer.extend(hit)
        self.arrayBounceHit.extend(bh)
        self.arrayForeBack.extend(fb)
        self.arrayDirection.extend(d)
        self.array_x1.extend(x1)
        self.array_y1.extend(y1)
        self.array_x2.extend(x2)
        self.array_y2.extend(y2)
        self.array_x3.extend(x3)
        self.array_y3.extend(y3)
        self.array_x4.extend(x4)
        self.array_y4.extend(y4)

        if self.number == len(self.shot_frame):  # if last data is none add []
            self.shot_frame.append([])
            self.array_ball_position_shot_x.append([])
            self.array_ball_position_shot_y.append([])
            self.arrayPlayerAPosition_x.append([])
            self.arrayPlayerAPosition_y.append([])
            self.arrayPlayerBPosition_x.append([])
            self.arrayPlayerBPosition_y.append([])
            self.arrayHitPlayer.append([])
            self.arrayBounceHit.append([])
            self.arrayForeBack.append([])
            self.arrayDirection.append([])
            self.array_x1.append([])
            self.array_y1.append([])
            self.array_x2.append([])
            self.array_y2.append([])
            self.array_x3.append([])
            self.array_y3.append([])
            self.array_x4.append([])
            self.array_y4.append([])

        conn.close()
        r = len(df_shot)
        return r

    def pop_array_from_df(self, df, label):
        if label in df.columns.values:
            array = self.df_float2fillna(df[label]).values.tolist()
        else:
            array = [[]] * len(df)
        return array

    def df_float2fillna(self, df):
        """convert nan to str"" because cannot convert str directly ,once convert to num 999

        Parameters
        ----------
        df:pandas dataframe

        Returns
        ----------
        df:pandas dataframe
        """
        df = pd.to_numeric(df, errors="coerce")
        df = df.fillna(999)
        # df = df.astype(np.int64)
        df = df.replace(999, "")
        df = df
        return df

    def load_database(self):
        print("loadDatabase")
        self.clear_array()  # arrayをクリア
        self.load_database_score(self.dbName)  # scoreテーブルを配列に格納
        self.load_database_basic(self.dbName)
        self.load_database_shot(self.dbName)

    def array2arrays(self, frame, ballx, bally):
        """convert array to arrays by point num
        example
        # point=[1,2,3,3,4,4,4,4]
        hit=["A","B","A","B","A","B","A","B"]
        array_hit=[[], ['A'], ['B'], ['A', 'B'], ['A', 'B', 'A', 'B']]
        """
        # if len(frame) > 0:
        #     lastP = frame[len(frame) - 1] + 1
        # else:
        #     lastP = 0
        # # print("lastP:",lastP)
        r = []
        # for i in range(lastP):
        #     r.append([])
        for i in range(len(frame)):
            temp = []
            temp.append(frame[i])
            temp.append(ballx[i])
            temp.append(bally[i])
            r.append(temp)
        return r

    def array2arrays2(
        self, point, hit, bouncehit, foreback, direction, x1, y1, x2, y2, x3, y3, x4, y4
    ):
        if len(point) > 0:
            lastP = point[len(point) - 1] + 1
        else:
            lastP = 0
        # print("lastP:",lastP)
        array_hit = []
        array_bouncehit = []
        array_foreback = []
        array_direction = []
        array_x1 = []
        array_y1 = []
        array_x2 = []
        array_y2 = []
        array_x3 = []
        array_y3 = []
        array_x4 = []
        array_y4 = []
        for i in range(lastP):
            array_hit.append([])
            array_bouncehit.append([])
            array_foreback.append([])
            array_direction.append([])
            array_x1.append([])
            array_y1.append([])
            array_x2.append([])
            array_y2.append([])
            array_x3.append([])
            array_y3.append([])
            array_x4.append([])
            array_y4.append([])

        for i in range(len(point)):
            n = point[i]
            # print(i,n)
            array_hit[n].append(hit[i])
            array_bouncehit[n].append(bouncehit[i])
            array_foreback[n].append(foreback[i])
            array_direction[n].append(direction[i])
            array_x1[n].append(x1[i])
            array_y1[n].append(y1[i])
            array_x2[n].append(x2[i])
            array_y2[n].append(y2[i])
            array_x3[n].append(x3[i])
            array_y3[n].append(y3[i])
            array_x4[n].append(x4[i])
            array_y4[n].append(y4[i])

        return (
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
        )

    def check_size_return_array(self, db_array, size):
        if len(db_array) < size:
            score_array = db_array
            for i in range(len(db_array), size):
                score_array.append([])
        else:
            score_array = db_array
        return score_array

    def db2score(self):
        """
        convert database array to score array
        """
        print("db2score")
        self.score.array_frame_start = self.arrayFrameStart
        self.score.array_frame_end = self.arrayFrameEnd
        self.score.arraySet = self.arraySet
        self.score.arrayGame = self.arrayGame
        self.score.arrayScore = self.arrayScore
        self.score.arrayScoreResult = self.arrayScoreResult
        self.score.arrayFirstSecond = self.arrayFirstSecond
        self.score.arrayServer = self.arrayServer

        self.score.arrayPointWinner = self.arrayPointWinner
        self.score.pointWin = self.pointWin
        self.score.arrayPointPattern = self.arrayPointPattern
        self.score.arrayForeBack = self.arrayForeBack

        self.score.arrayContactServe = self.arrayContactServe
        self.score.arrayCourt = self.arrayCourt

        self.score.playerA = self.playerA
        self.score.playerB = self.playerB
        self.score.number = self.number
        self.score.totalGame = self.totalGame
        self.score.faultFlug = self.faultFlug
        self.score.arrayFault = self.arrayFault

        # size = len(self.score.array_frame_start)

        self.score.shot_frame = self.shot_frame
        self.score.array_ball_position_shot_x = self.array_ball_position_shot_x
        self.score.array_ball_position_shot_y = self.array_ball_position_shot_y
        self.score.arrayPlayerAPosition_x = self.arrayPlayerAPosition_x
        self.score.arrayPlayerAPosition_y = self.arrayPlayerAPosition_y
        self.score.arrayPlayerBPosition_x = self.arrayPlayerBPosition_x
        self.score.arrayPlayerBPosition_y = self.arrayPlayerBPosition_y
        self.score.arrayHitPlayer = self.arrayHitPlayer
        self.score.arrayBounceHit = self.arrayBounceHit
        self.score.arrayForeBack = self.arrayForeBack
        self.score.arrayDirection = self.arrayDirection

        self.score.array_x1 = self.array_x1
        self.score.array_y1 = self.array_y1
        self.score.array_x2 = self.array_x2
        self.score.array_y2 = self.array_y2
        self.score.array_x3 = self.array_x3
        self.score.array_y3 = self.array_y3
        self.score.array_x4 = self.array_x4
        self.score.array_y4 = self.array_y4

        self.score.array_frame_start = self.arrayFrameStart
        self.score.shot_index = self.score.index_shot(
            self.score.array_frame_start, self.score.shot_frame
        )

        # for i in len(self.score.array_frame_start):
        # self.score.shot_index = [0 for i in range(len(self.array_ball_position_shot))]#あとで変更の必要あり

        # self.score.array_ball_position_shot = self.check_size_return_array(
        #     self.array_ball_position_shot, size
        # )
        # self.score.arrayPlayerAPosition = self.check_size_return_array(
        #     self.arrayPlayerAPosition, size
        # )
        # self.score.arrayPlayerBPosition = self.check_size_return_array(
        #     self.arrayPlayerBPosition, size
        # )
        # self.score.arrayHitPlayer = self.check_size_return_array(
        #     self.arrayHitPlayer, size
        # )
        # self.score.arrayBounceHit = self.check_size_return_array(
        #     self.arrayBounceHit, size
        # )
        # self.score.arrayForeBack = self.check_size_return_array(
        #     self.arrayForeBack, size
        # )
        # self.score.arrayDirection = self.check_size_return_array(
        #     self.arrayDirection, size
        # )

        # self.score.array_x1 = self.check_size_return_array(self.array_x1, size)
        # self.score.array_y1 = self.check_size_return_array(self.array_y1, size)
        # self.score.array_x2 = self.check_size_return_array(self.array_x2, size)
        # self.score.array_y2 = self.check_size_return_array(self.array_y2, size)
        # self.score.array_x3 = self.check_size_return_array(self.array_x3, size)
        # self.score.array_y3 = self.check_size_return_array(self.array_y3, size)
        # self.score.array_x4 = self.check_size_return_array(self.array_x4, size)
        # self.score.array_y4 = self.check_size_return_array(self.array_y4, size)

        return self.score

    def csv2_db_start_end(self, csv_filename):
        """
        convert start_end.csv to db file
        other data is zeros

        """
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        df_se = pd.read_csv(csv_filename).dropna().astype("int64")
        arrayFrameStart = df_se["StartFrame"].astype("int64").tolist()
        arrayFrameEnd = df_se["EndFrame"].astype("int64").tolist()
        arrayZeros = np.zeros(len(arrayFrameStart), dtype=int)
        arrayZeroColumns = [[0, 0] for i in range(len(arrayFrameStart))]
        arrayKara = [np.NaN for i in range(len(arrayFrameStart))]

        df = pd.DataFrame(
            {
                "StartFrame": arrayFrameStart,
                "EndFrame": arrayFrameEnd,
                "Set": arrayKara,
                "Game": arrayKara,
                "Score": arrayKara,
                "ScoreResult": arrayKara,
                "FirstSecond": arrayZeros,
                "Server": arrayKara,
                "PointWinner": arrayKara,
                "PointWinA": arrayKara,
                "PointWinB": arrayKara,
                "PointPattern": arrayKara,
                "Fault": arrayKara,
                "ContactServeX": arrayZeros,
                "ContactServeY": arrayZeros,
                "Court1X": arrayZeros,
                "Court1Y": arrayZeros,
                "Court2X": arrayZeros,
                "Court2Y": arrayZeros,
                "Court3X": arrayZeros,
                "Court3Y": arrayZeros,
                "Court4X": arrayZeros,
                "Court4Y": arrayZeros,
            }
        )

        df_basic = pd.DataFrame(
            {
                "playerA": self.playerA,
                "playerB": self.playerB,
                "number": self.number,
                "totalGame": self.totalGame,
                "faultFlug": self.faultFlug,
            },
            index=[0],
        )
        point = []
        frame = []
        bx = []
        by = []
        pax = []
        pay = []
        pbx = []
        pby = []
        h = []
        bh = []
        fb = []
        d = []
        for i in range(len(self.array_ball_position_shot)):
            for j in range(len(self.array_ball_position_shot[i])):
                point.append(self.array_ball_position_shot[i][j][0])
                frame.append(self.array_ball_position_shot[i][j][1])
                bx.append(self.array_ball_position_shot[i][j][2])
                by.append(self.array_ball_position_shot[i][j][3])
                pax.append(self.arrayPlayerAPosition[i][j][2])
                pay.append(self.arrayPlayerAPosition[i][j][3])
                pbx.append(self.arrayPlayerBPosition[i][j][2])
                pby.append(self.arrayPlayerBPosition[i][j][3])
                h.append(self.arrayHitPlayer[i][j])
                bh.append(self.arrayBounceHit[i][j])
                fb.append(self.arrayForeBack[i][j])  # arrayDirection
                d.append(self.arrayDirection[i][j])
                # print(self.arrayHitPlayer[i][j])
        df_shot = pd.DataFrame(
            {
                "point": point,
                "frame": frame,
                "ballx": bx,
                "bally": by,
                "playerAx": pax,
                "playerAy": pay,
                "playerBx": pbx,
                "playerBy": pby,
                "hitplayer": h,
                "bouncehit": bh,
                "foreback": fb,
                "direction": d,
            }
        )

        df_basic.to_sql("match", conn, if_exists="replace")
        df.to_sql("score", conn, if_exists="replace")
        df_shot.to_sql("shot", conn, if_exists="replace")

        conn.commit()
        conn.close()
