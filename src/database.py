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
        # self.arrayForeBack = score.arrayForeBack

        self.arrayContactServe = score.arrayContactServe
        self.arrayCourt = score.arrayCourt

        self.playerA = score.playerA
        self.playerB = score.playerB
        print("self.playerA,self.playerB",self.playerA,self.playerB)

        self.number = score.number
        self.totalGame = score.totalGame
        self.faultFlug = score.faultFlug
        # self.arrayContactBalls = score.arrayContactBalls
        self.arrayFault = score.arrayFault

        self.arrayBallPosition=score.arrayBallPosition
        self.arrayPlayerAPosition=score.arrayPlayerAPosition
        self.arrayPlayerBPosition=score.arrayPlayerBPosition
        self.arrayHitPlayer=score.arrayHitPlayer
        self.arrayBounceHit=score.arrayBounceHit
        self.arrayForeBack=score.arrayForeBack
        self.arrayDirection=score.arrayDirection


    def saveDatabase(self):
        print("saveDatabase", self.dbName)
        #print("saveDatabase", self.arrayFrameEnd)
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        df = pd.DataFrame({'StartFrame': self.arrayFrameStart, 'EndFrame': self.arrayFrameEnd, 'Set': self.arraySet, 'Game': self.arrayGame,
                           'Score': self.arrayScore, 'ScoreResult': self.arrayScoreResult, 'FirstSecond': self.arrayFirstSecond, 'Server': self.arrayServer,
                           'PointWinner': self.arrayPointWinner, 'PointWinA': self.pointWin[0], 'PointWinB': self.pointWin[1],
                           'PointPattern': self.arrayPointPattern, 'Fault': self.arrayFault,
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
        point=[]
        frame=[]
        bx=[]
        by=[]
        pax=[]
        pay=[]
        pbx=[]
        pby=[]
        h=[]
        bh=[]
        fb=[]
        d=[]
        for i in range(len(self.arrayBallPosition)):
            for j in range(len(self.arrayBallPosition[i])):
                point.append(self.arrayBallPosition[i][j][0])
                frame.append(self.arrayBallPosition[i][j][1])
                bx.append(self.arrayBallPosition[i][j][2])
                by.append(self.arrayBallPosition[i][j][3])
                pax.append(self.arrayPlayerAPosition[i][j][2])
                pay.append(self.arrayPlayerAPosition[i][j][3])
                pbx.append(self.arrayPlayerBPosition[i][j][2])
                pby.append(self.arrayPlayerBPosition[i][j][3])
                h.append(self.arrayHitPlayer[i][j])
                bh.append(self.arrayBounceHit[i][j])
                fb.append(self.arrayForeBack[i][j])#arrayDirection
                d.append(self.arrayDirection[i][j])
                # print(self.arrayHitPlayer[i][j])
        df_shot=pd.DataFrame({'point':point,'frame':frame,'ballx':bx,'bally':by,
                            'playerAx':pax,'playerAy':pay,'playerBx':pbx,'playerBy':pby,
                            'hitplayer':h,'bouncehit':bh,'foreback':fb,'direction':d
        })

        # print(self.arrayBallPosition)
        # print(self.arrayPlayerAPosition)
        # print(self.arrayPlayerBPosition)
        # print(self.arrayHitPlayer)
        # print(self.arrayBounceHit)
        # print(self.arrayForeBack)
        # print(self.arrayDirection)
        
        # with open('contactBalls.csv', 'w') as f:
            # writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
            # writer.writerows(self.arrayContactBalls)  # 2次元配列も書き込める
        df_basic.to_sql("match", conn, if_exists="replace")
        df.to_sql("score", conn, if_exists="replace")
        df_shot.to_sql("shot",conn,if_exists="replace")
        conn.close()

    def loadDatabase(self):
        print("loadDatabase")
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
        # self.arrayContactBalls.clear()
        self.arrayFault.clear()

        self.arrayBallPosition.clear()
        self.arrayPlayerAPosition.clear()
        self.arrayPlayerBPosition.clear()
        self.arrayHitPlayer.clear()
        self.arrayBounceHit.clear()
        self.arrayForeBack.clear()
        self.arrayDirection.clear()

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
        # self.arrayForeBack.extend(df['ForeBack'].values.tolist())
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
        self.playerA = df_basic['playerA'].values[0]
        self.playerB = df_basic['playerB'].values[0]

        self.number = len(df) - 1
        self.totalGame = df_basic['totalGame'].values[0]
        self.faultFlug = df_basic['faultFlug'].values[0]


        df_shot = pd.read_sql("select * from shot", conn)
        point=df_shot['point'].values.tolist()
        frame=df_shot['frame'].values.tolist()
        ballx=df_shot['ballx'].values.tolist()
        bally=df_shot['bally'].values.tolist()
        pax=df_shot['playerAx'].values.tolist()
        pay=df_shot['playerAy'].values.tolist()
        pbx=df_shot['playerBx'].values.tolist()
        pby=df_shot['playerBy'].values.tolist()

        hit=df_shot['hitplayer'].values.tolist()
        bh=df_shot['bouncehit'].values.tolist()
        fb=df_shot['foreback'].values.tolist()
        d=df_shot['direction'].values.tolist()
        #print(self.array2arrays(point,frame,ballx,bally))
        print(df_shot)
        

        self.arrayBallPosition.extend(self.array2arrays(point,frame,ballx,bally))
        self.arrayPlayerAPosition.extend(self.array2arrays(point,frame,pax,pay))
        self.arrayPlayerBPosition.extend(self.array2arrays(point,frame,pbx,pby))

        array_hit,array_bouncehit,array_foreback,array_direction=self.array2arrays2(point,hit,bh,fb,d)
        self.arrayHitPlayer.extend(array_hit)
        self.arrayBounceHit.extend(array_bouncehit)
        self.arrayForeBack.extend(array_foreback)
        self.arrayDirection.extend(array_direction)


        if(self.number==len(self.arrayBallPosition)):
            self.arrayBallPosition.append([])
            self.arrayPlayerAPosition.append([])
            self.arrayPlayerBPosition.append([])
            self.arrayHitPlayer.append([])
            self.arrayBounceHit.append([])
            self.arrayForeBack.append([])
            self.arrayDirection.append([])

        # print("arrayBallPosition",self.arrayBallPosition)
        # print("arrayPlayerAPosition",self.arrayPlayerAPosition)
        # print("arrayPlayerBPosition",self.arrayPlayerBPosition)
        # print("arrayHitPlayer",self.arrayHitPlayer)
        # print("arrayBounceHit",self.arrayBounceHit)
        # print("arrayForeBack",self.arrayForeBack)
        # print("arrayDirection",self.arrayDirection)

        conn.close()
    # def array2arrays(self,point,frame,ballx,bally):
    #     temp2=[]
    #     r=[]
    #     for i in range(len(point)):
    #         print(r)
    #         if(i==0):
    #             r.append([])
    #         if(((point[i]-point[i-1])>1 and i>0)):#i=0 point[0]==1
    #             print("point[i]:",i,point[i])
    #             r.append([])
    #         else:
    #             temp1=[]
    #             if(((point[i]-point[i-1])==1) and i>0):
    #                 r.append(temp2)
    #                 temp2=[]
    #             temp1.append(point[i])
    #             temp1.append(frame[i])
    #             temp1.append(ballx[i])
    #             temp1.append(bally[i])
    #             temp2.append(temp1)
    #             if(i==len(point)-1):
    #                 r.append(temp2)
    #     print("r",r)
    #     return r

    def array2arrays(self,point,frame,ballx,bally):
        lastP=point[len(point)-1]+1
        #print("lastP:",lastP)
        r=[]
        for i in range(lastP):
            r.append([])
        #print("r",r)
        for i in range(len(point)):
            n=point[i]
            # print(i,n)
            temp=[]
            temp.append(point[i])
            temp.append(frame[i])
            temp.append(ballx[i])
            temp.append(bally[i])
            r[n].append(temp)
        #print("r",r)
        return r

    def array2arrays2(self,point,hit,bouncehit,foreback,direction):
        lastP=point[len(point)-1]+1
        # print("lastP:",lastP)
        array_hit=[]
        array_bouncehit=[]
        array_foreback=[]
        array_direction=[]
        for i in range(lastP):
            array_hit.append([])
            array_bouncehit.append([])
            array_foreback.append([])
            array_direction.append([])

        for i in range(len(point)):
            n=point[i]
            # print(i,n)
            array_hit[n].append(hit[i])
            array_bouncehit[n].append(bouncehit[i])
            array_foreback[n].append(foreback[i])
            array_direction[n].append(direction[i])
        # print(array_hit)
        # print(array_bouncehit)
        # print(array_foreback)
        # print(array_direction)
        return array_hit,array_bouncehit,array_foreback,array_direction    

    # def array2arrays2(self,point,hit,bouncehit,foreback,direction):
    #     array_hit=[]
    #     array_bouncehit=[]
    #     array_foreback=[]
    #     array_direction=[]

    #     array_hit_temp=[]
    #     array_bouncehit_temp=[]
    #     array_foreback_temp=[]
    #     array_direction_temp=[]

    #     for i in range(len(point)):
    #         if(i==0):
    #             array_hit.append([])
    #             array_bouncehit.append([])
    #             array_foreback.append([])
    #             array_direction.append([])
    #         if((point[i]-point[i-1]>1 and i>0)):
    #             array_hit.append([])
    #             array_bouncehit.append([])
    #             array_foreback.append([])
    #             array_direction.append([])
    #         else:
    #             if(point[i]!=point[i-1] and i>0):
    #                 array_hit.append(array_hit_temp)
    #                 array_hit_temp=[]
    #                 array_bouncehit.append(array_bouncehit_temp)
    #                 array_bouncehit_temp=[]
    #                 array_foreback.append(array_foreback_temp)
    #                 array_foreback_temp=[]
    #                 array_direction.append(array_direction_temp)
    #                 array_direction_temp=[]
    #             array_hit_temp.append(hit[i])
    #             array_bouncehit_temp.append(bouncehit[i])
    #             array_foreback_temp.append(foreback[i])
    #             array_direction_temp.append(direction[i])

    #             if(i==len(point)-1):
    #                 array_hit.append(array_hit_temp)
    #                 array_bouncehit.append(array_bouncehit_temp)
    #                 array_foreback.append(array_foreback_temp)
    #                 array_direction.append(array_direction_temp)
        
    #     return array_hit,array_bouncehit,array_foreback,array_direction


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
        # self.score.arrayContactBalls = self.arrayContactBalls
        self.score.arrayFault = self.arrayFault

        self.score.arrayBallPosition = self.arrayBallPosition
        self.score.arrayPlayerAPosition = self.arrayPlayerAPosition
        self.score.arrayPlayerBPosition = self.arrayPlayerBPosition
        self.score.arrayHitPlayer = self.arrayHitPlayer
        self.score.arrayBounceHit = self.arrayBounceHit
        self.score.arrayForeBack = self.arrayForeBack
        self.score.arrayDirection = self.arrayDirection

        return self.score