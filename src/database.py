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

class Database():
    def __init__(self, dbName, score):
        self.dbName = dbName
        self.score=score

        self.patternString = const.PATTERN
        self.firstSecondString = ["", "1st", "2nd"]

        self.arrayFrameStart = score.array_frame_start
        self.arrayFrameEnd = score.array_frame_end
        self.arraySet = score.arraySet
        # self.array_set_a=score.array_set_a
        # self.array_set_b=score.array_set_b

        self.arrayGame = score.arrayGame
        # self.array_game_a=score.array_game_a
        # self.array_game_b=score.array_game_b

        self.arrayScore = score.arrayScore
        # self.array_score_a=score.array_score_a
        # self.array_score_b=score.array_score_b

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

        self.number = score.number
        self.totalGame = score.totalGame
        self.faultFlug = score.faultFlug
        self.arrayFault = score.arrayFault

        self.arrayBallPosition=score.arrayBallPosition
        self.arrayPlayerAPosition=score.arrayPlayerAPosition
        self.arrayPlayerBPosition=score.arrayPlayerBPosition
        self.arrayHitPlayer=score.arrayHitPlayer
        self.arrayBounceHit=score.arrayBounceHit
        self.arrayForeBack=score.arrayForeBack
        self.arrayDirection=score.arrayDirection

    def save_temp_db(self):#
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
        df.to_sql("score", conn, if_exists="replace")
        conn.close()                  


    def save_database_score(self,db_name):
        r=0
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        try:
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
            r=len(df)
        except ValueError as e:
            print("Error",e)
        else:
            try:
                df.to_sql("score", conn, if_exists="replace")
            except pd.io.sql.DatabaseError as e:
                print("Error",e)
        finally:
            conn.close()
        return r

    def save_database_shot(self,db_name):
        r=0
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()

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
        print(len(self.arrayBallPosition))
        try:
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
        except IndexError as e:
            print("Error",e)
        try:
            df_shot=pd.DataFrame({'point':point,'frame':frame,'ballx':bx,'bally':by,
                            'playerAx':pax,'playerAy':pay,'playerBx':pbx,'playerBy':pby,
                            'hitplayer':h,'bouncehit':bh,'foreback':fb,'direction':d
            })
        except ValueError as e:
            print("Error",e)
        else:
            df_shot.to_sql("shot",conn,if_exists="replace")
            r=len(df_shot)
        finally:
            conn.close()
        return r

    def save_database_basic(self,db_name):
        r=0
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        try:
            df_basic = pd.DataFrame({'playerA': self.playerA,
                                 'playerB': self.playerB,
                                 'number': self.number,
                                 'totalGame': self.totalGame,
                                 'faultFlug': self.faultFlug},
                                index=[0])
        except ValueError as e:
            print("Error",e)
        else:
            df_basic.to_sql("match", conn, if_exists="replace")
            r=len(df_basic)
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
        self.arrayBallPosition.clear()
        self.arrayPlayerAPosition.clear()
        self.arrayPlayerBPosition.clear()
        self.arrayHitPlayer.clear()
        self.arrayBounceHit.clear()
        self.arrayForeBack.clear()
        self.arrayDirection.clear()
        
    def load_database_score(self,db_name):
        r=0
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()

        df = pd.read_sql("select * from score", conn)

        df=df.fillna("")

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
        self.number = len(df) - 1
        print("df",df)
        r=len(df)
        conn.close()
        return r

    def load_database_basic(self,db_name):
        r=0
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        #df_basic
        df_basic = pd.read_sql("select * from match", conn)
        self.playerA = df_basic['playerA'].values[0]
        self.playerB = df_basic['playerB'].values[0]
        self.totalGame = df_basic['totalGame'].values[0]
        self.faultFlug = df_basic['faultFlug'].values[0]
        # print(df_basic)
        conn.close()
        r=len(df_basic)
        return r

    def load_database_shot(self,db_name):
        r=0
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        #df_shot
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
        # print(df_shot)
        
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
        conn.close()
        r=len(df_shot)
        return r

    def load_database(self):
        print("loadDatabase")
        self.clear_array()#arrayをクリア
        self.load_database_score(self.dbName)#scoreテーブルを配列に格納
        self.load_database_basic(self.dbName)
        self.load_database_shot(self.dbName)

    def array2arrays(self,point,frame,ballx,bally):
        if len(point)>0:
            lastP=point[len(point)-1]+1
        else:
            lastP=0
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
        return r

    def array2arrays2(self,point,hit,bouncehit,foreback,direction):
        if len(point)>0:
            lastP=point[len(point)-1]+1
        else:
            lastP=0
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

    
    def db2score(self):#return
        print("db2score")
        # score=src.Score()
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

        if(len(self.arrayBallPosition)<len(self.score.array_frame_start)):
            self.score.arrayBallPosition=[[] for i in range(len(self.arrayBallPosition),len(self.score.array_frame_start))]
        else:
            self.score.arrayBallPosition = self.arrayBallPosition

        if(len(self.arrayPlayerAPosition)<len(self.score.array_frame_start)):
            self.score.arrayPlayerAPosition=[[] for i in range(len(self.arrayPlayerAPosition),len(self.score.array_frame_start))]
        else:
            self.score.arrayPlayerAPosition = self.arrayPlayerAPosition

        if(len(self.arrayPlayerBPosition)<len(self.score.array_frame_start)):
            self.score.arrayPlayerBPosition=[[] for i in range(len(self.arrayPlayerBPosition),len(self.score.array_frame_start))]
        else:
            self.score.arrayPlayerBPosition = self.arrayPlayerBPosition

        if(len(self.arrayHitPlayer)<len(self.score.array_frame_start)):
            self.score.arrayHitPlayer=[[] for i in range(len(self.arrayHitPlayer),len(self.score.array_frame_start))]
        else:
            self.score.arrayHitPlayer = self.arrayHitPlayer

        if(len(self.arrayBounceHit)<len(self.score.array_frame_start)):
            self.score.arrayBounceHit=[[] for i in range(len(self.arrayBounceHit),len(self.score.array_frame_start))]
        else:
            self.score.arrayBounceHit = self.arrayBounceHit
        
        if(len(self.arrayForeBack)<len(self.score.array_frame_start)):
            self.score.arrayForeBack=[[] for i in range(len(self.arrayForeBack),len(self.score.array_frame_start))]
        else:
            self.score.arrayForeBack = self.arrayForeBack

        if(len(self.arrayDirection)<len(self.score.array_frame_start)):
            self.score.arrayDirection=[[] for i in range(len(self.arrayDirection),len(self.score.array_frame_start))]
        else:
            self.score.arrayDirection = self.arrayDirection


        return self.score