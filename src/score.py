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
import re

import const


class Score:
    def __init__(self, firstSever):
        self.firstServer = firstSever

        self.setPlayerName("PlayerA", "PlayerB")
        self.patternString = const.PATTERN  # PATTERN=[
        # "サービスエース",
        # "ストロークウィナー",
        # "ボレーウィナー",
        # "リターンエラー",
        # "ストロークエラー",
        # "ボレーエラー",
        # "フォルト",
        # "ダブルフォルト"]
        self.firstSecondString = ["", "1st", "2nd"]

        self.pointXYNum = 0
        self.arrayPointXY = (
            []
        )  # 選択したポイントのコート4点のXY座標 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]　表示画面サイズ
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])

        self.arrayCourt = [
            [],
            [],
            [],
            [],
        ]  # 配列 コート4点のXY座標 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        self.arrayCourt[0].append([0, 0])
        self.arrayCourt[1].append([0, 0])
        self.arrayCourt[2].append([0, 0])
        self.arrayCourt[3].append([0, 0])
        self.arrayContactServe = []  # [[0, 0],[1, 1],[2, 2],[3, 3]]
        self.arrayContactServe.append([0, 0])

        self.array_frame_start = [0]
        self.array_frame_end = [0]
        self.arraySet = [""]  # セット
        self.arrayGame = [""]  # ゲーム
        self.arrayScore = [""]  # スコア
        self.arrayScoreResult = [""]  # スコア結果
        self.arrayServer = [""]  # サーバー
        self.arrayPointWinner = [""]  # ウィナーの名前

        self.pointWin = []  # 0 1:won
        self.pointA = []
        self.pointB = []
        self.pointA.append(2)
        self.pointB.append(2)
        self.pointWin.append(self.pointA)  # pointA 勝ったら1を格納
        self.pointWin.append(self.pointB)  # pointB 勝ったら1を格納

        self.arrayPointPattern = [""]  # ポイントパターン
        self.arrayFirstSecond = [0]  # 0:not fault    1:1st fault    2:2nd fault

        self.arrayFault = [0]  # フォルト

        self.faultFlug = 0
        self.number = 0
        self.totalGame = 0
        self.mode = 1  # なんのモード？
        self.winner = 0
        self.rally = 0

        self.total_point = []
        self.total_point.append(0)
        self.total_point.append(0)

        self.serve_point = []
        self.serve_point.append(0)
        self.serve_point.append(0)

        # shotデータ
        self.shot_frame = []
        self.shot_index = []  # [0,0,0,1,1,1,2] ショットがどのポイントに属するか
        self.arrayHitPlayer = []
        self.arrayBounceHit = []
        self.arrayForeBack = []
        self.arrayDirection = []
        self.array_ball_position_shot_x = []  # [num,pos_seek,xball]
        self.array_ball_position_shot_y = []  # [num,pos_seek,xball,yball]
        self.arrayPlayerAPosition_x = []
        self.arrayPlayerAPosition_y = []
        self.arrayPlayerBPosition_x = []
        self.arrayPlayerBPosition_y = []

        self.array_x1 = []  # ビデオサイズでのコート4点のXY座標
        self.array_y1 = []
        self.array_x2 = []
        self.array_y2 = []
        self.array_x3 = []
        self.array_y3 = []
        self.array_x4 = []
        self.array_y4 = []

    def init_array(self):
        array = []
        array.append([])
        return array

    def add_new_tree_point(self, current_frame):
        """if new frame added, append new array"""
        end = self.array_frame_end[len(self.array_frame_end) - 1]  # 終了フレームを一時記憶
        if current_frame < end:
            self.array_frame_start.append(current_frame)
            self.array_frame_end.insert(
                len(self.array_frame_end) - 1, current_frame - 1
            )

            self.arrayPointPattern.append("")
            self.arrayPointWinner.append("")
            self.pointWin[0].append(2)
            self.pointWin[1].append(2)
            self.arraySet.append("")
            self.arrayGame.append("")
            self.arrayScore.append("")
            self.arrayScoreResult.append("")
            self.arrayFirstSecond.append(0)
            self.arrayServer.append("")

            self.arrayCourt[0].append([0, 0])
            self.arrayCourt[1].append([0, 0])
            self.arrayCourt[2].append([0, 0])
            self.arrayCourt[3].append([0, 0])
            self.arrayContactServe.append([0, 0])
            self.arrayFault.append(0)

    # def next_append(self, pos_seek):
    #     """if new next point frame added, """
    #     end = self.array_frame_end[self.number]  # 次のフレームに行く前に終了フレームを一時記憶
    #     self.array_frame_end.insert(self.number, end)
    #     self.number += 1
    #     self.add_new_tree_point() #新フレーム群を追加
    #     self.array_frame_start.append(int(pos_seek))
    #     self.array_frame_end[self.number] = int(pos_seek) - 1  # 終了フレーム
    #     self.rally = 0

    def load_scene(self, num_scene):
        self.array_ball_position_shot = [
            [] for i in range(len(self.array_ball_position_shot), num_scene)
        ]

    def setPlayerName(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB
        self.playerName = [self.playerA, self.playerB]

    def calcScore(self):  # 最初のポイントからすべて計算する
        # print("calcScore")
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

        # print("len(self.pointWin[0])",len(self.pointWin[0]))

        for i in range(len(self.pointWin[0])):  # ポイント間も含め全ポイントを計算する

            # todo ボタン記録されていない箇所（最終行）は計算しないようにしたい
            if self.pointWin[0][i] != 2:
                self.arrayServer[i] = self.playerName[
                    (self.firstServer + g[0] + g[1]) % 2
                ]  # step1 サーバーの計算

                # step2 どちらがポイントを取得したか
                if self.arrayFault[i] == 1:  # フォルトの場合
                    self.arrayScore[i] = ""
                    self.arrayScoreResult[i] = ""
                    self.arrayGame[i] = ""
                    self.arraySet[i] = ""
                    self.arrayFirstSecond[i] = 1

                elif self.arrayFault[i] == 2:  # ダブルフォルトの場合
                    self.arrayFirstSecond[i] = 2
                    (
                        nextScore,
                        nextGame,
                        nextSet,
                        p,
                        g,
                        s,
                        scoreA,
                        scoreB,
                    ) = self.calcScore2(
                        i, nextScore, nextGame, nextSet, p, g, s, scoreA, scoreB
                    )

                elif self.arrayFault[i] == 0:  # フォルトなしの場合
                    if i > 0:
                        if self.arrayFault[i - 1] == 1:  # 前のポイントがフォルト
                            self.arrayFirstSecond[i] = 2
                        else:
                            self.arrayFirstSecond[i] = 1
                    (
                        nextScore,
                        nextGame,
                        nextSet,
                        p,
                        g,
                        s,
                        scoreA,
                        scoreB,
                    ) = self.calcScore2(
                        i, nextScore, nextGame, nextSet, p, g, s, scoreA, scoreB
                    )

    def calcScore2(self, i, nextScore, nextGame, nextSet, p, g, s, scoreA, scoreB):
        self.arrayScore[i] = nextScore
        self.arrayGame[i] = nextGame
        self.arraySet[i] = nextSet
        if self.pointWin[0][i] == 1:
            p[0] += 1
            self.total_point[0] += 1
        if self.pointWin[1][i] == 1:
            p[1] += 1
            self.total_point[1] += 1
        self.serve_point[(self.firstServer + g[0] + g[0]) % 2] += 1

        # print("point:",p[0],p[1])

        scoreA, scoreB, p[0], p[1], g[0], g[1], s[0], s[1] = self.convert_score(
            p[0], p[1], g[0], g[1], s[0], s[1]
        )
        nextScore = scoreA + "-" + scoreB
        nextGame = str(g[0]) + "-" + str(g[1])
        nextSet = str(s[0]) + "-" + str(s[1])
        self.arrayScoreResult[i] = nextScore

        return nextScore, nextGame, nextSet, p, g, s, scoreA, scoreB

    def calc_stats(self, gamePointA, gamePointB, gameA, gameB, setA, setB):
        total_points = self.total_point[0] + self.total_point[1]
        total_point_won[0] = self.total_point[0] / total_points
        total_point_won[1] = self.total_point[1] / total_points

    def convert_score(
        self, gamePointA, gamePointB, gameA, gameB, setA, setB
    ):  # ポイント数からスコアに変換
        """
        Convert to Score String from current gamepoint,game,set
        If Gameup or Setup,change the gamepoint to 0

        Parameters
        ----------
        gamePointA:int
        gamePointB:int
        gameA:int
        gameB:int
        setA:int
        setB:int

        Returns
        ----------
        scoreA:str
        scoreB:str
        gamePointA
        gamePointB
        gameA:int
        gameB:int
        setA:int
        setB:int
        """
        if (gameA == 6) and (gameB == 6):  # タイブレーク
            if gamePointA > 5 and gamePointB > 5:
                if (gamePointA - gamePointB) > 1:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif (gamePointB - gamePointA) > 1:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                else:
                    scoreA = str(gamePointA)
                    scoreB = str(gamePointB)

            else:
                if gamePointA == 7:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif gamePointB == 7:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                else:
                    scoreA = str(gamePointA)
                    scoreB = str(gamePointB)

        else:  # タイブレーク以外
            if gamePointA > 2 and gamePointB > 2:  # 40-40以降
                if (gamePointA - gamePointB) > 1:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif (gamePointB - gamePointA) > 1:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif (gamePointA - gamePointB) == 1:
                    scoreA = "Ad"
                    scoreB = "40"
                elif (gamePointB - gamePointA) == 1:
                    scoreA = "40"
                    scoreB = "Ad"
                else:
                    scoreA = "40"
                    scoreB = "40"
            else:
                if gamePointA == 0:
                    scoreA = "0"
                if gamePointB == 0:
                    scoreB = "0"
                if gamePointA == 1:
                    scoreA = "15"
                if gamePointB == 1:
                    scoreB = "15"
                if gamePointA == 2:
                    scoreA = "30"
                if gamePointB == 2:
                    scoreB = "30"
                if gamePointA == 3:
                    scoreA = "40"
                if gamePointB == 3:
                    scoreB = "40"
                if gamePointA > 3 and gamePointB < 3:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif gamePointB > 3 and gamePointA < 3:
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameB += 1
                    # totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1

        gameA, gameB, setA, setB = self.convert_set(gameA, gameB, setA, setB)

        return scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB

    def convert_set(self, gameA, gameB, setA, setB):
        """
        If setup,increment set,and convert game to 0

        Parameters
        ----------
        gameA:int
        gameB:int
        setA:int
        setB:int
        """
        if gameA > 5 and gameB < 5:  # 6-4
            setA += 1
            gameA = 0
            gameB = 0
        elif gameB > 5 and gameA < 5:  # 4-6
            setB += 1
            gameA = 0
            gameB = 0
        elif gameA > 4 and gameB > 4:  # 7-6
            if gameA == 7:
                setA += 1
                gameA = 0
                gameB = 0
            elif gameB == 7:
                setB += 1
                gameA = 0
                gameB = 0
        return gameA, gameB, setA, setB

    def divide_left_right(self, text_score):
        left = re.findall(r"([0-9a-zA-Z]*)-", text_score)
        right = re.findall(r"-([0-9a-zA-Z]*)", text_score)
        if len(left) > 0:
            left = left[0]
        else:
            left = ""
        if len(right) > 0:
            right = right[0]
        else:
            right = ""
        return left, right

    def score2count(self, score):
        """
        convert string score to count

        Parameters
        ----------
        score:string

        Returns
        ----------
        count:int
        """
        if score == "0":
            count = 0
        elif score == "15":
            count = 1
        elif score == "30":
            count = 2
        elif score == "40":
            count = 3
        elif score == "Ad" or score == "A":
            count = 4
        else:
            count = -1
        return count

    def get_winner(self, pre_count_a, count_a, pre_count_b, count_b):  # １つ前のデータと比較
        """
        return winner by comparing count and pre_count

        Parameters
        ----------
        pre_count_b:int
        count_a:int
        pre_count_a:int
        count_b:int

        Returns
        ----------
        winner:int
        """
        winner = 3  # not point
        if count_a == 0 and count_b == 0:
            if pre_count_a == count_a and pre_count_b == count_b:  # fault
                winner = 2
            elif pre_count_a == 4:
                winner = 0
            elif pre_count_b == 4:
                winner = 1
            elif pre_count_a == 3:
                winner = 0
            elif pre_count_b == 3:
                winner = 1
        else:
            if pre_count_a == count_a and pre_count_b == count_b:  # fault
                winner = 2
            elif pre_count_a == 4 and count_a == 3:  # A->40
                winner = 1
            elif pre_count_b == 4 and count_b == 3:  # A->40
                winner = 0
            elif pre_count_a < count_a and pre_count_b == count_b:
                winner = 0
            elif pre_count_a == count_a and pre_count_b < count_b:
                winner = 1

        return winner

    def get_winner_list(self, array_score):
        """
        convert array_score to winner_array

        Parameters
        ----------
        array_score:list["0-0","0-15"]

        Returns
        ----------
        winner_array:list[int,int]
        0 winner a
        1 winner b
        2 fault
        3 not point
        """
        winner_array = []
        pre_l_count = -1
        pre_r_count = -1
        temp_flug = False
        temp_index = 0
        for i in range(len(array_score)):
            l, r = self.divide_left_right(array_score[i])
            l_count = self.score2count(l)
            r_count = self.score2count(r)

            if i + 1 < len(array_score):
                n_l, n_r = self.divide_left_right(array_score[i + 1])
                next_l_count = self.score2count(n_l)
                next_r_count = self.score2count(n_r)
                if (
                    l_count > -1
                    and r_count > -1
                    and next_l_count > -1
                    and next_r_count > -1
                ):
                    winner = self.get_winner(
                        l_count, next_l_count, r_count, next_r_count
                    )
                    winner_array.append(winner)
                    if temp_flug:
                        winner = self.get_winner(
                            pre_l_count, l_count, pre_r_count, r_count
                        )
                        winner_array[temp_index] = winner
                        temp_flug = False
                else:
                    winner_array.append(3)  # not point
                    temp_flug = True
                    temp_index = i
            else:
                winner_array.append(3)  # not point
            if l_count > -1 or r_count > -1:
                pre_l_count = l_count
                pre_r_count = r_count
        return winner_array

    def winner2player_fault(
        self, winner_array, player_name, point_pattern
    ):  # TODO 1st 2nd　winnerポイントにもつける
        """
        convert array_score to winner_array

        Parameters
        ----------
        winner_array:list[0,1,,]
        player_name:list["playername_a","playername_b"]
        point_pattern:list["Fault","DoubleFault",,,]

        Returns
        ----------
        point_winner_array:list[string,string,,]
        first_second_array:list[int,int,,]
        0:not point
        1:1st point
        2:2nd point
        point_pattern:list[string,string,,]
        """

        point_winner_array = []
        first_second_array = []
        fault_flug = False
        for i in range(len(winner_array)):
            if winner_array[i] < 2:  # point winner 0 1
                point_winner_array.append(player_name[winner_array[i]])
                if fault_flug == False:
                    first_second_array.append(1)
                else:
                    first_second_array.append(2)
                    fault_flug = False
            else:  # fault or not point
                point_winner_array.append("")
                if winner_array[i] == 2:  # fault
                    if fault_flug == False:  #
                        point_pattern[i] = const.PATTERN[6]
                        first_second_array.append(1)
                        fault_flug = True
                    else:  # double fault
                        point_pattern[i] = const.PATTERN[7]
                        first_second_array.append(2)
                        fault_flug = False
                elif winner_array[i] == 3:  # not point
                    first_second_array.append(0)
            pre_first_second = first_second_array[-1]

        return point_winner_array, first_second_array, point_pattern

    def get_game_list(self, array_score):
        """
        array_scoreからゲームの切り替わりを検出してgame_listを返す
        Parameters
        ----------
        array_score:[string] ["0-0","15-0",,]

        Returns
        ----------
        game_list:[int]
        """
        set_a = 0
        set_b = 0
        set_list = ["0-0"]

        game_a = 0
        game_b = 0
        game_list = ["0-0"]
        for i in range(1, len(array_score)):
            if array_score[i] == "0-0":
                l_p, r_p = self.divide_left_right(array_score[i - 1])
                pre_l_count = self.score2count(l_p)
                pre_r_count = self.score2count(r_p)

                l, r = self.divide_left_right(array_score[i])
                l_count = self.score2count(l)
                r_count = self.score2count(r)

                winner = self.get_winner(pre_l_count, l_count, pre_r_count, r_count)
                if winner == 0:
                    game_a += 1
                elif winner == 1:
                    game_b += 1

            game_a, game_b, set_a, set_b = self.get_game_reset(
                game_a, game_b, set_a, set_b
            )

            game_list.append(str(game_a) + "-" + str(game_b))
            set_list.append(str(set_a) + "-" + str(set_b))
        return game_list, set_list

    def get_game_reset(self, game_a, game_b, set_a, set_b):
        if game_a > 5 or game_b > 5:
            if game_a - game_b > 1:
                set_a += 1
                game_a = 0
                game_b = 0
            elif game_b - game_a > 1:
                set_b += 1
                game_a = 0
                game_b = 0
            elif game_a - game_b == 1:
                set_a += 1
                game_a = 0
                game_b = 0
            elif game_b - game_a == 1:
                set_b += 1
                game_a = 0
                game_b = 0
        return game_a, game_b, set_a, set_b

    def get_server_num(self, text_game):
        """ゲームスコアからtotalgameを返す
        Parameters
        ----------
        text_game:string "0-1"

        Returns
        ----------
        total_game:int
        not number :-1
        """
        # print(text_game)
        left = re.findall(r"([0-9]*)-", text_game)
        right = re.findall(r"-([0-9]*)", text_game)
        if len(left) > 0 and len(right) > 0:
            if left[0].isdecimal() and right[0].isdecimal():
                totalGame = int(left[0]) + int(right[0])
            else:
                totalGame = -1
        else:
            totalGame = -1
        return totalGame

    def get_server_list(self, array_game):
        """"""
        server_array = []
        for i in range(len(array_game)):
            text_game = array_game[i]
            # print("text_game", text_game)
            totalGame = self.get_server_num(text_game)
            server_array.append(self.playerName[(self.firstServer + totalGame) % 2])
        return server_array

    def delete_position_data(self, i):
        """
        delete position data which is selected tree data
        Parameters
        ----------
        i:selected num
        """

        # num = self.number
        # j = self.array_ball_position_shot[num][i][0]
        self.shot_index.pop(i)
        self.shot_frame.pop(i)
        self.array_ball_position_shot_x.pop(i)
        self.array_ball_position_shot_y.pop(i)
        self.arrayPlayerAPosition_x.pop(i)
        self.arrayPlayerAPosition_y.pop(i)
        self.arrayPlayerBPosition_x.pop(i)
        self.arrayPlayerBPosition_y.pop(i)
        self.arrayHitPlayer.pop(i)
        self.arrayBounceHit.pop(i)
        self.arrayForeBack.pop(i)
        self.arrayDirection.pop(i)

        self.array_x1.pop(i)
        self.array_y1.pop(i)
        self.array_x2.pop(i)
        self.array_y2.pop(i)
        self.array_x3.pop(i)
        self.array_y3.pop(i)
        self.array_x4.pop(i)
        self.array_y4.pop(i)

    def delete_tree_shot_shift(self, start_shot, end_shot):
        for i in reversed(range(start_shot, end_shot + 1)):  # 1,2
            self.delete_position_data(i)

    def delete_tree_point(self):
        print("delete_tree_point")
        i = self.number
        print(i)
        # delete point
        self.array_frame_start.pop(i)
        self.array_frame_end.pop(i)
        self.arraySet.pop(i)
        self.arrayGame.pop(i)
        self.arrayScore.pop(i)
        self.arrayScoreResult.pop(i)
        self.arrayFirstSecond.pop(i)
        self.arrayServer.pop(i)
        self.arrayPointWinner.pop(i)
        self.pointWin[0].pop(i)
        self.pointWin[1].pop(i)
        self.arrayPointPattern.pop(i)
        self.arrayFault.pop(i)

        self.arrayContactServe.pop(i)

        self.arrayCourt[0].pop(i)
        self.arrayCourt[1].pop(i)
        self.arrayCourt[2].pop(i)
        self.arrayCourt[3].pop(i)

        self.shot_index = self.create_index_shot(
            self.array_frame_start, self.shot_frame
        )


    def create_index_shot(self, score_frame, shot_frame):
        """scoreフレームとshotフレームを比較してshotのindexを作成
        score_frameが変化したときにshotのindexを振りなおす
        各shot_frameが何番目のframeに存在するかのindexを作成
        Parameters
        -----------
        score_frame:[int] [0, 100, 200, 300, 400, 500]
        shot_frame:[int] [50,80,130,250,450,550,1000,3200]
        Returns
        array_shot:[int]
        """
        shot_index = []

        for i in range(len(shot_frame)):
            s = 0
            for j in range(len(score_frame)):
                if shot_frame[i] > score_frame[j]:
                    s = j
            shot_index.append(s)

        return shot_index

    def get_index_array_shot(self, num_point, shot_index):
        shot_index_np = np.array(shot_index)
        display_shot_index = np.where(shot_index_np == num_point)
        if len(display_shot_index) > 0:
            display_shot_index = display_shot_index[0].tolist()
        else:
            display_shot_index = []
        return display_shot_index

    def get_index_shot(self, num_point, num_shot, shot_index):
        shot_index_array = self.get_index_array_shot(num_point, shot_index)
        index = shot_index_array[0] + num_shot
        return index

    def insert_tree_point(self):
        """右クリックでinsertを選択したときに行を挿入する"""
        i = self.number
        start = self.array_frame_start[i]
        self.array_frame_start.insert(i, start)
        self.array_frame_end.insert(i, start + 1)
        self.array_frame_start[i + 1] = start + 2  # 次のポイントのstartを
        self.arraySet.insert(i, "")
        self.arrayGame.insert(i, "")
        self.arrayScore.insert(i, "")
        self.arrayScoreResult.insert(i, "")
        self.arrayFirstSecond.insert(i, 0)  # 0:not fault    1:1st fault    2:2nd fault
        self.arrayServer.insert(i, "")
        self.arrayPointWinner.insert(i, "")
        self.pointWin[0].insert(i, 0)
        self.pointWin[1].insert(i, 0)
        self.arrayPointPattern.insert(i, "")
        self.arrayFault.insert(i, 0)
        self.arrayContactServe.insert(i, [0, 0])
        self.arrayCourt[0].insert(i, [0, 0])
        self.arrayCourt[1].insert(i, [0, 0])
        self.arrayCourt[2].insert(i, [0, 0])
        self.arrayCourt[3].insert(i, [0, 0])

        self.shot_index = self.create_index_shot(
            self.array_frame_start, self.shot_frame
        )

    def get_index_frame(self, frame, array_frame):
        """現在のフレーム位置から、array_frameのインデックスを返す
        Parameters
        -----
        frame:int
        array_frame:[int]
        frameが100であれば、array_frame[11, 51, 101,201]の51から101の間のため、index=1を返す

        Returns
        -----
        index:int

        """
        index = -1
        for i in range(len(array_frame)):
            if frame >= array_frame[i]:
                index = i
            else:
                # index = i
                break
        return index

    def insert_tree_shot(self, i, frame):
        """
        i番目のshot_treeに挿入する
        """
        self.shot_index.insert(i, self.number)
        self.shot_frame.insert(i, frame)
        if i > 0:
            self.array_ball_position_shot_x.insert(
                i, self.array_ball_position_shot_x[i - 1]
            )
            self.array_ball_position_shot_y.insert(
                i, self.array_ball_position_shot_y[i - 1]
            )
            self.arrayPlayerAPosition_x.insert(i, self.arrayPlayerAPosition_x[i - 1])
            self.arrayPlayerAPosition_y.insert(i, self.arrayPlayerAPosition_y[i - 1])
            self.arrayPlayerBPosition_x.insert(i, self.arrayPlayerBPosition_x[i - 1])
            self.arrayPlayerBPosition_y.insert(i, self.arrayPlayerBPosition_y[i - 1])
            self.arrayHitPlayer.insert(i, self.arrayHitPlayer[i - 1])
            self.arrayBounceHit.insert(i, self.arrayBounceHit[i - 1])
            self.arrayForeBack.insert(i, self.arrayForeBack[i - 1])
            self.arrayDirection.insert(i, self.arrayDirection[i - 1])

            self.array_x1.insert(i, self.array_x1[i - 1])
            self.array_y1.insert(i, self.array_y1[i - 1])
            self.array_x2.insert(i, self.array_x2[i - 1])
            self.array_y2.insert(i, self.array_y2[i - 1])
            self.array_x3.insert(i, self.array_x3[i - 1])
            self.array_y3.insert(i, self.array_y3[i - 1])
            self.array_x4.insert(i, self.array_x4[i - 1])
            self.array_y4.insert(i, self.array_y4[i - 1])
        else:
            self.array_ball_position_shot_x.insert(i, 0)
            self.array_ball_position_shot_y.insert(i, 0)
            self.arrayPlayerAPosition_x.insert(i, 0)
            self.arrayPlayerAPosition_y.insert(i, 0)
            self.arrayPlayerBPosition_x.insert(i, 0)
            self.arrayPlayerBPosition_y.insert(i, 0)
            self.arrayHitPlayer.insert(i, "")
            self.arrayBounceHit.insert(i, "")
            self.arrayForeBack.insert(i, "")
            self.arrayDirection.insert(i, "")

            self.array_x1.insert(i, 0)
            self.array_y1.insert(i, 0)
            self.array_x2.insert(i, 0)
            self.array_y2.insert(i, 0)
            self.array_x3.insert(i, 0)
            self.array_y3.insert(i, 0)
            self.array_x4.insert(i, 0)
            self.array_y4.insert(i, 0)

    def insert_position_xy_a(self, frame, x_c, y_c):
        """frameに合わせてコート位置情報を格納する"""
        index = self.get_index_frame(frame, self.shot_frame)
        self.arrayPlayerAPosition_x[index] = x_c
        self.arrayPlayerAPosition_y[index] = y_c

    def insert_position_xy_b(self, frame, x_c, y_c):
        """frameに合わせてコート位置情報を格納する"""
        index = self.get_index_frame(frame, self.shot_frame)
        self.arrayPlayerBPosition_x[index] = x_c
        self.arrayPlayerBPosition_y[index] = y_c

    def insert_position_xy_ball(self, frame, x_c, y_c):
        """frameに合わせてコート位置情報を格納する"""
        index = self.get_index_frame(frame, self.shot_frame)
        self.array_ball_position_shot_x[index] = x_c
        self.array_ball_position_shot_y[index] = y_c

    # def insert_court_right_up(self, frame, x_c, y_c):
    #     """frameに合わせてコート位置情報を格納する
    #     """
    #     index = self.get_index_frame(frame, self.shot_frame)
    #     self.array_x1[index] = x_c
    #     self.array_y1[index] = y_c

    def insert_court(self, frame, x_c, y_c, i):
        """frameに合わせてコート位置情報を格納する"""
        index = self.get_index_frame(frame, self.shot_frame)
        if i == 0:
            self.array_x1[index] = x_c
            self.array_y1[index] = y_c
        elif i == 1:
            self.array_x2[index] = x_c
            self.array_y2[index] = y_c
        elif i == 2:
            self.array_x3[index] = x_c
            self.array_y3[index] = y_c
        elif i == 3:
            self.array_x4[index] = x_c
            self.array_y4[index] = y_c

    def divide_track_data(
        self,
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
    ):  #
        for i in range(len(start_frame) - 1):
            for j in range(len(track_frame)):
                if (
                    start_frame[i] <= track_frame[j]
                    and track_frame[j] < start_frame[i + 1]
                ):
                    # print(i,track_frame[j],bx[j],by[j])
                    self.array_ball_position_shot[i].append(
                        [i, track_frame[j], bx[j], by[j]]
                    )
                    self.arrayPlayerAPosition[i].append(
                        [i, track_frame[j], xa[j], ya[j]]
                    )
                    self.arrayPlayerBPosition[i].append(
                        [i, track_frame[j], xb[j], yb[j]]
                    )
                    self.array_x1[i].append(x1[j])
                    self.array_y1[i].append(y1[j])
                    self.array_x2[i].append(x2[j])
                    self.array_y2[i].append(y2[j])
                    self.array_x3[i].append(x3[j])
                    self.array_y3[i].append(y3[j])
                    self.array_x4[i].append(x4[j])
                    self.array_y4[i].append(y4[j])

                    if "Hit" in hit_bounce[j]:
                        self.arrayBounceHit[i].append("Hit")
                    elif "Bounce" in hit_bounce[j]:
                        self.arrayBounceHit[i].append("Bounce")
                    else:
                        self.arrayBounceHit[i].append("")

                    if "Back" in hit_bounce[j]:
                        self.arrayHitPlayer[i].append("Up")
                    elif "Front" in hit_bounce[j]:
                        self.arrayHitPlayer[i].append("Down")
                    else:
                        self.arrayHitPlayer[i].append("")

                    self.arrayForeBack[i].append("TEST")  # TODO
                    self.arrayDirection[i].append("TEST")  # TODO

    def convert_bally2player_y(self):
        """
        ボールy座標を選手座標に合わせる
        """
        for i in range(len(self.array_ball_position_shot_x)):
            if self.arrayHitPlayer[i] == "Up":
                self.array_ball_position_shot_y[i] = self.arrayPlayerAPosition_y[i]
            elif self.arrayHitPlayer[i] == "Down":
                self.array_ball_position_shot_y[i] = self.arrayPlayerBPosition_y[i]

    def calc_fault_all(self):
        """calc all point arrayFault[i] which 0,1,2 by pre point
        0:not fault
        1:fault
        2:double fault

        pre,current
        1  ,0      ->arrayFirstSecond[i] = 1
        1  ,1 2    ->arrayFault[i] = 2 doublefault
        0  ,0      ->
        0  ,1 2    ->arrayFault[i] = 1
        """

        pre = None
        current = None
        for i in range(len(self.arrayFault)):
            if i > 0:
                if self.arrayFault[i - 1] != None:
                    pre = self.arrayFault[i - 1]
                if self.arrayFault[i] != None:
                    current = self.arrayFault[i]

                if pre != None and current != None and pre != '' and current != '':
                    pre = int(pre)
                    current = int(current)
                    if pre == 1:  # 前のポイントがフォルト
                        if current == 0:  # 現在ポイントがフォルト以外
                            self.arrayFirstSecond[i] = 1  # 0じゃない？
                        elif current > 0:  # 現在ポイントがフォルトorダブルフォルト
                            self.arrayFault[i] = 2  # ダブルフォルトにする
                    else:  # 前のポイントがフォルト以外
                        if current == 0:  # 現在ポイントがフォルト以外
                            pass
                        elif current > 0:  # 現在ポイントがフォルトorダブルフォルト
                            self.arrayFault[i] = 1
                else:
                    if self.arrayFault[i - 1] == None or self.arrayFault[i - 1] == '':
                        self.arrayFirstSecond[i - 1] = 0
                    if self.arrayFault[i] == None or self.arrayFault[i] == '':
                        self.arrayFirstSecond[i] = 0
