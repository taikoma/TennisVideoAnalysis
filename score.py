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
import os


class Score():
    def __init__(self, firstSever):
        self.firstServer = firstSever

        self.setPlayerName("PlayerA", "PlayerB")
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

        self.pointXYNum = 0
        self.arrayPointXY = []  # コートのXY座標
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])

        self.arrayPointXY2 = []  # コートのXY座標
        self.arrayPointXY2.append([0, 0])
        self.arrayPointXY2.append([0, 0])
        self.arrayPointXY2.append([0, 0])
        self.arrayPointXY2.append([0, 0])

        self.arrayCourt = [[], [], [], []]
        self.arrayCourt[0].append([0, 0])
        self.arrayCourt[1].append([0, 0])
        self.arrayCourt[2].append([0, 0])
        self.arrayCourt[3].append([0, 0])
        self.arrayContactServe = []
        self.arrayContactServe.append([0, 0])

        self.arrayFrameStart = []
        self.arrayFrameStart.append(0)
        self.arrayFrameEnd = []
        self.arrayFrameEnd.append(0)
        self.arraySet = []  # セット
        self.arraySet.append("")
        self.arrayGame = []  # ゲーム
        self.arrayGame.append("")
        self.arrayScore = []  # スコア
        self.arrayScore.append("")
        self.arrayScoreResult = []  # スコア結果
        self.arrayScoreResult.append("")
        self.arrayServer = []  # サーバー
        self.arrayServer.append("")
        self.arrayPointWinner = []  # ウィナーの名前
        self.arrayPointWinner.append("")

        self.pointWin = []
        self.pointWin = []
        self.pointA = []
        self.pointB = []
        self.pointA.append(0)
        self.pointB.append(0)
        self.pointWin.append(self.pointA)  # pointA 勝ったら1を格納
        self.pointWin.append(self.pointB)  # pointB 勝ったら1を格納

        self.arrayPointPattern = []  # ポイントパターン
        self.arrayPointPattern.append("")
        self.arrayFirstSecond = []  # 0    1    2
        self.arrayFirstSecond.append(0)
        self.arrayForeBack = []  # サーバー
        self.arrayForeBack.append("")

        self.arrayFault = []  # フォルト
        self.arrayFault.append(0)

        self.faultFlug = 0
        self.number = 0
        self.totalGame = 0
        self.mode = 1
        self.winner = 0

        #追加
        self.arrayContactBalls = []  # 初期化のappendは必要なし
        self.arrayContactBalls.append([])

    def setPlayerName(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB
        self.playerName = [self.playerA, self.playerB]

    # def calcScore_buckup(self):  # 最初のポイントからすべて計算する
    #     p = []
    #     p.append(0)
    #     p.append(0)
    #     g = []
    #     g.append(0)
    #     g.append(0)
    #     s = []
    #     s.append(0)
    #     s.append(0)
    #     scoreA = ""
    #     scoreB = ""
    #     nextScore = "0-0"
    #     nextGame = "0-0"
    #     nextSet = "0-0"
    #     self.totalGame = 0

    #     for i in range(len(self.pointWin[0])):  # ポイント間も含め全ポイントを計算する　
    #         if(self.pointWin[0][i] == 2):  # ポイント間で、winデータなし
    #             self.arrayScore[i] = ""
    #             self.arrayScoreResult[i] = ""
    #             self.arrayGame[i] = ""
    #             self.arraySet[i] = ""
    #         else:
    #             self.arrayScore[i] = nextScore
    #             self.arrayGame[i] = nextGame
    #             self.arraySet[i] = nextSet
    #             if(self.pointWin[0][i] == 1):
    #                 p[0] += 1
    #             if(self.pointWin[1][i] == 1):
    #                 p[1] += 1
    #             scoreA, scoreB, p[0], p[1], g[0], g[1], s[0], s[1] = self.convertScore(
    #                 p[0], p[1], g[0], g[1], s[0], s[1])
    #             nextScore = scoreA + "-" + scoreB
    #             nextGame = str(g[0]) + "-" + str(g[1])
    #             nextSet = str(s[0]) + "-" + str(s[1])
    #             if(self.arrayPointPattern[i] == self.patternString[6]):  # フォルトのとき
    #                 self.arrayScoreResult[i] = ""
    #             else:
    #                 self.arrayScoreResult[i] = nextScore
    #     if((p[0] + p[1]) != 0):
    #         self.arrayServer[self.number] = self.playerName[(
    #             self.firstServer + g[0] + g[1]) % 2]
    #     else:
    #         self.arrayServer[self.number] = self.playerName[(
    #             self.firstServer + g[0] + g[1] + 1) % 2]

    def calcScore(self):  # 最初のポイントからすべて計算する
        print("calcScore")
        p = []
        p.append(0)
        p.append(0)
        g = []
        g.append(0)
        g.append(0)
        s = []
        s.append(0)
        s.append(0)
        scoreA = ""
        scoreB = ""
        nextScore = "0-0"
        nextGame = "0-0"
        nextSet = "0-0"
        self.totalGame = 0

        for i in range(len(self.pointWin[0])):  # ポイント間も含め全ポイントを計算する

            #todo ボタン記録されていない箇所（最終行）は計算しないようにしたい
            if(self.pointWin[0][i] != 2):
                self.arrayServer[i] = self.playerName[(
                    self.firstServer + g[0] + g[1]) % 2]  # step1 サーバーの計算

                #step2 どちらがポイントを取得したか
                if(self.arrayFault[i] == 1):  # フォルトの場合
                    self.arrayScore[i] = ""
                    self.arrayScoreResult[i] = ""
                    self.arrayGame[i] = ""
                    self.arraySet[i] = ""
                    self.arrayFirstSecond[i] = 1

                elif(self.arrayFault[i] == 2):  # ダブルフォルトの場合
                    self.arrayFirstSecond[i] = 2
                    nextScore,nextGame,nextSet,p,g,s,scoreA,scoreB=self.calcScore2(
                        i,
                        nextScore,
                        nextGame,
                        nextSet,
                        p,
                        g,
                        s,
                        scoreA,
                        scoreB)

                elif(self.arrayFault[i] == 0):  # フォルトなしの場合
                    if(i > 0):
                        if(self.arrayFault[i - 1] == 1):  # 前のポイントがフォルト
                            self.arrayFirstSecond[i] = 2
                        else:
                            self.arrayFirstSecond[i] = 1
                    nextScore,nextGame,nextSet,p,g,s,scoreA,scoreB=self.calcScore2(
                        i,
                        nextScore,
                        nextGame,
                        nextSet,
                        p,
                        g,
                        s,
                        scoreA,
                        scoreB)
        #print("arrayFault", self.arrayFault)
        #print("arrayFirstSecond", self.arrayFirstSecond)
        #print("score arrayScore",self.arrayScore)

    def calcScore2(
            self,
            i,
            nextScore,
            nextGame,
            nextSet,
            p,
            g,
            s,
            scoreA,
            scoreB):
        self.arrayScore[i] = nextScore
        self.arrayGame[i] = nextGame
        self.arraySet[i] = nextSet
        if(self.pointWin[0][i] == 1):
            p[0] += 1
        if(self.pointWin[1][i] == 1):
            p[1] += 1
        scoreA, scoreB, p[0], p[1], g[0], g[1], s[0], s[1] = self.convertScore(
            p[0], p[1], g[0], g[1], s[0], s[1])
        nextScore = scoreA + "-" + scoreB
        nextGame = str(g[0]) + "-" + str(g[1])
        nextSet = str(s[0]) + "-" + str(s[1])
        self.arrayScoreResult[i] = nextScore


        return nextScore,nextGame,nextSet,p,g,s,scoreA,scoreB

    def convertScore(self, gamePointA, gamePointB, gameA, gameB, setA, setB):  # ポイント数からスコアに変換
        if((gameA == 6) and (gameB == 6)):
            if(gamePointA > 5 and gamePointB > 5):
                if((gamePointA - gamePointB) > 1):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif((gamePointB - gamePointA) > 1):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                else:
                    scoreA = str(gamePointA)
                    scoreB = str(gamePointB)

            else:
                scoreA = str(gamePointA)
                scoreB = str(gamePointB)

        else:
            if(gamePointA > 2 and gamePointB > 2):  # 40-40以降
                if((gamePointA - gamePointB) > 1):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif((gamePointB - gamePointA) > 1):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif((gamePointA - gamePointB) == 1):
                    scoreA = "Ad"
                    scoreB = "40"
                elif((gamePointB - gamePointA) == 1):
                    scoreA = "40"
                    scoreB = "Ad"
                else:
                    scoreA = "40"
                    scoreB = "40"
            else:
                if(gamePointA == 0):
                    scoreA = "0"
                if(gamePointB == 0):
                    scoreB = "0"
                if(gamePointA == 1):
                    scoreA = "15"
                if(gamePointB == 1):
                    scoreB = "15"
                if(gamePointA == 2):
                    scoreA = "30"
                if(gamePointB == 2):
                    scoreB = "30"
                if(gamePointA == 3):
                    scoreA = "40"
                if(gamePointB == 3):
                    scoreB = "40"
                if(gamePointA > 3 and gamePointB < 3):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif(gamePointB > 3 and gamePointA < 3):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1

        gameA, gameB, setA, setB = self.convertSet(gameA, gameB, setA, setB)

        return scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB

    def convertSet(self, gameA, gameB, setA, setB):
        if(gameA > 5 and gameB < 5):
            setA += 1
            gameA = 0
            gameB = 0
        elif(gameB > 5 and gameA < 5):
            setB += 1
            gameA = 0
            gameB = 0
        elif(gameA > 5 and gameB > 5):
            if(gameA == 7):
                setA += 1
                gameA = 0
                gameB = 0
            elif(gameB == 7):
                setB += 1
                gameA = 0
                gameB = 0
        return gameA, gameB, setA, setB