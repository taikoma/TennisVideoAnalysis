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

class Application(tkinter.Frame):
    #GUIウィンドウの設定と画像描画
    def __init__(self, score, master=None):
        super().__init__(master)
        self.score = score
        self.master = master

        self.pack()

        self.winner = tkinter.IntVar()
        self.winner.set(0)

        self.firstServer = tkinter.IntVar()
        self.firstServer.set(score.firstServer)

        self.delay = 33
        self.frame_count = 1
        self.mode = 0
        self.courtsize=360/27.77

    def loadVideo(self, vid):
        self.vid = vid
        self.video = vid.video
        self.frame_count = vid.frame_count
        self.score.arrayFrameEnd[len(
            self.score.arrayFrameEnd) - 1] = self.frame_count

        self.vid.set_start_frame(self.vid.start_frame)
        self.vid.set_end_frame(self.vid.end_frame)
        self.delay = int(1000 / self.vid.fps / 2)
        print("self.delay", self.delay)

    def create_widgets(self, score, w, h):  # ウィジェット作成

        self.create_menu_bar()

        self.w = w
        self.h = h
        self.pw = tkinter.PanedWindow(self, orient='horizontal')  # 全画面
        self.pw.pack(expand=True)

        self.pwLeft = tkinter.PanedWindow(self.pw, orient='vertical')  # 左画面
        self.pw.add(self.pwLeft)

        self.pwRight = tkinter.PanedWindow(self.pw, orient='vertical')  # 右画面
        self.pw.add(self.pwRight)

        self.pwLeftUp = tkinter.PanedWindow(self.pwLeft, orient='horizontal') # 左画面の上側
        self.pwLeft.add(self.pwLeftUp)

        self.pwRightUp = tkinter.PanedWindow(self.pwRight, orient='horizontal') # 右画面の上側
        self.pwRight.add(self.pwRightUp)

        self.create_image()  # 左画面の上側 画像描画部分
        self.create_scale()  # 左画面の上側 スケール

        self.canvas1 = tkinter.Canvas(self.pwRightUp, width = 195, height = 380)#テニスコート用のcanvas作成
        self.createCourt(self.canvas1,self.courtsize,self.pwRightUp)#テニスコート

        self.canvas2 = tkinter.Canvas(self.pwRightUp, width = 195, height = 380)#テニスコート用のcanvas作成
        self.createCourt(self.canvas2,self.courtsize,self.pwRightUp)#テニスコート


        self.pwLeftDown = tkinter.PanedWindow(self.pwLeft, orient='horizontal') # 左画面の下側
        self.pwLeft.add(self.pwLeftDown)

        self.pwRightDown = tkinter.PanedWindow(self.pwRight, orient='horizontal') # 右画面の下側
        self.pwRight.add(self.pwRightDown)


        self.pwLeftLeft = tkinter.PanedWindow(self.pwLeftDown, orient='vertical') # 左画面の下側 左
        self.pwLeftDown.add(self.pwLeftLeft)

        self.pwLeftRight = tkinter.PanedWindow(self.pwLeftDown, orient='vertical') # 左画面の下側 右
        self.pwLeftDown.add(self.pwLeftRight)

        self.pw1_1 = tkinter.PanedWindow(self.pwLeft, orient='horizontal') # コマ送り
        self.pwLeftLeft.add(self.pw1_1)
        self.create_button(self.pw1_1)

        self.pw1_2 = tkinter.PanedWindow(self.pwLeft, orient='horizontal') # 動画再生UI
        self.pwLeftLeft.add(self.pw1_2)
        self.create_button2(self.pw1_2)

        self.pw1_3 = tkinter.PanedWindow(self.pwLeftLeft, orient='horizontal') # 左画面の下側 左
        self.pwLeftLeft.add(self.pw1_3)
        self.create_button3()

        self.pw1_4 = tkinter.PanedWindow(self.pwLeftLeft, orient='horizontal') # 左画面の下側 左 ポイント種別
        self.pwLeftLeft.add(self.pw1_4)
        self.create_button4(self.pw1_4)


        self.create_tree()#タグ一覧を右に描画
        self.setTree()
        self.tree.bind('<ButtonRelease-1>', self.select)  # Double-1
        self.tree.selection_set(self.tree.get_children()[0])

        self.change_state()

    def createCourt(self,canvas,s,pw):
        out=2*s
        single=1.37*s
        net=0.914*s
        canvas.create_rectangle(0, 0, 10.97*s+out*2, 23.77*s+out*2, fill = '#2E9AFE',width = 0)#塗りつぶし
        canvas.create_rectangle(0+out, 0+out, 10.97*s+out, 23.77*s+out, fill = '#0080FF',width = 0)#塗りつぶし
        canvas.create_line(0+out,0+out,10.97*s+out,0+out,10.97*s+out,23.77*s+out,
                            0+out,23.77*s+out,0+out,0+out,
                            fill='#FFFFFF',width = 2.0)
        canvas.create_line(0+out-net,23.77*s/2+out,10.97*s+out+net,23.77*s/2+out,fill='#FFFFFF',width = 2.0)
        canvas.create_line(0+out+single,0+out,0+out+single,23.77*s+out,fill='#FFFFFF',width = 2.0)
        canvas.create_line(10.97*s+out-single,0+out,10.97*s+out-single,23.77*s+out,fill='#FFFFFF',width = 2.0)
        canvas.create_line(10.97*s/2+out,23.77*s/4+out,10.97*s/2+out,23.77*s/4*3+out,fill='#FFFFFF',width = 2.0)

        canvas.create_line(0+out+single,23.77*s/4+out,10.97*s+out-single,23.77*s/4+out,fill='#FFFFFF',width = 2.0)
        canvas.create_line(0+out+single,23.77*s/4*3+out,10.97*s+out-single,23.77*s/4*3+out,fill='#FFFFFF',width = 2.0)
        #canvas.create_line(6*s,23.77/4*3*s+1*s,7*s,4*s,10.97*s-1*s,23.77*s-1*s,fill='red',width=1.0)
        canvas.place(x=0,y=0)
        pw.add(canvas,pady=10)

    def drawContact(self):
        print("drawContact",len(self.score.arrayContactServe))
        self.canvas1.delete("all")
        self.createCourt(self.canvas1,self.courtsize,self.pwRightUp)
        r=1*1
        s=self.courtsize        
        for i in range(len(self.score.arrayContactServe)):
            if(self.score.arrayContactServe[i][0]+self.score.arrayContactServe[i][1]>0):#サーブ以外のポイントは排除
                print(i)
                p1=[float(self.score.arrayCourt[1][i][0]),float(self.score.arrayCourt[1][i][1])]
                p2=[float(self.score.arrayCourt[2][i][0]),float(self.score.arrayCourt[2][i][1])]
                p3=[float(self.score.arrayCourt[3][i][0]),float(self.score.arrayCourt[3][i][1])]
                p4=[float(self.score.arrayCourt[0][i][0]),float(self.score.arrayCourt[0][i][1])]

                c1,c2,c3,c4=[0, 0],[0, 23.78],[8.23, 23.78],[8.23, 0]

                src_pts = np.float32([p1,p2,p3,p4]).reshape(-1,1,2)
                dst_pts = np.float32([c1,c2,c3,c4]).reshape(-1,1,2)

                M,mask=cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                pts=np.array([[[float(self.score.arrayContactServe[i][0]),
                    float(self.score.arrayContactServe[i][1])]]])
                # print(float(self.score.arrayCourt[0][i][0]))
                # print(pts)
                # print(src_pts)
                # print(dst_pts)
                dst = cv2.perspectiveTransform(pts,M)

                x_temp=dst[0][0][0]
                y_temp=dst[0][0][1]

                if(self.score.arrayServer[i]==self.score.playerName[0]):
                    #print(self.score.arrayFirstSecond[i])
                    if(y_temp<11.89):#上半分の場合、そのまま表示
                        x=x_temp*s+2*s+1.37*s
                        y=y_temp*s+2*s
                        if(score.arrayFirstSecond[i] == 0):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FF0000',width=0)
                        elif(score.arrayFirstSecond[i] == 1):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FFFF00',width=0)
                    else:#下半分の場合、反転して上側に表示
                        x=(8.23-x_temp)*s+2*s+1.37*s
                        y=(23.78-y_temp)*s+2*s
                        if(score.arrayFirstSecond[i] == 0):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FF0000',width=0)
                        elif(score.arrayFirstSecond[i] == 1):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FFFF00',width=0)
                elif(self.score.arrayServer[i]==self.score.playerName[1]):
                    print("arrayFirstSecond",score.arrayFirstSecond[i])
                    if(y_temp>=11.89):#下半分の場合、そのまま表示
                        x=x_temp*s+2*s+1.37*s
                        y=y_temp*s+2*s
                        if(score.arrayFirstSecond[i] == 1):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FF0000',width=0)#赤色
                        elif(score.arrayFirstSecond[i] == 2):
                            self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FFFF00',width=0)#黄色
                    else:#上半分の場合、反転して下側に表示
                        x=(8.23-x_temp)*s+2*s+1.37*s
                        y=(23.78-y_temp)*s+2*s
                        if(score.arrayFirstSecond[i] == 1):
                           self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FF0000',width=0)
                        elif(score.arrayFirstSecond[i] == 2):
                           self.canvas1.create_oval(x-r, y-r, x+r, y+r, tag="oval",fill='#FFFF00',width=0)
                #print("dst",x,y)

                #print(i,self.score.arrayContactServe[i][0],self.score.arrayContactServe[i][1])

        
        

    def create_scale(self):
        self.myval = tkinter.DoubleVar()
        self.myval.trace("w", self.value_changed)
        self.sc = tkinter.Scale(
            variable=self.myval, orient='horizontal', length=self.w, from_=0, to=(
                self.frame_count - 1))
        self.pwLeft.add(self.sc, padx=10)

    def value_changed(self, *args):  # scaleの値が変化したとき
        if(self.myval.get() > score.arrayFrameEnd[score.number]):
            score.number += 1
            self.tree.selection_set(self.tree.get_children()[score.number])
        elif(self.myval.get() < score.arrayFrameStart[score.number]):
            score.number -= 1
            self.tree.selection_set(self.tree.get_children()[score.number])
        if(self.mode == 0):
            self.imageShow()

    def create_image(self):
        # gimg=self.readImage(0)
        gimg = np.zeros((self.w, self.h, 3), dtype=np.uint8)
        img_copy = np.copy(gimg)
        image_change = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image_change)
        self.imgtk = ImageTk.PhotoImage(image=im)

        self.panel = tkinter.Label(self, image=self.imgtk)
        self.panel.bind("<Button-1>", self.mouseclicked)
        self.pwLeftUp.add(self.panel, padx=10, pady=10)

    def mouseclicked_buckup(self, event):  # mouseevent 着弾点をマウスでクリック
        if((score.arrayContactServe[score.number][0] > 0) and(score.arrayContactServe[score.number][1] > 0)):
            msg = tkinter.messagebox.askyesno('serve', 'サーブ座標データを上書きしますか？')
            if msg == 1:  # true
                score.arrayContactServe[number] = [0, 0]
        else:
            if(score.mode == 0):
                print("mode", score.mode)
                gimg = self.readImage(self.myval.get())
                pts, dilation = calcCourtPoints(gimg)
                img_copy = np.copy(gimg)
                cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
                h, w = img_copy.shape[0], img_copy.shape[1]
                cv2.line(img_copy, (event.x - 2, 0),
                         (event.x - 2, h - 1), (255, 0, 0))
                cv2.line(img_copy, (0, event.y - 2),
                         (w - 1, event.y - 2), (255, 0, 0))
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
            elif(score.mode == 1):
                print("mode", score.mode)
                gimg = self.readImage(self.myval.get())
                img_copy = np.copy(gimg)
                cv2.circle(img_copy, (event.x - 2, event.y - 2),
                           2, (0, 255, 0), -1)
                score.arrayPointXY[score.pointXYNum][0] = event.x - 2
                score.arrayPointXY[score.pointXYNum][1] = event.y - 2

                # arrayCourt[0]
                score.arrayCourt[score.pointXYNum][score.number][0] = event.x - 2
                score.arrayCourt[score.pointXYNum][score.number][1] = event.y - 2

                #score.pointXYNum.set(score.pointXYNum + 1)
                score.pointXYNum = score.pointXYNum + 1

                if(score.pointXYNum < 4):
                    image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(image)
                    imgtk = ImageTk.PhotoImage(image=im)
                    self.panel.configure(image=imgtk)
                    self.panel.image = imgtk
                else:
                    pts = np.array([score.arrayPointXY[0],
                                    score.arrayPointXY[1],
                                    score.arrayPointXY[2],
                                    score.arrayPointXY[3]],
                                   dtype=int)
                    # print(pts)
                    cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
                    image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(image)
                    imgtk = ImageTk.PhotoImage(image=im)
                    self.panel.configure(image=imgtk)
                    self.panel.image = imgtk

                    score.pointXYNum = 0
                    #score.mode.set(2)
                    score.mode = 2
            elif(score.mode == 2):
                print("mode", score.mode)
                gimg = self.readImage(self.myval.get())
                pts = np.array([score.arrayPointXY[0],
                                score.arrayPointXY[1],
                                score.arrayPointXY[2],
                                score.arrayPointXY[3]],
                               dtype=int)
                img_copy = np.copy(gimg)
                cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
                h, w = img_copy.shape[0], img_copy.shape[1]
                cv2.line(img_copy, (event.x - 2, 0),
                         (event.x - 2, h - 1), (255, 0, 0))
                cv2.line(img_copy, (0, event.y - 2),
                         (w - 1, event.y - 2), (255, 0, 0))
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
                score.mode = 1

                score.arrayContactServe[score.number] = [
                    event.x - 2, event.y - 2]
                self.setTree()

    def mouseclicked(self, event):  # mouseevent 着弾点をマウスでクリック
        if(score.mode == 0):
            gimg = self.readImage(self.myval.get())
            pts, dilation = calcCourtPoints(gimg)
            img_copy = np.copy(gimg)
            cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
            h, w = img_copy.shape[0], img_copy.shape[1]
            cv2.line(img_copy, (event.x - 2, 0),
                     (event.x - 2, h - 1), (255, 0, 0))
            cv2.line(img_copy, (0, event.y - 2),
                     (w - 1, event.y - 2), (255, 0, 0))
            image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im)
            self.panel.configure(image=imgtk)
            self.panel.image = imgtk
        elif(score.mode == 1):  # コート範囲選択（4点選択）
            gimg = self.readImage(self.myval.get())
            img_copy = np.copy(gimg)
            cv2.circle(
                img_copy, (event.x - 2, event.y - 2), 2, (0, 255, 0), -1)
            score.arrayPointXY[score.pointXYNum][0] = event.x - 2
            score.arrayPointXY[score.pointXYNum][1] = event.y - 2
            score.arrayCourt[score.pointXYNum][score.number][0] = event.x - 2
            score.arrayCourt[score.pointXYNum][score.number][1] = event.y - 2
            score.pointXYNum = score.pointXYNum + 1
            if(score.pointXYNum < 4):
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
            else:
                pts = np.array([score.arrayPointXY[0],
                                score.arrayPointXY[1],
                                score.arrayPointXY[2],
                                score.arrayPointXY[3]],
                               dtype=int)
                cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
                score.pointXYNum = 0
                score.mode = 2
        elif(score.mode == 2):  # サーブの着地点を検出
            gimg = self.readImage(self.myval.get())
            pts = np.array([score.arrayPointXY[0],
                            score.arrayPointXY[1],
                            score.arrayPointXY[2],
                            score.arrayPointXY[3]],
                           dtype=int)
            img_copy = np.copy(gimg)
            cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
            h, w = img_copy.shape[0], img_copy.shape[1]
            cv2.line(img_copy, (event.x - 2, 0),
                     (event.x - 2, h - 1), (255, 0, 0))
            cv2.line(img_copy, (0, event.y - 2),
                     (w - 1, event.y - 2), (255, 0, 0))
            image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im)
            self.panel.configure(image=imgtk)
            self.panel.image = imgtk
            score.mode = 3
            score.arrayContactServe[score.number] = [event.x - 2, event.y - 2]
            self.setTree()
        elif(score.mode == 3):  # コート範囲選択（4点選択）
            gimg = self.readImage(self.myval.get())
            img_copy = np.copy(gimg)
            cv2.circle(
                img_copy, (event.x - 2, event.y - 2), 2, (0, 255, 0), -1)
            score.arrayPointXY2[score.pointXYNum][0] = event.x - 2
            score.arrayPointXY2[score.pointXYNum][1] = event.y - 2
            score.pointXYNum = score.pointXYNum + 1
            if(score.pointXYNum < 4):
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
            else:
                pts = np.array([score.arrayPointXY2[0],
                                score.arrayPointXY2[1],
                                score.arrayPointXY2[2],
                                score.arrayPointXY2[3]],
                               dtype=int)
                cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
                image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
                score.pointXYNum = 0
                score.mode = 4
        elif(score.mode == 4):
            gimg = self.readImage(self.myval.get())
            pts = np.array([score.arrayPointXY2[0],
                            score.arrayPointXY2[1],
                            score.arrayPointXY2[2],
                            score.arrayPointXY2[3]],
                           dtype=int)
            img_copy = np.copy(gimg)
            cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
            h, w = img_copy.shape[0], img_copy.shape[1]
            cv2.line(img_copy, (event.x - 2, 0),
                     (event.x - 2, h - 1), (255, 0, 0))
            cv2.line(img_copy, (0, event.y - 2),
                     (w - 1, event.y - 2), (255, 0, 0))
            image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im)
            self.panel.configure(image=imgtk)
            self.panel.image = imgtk
            score.arrayContactBalls[score.number].append([score.number,
                                                          self.myval.get(),
                                                          score.arrayPointXY2[0][0],
                                                          score.arrayPointXY2[0][1],
                                                          score.arrayPointXY2[1][0],
                                                          score.arrayPointXY2[1][1],
                                                          score.arrayPointXY2[2][0],
                                                          score.arrayPointXY2[2][1],
                                                          score.arrayPointXY2[3][0],
                                                          score.arrayPointXY2[3][1],
                                                          event.x - 2,
                                                          event.y - 2])
            print("arrayContactBalls", score.arrayContactBalls)
            score.mode = 3

    def readImage(self, frameIndex):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        ok, frame = self.video.read()
        return cv2.resize(frame, (self.h, self.w))

    def imageShow(self):  # 画像描画
        gimg = self.readImage(self.myval.get())
        img_copy = np.copy(gimg)
        image_change = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image_change)
        self.imgtk = ImageTk.PhotoImage(image=im)
        self.panel.configure(image=self.imgtk)
        self.panel.image = self.imgtk

    def update(self):
        if(self.mode == 1):
            ret, frame = self.vid.get_frame()
            if ret:
                frame = cv2.resize(frame, (self.h, self.w))
                im = Image.fromarray(frame)
                self.imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=self.imgtk)
                self.panel.image = self.imgtk
                thread = threading.Thread(target=self.count_frame)
                thread.start()
                self.master.after(self.delay, self.update)
            else:
                self.mode = 0

    def count_frame(self):
            self.frame_no = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            self.myval.set(self.frame_no)

    def open_video(self):
        print("openvideo!")
        dir = 'C:\\'
        fld = filedialog.askopenfilename(
            initialdir=dir, filetypes=[
                ('Video Files', ('.mp4', '.avi'))])
        print(fld)

        videoFile = fld
        vid = video.Video(videoFile)
        self.loadVideo(vid)
        self.imageShow()
        self.sc.configure(to=self.frame_count)

    def open_data(self):
        dir = 'C:\\'
        self.fld = filedialog.askopenfilename(
            initialdir=dir, filetypes=[
                ('Db Files', ('.db'))])
        if(self.fld):
            msg = tkinter.messagebox.askyesno('save', 'データを読み込みますか？')
            if msg == 1:  # true
                #db=Database("tennis1.db",self.score)
                db = database.Database(self.fld, self.score)
                db.loadDatabase()
                score = db.dbToScore()
                self.drawContact()
                self.setTree()
                curItem = self.tree.get_children()[score.number]
                self.myval.set(int(self.tree.item(curItem)["values"][1]))
                

    def save_data(self):
        if not (self.fld):
            dir = 'C:\\'
            self.fld = filedialog.asksaveasfilename(
                initialdir=dir, filetypes=[
                    ('Db Files', ('.db'))])
            if(self.fld):
                db = database.Database(self.fld, self.score)
                db.saveDatabase()

    def save_data_as(self):
        dir = 'C:\\'
        self.fld = filedialog.asksaveasfilename(
            initialdir=dir, filetypes=[
                ('Db Files', ('.db'))])
        if(self.fld):
            db = database.Database(self.fld, self.score)
            db.saveDatabase()

    def create_menu_bar(self):
        self.menu_bar = Menu(self.master)  # Menuオブジェクト作成
        self.master.configure(menu=self.menu_bar)  # rootオブジェクトにMenuオブジェクトを設定

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Open Video', command=self.open_video)
        self.file_menu.add_command(label='Open Data', command=self.open_data)
        self.file_menu.add_command(label='Save Data', command=self.save_data)
        self.file_menu.add_command(label='Save Data As', command=self.save_data_as)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.stats_menu = Menu(self.menu_bar, tearoff=0)
        self.stats_menu.add_command(label='View Stats')
        self.menu_bar.add_cascade(label='Stats', menu=self.stats_menu)

    def create_button(self,pw):

        Button_backward100 = tkinter.Button(text=u'100←', width=10)
        Button_backward100.bind("<Button-1>", self.button_backward100)
        pw.add(Button_backward100)

        Button_backward10 = tkinter.Button(text=u'10←', width=10)
        Button_backward10.bind("<Button-1>", self.button_backward10)
        pw.add(Button_backward10)

        Button_backward1 = tkinter.Button(text=u'1←', width=10)
        Button_backward1.bind("<Button-1>", self.button_backward1)
        pw.add(Button_backward1)

        Button_forward1 = tkinter.Button(text=u'→1', width=10)
        Button_forward1.bind("<Button-1>", self.button_forward1)
        pw.add(Button_forward1)

        Button_forward10 = tkinter.Button(text=u'→10', width=10)
        Button_forward10.bind("<Button-1>", self.button_forward10)
        pw.add(Button_forward10)

        Button_forward100 = tkinter.Button(text=u'→100', width=10)
        Button_forward100.bind("<Button-1>", self.button_forward100)
        pw.add(Button_forward100)

    def create_button2(self,pw):

        Button_play = tkinter.Button(text=u'Play', width=10)
        Button_play.bind("<Button-1>", self.play)
        pw.add(Button_play)

        Button_stop = tkinter.Button(text=u'Stop', width=10)
        Button_stop.bind("<Button-1>", self.stop)
        pw.add(Button_stop)

        Button_play_scene = tkinter.Button(text=u'Play\nScene', width=10)
        Button_play_scene.bind("<Button-1>", self.play_scene)
        pw.add(Button_play_scene)

    def create_button3(self):
        if(self.score.firstServer==0):
            firstServer=tkinter.Label(text="1stServer:"+self.score.playerA)
        else:
            firstServer=tkinter.Label(text="1stServer:"+self.score.playerB)
        
        self.pw1_3.add(firstServer)

        self.pw1_3_1 = tkinter.PanedWindow(
            self.pwLeft, orient='vertical')  # ラジオボタン whichポイント
        self.pw1_3.add(self.pw1_3_1)

        self.winner.set(score.winner)
        radio1 = tkinter.Radiobutton(
            text=score.playerA,
            variable=self.winner,
            value=0,
            command=self.change_state)
        self.pw1_3_1.add(radio1)
        radio2 = tkinter.Radiobutton(
            text=score.playerB,
            variable=self.winner,
            value=1,
            command=self.change_state)
        self.pw1_3_1.add(radio2)

        label1 = tkinter.Label(text=u'のポイント')
        self.pw1_3.add(label1)

        self.Button_fault = tkinter.Button(text=u'フォルト', width=10)
        self.Button_fault.bind("<Button-1>", self.buttonFault_clicked)
        self.pw1_3.add(self.Button_fault)
        Button_end = tkinter.Button(text=u'終了フレーム', width=10)
        Button_end.bind("<Button-1>", self.button_end)
        self.pw1_3.add(Button_end)

        self.pw1_3_2 = tkinter.PanedWindow(
            self.pwLeft, orient='vertical')  # ラジオボタン サーバー
        self.pw1_3.add(self.pw1_3_2)

        self.firstServer.set(score.firstServer)
        radio3 = tkinter.Radiobutton(
            text=score.playerA,
            variable=self.firstServer,
            value=0,
            command=self.change_state)
        self.pw1_3_2.add(radio3)
        radio4 = tkinter.Radiobutton(
            text=score.playerB,
            variable=self.firstServer,
            value=1,
            command=self.change_state)
        self.pw1_3_2.add(radio4)

    def create_button4(self,pw):
        self.pw1_4_1 = tkinter.PanedWindow(self.pw1_4, orient='vertical')
        pw.add(self.pw1_4_1)
        self.pw1_4_2 = tkinter.PanedWindow(self.pw1_4, orient='vertical')
        self.pw1_4.add(self.pw1_4_2)
        self.pw1_4_3 = tkinter.PanedWindow(self.pw1_4, orient='vertical')
        self.pw1_4.add(self.pw1_4_3)

        self.Button1 = tkinter.Button(text=u'サービスエース(1)', width=20)
        self.Button1.bind("<Button-1>", self.button1_clicked)
        self.pw1_4_1.add(self.Button1)
        self.Button4 = tkinter.Button(text=u'リターンエラー(4)', width=20)
        self.Button4.bind("<Button-1>", self.button4_clicked)
        self.pw1_4_1.add(self.Button4)

        self.Button2 = tkinter.Button(text=u'ストロークウィナー(2)', width=20)
        self.Button2.bind("<Button-1>", self.button2_clicked)
        self.pw1_4_2.add(self.Button2)
        self.Button5 = tkinter.Button(text=u'ストロークエラー(5)', width=20)
        self.Button5.bind("<Button-1>", self.button5_clicked)
        self.pw1_4_2.add(self.Button5)

        self.Button3 = tkinter.Button(text=u'ボレーウィナー(3)', width=20)
        self.Button3.bind("<Button-1>", self.button3_clicked)
        self.pw1_4_3.add(self.Button3)
        self.Button6 = tkinter.Button(text=u'ボレーエラー(6)', width=20)
        self.Button6.bind("<Button-1>", self.button6_clicked)
        self.pw1_4_3.add(self.Button6)

    def create_tree(self):
        self.tree = ttk.Treeview(root, selectmode="browse")
        self.tree["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        self.tree["show"] = "headings"
        self.tree.column(1, width=30)
        self.tree.column(2, width=60)
        self.tree.column(3, width=60)
        self.tree.column(4, width=40)
        self.tree.column(5, width=40)
        self.tree.column(6, width=40)
        self.tree.column(7, width=40)
        self.tree.column(8, width=40)
        self.tree.column(9, width=75)
        self.tree.column(10, width=75)
        self.tree.column(11, width=75)
        self.tree.column(12, width=75)
        self.tree.column(13, width=40)
        self.tree.column(14, width=40)
        self.tree.heading(1, text="No")
        self.tree.heading(2, text="Start")
        self.tree.heading(3, text="End")
        self.tree.heading(4, text="Set")
        self.tree.heading(5, text="Game")
        self.tree.heading(6, text="Score")
        self.tree.heading(7, text="Result")
        self.tree.heading(8, text="Serve")
        self.tree.heading(9, text="Server")
        self.tree.heading(10, text="Won")
        self.tree.heading(11, text="Pattern")
        self.tree.heading(12, text="FrBc")
        self.tree.heading(13, text="X")
        self.tree.heading(14, text="Y")
        self.pwRightDown.add(self.tree)

    def buttonFault_clicked2(self, event):
        if(score.faultFlug == 0):
            score.faultFlug = 1
            score.arrayFirstSecond[score.number] = 1  # 1stフォルト
            score.arrayPointPattern[score.number] = score.patternString[6]
            score.arrayPointWinner[score.number] = ""
            score.pointWin[0][score.number] = 2
            score.pointWin[1][score.number] = 2

            score.calcScore()

        elif(score.faultFlug == 1):
            score.faultFlug = 0
            score.arrayFirstSecond[score.number] = 2  # 2ndフォルト=ダブルフォルト
            score.arrayPointPattern[score.number] = score.patternString[7]
            score.pointWin[(score.firstServer + score.totalGame) %
                           2][score.number] = 0
            score.pointWin[(score.firstServer + score.totalGame + 1) %
                           2][score.number] = 1
            score.arrayPointWinner[score.number] = score.playerName[(
                score.firstServer + score.totalGame + 1) % 2]

            score.calcScore()  # arrayScoreにスコアを格納
        score.arrayServer[score.number] = score.playerName[(
            score.firstServer + score.totalGame) % 2]
        self.setTree()

    

    def buttonFault_clicked(self, event):

        if(score.number == 0):
            self.firstFault()
        else:
            if(score.arrayFault[score.number - 1] == 1):  # 前のポイントが1stフォルト
                self.secondFault()
            else:
                self.firstFault()
        #print(score.arrayFault)
        #print(score.arrayFirstSecond)

        self.calcFaultAll()
        score.calcScore()

        self.setTree()
        #disabledPatternButton()

    def calcFaultAll(self):
        for i in range(len(score.arrayFault)):
            if(i > 0):
                if(score.arrayFault[i - 1] == 1):  # 前のポイントがフォルト
                    if(score.arrayFault[i] == 0):  # 現在ポイントがフォルト以外
                        print("1")
                        score.arrayFirstSecond[i] = 1
                    else:  # 現在ポイントがフォルトorダブルフォルト
                        print("2")
                        score.arrayFault[i] = 2  # ダブルフォルトにする
                else:  # 前のポイントがフォルト以外
                    if(score.arrayFault[i] == 0):  # 現在ポイントがフォルト以外
                        print("3")
                    else:  # 現在ポイントがフォルトorダブルフォルト
                        print("4")
                        score.arrayFault[i] = 1

    def firstFault(self):
        print("firstFault")
        score.arrayFault[score.number] = 1  # 2⇒ダブルフォルト 1⇒フォルト 0⇒フォルトなし
        score.arrayFirstSecond[score.number] = 1
        score.arrayPointWinner[score.number] = ""
        score.pointWin[0][score.number] = 2
        score.pointWin[1][score.number] = 2
        score.arrayPointPattern[score.number] = score.patternString[6]
        score.calcScore()
        if(score.number == (len(score.arrayFault) - 1)):
            score.faultFlug = 1

    def secondFault(self):
        print("secondFault")
        score.arrayFault[score.number] = 2  # 2⇒ダブルフォルト 1⇒フォルト 0⇒フォルトなし
        score.arrayFirstSecond[score.number] = 2
        score.arrayPointPattern[score.number] = score.patternString[7]
        score.pointWin[(score.firstServer + score.totalGame) %
                       2][score.number] = 0
        score.pointWin[(score.firstServer + score.totalGame + 1) %
                       2][score.number] = 1
        score.arrayPointWinner[score.number] = score.playerName[(
            score.firstServer + score.totalGame + 1) % 2]
        if(score.number == (len(score.arrayFault) - 1)):
            score.faultFlug = 0

    def button_end(self, event):
        if(self.myval.get() > score.arrayFrameStart[score.number]):
            end = score.arrayFrameEnd[score.number]  # 次のフレームに行く前に終了フレームを一時記憶
            score.arrayFrameEnd[score.number] = int(
                self.myval.get() - 1)  # 終了フレーム
            #normalPatternButton()
            if(score.faultFlug == 1):
                self.Button_fault["text"] = "ダブルフォルト"
            else:
                self.Button_fault["text"] = "フォルト"

            #number.set(number.get() + 1)  # 次のシーン
            score.number += 1
            score.arrayFrameStart.insert(
                score.number, int(
                    self.myval.get()))  # 開始フレーム
            score.arrayFrameEnd.insert(score.number, end)
            score.arrayPointPattern.insert(score.number, "")  # パターン
            score.arrayPointWinner.insert(score.number, "")  # ポイント勝者+
            score.pointWin[0].insert(score.number, 2)
            score.pointWin[1].insert(score.number, 2)
            score.arraySet.insert(score.number, "")  # スコア
            score.arrayGame.insert(score.number, "")  # スコア
            score.arrayScore.insert(score.number, "")  # スコア
            score.arrayScoreResult.insert(score.number, "")  # スコア
            score.arrayFirstSecond.insert(score.number, 0)  # 1st2nd
            score.arrayServer.insert(score.number, "")  # サーバー
            score.arrayForeBack.insert(score.number, "")  # フォアバック
            score.arrayCourt[0].insert(score.number, [0, 0])
            score.arrayCourt[1].insert(score.number, [0, 0])
            score.arrayCourt[2].insert(score.number, [0, 0])
            score.arrayCourt[3].insert(score.number, [0, 0])
            score.arrayContactServe.insert(score.number, [0, 0])
            score.arrayContactBalls.insert(score.number, [])

            score.arrayFault.insert(score.number, 0)

            self.setButtonFault()

            score.mode = 1

            self.setTree()

    def change_state(self):
        score.winner = self.winner.get()
        score.firstServer = self.firstServer.get()
        if (score.winner != (score.firstServer + score.totalGame + 1) % 2):
            self.Button1.configure(state="normal")
            self.Button4.configure(state="normal")
        elif (score.winner == (score.firstServer + score.totalGame + 1) % 2):
            self.Button1.configure(state="disabled")
            self.Button4.configure(state="disabled")

    def button1_clicked(self, event):  # Ace
        self.setPattern(0)

    def button2_clicked(self, event):  # STW
        self.setPattern(1)

    def button3_clicked(self, event):  # VlW
        self.setPattern(2)

    def button4_clicked(self, event):  # RtE
        self.setPattern(3)

    def button5_clicked(self, event):  # StE
        self.setPattern(4)

    def button6_clicked(self, event):  # VlE
        self.setPattern(5)

    def button_forward10(self, event):
        self.myval.set(self.myval.get() + 10)

    def button_backward10(self, event):
        self.myval.set(self.myval.get() - 10)

    def button_forward1(self, event):
        self.myval.set(self.myval.get() + 1)

    def play(self, event):
        self.vid.set_start_frame(self.myval.get())
        self.vid.set_end_frame(self.frame_count)
        self.mode = 1
        self.update()
    def keyA(self,event):
        print("test!")

    def key(self,event):
        print("pressed", repr(event.keysym))

    def stop(self, event):
        # self.vid.set_start_frame(self.myval.get())
        # self.vid.set_end_frame(score.arrayFrameEnd[score.number])
        self.mode = 0
        # self.update()

    def play_scene(self, event):
        self.vid.set_start_frame(self.myval.get())
        self.vid.set_end_frame(score.arrayFrameEnd[score.number])
        self.mode = 1
        self.update()

    def button_backward1(self, event):
        self.myval.set(self.myval.get() - 1)

    def button_forward100(self, event):
        self.myval.set(self.myval.get() + 100)

    def button_backward100(self, event):
        self.myval.set(self.myval.get() - 100)

    def setPattern(self, pattern):
        #self.setScore()
        if(score.arrayPointPattern[score.number] == ""):
            self.setPattern2(pattern)
        else:
            msg = tkinter.messagebox.askyesno('data', 'データを上書きしますか？')
            if msg == 1:
                self.setPattern2(pattern)

    def setPattern2(self, pattern):

        score.pointWin[score.winner][score.number] = 1
        score.pointWin[(score.winner + 1) % 2][score.number] = 0
        score.calcScore()  # arrayScoreにスコアを格納

        # 勝者の名前を格納
        score.arrayPointWinner[score.number] = score.playerName[score.winner]
        # パターンを格納
        score.arrayPointPattern[score.number] = score.patternString[pattern]
        if(score.number == 0):
            self.firstPattern()
        else:
            if(score.arrayFault[score.number - 1] == 1):  # 前のポイントが1stフォルト
                self.secondPattern()
            else:
                self.firstPattern()

        self.setTree()
        print("number", score.number)
        print("arrayFault", score.arrayFault)
        print("arrayFirstSecond", score.arrayFirstSecond)

    def setButtonFault(self):
        print("setButtonFault")
        print("arrayFault", score.arrayFault)
        print("score.number", score.number)

        if(score.number == 0):
            score.faultFlug = 0
        elif(score.number == 1):
            if(score.arrayFault[0] == 0):
                score.faultFlug = 0
            else:
                score.faultFlug = 1
        else:
            if((score.arrayFault[score.number - 1] - score.arrayFault[score.number - 2]) == 1):
                print("ダブルフォルト")
                score.faultFlug = 1  # ダブルフォルト
            else:
                print("フォルト")
                score.faultFlug = 0  # フォルト

        print("score.faultFlug", score.faultFlug)
        if(score.faultFlug == 1):
            print("ダブルフォルト")
            self.Button_fault["text"] = "ダブルフォルト"
        else:
            print("フォルト")
            self.Button_fault["text"] = "フォルト"

    def firstPattern(self):
        print("firstPattern")
        score.arrayFault[score.number] = 0
        score.arrayFirstSecond[score.number] = 1
        if(score.number == (len(score.arrayFault) - 1)):
            score.faultFlug = 0

    def secondPattern(self):
        print("secondPattern")
        score.arrayFault[score.number] = 0
        score.arrayFirstSecond[score.number] = 2
        if(score.number == (len(score.arrayFault) - 1)):
            score.faultFlug = 1

    def setPattern22(self, pattern):
        score.pointWin[score.winner][score.number] = 1
        score.pointWin[(score.winner + 1) % 2][score.number] = 0
        score.calcScore()  # arrayScoreにスコアを格納

        # 勝者の名前を格納
        score.arrayPointWinner[score.number] = score.playerName[score.winner]
        # パターンを格納
        score.arrayPointPattern[score.number] = score.patternString[pattern]
        if(score.faultFlug == 1):  # 前のポイントでフォルトをしていた場合
            score.arrayFirstSecond[score.number] = 2

        elif(score.faultFlug == 0):
            score.arrayFirstSecond[score.number] = 1
            if(score.number == (len(score.arrayFault) - 1)):
                score.faultFlug = 0
        self.setTree()

    def setTree(self):
        print("setTree", len(score.arrayFrameStart))
        for i, t in enumerate(self.tree.get_children()):
            self.tree.delete(t)
        for i in range(len(score.arrayFrameStart)):
            self.tree.insert("",
                             i,
                             values=(i,
                                     score.arrayFrameStart[i],
                                     score.arrayFrameEnd[i],
                                     score.arraySet[i],
                                     score.arrayGame[i],
                                     score.arrayScore[i],
                                     score.arrayScoreResult[i],
                                     score.firstSecondString[score.arrayFirstSecond[i]],
                                     score.arrayServer[i],
                                     score.arrayPointWinner[i],
                                     score.arrayPointPattern[i],
                                     "",
                                     score.arrayContactServe[i][0],
                                     score.arrayContactServe[i][1]))
        self.tree.selection_set(self.tree.get_children()[score.number])

    def select(self, event):
        curItem = self.tree.focus()
        score.number = int(self.tree.item(curItem)["values"][0])
        self.myval.set(int(self.tree.item(curItem)["values"][1]))

    def close(self):
        if(self.vid):
            self.vid.close()