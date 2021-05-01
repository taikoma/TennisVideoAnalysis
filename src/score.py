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

class Score():
    def __init__(self, firstSever):
        self.firstServer = firstSever

        self.setPlayerName("PlayerA", "PlayerB")
        self.patternString = const.PATTERN
        self.firstSecondString = ["", "1st", "2nd"]

        self.pointXYNum = 0
        self.arrayPointXY = []  #コート4点のXY座標 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]　表示画面サイズ
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])
        self.arrayPointXY.append([0, 0])

        self.arrayCourt = [[], [], [], []]#[[], [], [], []]
        self.arrayCourt[0].append([0, 0])
        self.arrayCourt[1].append([0, 0])
        self.arrayCourt[2].append([0, 0])
        self.arrayCourt[3].append([0, 0])
        self.arrayContactServe = []
        self.arrayContactServe.append([0, 0])

        

        self.array_frame_start = []
        self.array_frame_start.append(0)
        self.array_frame_end = []
        self.array_frame_end.append(0)
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
        # self.pointWin = []
        self.pointA = []
        self.pointB = []
        self.pointA.append(0)
        self.pointB.append(0)
        self.pointWin.append(self.pointA)  # pointA 勝ったら1を格納
        self.pointWin.append(self.pointB)  # pointB 勝ったら1を格納
        # print("pointwin",self.pointWin)

        self.arrayPointPattern = []  # ポイントパターン
        self.arrayPointPattern.append("")
        self.arrayFirstSecond = [] #0:not fault    1:1st fault    2:2nd fault
        self.arrayFirstSecond.append(0)
        # self.arrayForeBack = []  # サーバー
        # self.arrayForeBack.append("")

        

        self.arrayFault = []  # フォルト
        self.arrayFault.append(0)

        self.faultFlug = 0
        self.number = 0
        self.totalGame = 0
        self.mode = 1
        self.winner = 0
        self.rally=0

        self.total_point=[]
        self.total_point.append(0)
        self.total_point.append(0)

        self.serve_point=[]
        self.serve_point.append(0)
        self.serve_point.append(0)

        #shotデータ
        self.arrayHitPlayer=self.init_array()
        self.arrayBounceHit=self.init_array()
        self.arrayForeBack=self.init_array()
        self.arrayDirection=self.init_array()
        self.array_ball_position_shot = self.init_array()
        self.arrayPlayerAPosition = self.init_array()
        self.arrayPlayerBPosition = self.init_array()

        self.array_x1=self.init_array()#ビデオサイズでのコート4点のXY座標
        self.array_y1=self.init_array()
        self.array_x2=self.init_array()
        self.array_y2=self.init_array()
        self.array_x3=self.init_array()
        self.array_y3=self.init_array()
        self.array_x4=self.init_array()
        self.array_y4=self.init_array()

    def init_array(self):
        array=[]
        array.append([])
        return array

    def nextAppend(self):#button_endで呼び出される
        self.rally=0
        self.arrayPlayerAPosition.append([])
        self.arrayPlayerBPosition.append([])
        self.array_ball_position_shot.append([])
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

    def load_scene(self,num_scene):
        self.array_ball_position_shot=[[] for i in range(len(self.array_ball_position_shot),num_scene)]

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
            self.total_point[0]+=1
        if(self.pointWin[1][i] == 1):
            p[1] += 1
            self.total_point[1]+=1
        self.serve_point[(self.firstServer + g[0] + g[0]) % 2]+=1

        # print("point:",p[0],p[1])

        scoreA, scoreB, p[0], p[1], g[0], g[1], s[0], s[1] = self.convert_score(
            p[0], p[1], g[0], g[1], s[0], s[1])
        nextScore = scoreA + "-" + scoreB
        nextGame = str(g[0]) + "-" + str(g[1])
        nextSet = str(s[0]) + "-" + str(s[1])
        self.arrayScoreResult[i] = nextScore


        return nextScore,nextGame,nextSet,p,g,s,scoreA,scoreB

    def calc_stats(self, gamePointA, gamePointB, gameA, gameB, setA, setB):
        total_points=self.total_point[0]+self.total_point[1]
        total_point_won[0]=self.total_point[0]/total_points
        total_point_won[1]=self.total_point[1]/total_points




    def convert_score(self, gamePointA, gamePointB, gameA, gameB, setA, setB):  # ポイント数からスコアに変換
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
        if((gameA == 6) and (gameB == 6)):#タイブレーク
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
                if(gamePointA==7):
                    scoreA = "0"
                    scoreB = "0"
                    gamePointA = 0
                    gamePointB = 0
                    gameA += 1
                    #totalGame.set(totalGame.get() + 1)
                    self.totalGame += 1
                elif(gamePointB==7):
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

        else:#タイブレーク以外
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
        if(gameA > 5 and gameB < 5):#6-4
            setA += 1
            gameA = 0
            gameB = 0
        elif(gameB > 5 and gameA < 5):#4-6
            setB += 1
            gameA = 0
            gameB = 0
        elif(gameA > 4 and gameB > 4):#7-6
            if(gameA == 7):
                setA += 1
                gameA = 0
                gameB = 0
            elif(gameB == 7):
                setB += 1
                gameA = 0
                gameB = 0
        return gameA, gameB, setA, setB

    def divide_left_right(self,text_score):
        left=re.findall(r'([0-9a-zA-Z]*)-',text_score)
        right=re.findall(r'-([0-9a-zA-Z]*)',text_score)
        if len(left) > 0:
            left=left[0]
        else:
            left=""
        if len(right) > 0:
            right=right[0]
        else:
            right=""
        return left,right

    def score2count(self,score):
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
            count=0
        elif score == "15":
            count=1
        elif score == "30":
            count = 2
        elif score == "40":
            count = 3
        elif score == "A":
            count = 4
        else:
            count = -1
        return count

    def get_winner(self,pre_count_a,count_a,pre_count_b,count_b):#１つ前のデータと比較
        """
        convert string score to count

        Parameters
        ----------
        count_a:int
        count_b:int

        Returns
        ----------
        winner:int
        """
        winner = 3#not point
        # if count_a == -1 or count_b == -1:
        if pre_count_a == count_a and pre_count_b == count_b:#fault
            winner = 2
        elif pre_count_a == 4 and count_a == 3:
            winner = 1
        elif pre_count_b == 4 and count_b == 3:
            winner = 0
        elif pre_count_a < count_a and pre_count_b == count_b:
            winner = 0
        elif pre_count_a == count_a and pre_count_b < count_b:
            winner = 1

        return winner
        
    def get_winner_list(self,array_score):
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
        winner_array=[]
        pre_l_count = -1
        pre_r_count = -1
        temp_flug=False
        temp_index=0
        for i in range(len(array_score)):
            l,r=self.divide_left_right(array_score[i])
            l_count=self.score2count(l)
            r_count=self.score2count(r)

            if i+1 < len(array_score):
                n_l,n_r=self.divide_left_right(array_score[i+1])
                next_l_count=self.score2count(n_l)
                next_r_count=self.score2count(n_r)
                if l_count > -1 and r_count > -1 and next_l_count > -1 and next_r_count > -1:
                    winner = self.get_winner(l_count,next_l_count,r_count,next_r_count)
                    winner_array.append(winner)
                    if temp_flug:
                        winner = self.get_winner(pre_l_count,l_count,pre_r_count,r_count)
                        winner_array[temp_index]=winner
                        temp_flug=False
                else:
                    winner_array.append(3)#not point
                    temp_flug=True
                    temp_index=i
            else:
                winner_array.append(3)#not point
            if l_count > -1 or r_count > -1:
                pre_l_count=l_count
                pre_r_count=r_count
        return winner_array

    def winner2player_fault(self,winner_array,player_name,point_pattern):#TODO 1st 2nd　winnerポイントにもつける
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

        point_winner_array=[]
        first_second_array=[]
        fault_flug = False
        for i in range(len(winner_array)):
            if winner_array[i] < 2:#point winner 0 1
                point_winner_array.append(player_name[winner_array[i]])
                if fault_flug == False:
                    first_second_array.append(1)
                else:
                    first_second_array.append(2)
                    fault_flug = False
            else:#fault or not point
                point_winner_array.append("")
                if winner_array[i] == 2:#fault
                    if fault_flug == False:#
                        point_pattern[i]=const.PATTERN[6]
                        first_second_array.append(1)
                        fault_flug = True
                    else:#double fault
                        point_pattern[i]=const.PATTERN[7]
                        first_second_array.append(2)
                        fault_flug = False
                elif winner_array[i] == 3:#not point
                    first_second_array.append(0)
            pre_first_second = first_second_array[-1]
                
        return point_winner_array,first_second_array,point_pattern

    def position_data2array_insert(self,xball,yball,xa,ya,xb,yb,servereturn,hitBounce,foreback,crossstreat,x1,y1,x2,y2,x3,y3,x4,y4,pos_seek):
        num=self.number
        j=0
        for i in range(len(self.array_ball_position_shot[num])):
            print("pos_seek",pos_seek)
            print("array_ball_position_shot",self.array_ball_position_shot[num][i][1])
            if pos_seek > self.array_ball_position_shot[num][i][1]:
                j=i+1
        
        self.array_ball_position_shot[num].insert(j,[num,pos_seek,xball,yball])
        self.arrayPlayerAPosition[num].insert(j,[num,pos_seek,xa,ya])
        self.arrayPlayerBPosition[num].insert(j,[num,pos_seek,xb,yb])
        self.arrayHitPlayer[num].insert(j,self.playerName[(self.firstServer + servereturn + self.totalGame) % 2])
        self.arrayBounceHit[num].insert(j,hitBounce)
        self.arrayForeBack[num].insert(j,foreback)
        self.arrayDirection[num].insert(j,crossstreat)
        self.array_x1[num].insert(j,x1)
        self.array_y1[num].insert(j,y1)
        self.array_x2[num].insert(j,x2)
        self.array_y2[num].insert(j,y2)
        self.array_x3[num].insert(j,x3)
        self.array_y3[num].insert(j,y3)
        self.array_x4[num].insert(j,x4)
        self.array_y4[num].insert(j,y4)

        for j in range(len(self.array_ball_position_shot[num])):
            self.array_ball_position_shot[num][j][0]=j+1


    def position_data2array(self,xball,yball,xa,ya,xb,yb,servereturn,hitBounce,foreback,crossstreat,x1,y1,x2,y2,x3,y3,x4,y4,pos_seek):
        """
        position_data2array array[num].append([*,*]) num is self.number

        Parameters
        ----------
        xball:int
        yball:int
        xa:
        ya:
        xb:
        yb:
        servereturn:int which player hitting server or returner 0:server 1:returner
        hitBounce
        foreback
        cressstreat
        ----------

        Returns
        ----------

        ----------
        """
        num=self.number
        self.array_ball_position_shot[num].append([num,pos_seek,xball,yball])
        self.arrayPlayerAPosition[num].append([num,pos_seek,xa,ya])
        self.arrayPlayerBPosition[num].append([num,pos_seek,xb,yb])
        self.arrayHitPlayer[num].append(self.playerName[(self.firstServer + servereturn + self.totalGame) % 2])
        self.arrayBounceHit[num].append(hitBounce)
        self.arrayForeBack[num].append(foreback)
        self.arrayDirection[num].append(crossstreat)
        self.array_x1[num].append(x1)
        self.array_y1[num].append(y1)
        self.array_x2[num].append(x2)
        self.array_y2[num].append(y2)
        self.array_x3[num].append(x3)
        self.array_y3[num].append(y3)
        self.array_x4[num].append(x4)
        self.array_y4[num].append(y4)

    def position_data2array_fix(self,xball,yball,xa,ya,xb,yb,servereturn,hitBounce,foreback,crossstreat,x1,y1,x2,y2,x3,y3,x4,y4,pos_seek):#(self,xball,yball,xa,ya,xb,yb,servereturn,y1,y2):
        num=self.number
        rally=self.rally
        self.array_ball_position_shot[num][rally-1]=[num,pos_seek,xball,yball]
        self.arrayPlayerAPosition[num][rally-1]=[num,pos_seek,xa,ya]
        self.arrayPlayerBPosition[num][rally-1]=[num,pos_seek,xb,yb]
        self.arrayHitPlayer[num][rally-1]=self.playerName[(self.firstServer + servereturn + self.totalGame) % 2]
        self.arrayBounceHit[num][rally-1]=hitBounce
        self.arrayForeBack[num][rally-1]=foreback
        self.arrayDirection[num][rally-1]=crossstreat
        self.array_x1[num][rally-1]=x1
        self.array_y1[num][rally-1]=y1
        self.array_x2[num][rally-1]=x2
        self.array_y2[num][rally-1]=y2
        self.array_x3[num][rally-1]=x3
        self.array_y3[num][rally-1]=y3
        self.array_x4[num][rally-1]=x4
        self.array_y4[num][rally-1]=y4

    def delete_position_data(self,i):
        """
        delete position data which is selected tree data
        Parameters
        ----------
        i:selected num
        """
        
        num=self.number
        j=self.array_ball_position_shot[num][i][0]
        self.array_ball_position_shot[num].pop(i)
        self.arrayPlayerAPosition[num].pop(i)
        self.arrayPlayerBPosition[num].pop(i)
        self.arrayHitPlayer[num].pop(i)
        self.arrayBounceHit[num].pop(i)
        self.arrayForeBack[num].pop(i)
        self.arrayDirection[num].pop(i)

        self.array_x1[num].pop(i)
        self.array_y1[num].pop(i)
        self.array_x2[num].pop(i)
        self.array_y2[num].pop(i)
        self.array_x3[num].pop(i)
        self.array_y3[num].pop(i)
        self.array_x4[num].pop(i)
        self.array_y4[num].pop(i)

        for j in range(len(self.array_ball_position_shot[num])):
            self.array_ball_position_shot[num][j][0]=j+1
            self.arrayPlayerAPosition[num][j][0]=j+1
            self.arrayPlayerBPosition[num][j][0]=j+1

    def delete_tree_shot_shift(self,start_shot,end_shot):
        for i in reversed(range(start_shot,end_shot+1)):#1,2
            self.delete_position_data(i)

    def delete_tree_point(self):
        i=self.number
        print(i)
        #delete point
        self.array_frame_start.pop(i)
        self.array_frame_end.pop(i)
        self.arraySet.pop(i)
        self.arrayGame.pop(i)
        self.arrayScore.pop(i)
        self.arrayScoreResult.pop(i)
        self.arrayFirstSecond.pop(i)
        self.arrayServer.pop(i)
        self.arrayPointWinner.pop(i)
        self.arrayPointPattern.pop(i)


        #delete shot all
        self.array_ball_position_shot.pop(i)
        self.arrayPlayerAPosition.pop(i)
        self.arrayPlayerBPosition.pop(i)
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

    def delete_after_end(self,num,end):
        # num=self.number
        print("len(self.array_ball_position_shot[num])",len(self.array_ball_position_shot[num]))
        print("self.array_ball_position_shot[num]",self.array_ball_position_shot[num])
        array=[]
        for i in range(len(self.array_ball_position_shot[num])):
            print(self.array_ball_position_shot[num][i])
            if len(self.array_ball_position_shot[num][i])>0:
                if end < self.array_ball_position_shot[num][i][1]:
                    array.append(i)

        for i in sorted(array, reverse=True):
            self.array_ball_position_shot[num].pop(i)
            self.arrayPlayerAPosition[num].pop(i)
            self.arrayPlayerBPosition[num].pop(i)
            self.arrayHitPlayer[num].pop(i)
            self.arrayBounceHit[num].pop(i)
            self.arrayForeBack[num].pop(i)
            self.arrayDirection[num].pop(i)

            self.array_x1[num].pop(i)
            self.array_y1[num].pop(i)
            self.array_x2[num].pop(i)
            self.array_y2[num].pop(i)
            self.array_x3[num].pop(i)
            self.array_y3[num].pop(i)
            self.array_x4[num].pop(i)
            self.array_y4[num].pop(i)

            # self.array_ball_position_shot
        


    def divide_track_data(self,start_frame,track_frame,bx,by,xa,ya,xb,yb,hit_bounce,x1,y1,x2,y2,x3,y3,x4,y4):#
        for i in range(len(start_frame)-1):
            for j in range(len(track_frame)):
                if start_frame[i]<=track_frame[j] and track_frame[j]<start_frame[i+1]:
                    # print(i,track_frame[j],bx[j],by[j])
                    self.array_ball_position_shot[i].append([i,track_frame[j],bx[j],by[j]])
                    self.arrayPlayerAPosition[i].append([i,track_frame[j],xa[j],ya[j]])
                    self.arrayPlayerBPosition[i].append([i,track_frame[j],xb[j],yb[j]])
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

                    self.arrayForeBack[i].append("TEST")#TODO
                    self.arrayDirection[i].append("TEST")#TODO

    def convert_bally2playery(self):
        for i in range(len(self.array_ball_position_shot)):
            for j in range(len(self.array_ball_position_shot[i])):
                if self.arrayHitPlayer[i][j]=="Up":
                    self.array_ball_position_shot[i][j][3]=self.arrayPlayerAPosition[i][j][3]
                elif self.arrayHitPlayer[i][j]=="Down":
                    self.array_ball_position_shot[i][j][3]=self.arrayPlayerBPosition[i][j][3]

        
                
        