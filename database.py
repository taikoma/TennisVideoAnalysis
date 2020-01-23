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
# import score as scr

class Database():
    def __init__(self, dbName, score):
        self.dbName = dbName
        self.score=score

        self.patternString = [
            "サービスエース",
            "ストロークウィナー",
            "ボレーウィナー",
            "リターンエラー",
            "ストロークエラー",
            "ボレーエラー",
            "フォルト",
            "ダブルフォルト"]
        self.firstSecondString = ["", "1st", "2nd"]

        self.arrayFrameStart = score.arrayFrameStart
        self.arrayFrameEnd = score.arrayFrameEnd
        self.arraySet = score.arraySet
        self.arrayGame = score.arrayGame
        self.arrayScore = score.arrayScore
        self.arrayScoreResult = score.arrayScoreResult
        self.arrayFirstSecond = score.arrayFirstSecond
        self.arrayServer = score.arrayServer

        self.arrayPointWinner = score.arrayPointWinner
        self.pointWin = score.pointWin
        self.arrayPointPattern = score.arrayPointPattern
        self.arrayForeBack = score.arrayForeBack

        self.arrayContactServe = score.arrayContactServe
        self.arrayCourt = score.arrayCourt

        self.playerA = score.playerA
        self.playerB = score.playerB
        self.number = score.number
        self.totalGame = score.totalGame
        self.faultFlug = score.faultFlug
        self.arrayContactBalls = score.arrayContactBalls
        self.arrayFault = score.arrayFault

    def saveDatabase(self):
        #print("saveDatabase", self.dbName)
        #print("saveDatabase", self.arrayFrameEnd)
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()

        df = pd.DataFrame({'StartFrame': self.arrayFrameStart, 'EndFrame': self.arrayFrameEnd, 'Set': self.arraySet, 'Game': self.arrayGame,
                           'Score': self.arrayScore, 'ScoreResult': self.arrayScoreResult, 'FirstSecond': self.arrayFirstSecond, 'Server': self.arrayServer,
                           'PointWinner': self.arrayPointWinner, 'PointWinA': self.pointWin[0], 'PointWinB': self.pointWin[1],
                           'PointPattern': self.arrayPointPattern, 'ForeBack': self.arrayForeBack, 'Fault': self.arrayFault,
                           'ContactServeX': list(np.array(self.arrayContactServe)[:, 0]), 'ContactServeY': list(np.array(self.arrayContactServe)[:, 1]),
                           'Court1X': list(np.array(self.arrayCourt)[0][:, 0]), 'Court1Y': list(np.array(self.arrayCourt)[0][:, 1]),
                           'Court2X': list(np.array(self.arrayCourt)[1][:, 0]), 'Court2Y': list(np.array(self.arrayCourt)[1][:, 1]),
                           'Court3X': list(np.array(self.arrayCourt)[2][:, 0]), 'Court3Y': list(np.array(self.arrayCourt)[2][:, 1]),
                           'Court4X': list(np.array(self.arrayCourt)[3][:, 0]), 'Court4Y': list(np.array(self.arrayCourt)[3][:, 1])
                           })
        df_basic = pd.DataFrame({'playerA': self.playerA,
                                 'playerB': self.playerB,
                                 'number': self.number,
                                 'totalGame': self.totalGame,
                                 'faultFlug': self.faultFlug},
                                index=[0])
        with open('contactBalls.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
            writer.writerows(self.arrayContactBalls)  # 2次元配列も書き込める

        df.to_sql("score", conn, if_exists="replace")
        df_basic.to_sql("match", conn, if_exists="replace")

        conn.close()

    def loadDatabase(self):
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
        self.arrayContactBalls.clear()
        self.arrayFault.clear()

        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        df = pd.read_sql("select * from score", conn)
        self.arrayFrameStart.extend(df['StartFrame'].values.tolist())
        self.arrayFrameEnd.extend(df['EndFrame'].values.tolist())
        self.arraySet.extend(df['Set'].values.tolist())
        self.arrayGame.extend(df['Game'].values.tolist())
        self.arrayScore.extend(df['Score'].values.tolist())
        self.arrayScoreResult.extend(df['ScoreResult'].values.tolist())
        self.arrayFirstSecond.extend(df['FirstSecond'].values.tolist())
        self.arrayServer.extend(df['Server'].values.tolist())
        self.arrayPointWinner.extend(df['PointWinner'].values.tolist())
        self.arrayPointPattern.extend(df['PointPattern'].values.tolist())
        self.arrayForeBack.extend(df['ForeBack'].values.tolist())
        self.arrayFault.extend(df['Fault'].values.tolist())

        self.pointWin[0].extend(df['PointWinA'].values.tolist())
        self.pointWin[1].extend(df['PointWinB'].values.tolist())

        for i in range(len(df['ContactServeX'].values.tolist())):
            self.arrayContactServe.append([df['ContactServeX'].values.tolist()[
                i], df['ContactServeY'].values.tolist()[i]])
        self.arrayCourt.append([])
        self.arrayCourt.append([])
        self.arrayCourt.append([])
        self.arrayCourt.append([])
        for i in range(len(df['Court1X'].values.tolist())):
            self.arrayCourt[0].insert(i, [df['Court1X'].values.tolist()[
                i], df['Court1Y'].values.tolist()[i]])
            self.arrayCourt[1].insert(i, [df['Court2X'].values.tolist()[
                i], df['Court2Y'].values.tolist()[i]])
            self.arrayCourt[2].insert(i, [df['Court3X'].values.tolist()[
                i], df['Court3Y'].values.tolist()[i]])
            self.arrayCourt[3].insert(i, [df['Court4X'].values.tolist()[
                i], df['Court4Y'].values.tolist()[i]])

        df_basic = pd.read_sql("select * from match", conn)
        #self.playerA.set(df_basic['playerA'].values)
        #self.playerB.set(df_basic['playerB'].values)
        self.playerA = df_basic['playerA'].values
        self.playerB = df_basic['playerB'].values

#         self.number.set(len(df) - 1)
#         self.totalGame.set(df_basic['totalGame'].values[0])
#         self.faultFlug.set(df_basic['faultFlug'].values[0])

        self.number = len(df) - 1
        self.totalGame = df_basic['totalGame'].values[0]
        self.faultFlug = df_basic['faultFlug'].values[0]

        with open('contactBalls.csv') as f:
            self.arrayContactBalls = list(csv.reader(f))
        #print(self.arrayContactBalls)

        conn.close()

    def dbToScore(self):#return
        print("dbToScore")
        # score=src.Score()
        self.score.arrayFrameStart = self.arrayFrameStart
        self.score.arrayFrameEnd = self.arrayFrameEnd
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
        self.score.arrayContactBalls = self.arrayContactBalls
        self.score.arrayFault = self.arrayFault

        return self.score