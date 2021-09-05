import importlib
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
import sys
import logging
import time
import re

import score
import setting
import video
import view
import database
import track_data


class Application(tkinter.Frame):
    """
    画面アプリケーションクラス

    """

    # GUIウィンドウの設定と画像描画
    def __init__(
        self,
        score,
        mode_predict_court,
        mode_predict_player,
        mode_detect_score,
        master=None,
    ):
        super().__init__(master)
        # Instantiate other classes
        self.w = 640  # 表示画面サイズ640, 360
        self.h = 360  # 表示画面サイズ

        self.score = score
        self.view = view
        self.master = master

        self.pack()

        self.winner = tkinter.IntVar()
        self.winner.set(0)

        self.firstServer = tkinter.IntVar()
        self.firstServer.set(self.score.firstServer)

        self.delay = 33
        self.frame_count = 1
        self.mode_play = False
        self.courtsize = 360 / 27.77 * 0.8

        self.pts = np.array([[0, 0]], dtype=int)
        self.video = None
        self.clickPlayerA = False
        self.clickPlayerB = False
        self.clickCourtRightUp = False
        self.clickCourtLeftUp = False
        self.clickCourtRightDown = False
        self.clickCourtLeftDown = False

        self.mode_click_select_score_range = False
        self.click_select_score_range_active = False

        self.mouse_hover = 4
        self.move_active = False

        self.fld = "data.db"

        self.mode_predict = mode_predict_court
        self.mode_predictPlayer = mode_predict_player
        self.mode_detect_score = mode_detect_score

        self.sx1 = 0  # スコア選択領域の座標
        self.sy1 = 0  # スコア選択領域の座標
        self.sx2 = 0  # スコア選択領域の座標
        self.sy2 = 0  # スコア選択領域の座標

        p1 = [int(self.w * 2 / 3), int(self.h / 4)]
        p2 = [int(self.w / 3), int(self.h / 4)]
        p3 = [int(self.w / 6), int(self.h * 3 / 4)]
        p4 = [int(self.w * 5 / 6), int(self.h * 3 / 4)]
        self.array_court_xy = [p1, p2, p3, p4]

        if self.mode_predict:
            from predict import predict

            filepath = "./predict/weights/predict_court_10000.pth"
            self.predict = predict.Predict(filepath)
        if self.mode_predictPlayer:
            from predict import playerDetect

            filepath = "./predict/weights/ssd300_300.pth"
            self.playerDetect = playerDetect.PlayerDetect(filepath)
        if self.mode_detect_score:
            import predict.detect_score as detect_score
            from predict import detect_score

            self.ds = detect_score.DetectScore()

        self.track_data = track_data.TrackData()

        self.xa_c = 0  # player a x position on court
        self.ya_c = 0  # player a y position on court
        self.xb_c = 0  # player b x position on court
        self.yb_c = 0  # player b y position on court

        self.xball = 0
        self.yball = 0

        self.xa = 0  # player a x position on resized image
        self.xb = 0  # player a y position on resized image
        self.ya = 0  # player b x position on resized image
        self.yb = 0  # player b y position on resized image
        self.rxa = 40
        self.rya = 20
        self.rxb = 40
        self.ryb = 20

        self.num_shot = 0

    def reselectOff(self):
        self.clickPlayerA = False
        self.clickPlayerB = False
        self.clickCourtRightUp = False
        self.clickCourtLeftUp = False
        self.clickCourtRightDown = False
        self.clickCourtLeftDown = False

    def load_video(self, vid):
        self.vid = vid
        self.video = vid.video
        self.frame_count = vid.frame_count
        self.score.array_frame_end[
            len(self.score.array_frame_end) - 1
        ] = self.frame_count

        self.vid.set_start_frame(self.vid.start_frame)
        self.vid.set_end_frame(self.vid.end_frame)
        if self.vid.fps > 0:
            self.delay = int(1000 / self.vid.fps / 2)
        self.set_tree()

    def create_widgets(self):  # ウィジェット作成
        self.create_menu_bar()

        print("wh:", self.w, self.h)
        self.pw = tkinter.PanedWindow(self, orient="horizontal")  # 全画面
        self.pw.pack(expand=True)

        self.pw_left = tkinter.PanedWindow(self.pw, orient="vertical")  # 左画面
        self.pw.add(self.pw_left)

        self.pw_right = tkinter.PanedWindow(self.pw, orient="vertical")  # 右画面
        self.pw.add(self.pw_right)

        self.pw_left_up = tkinter.PanedWindow(
            self.pw_left, orient="horizontal"
        )  # 左画面の上側
        self.pw_left.add(self.pw_left_up)

        self.pw_right_up = tkinter.PanedWindow(
            self.pw_right, orient="horizontal"
        )  # 右画面の上側
        self.pw_right.add(self.pw_right_up)

        self.create_image(self.pw_left_up)  # 左画面の上側 画像描画部分
        self.create_seekbar(self.pw_left)  # 左画面の上側 スケール

        self.pw_right_up_left = tkinter.PanedWindow(
            self.pw_right_up, orient="horizontal"
        )  # pwRightUpLeft
        self.pw_right_up.add(self.pw_right_up_left)
        self.canvas1 = tkinter.Canvas(
            self.pw_right_up_left, width=195, height=380
        )  # 右画面の上テニスコート用のcanvas作成
        self.create_court(self.canvas1, self.courtsize, self.pw_right_up_left)  # テニスコート

        self.pw_right_up_right = tkinter.PanedWindow(
            self.pw_right_up, orient="horizontal"
        )  # pwRightUpRight
        self.pw_right_up.add(self.pw_right_up_right)

        self.create_shot_tree(self.pw_right_up_right)
        self.shot_tree.bind("<ButtonRelease-1>", self.select_shot)  # Double-1
        self.shot_tree.bind("<Shift-ButtonRelease-1>", self.shift_select)  # Double-1

        self.pw_left_down = tkinter.PanedWindow(
            self.pw_left, orient="horizontal"
        )  # 左画面の下側
        self.pw_left.add(self.pw_left_down)

        self.pw_right_down = tkinter.PanedWindow(
            self.pw_right, orient="vertical"
        )  # 右画面の下側
        self.pw_right.add(self.pw_right_down)

        self.pw_right_down_up = tkinter.PanedWindow(self.pw_right, orient="horizontal")
        self.pw_right_down.add(self.pw_right_down_up)

        self.entry_edit_start = ttk.Entry(self, width=10)
        self.entry_edit_end = ttk.Entry(self, width=10)
        self.entry_edit_set_a = ttk.Entry(self, width=10)
        self.entry_edit_set_b = ttk.Entry(self, width=10)
        self.entry_edit_game_a = ttk.Entry(self, width=10)
        self.entry_edit_game_b = ttk.Entry(self, width=10)
        self.entry_edit_score_a = ttk.Entry(self, width=10)
        self.entry_edit_score_b = ttk.Entry(self, width=10)

        self.pw_right_down_up.add(self.entry_edit_start)
        self.pw_right_down_up.add(self.entry_edit_end)
        self.pw_right_down_up.add(self.entry_edit_set_a)
        self.pw_right_down_up.add(self.entry_edit_set_b)
        self.pw_right_down_up.add(self.entry_edit_game_a)
        self.pw_right_down_up.add(self.entry_edit_game_b)
        self.pw_right_down_up.add(self.entry_edit_score_a)
        self.pw_right_down_up.add(self.entry_edit_score_b)

        option_serve_list = ["1st", "2nd"]
        self.variable_serve = tkinter.StringVar(self)
        self.variable_serve.set(option_serve_list[0])
        self.variable_serve.trace("w", self.option_serve)
        self.opt_serve = ttk.OptionMenu(
            self, self.variable_serve, *option_serve_list
        )
        self.pw_right_down_up.add(self.opt_serve)

        option_which_server_list = [self.score.playerName[0], self.score.playerName[1]]
        self.variable_which_server = tkinter.StringVar(self)
        self.variable_which_server.set(option_which_server_list[0])
        self.variable_which_server.trace("w", self.option_which_server)
        self.opt_server = ttk.OptionMenu(
            self, self.variable_which_server, *option_which_server_list
        )
        self.pw_right_down_up.add(self.opt_server)

        option_winner_list = [self.score.playerName[0], self.score.playerName[1]]
        self.variable_winner = tkinter.StringVar(self)
        self.variable_winner.set(option_winner_list[0])
        self.variable_winner.trace("w", self.option_winner)
        self.opt_winner = ttk.OptionMenu(
            self, self.variable_winner, *option_winner_list
        )
        self.pw_right_down_up.add(self.opt_winner)

        option_pattern_list = self.score.patternString
        self.variable_pattern = tkinter.StringVar(self)
        self.variable_pattern.set(option_pattern_list[0])
        self.variable_pattern.trace("w", self.option_pattern)
        self.opt_pattern = ttk.OptionMenu(
            self, self.variable_pattern, *option_pattern_list
        )
        self.pw_right_down_up.add(self.opt_pattern)

        button_update = ttk.Button(text=u"Update", width=10)
        button_update.bind("<Button-1>", self.button_update_tree)
        self.pw_right_down_up.add(button_update)

        self.pw_right_down_down = tkinter.PanedWindow(
            self.pw_right, orient="horizontal"
        )
        self.pw_right_down_down.pack(fill=tkinter.BOTH)
        #side=tkinter.RIGHT, fill="y")

        self.pw_right_down.add(self.pw_right_down_down)
        


        self.pw_left_down_left = tkinter.PanedWindow(
            self.pw_left_down, orient="vertical"
        )  # 左画面の下側 左
        self.pw_left_down.add(self.pw_left_down_left)

        # self.pw_left_down_right = tkinter.PanedWindow(
        #     self.pw_left_down, orient="vertical"
        # )  # 左画面の下側 右
        # self.pw_left_down.add(self.pw_left_down_right)

        self.pw1_1 = tkinter.PanedWindow(self.pw_left, orient="horizontal")  # コマ送り

        self.pw1_1.pack(expand = True, fill = tkinter.BOTH)

        self.pw_left_down_left.add(self.pw1_1)
        self.create_button_seek(self.pw1_1)

        self.pw1_2 = tkinter.PanedWindow(self.pw_left, orient="horizontal")  # 動画再生UI
        self.pw_left_down_left.add(self.pw1_2)
        self.create_button_play(self.pw1_2)

        self.pw1_3 = tkinter.PanedWindow(
            self.pw_left_down_left, orient="horizontal"
        )  # 左画面の下側 左
        self.pw_left_down_left.add(self.pw1_3)
        self.create_button_server()

        self.pw1_4 = tkinter.PanedWindow(
            self.pw_left_down_left, orient="horizontal"
        )  # 左画面の下側 左 ポイント種別
        self.pw_left_down_left.add(self.pw1_4)
        self.create_button_pointpattern(self.pw1_4)

        # self.pw_right_down_down.pack(fill=tkinter.BOTH)
        self.create_tree(self.pw_right_down_down)  # タグ一覧を右に描画
        self.set_tree()
        self.tree.bind("<ButtonRelease-1>", self.select)  # Double-1

        self.tree.selection_set(self.tree.get_children()[0])

        self.change_state()

    def create_court(self, canvas, s, pw):
        out = 5 * s
        single = 1.37 * s
        net = 0.914 * s
        canvas.create_rectangle(
            0, 0, 10.97 * s + out * 2, 23.77 * s + out * 2, fill="#2E9AFE", width=0
        )  # 塗りつぶし
        canvas.create_rectangle(
            0 + out, 0 + out, 10.97 * s + out, 23.77 * s + out, fill="#0080FF", width=0
        )  # 塗りつぶし
        canvas.create_line(
            0 + out,
            0 + out,
            10.97 * s + out,
            0 + out,
            10.97 * s + out,
            23.77 * s + out,
            0 + out,
            23.77 * s + out,
            0 + out,
            0 + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.create_line(
            0 + out - net,
            23.77 * s / 2 + out,
            10.97 * s + out + net,
            23.77 * s / 2 + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.create_line(
            0 + out + single,
            0 + out,
            0 + out + single,
            23.77 * s + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.create_line(
            10.97 * s + out - single,
            0 + out,
            10.97 * s + out - single,
            23.77 * s + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.create_line(
            10.97 * s / 2 + out,
            23.77 * s / 4 + out,
            10.97 * s / 2 + out,
            23.77 * s / 4 * 3 + out,
            fill="#FFFFFF",
            width=2.0,
        )

        canvas.create_line(
            0 + out + single,
            23.77 * s / 4 + out,
            10.97 * s + out - single,
            23.77 * s / 4 + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.create_line(
            0 + out + single,
            23.77 * s / 4 * 3 + out,
            10.97 * s + out - single,
            23.77 * s / 4 * 3 + out,
            fill="#FFFFFF",
            width=2.0,
        )
        canvas.place(x=0, y=0)
        pw.add(canvas, pady=10)

    def draw_contact_all(self):
        # print("drawContact",len(self.score.arrayContactServe))
        self.canvas1.delete("all")
        self.create_court(self.canvas1, self.courtsize, self.pw_right_up_left)
        r = 1 * 1
        s = self.courtsize
        for i in range(len(self.score.arrayContactServe)):
            self.draw_contact(i, r, s)

    def draw_contact(self, i, r, s):
        if (
            self.score.arrayContactServe[i][0] + self.score.arrayContactServe[i][1] > 0
        ):  # サーブ以外のポイントは排除
            # print(i)
            p1 = [
                float(self.score.arrayCourt[1][i][0]),
                float(self.score.arrayCourt[1][i][1]),
            ]
            p2 = [
                float(self.score.arrayCourt[2][i][0]),
                float(self.score.arrayCourt[2][i][1]),
            ]
            p3 = [
                float(self.score.arrayCourt[3][i][0]),
                float(self.score.arrayCourt[3][i][1]),
            ]
            p4 = [
                float(self.score.arrayCourt[0][i][0]),
                float(self.score.arrayCourt[0][i][1]),
            ]

            # c1,c2,c3,c4=[0, 0],[0, 23.78],[8.23, 23.78],[8.23, 0]#シングルスコートの4隅
            c1, c2, c3, c4 = (
                [10.97, 0],
                [0, 0],
                [0, 23.78],
                [10.97, 23.78],
            )  # ダブルスコートの4隅
            src_pts = np.float32([p1, p2, p3, p4]).reshape(-1, 1, 2)
            dst_pts = np.float32([c1, c2, c3, c4]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            pts = np.array(
                [
                    [
                        [
                            float(self.score.arrayContactServe[i][0]),
                            float(self.score.arrayContactServe[i][1]),
                        ]
                    ]
                ]
            )
            dst = cv2.perspectiveTransform(pts, M)

            x_temp = dst[0][0][0]
            y_temp = dst[0][0][1]

            # print("i",i)
            # print("server",self.score.arrayServer[i])
            # print("playerName[0]",self.score.playerName[0])
            # print("playerName[1]",self.score.playerName[1])
            # print(x_temp,y_temp)#4.538057930289974 4.405105323121075
            server = self.score.arrayServer[i]
            if server == "":
                # print(self.score.firstServer)
                # print(self.score.totalGame)
                server = self.score.playerName[
                    (self.score.firstServer + self.score.totalGame) % 2
                ]

            if server == self.score.playerName[0]:
                print("playerAのサーブ:", self.score.arrayFirstSecond[i])
                if y_temp < 11.89:  # 上半分の場合、そのまま表示
                    x = x_temp * s + 2 * s + 1.37 * s
                    y = y_temp * s + 2 * s
                    if self.score.arrayFirstSecond[i] == 1:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FF0000",
                            width=0,
                        )
                    elif self.score.arrayFirstSecond[i] == 2:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FFFF00",
                            width=0,
                        )
                else:  # 下半分の場合、反転して上側に表示
                    x = (8.23 - x_temp) * s + 2 * s + 1.37 * s
                    y = (23.78 - y_temp) * s + 2 * s
                    if self.score.arrayFirstSecond[i] == 1:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FF0000",
                            width=0,
                        )
                    elif self.score.arrayFirstSecond[i] == 2:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FFFF00",
                            width=0,
                        )
            elif server == self.score.playerName[1]:
                print("playerBのサーブ:", self.score.arrayFirstSecond[i])
                if y_temp >= 11.89:  # 下半分の場合、そのまま表示
                    x = x_temp * s + 2 * s + 1.37 * s
                    y = y_temp * s + 2 * s
                    if self.score.arrayFirstSecond[i] == 1:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FF0000",
                            width=0,
                        )  # 赤色
                    elif self.score.arrayFirstSecond[i] == 2:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FFFF00",
                            width=0,
                        )  # 黄色
                else:  # 上半分の場合、反転して下側に表示
                    x = (8.23 - x_temp) * s + 2 * s + 1.37 * s
                    y = (23.78 - y_temp) * s + 2 * s
                    if self.score.arrayFirstSecond[i] == 1:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FF0000",
                            width=0,
                        )
                    elif self.score.arrayFirstSecond[i] == 2:
                        self.canvas1.create_oval(
                            x - r,
                            y - r,
                            x + r,
                            y + r,
                            tag="oval",
                            fill="#FFFF00",
                            width=0,
                        )
            # print(x_temp,y_temp)
            # print(x,y)

    def create_seekbar(self, pw):
        self.pos_seek = tkinter.IntVar()
        self.pos_seek.trace("w", self.pos_seek_changed)
        self.sc = ttk.Scale(
            variable=self.pos_seek,
            orient="horizontal",
            length=self.w,
            from_=0,
            to=(self.frame_count - 1),
        )
        pw.add(self.sc, padx=10)

    def pos_seek_changed(self, *args):
        """if pos_seek changed"""
        if self.video:
            pos = int(self.pos_seek.get())
            if len(self.score.array_frame_start) > self.score.number + 1:
                print(len(self.score.array_frame_start))
                print(self.pos_seek.get())
                print(self.score.array_frame_start[self.score.number + 1])
                print(self.score.number)

                if pos > self.score.array_frame_start[self.score.number + 1]:
                    self.score.number += 1
                    self.tree.selection_set(self.tree.get_children()[self.score.number])
            elif pos < self.score.array_frame_start[self.score.number]:
                self.score.number -= 1
                self.tree.selection_set(self.tree.get_children()[self.score.number])
            if not (self.mode_play):
                self.image_show()

    def showPopup(self, event):
        self.menu_top.post(event.x_root, event.y_root)

    # def showPopup2(self,event):
    #    self.menu_top2.post(event.x_root,event.y_root)

    def selectPlayerA(self):
        self.reselectOff()
        self.clickPlayerA = True

    def selectPlayerB(self):
        self.reselectOff()
        self.clickPlayerB = True

    def selectCourtRightUp(self):
        self.reselectOff()
        self.clickCourtRightUp = True

    def selectCourtLeftUp(self):
        self.reselectOff()
        self.clickCourtLeftUp = True

    def selectCourtRightDown(self):
        self.reselectOff()
        self.clickCourtRightDown = True

    def selectCourtLeftDown(self):
        self.reselectOff()
        self.clickCourtLeftDown = True

    def select_score_range(self):
        self.mode_click_select_score_range = True

    def select_ball_position(self):
        self.mode_click_select_score_range = False

    def delete_tree_point(self):
        self.score.delete_tree_point()
        self.set_tree()
        self.active_select()

    def delete_tree_shot(self):
        curItem = self.shot_tree.focus()
        if curItem:
            self.score.delete_tree_shot_shift(self.start_shot, self.end_shot)
            self.set_shot_tree()
        else:
            tkinter.messagebox.showinfo("Error", "データが選択されていません")

    def delete_tree_shot_after_end(self):
        num = self.score.number
        end = self.score.array_frame_end[num]
        self.score.delete_after_end(num, end)
        self.set_shot_tree()

    def delete_tree_shot_after_end_all(self):
        for i in range(len(self.score.array_frame_end)):
            end = self.score.array_frame_end[i]
            print(i, end)
            self.score.delete_after_end(i, end)
        self.set_shot_tree()

    def create_image(self, pw):
        gimg = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        img_copy = np.copy(gimg)
        image_change = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image_change)
        self.imgtk = ImageTk.PhotoImage(image=im)
        self.create_right_menu()
        self.panel = tkinter.Label(self, image=self.imgtk)
        self.panel.bind("<Button-1>", self.mouse_clicked)  # マウスクリック左
        self.panel.bind("<Button-3>", self.showPopup)  # マウスクリック右
        self.panel.bind("<Motion>", self.mouse_motion)
        # self.panel.bind("<B1-Motion>", self.mouse_b1_motion)
        # self.pw_left_up.add(self.panel, padx=10, pady=10)
        pw.add(self.panel, padx=10, pady=10)

    def draw_line(self, img_copy, line, inv_M):
        """draw a line"""
        dst_inv = cv2.perspectiveTransform(line, inv_M)
        cv2.line(
            img_copy,
            (int(dst_inv[0][0][0]), int(dst_inv[0][0][1])),
            (int(dst_inv[0][1][0]), int(dst_inv[0][1][1])),
            (0, 255, 0),
            1,
        )

    def draw_court_line(self, pts, img_copy, inv_M):
        """Draw tenniscourt line on the image

        Parameters
        ----------
        pts:
        img_copy:img
        inv_M:3x3 matrix
        """
        cv2.polylines(img_copy, [pts], True, (0, 255, 0), 1)
        ph = np.array(
            [[[1.37, 11.89], [1.37 + 8.23, 11.89]]], dtype="float32"
        )  # ネットライン
        phup = np.array(
            [[[1.37, 11.89 / 2], [1.37 + 8.23, 11.89 / 2]]], dtype="float32"
        )  # サービスライン上
        phdown = np.array(
            [[[1.37, 23.78 * 3 / 4], [1.37 + 8.23, 23.78 * 3 / 4]]], dtype="float32"
        )  # サービスライン下
        centerLine = np.array(
            [[[1.37 + 8.23 / 2, 11.89 / 2], [1.37 + 8.23 / 2, 23.78 * 3 / 4]]],
            dtype="float32",
        )
        phsingleleft = np.array([[[1.37, 0], [1.37, 23.78]]], dtype="float32")  #
        phsingleright = np.array(
            [[[1.37 + 8.23, 0], [1.37 + 8.23, 23.78]]], dtype="float32"
        )  #

        self.draw_line(img_copy, ph, inv_M)
        self.draw_line(img_copy, phup, inv_M)
        self.draw_line(img_copy, phdown, inv_M)
        self.draw_line(img_copy, centerLine, inv_M)
        self.draw_line(img_copy, phsingleleft, inv_M)
        self.draw_line(img_copy, phsingleright, inv_M)
        return img_copy

    def predictTransformMatrix(self, img):
        """画像内のテニスコート4隅の点を検出
        ホモグラフィ変換して、変換行列と逆行列を作成
        検出座標をscore.arrayPointXYに格納

        Parameters
        img:img

        Returns


        """
        start_predict = time.time()
        points = self.predict.predictPoints(img)
        end_predict = time.time()
        self.pts = np.array([points[0], points[1], points[2], points[3]], dtype=int)
        p1 = np.array(points[3])
        p2 = np.array(points[0])
        p3 = np.array(points[1])
        p4 = np.array(points[2])
        c1, c2, c3, c4 = [10.97, 0], [0, 0], [0, 23.78], [10.97, 23.78]  # ダブルスコートの4隅
        src_pts = np.float32([p1, p2, p3, p4]).reshape(-1, 1, 2)
        dst_pts = np.float32([c1, c2, c3, c4]).reshape(-1, 1, 2)
        self.M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        self.inv_M = np.linalg.inv(self.M)
        end_transform = time.time()
        self.score.arrayPointXY[0][0] = points[3][0]
        self.score.arrayPointXY[0][1] = points[3][1]
        self.score.arrayPointXY[1][0] = points[0][0]
        self.score.arrayPointXY[1][1] = points[0][1]
        self.score.arrayPointXY[2][0] = points[1][0]
        self.score.arrayPointXY[2][1] = points[1][1]
        self.score.arrayPointXY[3][0] = points[2][0]
        self.score.arrayPointXY[3][1] = points[2][1]
        print(
            "predict time:total:%s predict:%s transform:%s",
            end_transform - start_predict,
            end_predict - start_predict,
            end_transform - end_predict,
        )
        logging.info(
            "predict time:total:%s predict:%s transform:%s",
            end_transform - start_predict,
            end_predict - start_predict,
            end_transform - end_predict,
        )

    def xy2leftup(self, x, y):
        """convert xy to leftup reference """
        x = round(x + 10.97 / 2, 2)
        y = round(y + 23.78 / 2, 2)
        return x, y

    def detect_player(self, img):
        """Detect Player Position A and B,Return ellipse center(x,y),radius(rx,ry)

        Parameters
        ----------
        img:img

        Returns
        ----------
        x1:ellipse center position x player A
        y1:ellipse center position y player A
        x2:ellipse center position x player B
        y2:ellipse center position y player B
        rx1:ellipse radius x player A
        ry1:ellipse radius y player A
        rx2:ellipse radius x player B
        ry2:ellipse radius y player B
        """
        start_player_tracking = time.time()
        x1, y1, x2, y2, rx1, ry1, rx2, ry2 = self.playerDetect.detect_player(img)
        end_player_tracking = time.time()
        print(
            "player predict time:total:%s", end_player_tracking - start_player_tracking
        )

        return x1, y1, x2, y2, rx1, ry1, rx2, ry2

    def detect_ball(self, event):
        bx = event.x
        by = event.y
        return bx, by

    def image_change(self, img):
        "image_change"
        image_change = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image_change)
        self.imgtk = ImageTk.PhotoImage(image=im)
        self.panel.configure(image=self.imgtk)
        self.panel.image = self.imgtk

    def array2invM(self):
        """4 corner points"""
        self.pts = np.array(
            [
                self.score.arrayPointXY[0],
                self.score.arrayPointXY[1],
                self.score.arrayPointXY[2],
                self.score.arrayPointXY[3],
            ],
            dtype=int,
        )
        p1 = np.array(self.score.arrayPointXY[0])
        p2 = np.array(self.score.arrayPointXY[1])
        p3 = np.array(self.score.arrayPointXY[2])
        p4 = np.array(self.score.arrayPointXY[3])
        self.M, self.inv_M = self.calc_inv_matrix(p1, p2, p3, p4)

    def calc_inv_matrix(self, p1, p2, p3, p4):
        """Returns Homography Matrix,and InvM,from 4 points(p1,p2,p3,p4)

        Parameters
        ----------
        p1:float [x,y] rightup corner point
        p2:float [x,y] leftup corner point
        p3:float [x,y] leftdown corner point
        p4: float [x,y] rigntdown corner point

        Returns
        M:3x3 Matrix
        inv_M:3x3 Matrix
        """
        c1, c2, c3, c4 = [10.97, 0], [0, 0], [0, 23.78], [10.97, 23.78]  # ダブルスコートの4隅
        src_pts = np.float32([p1, p2, p3, p4]).reshape(-1, 1, 2)
        dst_pts = np.float32([c1, c2, c3, c4]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        inv_M = np.linalg.inv(M)
        return M, inv_M

    def disp_position_on_image_court(self, img_copy):
        """
        映像画面とテニスコート画面のプロット位置を表示する
        """
        # 1 テニスコート画面更新
        i = self.num_shot
        self.disp_track_data_court_one(i)

        # 2 映像画面更新
        img_copy = self.draw_court_line(self.pts, img_copy, self.inv_M)
        img_copy = self.disp_circle_on_position(
            img_copy,
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            self.rxa,
            self.rya,
            self.rxb,
            self.ryb,
        )
        self.image_change(img_copy)

    def calc_bounce_shot(self, img_copy, serve_return):
        """
        ball bounce position data to array
        """
        self.score.position_data2array(
            self.xball_c,
            self.yball_c,
            "",
            "",
            "",
            "",
            serve_return,
            "Bounce",
            "",
            "Cross",
            self.pos_seek.get(),
        )

    def calc_bounce_shot_fix(self, img_copy, serve_return):
        self.xball_c, self.yball_c = self.track_data.transform_position(
            self.xball, self.yball, self.M
        )
        self.score.position_data2array_fix(
            self.xball_c,
            self.yball_c,
            "",
            "",
            "",
            "",
            serve_return,
            "Bounce",
            "",
            "Cross",
            self.pos_seek.get(),
        )

    def calc_hit_shot(self, gimg, img_copy, serve_return):
        """
        transform court position
        disp player position on court
        positioin data to array
        """
        # calc player position
        (
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            self.rxa,
            self.rya,
            self.rxb,
            self.ryb,
        ) = self.detect_player(
            gimg
        )  # 予測
        self.xa_c, self.ya_c = self.track_data.transform_position(
            self.xa, self.ya, self.M
        )  # コート座標に変換
        self.xb_c, self.yb_c = self.track_data.transform_position(
            self.xb, self.yb, self.M
        )  # コート座標に変換

        # disp player position on image
        # self.disp_circle_on_position(img_copy,self.xa_c,self.ya_c,self.xb_c,self.yb_c,self.rxa,self.rya,self.rxb,self.ryb)#プレイヤーの位置を左画面に表示
        foreback, self.yball_c = self.whichForeBack(
            self.xball_c, self.yball_c, self.xa_c, self.ya_c, self.xb_c, self.yb_c
        )  # aの位置とbの位置でボールに近い方のy座標をボールの座標として変換

        kx = self.vid.width / self.w
        ky = self.vid.height / self.h
        x1 = self.score.arrayPointXY[0][0] * kx
        y1 = self.score.arrayPointXY[0][1] * ky
        x2 = self.score.arrayPointXY[1][0] * kx
        y2 = self.score.arrayPointXY[1][1] * ky
        x3 = self.score.arrayPointXY[2][0] * kx
        y3 = self.score.arrayPointXY[2][1] * ky
        x4 = self.score.arrayPointXY[3][0] * kx
        y4 = self.score.arrayPointXY[3][1] * ky
        self.score.position_data2array_insert(
            self.xball_c,
            self.yball_c,
            self.xa_c,
            self.ya_c,
            self.xb_c,
            self.yb_c,
            serve_return,
            "Hit",
            foreback,
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            self.pos_seek.get(),
        )

    def calc_hit_shot_fix(self, gimg, img_copy, serve_return):
        self.xball_c, self.yball_c = self.track_data.transform_position(
            self.xball, self.yball, self.M
        )
        self.xa_c, self.ya_c = self.track_data.transform_position(
            self.xa, self.ya, self.M
        )
        self.xb_c, self.yb_c = self.track_data.transform_position(
            self.xb, self.yb, self.M
        )
        self.disp_circle_on_position(
            img_copy,
            self.xa_c,
            self.ya_c,
            self.xb_c,
            self.yb_c,
            self.rxa,
            self.rya,
            self.rxb,
            self.ryb,
        )  # プレイヤーの位置を左画面に表示
        foreback, self.yball_c = self.whichForeBack(
            self.xball_c, self.yball_c, self.xa_c, self.ya_c, self.xb_c, self.yb_c
        )  # aの位置とbの位置でボールに近い方のy座標をボールの座標として変換

        kx = self.vid.width / self.w
        ky = self.vid.height / self.h
        x1 = self.score.arrayPointXY[0][0] * kx
        y1 = self.score.arrayPointXY[0][1] * ky
        x2 = self.score.arrayPointXY[1][0] * kx
        y2 = self.score.arrayPointXY[1][1] * ky
        x3 = self.score.arrayPointXY[2][0] * kx
        y3 = self.score.arrayPointXY[2][1] * ky
        x4 = self.score.arrayPointXY[3][0] * kx
        y4 = self.score.arrayPointXY[3][1] * ky
        self.score.position_data2array_fix(
            self.xball_c,
            self.yball_c,
            self.xa_c,
            self.ya_c,
            self.xb_c,
            self.yb_c,
            serve_return,
            "Hit",
            foreback,
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            self.pos_seek.get(),
        )

        # save track data
        curItem = self.shot_tree.get_children()[self.num_shot]
        index = self.track_data.track_frame_array.index(
            int(self.shot_tree.item(curItem)["values"][2])
        )

        kx = self.vid.width / self.w
        ky = self.vid.height / self.h
        self.track_data.track_x1[index] = self.score.arrayPointXY[0][0] * kx
        self.track_data.track_y1[index] = self.score.arrayPointXY[0][1] * ky
        self.track_data.track_x2[index] = self.score.arrayPointXY[1][0] * kx
        self.track_data.track_y2[index] = self.score.arrayPointXY[1][1] * ky

        self.track_data.track_x3[index] = self.score.arrayPointXY[2][0] * kx
        self.track_data.track_y3[index] = self.score.arrayPointXY[2][1] * ky
        self.track_data.track_x4[index] = self.score.arrayPointXY[3][0] * kx
        self.track_data.track_y4[index] = self.score.arrayPointXY[3][1] * ky

    def mouse_motion(self, event):
        """
        画面内でマウスの移動検知
        """
        if self.video:
            if self.click_select_score_range_active:  # スコア領域の作成
                gimg = self.read_resized_image(self.pos_seek.get())
                img_copy = np.copy(gimg)
                # h, w = img_copy.shape[0], img_copy.shape[1]
                x = event.x
                y = event.y
                xmin = min(x, self.sx1)
                ymin = min(y, self.sy1)
                xmax = max(x, self.sx1)
                ymax = max(y, self.sy1)
                cv2.rectangle(
                    img_copy, (xmin, ymin), (xmax, ymax), (0, 0, 255), thickness=2
                )
                self.image_change(img_copy)
            # else:  # コート点を修正
            elif not self.move_active:
                if (  # p1近辺のとき
                    self.is_in_point(
                        event.x,
                        event.y,
                        self.array_court_xy[0][0],
                        self.array_court_xy[0][1],
                    )
                    and self.mouse_hover == 4
                ):
                    self.en_large(0)
                elif (  # p2近辺のとき
                    self.is_in_point(
                        event.x,
                        event.y,
                        self.array_court_xy[1][0],
                        self.array_court_xy[1][1],
                    )
                    and self.mouse_hover == 4
                ):
                    self.en_large(1)
                elif (  # p3近辺のとき
                    self.is_in_point(
                        event.x,
                        event.y,
                        self.array_court_xy[2][0],
                        self.array_court_xy[2][1],
                    )
                    and self.mouse_hover == 4
                ):
                    self.en_large(2)
                elif (  # p4近辺のとき
                    self.is_in_point(
                        event.x,
                        event.y,
                        self.array_court_xy[3][0],
                        self.array_court_xy[3][1],
                    )
                    and self.mouse_hover == 4
                ):
                    self.en_large(3)
                elif (
                    (
                        self.is_in_point(
                            event.x,
                            event.y,
                            self.array_court_xy[0][0],
                            self.array_court_xy[0][1],
                        )
                        == False
                    )
                    and (
                        self.is_in_point(
                            event.x,
                            event.y,
                            self.array_court_xy[1][0],
                            self.array_court_xy[1][1],
                        )
                        == False
                    )
                    and (
                        self.is_in_point(
                            event.x,
                            event.y,
                            self.array_court_xy[2][0],
                            self.array_court_xy[2][1],
                        )
                        == False
                    )
                    and (
                        self.is_in_point(
                            event.x,
                            event.y,
                            self.array_court_xy[3][0],
                            self.array_court_xy[3][1],
                        )
                        == False
                    )
                    and self.mouse_hover < 4
                ):
                    gimg = self.read_resized_image(self.pos_seek.get())
                    img_copy = np.copy(gimg)
                    img_copy = self.plot_point_on_image(img_copy, self.array_court_xy)
                    self.image_change(img_copy)
                    self.mouse_hover = 4

    def en_large(self, num):
        gimg = self.read_resized_image(self.pos_seek.get())
        img_copy = np.copy(gimg)
        img_copy = self.plot_point_on_image(img_copy, self.array_court_xy, num)
        self.image_change(img_copy)
        self.mouse_hover = num

    def is_in_point(self, mx, my, px, py):
        """マウス位置がサーブポイント近辺かどうかを検知"""
        tf = False
        r = 20
        if (px - r) < mx and mx < px + r:
            if (py - r) < my and my < py + r:
                tf = True
        return tf

    def reselect_player_after(self, resized_image_copy):
        """"""
        # 映像画面に表示 x1,y1,x2,y2を使用する
        # self.disp_circle_on_position(resized_image_copy,self.xa_c,self.ya_c,self.xb_c,self.yb_c,self.rxa,self.rya,self.rxb,self.ryb)
        # self.draw_court_line(self.pts,resized_image_copy,self.inv_M)

        self.xball_c, self.yball_c = self.track_data.transform_position(
            self.xball, self.yball, self.M
        )
        foreback, self.yball_c = self.whichForeBack(
            self.xball_c, self.yball_c, self.xa_c, self.ya_c, self.xb_c, self.yb_c
        )  # aの位置とbの位置でボールに近い方のy座標をボールの座標として変換

        # コート上の座標に更新する
        num = self.score.number
        num_shot = self.num_shot
        kx = self.vid.width / self.w
        ky = self.vid.height / self.h
        x1 = self.score.array_x1[num][num_shot] * kx
        y1 = self.score.array_y1[num][num_shot] * ky
        x2 = self.score.array_x2[num][num_shot] * kx
        y2 = self.score.array_y2[num][num_shot] * ky
        x3 = self.score.array_x2[num][num_shot] * kx
        x3 = self.score.array_x3[num][num_shot] * kx
        y3 = self.score.array_y2[num][num_shot] * ky
        y3 = self.score.array_y3[num][num_shot] * ky
        x4 = self.score.array_x4[num][num_shot] * kx
        y4 = self.score.array_y4[num][num_shot] * ky
        self.score.position_data2array_fix(
            self.xball_c,
            self.yball_c,
            self.xa_c,
            self.ya_c,
            self.xb_c,
            self.yb_c,
            1,
            "Hit",
            foreback,
            "Cross",
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
            self.pos_seek.get(),
        )
        self.disp_position_on_image_court(resized_image_copy)  # 映像画面とテニスコート画面の情報を更新

        self.set_shot_tree()

    def reselect_player_a(self, event):
        """
        選手Aの位置を再選択したときの処理
        選手Aの位置をコート座標に変換し、arrayPlayerAPositionにデータ格納
        reselect_player_afterを呼び出す
        """

        self.clickPlayerA = False
        print("reselect_player_a")
        resized_image = self.read_resized_image(self.pos_seek.get())
        resized_image_copy = np.copy(resized_image)

        # x1,y1の処理
        self.xa = event.x
        self.ya = event.y
        xa_c, ya_c = self.track_data.transform_position(
            self.xa, self.ya, self.M
        )  # 選手Aの位置をコート座標に変換
        self.score.arrayPlayerAPosition[self.score.number][self.num_shot][2] = xa_c
        self.score.arrayPlayerAPosition[self.score.number][self.num_shot][3] = ya_c
        if self.score.arrayBounceHit[self.score.number] == "Hit":
            self.score.array_ball_position_shot[self.score.number][self.num_shot] = ya_c
        self.reselect_player_after(resized_image_copy)

    def reselect_player_b(self, event):
        """
        選手Bの位置を再選択したときの処理
        選手Bの位置をコート座標に変換し、arrayPlayerBPositionにデータ格納
        reselect_player_afterを呼び出す
        """
        self.clickPlayerA = False

        print("reselect_player_b")
        resized_image = self.read_resized_image(self.pos_seek.get())
        resized_image_copy = np.copy(resized_image)

        # x2,y2の処理 残す
        self.xb = event.x
        self.yb = event.y
        xb_c, yb_c = self.track_data.transform_position(
            self.xb, self.yb, self.M
        )  # コート座標に変換
        self.score.arrayPlayerBPosition[self.score.number][self.num_shot][2] = xb_c
        self.score.arrayPlayerBPosition[self.score.number][self.num_shot][3] = yb_c
        if self.score.arrayBounceHit[self.score.number] == "Hit":
            self.score.array_ball_position_shot[self.score.number][self.num_shot] = yb_c

        self.reselect_player_after(resized_image_copy)

    def option_serve(self, *args):
        self.score.arrayFirstSecond[
            self.score.number
        ] = self.score.firstSecondString.index(self.variable_serve.get())
        self.set_tree()

    def option_which_server(self, *args):
        self.score.arrayServer[self.score.number] = self.variable_which_server.get()
        self.set_tree()

    def option_winner(self, *args):
        self.score.arrayPointWinner[self.score.number] = self.variable_winner.get()
        self.set_tree()

    def option_pattern(self, *args):
        self.score.arrayPointPattern[self.score.number] = self.variable_pattern.get()
        self.set_tree()

    def mouse_clicked(self, event):
        """画像範囲内をマウスクリックしたときの処理"""
        if self.mode_click_select_score_range:  # スコア範囲選択
            if self.click_select_score_range_active != True:
                self.sx1 = event.x
                self.sy1 = event.y
                print(self.sx1, self.sy1)
                self.click_select_score_range_active = True
            else:
                self.sx2 = event.x
                self.sy2 = event.y
                print(self.sx2, self.sy2)
                x1 = int(self.sx1 / self.w * self.vid.width)
                y1 = int(self.sy1 / self.h * self.vid.height)
                x2 = int(self.sx2 / self.w * self.vid.width)
                y2 = int(self.sy2 / self.h * self.vid.height)
                self.ds.set_xy(x1, y1, x2, y2)
                self.click_select_score_range_active = False

        elif self.clickPlayerA:  # プレイヤーAの位置
            self.reselect_player_a(event)
            self.shot_tree.selection_set(self.shot_tree.get_children()[self.num_shot])

        elif self.clickPlayerB:  # プレイヤーBの位置
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)
            x2 = event.x
            y2 = event.y
            self.yb = y2
            rx2 = 40
            ry2 = 20
            self.xb, self.yb = self.track_data.transform_position(x2, y2, self.M)
            x1 = self.xa
            y1 = self.ya
            rx1 = self.rx1
            ry1 = self.ry1
            self.disp_circle_on_position(
                resized_image_copy, x1, y1, x2, y2, rx1, ry1, rx2, ry2
            )
            self.draw_court_line(self.pts, resized_image_copy, self.inv_M)

            self.xball_c, self.yball_c = self.track_data.transform_position(
                self.xball, self.yball, self.M
            )

            foreback, self.yball_c = self.whichForeBack(
                self.xball_c, self.yball_c, self.xa_c, self.ya_c, self.xb_c, self.yb_c
            )  # aの位置とbの位置でボールに近い方のy座標をボールの座標として変換
            self.score.position_data2array_fix(
                self.xball_c,
                self.yball_c,
                self.xa_c,
                self.ya_c,
                self.xb_c,
                self.yb_c,
                1,
                "Hit",
                foreback,
                "Cross",
                self.pos_seek.get(),
            )
            # self.disp_track_data_court_all()#plotposition全て
            self.disp_track_data_court_one(i)  # plotposition全て

            self.clickPlayerB = False
            self.image_change(resized_image_copy)
            self.set_shot_tree()
        elif self.clickCourtRightUp:
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)

            self.score.arrayPointXY[0] = [event.x, event.y]
            self.array2invM()
            self.clickCourtRightUp = False
            r = self.score.rally - 1
            if r % 4 == 0:  # サーブの着地 #self.bounceAdd(self.bx,self.by_clicked,0)
                self.calc_bounce_shot_fix(resized_image_copy, 0)
            elif r % 4 == 1:  # リターン側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 1)
            elif r % 4 == 2:  # リターンの着地
                self.calc_bounce_shot_fix(resized_image_copy, 1)
            elif r % 4 == 3:  # サーブ側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 0)
            self.disp_position_on_image_court(resized_image_copy)
            self.set_shot_tree()

        elif self.clickCourtLeftUp:  # self.score.rally-1にデータを入れていく必要がある
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)

            self.score.arrayPointXY[1] = [event.x, event.y]
            self.array2invM()
            self.clickCourtLeftUp = False
            r = self.score.rally - 1
            if r % 4 == 0:  # サーブの着地 #self.bounceAdd(self.bx,self.by_clicked,0)
                self.calc_bounce_shot_fix(resized_image_copy, 0)
            elif r % 4 == 1:  # リターン側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 1)
            elif r % 4 == 2:  # リターンの着地
                self.calc_bounce_shot_fix(resized_image_copy, 1)
            elif r % 4 == 3:  # サーブ側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 0)
            self.disp_position_on_image_court(resized_image_copy)
            self.set_shot_tree()
        elif self.clickCourtLeftDown:
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)

            self.score.arrayPointXY[2] = [event.x, event.y]
            self.array2invM()
            self.clickCourtLeftDown = False
            r = self.score.rally - 1
            if r % 4 == 0:  # サーブの着地 #self.bounceAdd(self.bx,self.by_clicked,0)
                self.calc_bounce_shot_fix(resized_image_copy, 0)
            elif r % 4 == 1:  # リターン側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 1)
            elif r % 4 == 2:  # リターンの着地
                self.calc_bounce_shot_fix(resized_image_copy, 1)
            elif r % 4 == 3:  # サーブ側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 0)
            self.disp_position_on_image_court(resized_image_copy)
            self.set_shot_tree()

        elif self.clickCourtRightDown:
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)

            self.score.arrayPointXY[3] = [event.x, event.y]
            self.array2invM()
            self.clickCourtRightDown = False
            r = self.score.rally - 1
            if r % 4 == 0:  # サーブの着地 #self.bounceAdd(self.bx,self.by_clicked,0)
                self.calc_bounce_shot_fix(resized_image_copy, 0)
            elif r % 4 == 1:  # リターン側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 1)
            elif r % 4 == 2:  # リターンの着地
                self.calc_bounce_shot_fix(resized_image_copy, 1)
            elif r % 4 == 3:  # サーブ側の打点
                self.calc_hit_shot_fix(resized_image, resized_image_copy, 0)
            self.disp_position_on_image_court(resized_image_copy)
            self.set_shot_tree()

        elif self.mode_predict:  # 予測モード
            resized_image = self.read_resized_image(self.pos_seek.get())
            resized_image_copy = np.copy(resized_image)
            self.xball, self.yball = self.detect_ball(event)  # ボールを検出
            self.predictTransformMatrix(resized_image)  # テニスコート4点予測し変換行列を作成
            self.xball_c, self.yball_c = self.track_data.transform_position(
                self.xball, self.yball, self.M
            )  # clicked position to court position
            r = self.score.rally

            self.calc_hit_shot(resized_image, resized_image_copy, 0)

            self.disp_position_on_image_court(resized_image_copy)
            self.score.rally = self.score.rally + 1
            self.set_shot_tree()

        elif self.mouse_hover < 4:
            num = self.mouse_hover
            gimg = self.read_resized_image(self.pos_seek.get())
            img_copy = np.copy(gimg)
            if not self.move_active:
                img_copy = self.plot_point_on_image(
                    img_copy, self.array_court_xy, num, True
                )
                self.image_change(img_copy)
                self.move_active = True
            else:
                self.array_court_xy[num][0] = event.x
                self.array_court_xy[num][1] = event.y
                img_copy = self.plot_point_on_image(img_copy, self.array_court_xy)
                self.image_change(img_copy)
                self.move_active = False

        # self.score.arrayContactServe[self.score.number] = [
        #             event.x,
        #             event.y,
        #         ]

        # else:  # 予測モード以外　手動でコート4隅をクリックする
        # if (self.score.arrayContactServe[self.score.number][0] > 0) and (
        #     self.score.arrayContactServe[self.score.number][1] > 0
        # ):
        #     msg = tkinter.messagebox.askyesno("serve", "サーブ座標データを上書きしますか？")
        #     if msg == 1:  # true
        #         self.score.arrayContactServe[self.score.number] = [0, 0]
        # else:
        #     if self.score.mode == 0:
        #         resized_image = self.read_resized_image(self.pos_seek.get())
        #         pts, dilation = self.calcCourtPoints(resized_image)
        #         resized_image_copy = np.copy(resized_image)
        #         cv2.polylines(resized_image_copy, [pts], True, (0, 255, 0), 2)
        #         h, w = resized_image_copy.shape[0], resized_image_copy.shape[1]
        #         cv2.line(
        #             resized_image_copy,
        #             (event.x - 2, 0),
        #             (event.x - 2, h - 1),
        #             (255, 0, 0),
        #         )
        #         cv2.line(
        #             resized_image_copy,
        #             (0, event.y - 2),
        #             (w - 1, event.y - 2),
        #             (255, 0, 0),
        #         )
        #         image = cv2.cvtColor(resized_image_copy, cv2.COLOR_BGR2RGB)
        #         im = Image.fromarray(image)
        #         imgtk = ImageTk.PhotoImage(image=im)
        #         self.panel.configure(image=imgtk)
        #         self.panel.image = imgtk
        #     elif self.score.mode == 1:  #
        #         self.score.arrayCourt[self.score.pointXYNum][self.score.number][
        #             0
        #         ] = (event.x - 2)
        #         self.score.arrayCourt[self.score.pointXYNum][self.score.number][
        #             1
        #         ] = (event.y - 2)

        #         self.score.arrayPointXY[self.score.pointXYNum][0] = event.x - 2
        #         self.score.arrayPointXY[self.score.pointXYNum][1] = event.y - 2
        #         self.score.pointXYNum = self.score.pointXYNum + 1
        #         resized_image_copy = self.plot_point_on_image(
        #             self.score.arrayPointXY
        #         )
        #         self.image_change(resized_image_copy)

        #         if self.score.pointXYNum > 3:  # クリックすると1からはじまる
        #             # else:#4点目(右下)をクリック
        #             self.pts = np.array(
        #                 [
        #                     self.score.arrayPointXY[0],
        #                     self.score.arrayPointXY[1],
        #                     self.score.arrayPointXY[2],
        #                     self.score.arrayPointXY[3],
        #                 ],
        #                 dtype=int,
        #             )

        #             p1 = np.array(self.score.arrayPointXY[0])
        #             p2 = np.array(self.score.arrayPointXY[1])
        #             p3 = np.array(self.score.arrayPointXY[2])
        #             p4 = np.array(self.score.arrayPointXY[3])

        #             centerLineLeft = np.array(
        #                 (
        #                     np.array(self.score.arrayPointXY[1])
        #                     + np.array(self.score.arrayPointXY[2])
        #                 )
        #                 / 2,
        #                 dtype=int,
        #             )
        #             centerLineRignt = np.array(
        #                 (
        #                     np.array(self.score.arrayPointXY[0])
        #                     + np.array(self.score.arrayPointXY[3])
        #                 )
        #                 / 2,
        #                 dtype=int,
        #             )
        #             c1, c2, c3, c4 = (
        #                 [10.97, 0],
        #                 [0, 0],
        #                 [0, 23.78],
        #                 [10.97, 23.78],
        #             )  # ダブルスコートの4隅
        #             src_pts = np.float32([p1, p2, p3, p4]).reshape(-1, 1, 2)
        #             dst_pts = np.float32([c1, c2, c3, c4]).reshape(-1, 1, 2)

        #             self.M, mask = cv2.findHomography(
        #                 src_pts, dst_pts, cv2.RANSAC, 5.0
        #             )
        #             pts_sub = np.array(
        #                 [[centerLineLeft, centerLineRignt]], dtype="float32"
        #             )
        #             self.inv_M = np.linalg.inv(self.M)
        #             # self.image_show()

        #             self.score.pointXYNum = 0
        #             self.score.mode = 2
        #     elif self.score.mode == 2:  # 着地点をクリック　コート座標をクリックしたあと
        #         # print("mode", self.score.mode)
        #         resized_image = self.read_resized_image(self.pos_seek.get())
        #         resized_image_copy = np.copy(resized_image)
        #         self.draw_court_line(self.pts, resized_image_copy, self.inv_M)
        #         h, w = resized_image_copy.shape[0], resized_image_copy.shape[1]

        #         cv2.line(
        #             resized_image_copy,
        #             (event.x - 2, 0),
        #             (event.x - 2, h - 1),
        #             (255, 0, 0),
        #         )
        #         cv2.line(
        #             resized_image_copy,
        #             (0, event.y - 2),
        #             (w - 1, event.y - 2),
        #             (255, 0, 0),
        #         )
        #         image = cv2.cvtColor(resized_image_copy, cv2.COLOR_BGR2RGB)
        #         im = Image.fromarray(image)
        #         imgtk = ImageTk.PhotoImage(image=im)
        #         self.panel.configure(image=imgtk)
        #         self.panel.image = imgtk
        #         self.score.mode = 3

        #         self.score.arrayContactServe[self.score.number] = [
        #             event.x - 2,
        #             event.y - 2,
        #         ]

        #         self.xball_c, self.yball_c = self.track_data.transform_position(
        #             event.x - 2, event.y - 2, self.M
        #         )  # clicked position to court position センター基準
        #         # self.score.array_ball_position_shot[self.score.number][i][2]=self.xball_c
        #         # self.score.array_ball_position_shot[self.score.number][i][3]=self.xball_c
        #         # print(self.xball_c,self.yball_c)

        #         xball_c = self.score.array_ball_position_shot[self.score.number][i][
        #             2
        #         ]
        #         yball_c = self.score.array_ball_position_shot[self.score.number][i][
        #             3
        #         ]
        #         xa = self.score.arrayPlayerAPosition[self.score.number][i][2]
        #         ya = self.score.arrayPlayerAPosition[self.score.number][i][3]
        #         xb = self.score.arrayPlayerBPosition[self.score.number][i][2]
        #         yb = self.score.arrayPlayerBPosition[self.score.number][i][3]

        #     elif self.score.mode == 3:  # 着地点をクリック　ボールをクリックしたあと選手を選択
        #         resized_image = self.read_resized_image(self.pos_seek.get())
        #         resized_image_copy = np.copy(resized_image)
        #         self.draw_court_line(self.pts, resized_image_copy, self.inv_M)
        #         h, w = resized_image_copy.shape[0], resized_image_copy.shape[1]

        #         cv2.line(
        #             resized_image_copy,
        #             (event.x - 2, 0),
        #             (event.x - 2, h - 1),
        #             (255, 0, 0),
        #         )
        #         cv2.line(
        #             resized_image_copy,
        #             (0, event.y - 2),
        #             (w - 1, event.y - 2),
        #             (255, 0, 0),
        #         )
        #         image = cv2.cvtColor(resized_image_copy, cv2.COLOR_BGR2RGB)
        #         im = Image.fromarray(image)
        #         imgtk = ImageTk.PhotoImage(image=im)
        #         self.panel.configure(image=imgtk)
        #         self.panel.image = imgtk

        #         self.xball_c, self.yball_c = self.track_data.transform_position(
        #             event.x - 2, event.y - 2, self.M
        #         )  # clicked position to court position センター基準
        #         print(self.xball_c, self.yball_c)

    # def mouse_b1_motion(self, event):
    #     print("move")
    #     if self.move_active:
    #         num = self.mouse_hover
    #         gimg = self.read_resized_image(self.pos_seek.get())
    #         img_copy = np.copy(gimg)
    #         self.array_court_xy[num][0] = event.x
    #         self.array_court_xy[num][1] = event.y
    #         self.plot_point_on_image(img_copy, self.array_court_xy, num)

    def plot_point_on_image(self, img, array_xy, num_large=4, red=False):
        """
        画像のxy位置に点を表示する　４点コート用
        array_xy [[x1,y1],[x2,y2],,,]
        """
        for i in range(len(array_xy)):
            x = array_xy[i][0]
            y = array_xy[i][1]
            if i == num_large:
                if red:
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                else:
                    cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
            else:
                cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        return img

    def read_resized_image(self, frameIndex):
        """return the resized frameindex image"""
        self.video.set(cv2.CAP_PROP_POS_FRAMES, int(frameIndex))
        ok, frame = self.video.read()
        return cv2.resize(frame, (self.w, self.h))

    def plot_position(self, x, y, color="#ffff00"):
        """
        plot circle on court player position
        """
        s = self.courtsize
        r = 2
        out = 5 * s
        # single=1.37*s
        # net=0.914*s
        x0 = out
        y0 = out
        x = x * s + x0
        y = y * s + y0
        self.canvas1.create_oval(
            x - r, y - r, x + r, y + r, tag="oval", fill=color, width=0
        )

    def image_show(self):
        """
        現在のシーク位置の画像を表示する

        """
        if self.video:
            gimg = self.read_resized_image(self.pos_seek.get())
            img_copy = np.copy(gimg)
            # スコア選択領域を表示する
            cv2.rectangle(
                img_copy,
                (self.sx1, self.sy1),
                (self.sx2, self.sy2),
                (0, 0, 255),
                thickness=2,
            )
            if (
                self.pos_seek.get() in self.track_data.frame_array
            ):  # トラッキングボールデータが存在すればボール位置を表示する
                index = self.track_data.frame_array.index(self.pos_seek.get())
                x = self.track_data.all_track_ball_x[index]
                y = self.track_data.all_track_ball_y[index]
                x, y = self.resize_xy_origin2disp(x, y)
                cv2.circle(img_copy, (x, y), 2, (0, 255, 255), 1)
            img_copy = self.plot_point_on_image(
                img_copy, self.array_court_xy
            )  # コート座標を表示する

            self.image_change(img_copy)

    def resize_xy_origin2disp(self, x, y):
        # x=int(x/self.w*self.vid.width)
        # y=int(y/self.h*self.vid.height)
        x = int(x / self.vid.width * self.w)
        y = int(y / self.vid.height * self.h)
        return x, y

    def whichForeBack(self, xball_c, yball_c, xa, ya, xb, yb):
        """Compare the coordinates ball and player position a,b and return fore or back,ball y position

        Parameters
        ----------
        xball_c:int
        yball_c:int
        xa:int
        ya:int
        xb:int
        yb:int

        Returns
        ----------
        foreback:
        yball_c:

        """
        a = np.array([xa, ya])
        b = np.array([xb, yb])
        ball = np.array([xball_c, yball_c])
        a_dist = np.linalg.norm(ball - a)
        b_dist = np.linalg.norm(ball - b)
        # print(a_dist,b_dist)
        if a_dist < b_dist:  # aの方が近い
            # bx,by=self.transformPosition(bx,y1)
            yball_c = ya
            if xa > xball_c:
                foreback = "Fore"
            else:
                foreback = "Back"
        else:  # bの方が近い
            # bx,by=self.transformPosition(bx,y2)
            yball_c = yb
            if xb < xball_c:
                foreback = "Fore"
            else:
                foreback = "Back"
        return foreback, yball_c

    def plot_ball_line(self):
        s = self.courtsize
        out = 5 * s
        net = 0.914 * s
        w = 0.5
        for i in range(1, len(self.score.array_ball_position_shot[self.score.number])):
            if (
                i % 2 == 0
                and self.score.arrayBounceHit[self.score.number][i] == "Bounce"
            ):
                xball_c_pre = self.score.array_ball_position_shot[self.score.number][
                    i - 1
                ][2]
                yball_c_pre = self.score.array_ball_position_shot[self.score.number][
                    i - 1
                ][3]
                xball_c = self.score.array_ball_position_shot[self.score.number][i][2]
                yball_c = self.score.array_ball_position_shot[self.score.number][i][3]
                self.canvas1.create_line(
                    xball_c_pre * s + out,
                    yball_c_pre * s + out,
                    xball_c * s + out,
                    yball_c * s + out,
                    fill="#ffff00",
                    width=w,
                )
                w = w + 0.2

    def disp_track_data_court_all(self):
        """
        ボールと選手の位置データxyをコート画面に表示　選択ポイントの全てのショット
        """
        print("disp_track_data_court_all")
        self.canvas1.delete("all")
        self.create_court(self.canvas1, self.courtsize, self.pw_right_up_left)
        self.plot_ball_line()
        for i in range(len(self.score.array_ball_position_shot[self.score.number])):
            self.disp_track_data_court(i)

    def disp_track_data_court_one(self, i):
        """
        ボールと選手の位置データxyをコート画面に表示　選択ショットのみ
        """
        self.canvas1.delete("all")
        self.create_court(self.canvas1, self.courtsize, self.pw_right_up_left)
        self.disp_track_data_court(i)

    def disp_track_data_court(self, i):
        """
        ボールと選手の位置データxyをコート画面に表示
        """
        xball_c = self.score.array_ball_position_shot[self.score.number][i][2]
        yball_c = self.score.array_ball_position_shot[self.score.number][i][3]
        xa = self.score.arrayPlayerAPosition[self.score.number][i][2]
        ya = self.score.arrayPlayerAPosition[self.score.number][i][3]
        xb = self.score.arrayPlayerBPosition[self.score.number][i][2]
        yb = self.score.arrayPlayerBPosition[self.score.number][i][3]

        print("position ball:", i, xball_c, yball_c)
        print("position a:", i, xa, ya)
        print("position b:", i, xb, yb)
        print("position b:", i, xb, yb)

        if xball_c != "" and yball_c != "":
            xball_c, yball_c = self.xy2leftup(xball_c, yball_c)
            self.plot_position(xball_c, yball_c, "#ffff00")  # 黄色
        if xa != "" and ya != "":
            xa, ya = self.xy2leftup(xa, ya)
            self.plot_position(xa, ya, "#0000FF")  # 赤#0000FF
        if xb != "" and yb != "":
            xb, yb = self.xy2leftup(xb, yb)
            self.plot_position(xb, yb, "#FF0000")  # 青

    def dispPlayerPositionCourt(self, xball_c, yball_c, xa, ya, xb, yb):
        # print("dispPlayerPositionCourt")
        # print(xball_c,yball_c,xa,ya,xb,yb)
        self.plot_position(xball_c, yball_c, "#ffff00")
        self.plot_position(xa, ya, "#0000FF")  # 赤#0000FF
        self.plot_position(xb, yb, "#FF0000")  # 青

    def disp_circle_on_position(self, image, x1, y1, x2, y2, rx1, ry1, rx2, ry2):
        """display circle on player position a and b

        Parameters:
        image:
        x1:int x player a position
        y1:int y player a position
        x2:int x player b position
        y2:int y player b position
        rx1:int
        ry1:int
        rx2:int
        ry2:int

        Returns:
        image:
        """
        print("disp_circle_on_position")
        cv2.ellipse(image, ((x1, y1), (rx1, ry1), 0), (255, 0, 0))  # Blue
        cv2.ellipse(image, ((x2, y2), (rx2, ry2), 0), (0, 0, 255))  # Red
        return image

    def show_popup_tree(self, event):
        self.menu_top_tree.post(event.x_root, event.y_root)

    def show_popup_tree_point(self, event):
        self.menu_top_tree_point.post(event.x_root, event.y_root)

    def update(self):
        if self.mode_play:
            ret, frame = self.vid.get_frame()
            if ret:
                frame = cv2.resize(frame, (self.w, self.h))
                im = Image.fromarray(frame)
                self.imgtk = ImageTk.PhotoImage(image=im)
                self.panel.configure(image=self.imgtk)
                self.panel.image = self.imgtk
                thread = threading.Thread(target=self.count_frame)
                thread.start()
                self.master.after(self.delay, self.update)
            else:
                self.mode_play = False

    def count_frame(self):
        self.frame_no = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
        self.pos_seek.set(self.frame_no)

    def open_video(self):
        dir = "../video/"
        fld = filedialog.askopenfilename(
            initialdir=dir, filetypes=[("Video Files", (".mp4", ".avi"))]
        )

        videoFile = fld
        if len(fld) > 0:
            vid = video.Video(videoFile)
            self.load_video(vid)
            self.image_show()
            self.sc.configure(to=self.frame_count)

    def open_data(self):
        dir = "../data/"
        self.fld = filedialog.askopenfilename(
            initialdir=dir, filetypes=[("Db Files", (".db"))]
        )
        if self.fld:
            msg = tkinter.messagebox.askyesno("load", "現在のデータ上書きします。データを読み込みますか？")
            if msg == 1:  # true
                self.load_data()

    def open_track_data(self):
        dir = "../data/"
        fld = filedialog.askopenfilename(
            initialdir=dir, filetypes=[("CSV Files", (".csv"))]
        )
        if fld:
            msg = tkinter.messagebox.askyesno("load", "現在のデータ上書きします。データを読み込みますか？")
            if msg == 1:  # true
                self.load_track_data(fld)

    def load_track_data(self, fld):
        """
        track_data.csvファイルを読み込んでscoreクラスにデータを入れる
        track_data位置データXYの座標はコート中心座標、コート4点はリサイズ前画像の座標
        """
        filename = fld
        self.track_data.load_track_data(filename)  # track_dataインスタンスに変数を格納する
        frame_start = self.score.array_frame_start
        track_fame = self.track_data.track_frame_array
        bx = self.track_data.track_ball_x
        by = self.track_data.track_ball_y
        xa = self.track_data.track_player_a_x
        ya = self.track_data.track_player_a_y
        xb = self.track_data.track_player_b_x
        yb = self.track_data.track_player_b_y
        x1 = self.track_data.track_x1
        y1 = self.track_data.track_y1
        x2 = self.track_data.track_x2
        y2 = self.track_data.track_y2
        x3 = self.track_data.track_x3
        y3 = self.track_data.track_y3
        x4 = self.track_data.track_x4
        y4 = self.track_data.track_y4

        bounce_hit = self.track_data.track_hit_bounce
        self.score.divide_track_data(
            frame_start,
            track_fame,
            bx,
            by,
            xa,
            ya,
            xb,
            yb,
            bounce_hit,
            x1,
            y1,
            x2,
            y2,
            x3,
            y3,
            x4,
            y4,
        )  #
        self.score.convert_bally2playery()  # ボールy座標を選手座標に合わせる
        self.set_shot_tree()

    def load_track_ball_data(self, filename):
        self.track_data.load_ball_data(filename)

    def load_data(self):
        print("load_data")
        db = database.Database(self.fld, self.score)
        db.load_database()
        self.score = db.db2score()
        self.draw_contact_all()
        self.set_tree()
        self.set_shot_tree()
        curItem = self.tree.get_children()[score.number]
        self.pos_seek.set(int(self.tree.item(curItem)["values"][1]))

    def save_data(self):
        print("save_data")
        print(self.fld)
        if not (self.fld):
            dir = "../data/"
            self.fld = filedialog.asksaveasfilename(
                initialdir=dir, filetypes=[("Db Files", (".db"))]
            )
        if self.fld:
            settings = setting.Setting()
            settings.save_data(
                self.score.playerA,
                self.score.playerB,
                self.score.firstServer,
                self.vid.videoFileName,
                self.sx1,
                self.sy1,
                self.sx2,
                self.sy2,
            )
            db = database.Database(self.fld, self.score)
            db.save_database()

    def save_data_as(self):
        dir = "../data/"
        self.fld = filedialog.asksaveasfilename(
            initialdir=dir, filetypes=[("Db Files", (".db"))]
        )
        if self.fld:
            settings = setting.Setting()
            settings.save_data(
                self.score.playerA,
                self.score.playerB,
                self.score.firstServer,
                self.vid.videoFileName,
                self.sx1,
                self.sy1,
                self.sx2,
                self.sy2,
            )
            db = database.Database(self.fld, self.score)
            db.save_database()

    def button_edit_save(self, enent):
        self.score.playerA = self.tw_txtA.get()
        self.score.playerB = self.tw_txtB.get()
        # self.score.firstServer==0
        self.score.firstServer = self.firstServer.get()

        if self.score.firstServer == 0:
            self.label_firstServer["text"] = "1stServer:" + self.score.playerA
        else:
            self.label_firstServer["text"] = "1stServer:" + self.score.playerB

        settings = setting.Setting()
        settings.save_data(
            self.score.playerA,
            self.score.playerB,
            self.score.firstServer,
            self.vid.videoFileName,
            self.sx1,
            self.sy1,
            self.sx2,
            self.sy2,
        )

        self.sub_win.destroy()
        self.updata_button()

    def button_update_tree(self, event):
        """ Update Tree Data"""

        self.score.array_frame_start[self.score.number] = int(
            self.entry_edit_start.get()
        )
        self.score.array_frame_end[self.score.number] = int(self.entry_edit_end.get())
        set_a = self.entry_edit_set_a.get()
        set_b = self.entry_edit_set_b.get()
        set_text = set_a + "-" + set_b
        self.score.arraySet[self.score.number] = set_text

        game_a = self.entry_edit_game_a.get()
        game_b = self.entry_edit_game_b.get()
        game_text = game_a + "-" + game_b
        self.score.arrayGame[self.score.number] = game_text

        score_a = self.entry_edit_score_a.get()
        score_b = self.entry_edit_score_b.get()
        score_text = score_a + "-" + score_b
        self.score.arrayScore[self.score.number] = score_text

        self.set_tree()

    def button_edit_cancel(self, event):
        self.sub_win.destroy()

    def edit_setting(self):
        self.sub_win = tkinter.Toplevel(self.master)
        self.sub_win.title("Edit Settings")
        self.sub_win.geometry("600x200")

        label_playerA = tkinter.Label(self.sub_win, text="PlayerA : ")

        label_playerA.grid(row=0, column=0, padx=5, pady=5)

        self.tw_txtA = tkinter.Entry(self.sub_win, width=20)
        self.tw_txtA.insert(tkinter.END, self.score.playerA)
        self.tw_txtA.grid(row=0, column=1, padx=5, pady=5)

        label_playerB = tkinter.Label(self.sub_win, text="PlayerB : ")
        label_playerB.grid(row=2, column=0, padx=5, pady=5)

        self.tw_txtB = tkinter.Entry(self.sub_win, width=20)
        self.tw_txtB.insert(tkinter.END, self.score.playerB)
        self.tw_txtB.grid(row=2, column=1, padx=5, pady=5)

        self.firstServer.set(self.score.firstServer)
        labelExample = tkinter.Label(self.sub_win, text="First Server")
        labelExample.grid(row=3, column=0, padx=5, pady=5)
        radio3 = tkinter.Radiobutton(
            self.sub_win,
            text=score.playerA,
            variable=self.firstServer,
            value=0,
            command=self.change_state,
        )
        radio3.grid(row=4, column=0, padx=5, pady=5)
        radio4 = tkinter.Radiobutton(
            self.sub_win,
            text=score.playerB,
            variable=self.firstServer,
            value=1,
            command=self.change_state,
        )
        radio4.grid(row=4, column=1, padx=5, pady=5)

        button_save = ttk.Button(self.sub_win, text=u"Save", width=10)
        button_save.bind("<Button-1>", self.button_edit_save)
        button_save.grid(row=5, column=0, padx=5, pady=5)

        button_cancel = ttk.Button(self.sub_win, text=u"Cancel", width=10)
        button_cancel.bind("<Button-1>", self.button_edit_cancel)
        button_cancel.grid(row=5, column=1, padx=5, pady=5)

    def create_menu_bar(self):
        self.menu_bar = Menu(self.master)  # Menuオブジェクト作成
        self.master.configure(menu=self.menu_bar)  # rootオブジェクトにMenuオブジェクトを設定

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Video", command=self.open_video)
        self.file_menu.add_command(label="Open Data", command=self.open_data)
        self.file_menu.add_command(
            label="Open Track Data", command=self.open_track_data
        )
        self.file_menu.add_command(label="Save Data", command=self.save_data)
        self.file_menu.add_command(label="Save Data As", command=self.save_data_as)
        self.file_menu.add_command(label="Settings", command=self.edit_setting)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(
            label="Delete shot data after end frame",
            command=self.delete_tree_shot_after_end_all,
        )
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.stats_menu = Menu(self.menu_bar, tearoff=0)
        self.stats_menu.add_command(label="View Stats")
        self.menu_bar.add_cascade(label="Stats", menu=self.stats_menu)

    def create_button_seek(self, pw):
        self.img_pre100 = tkinter.PhotoImage(file="../design/pre100.png")
        Button_backward100 =  ttk.Button(width=90, image=self.img_pre100)
        Button_backward100.bind("<Button-1>", self.button_backward100)
        pw.add(Button_backward100)

        self.img_pre10 = tkinter.PhotoImage(file="../design/pre10.png")
        Button_backward10 = ttk.Button(text="", width=90, image=self.img_pre10)
        Button_backward10.bind("<Button-1>", self.button_backward10)
        pw.add(Button_backward10)

        self.img_pre1 = tkinter.PhotoImage(file="../design/pre1.png")
        Button_backward1 = ttk.Button(text="", width=85, image=self.img_pre1)
        Button_backward1.bind("<Button-1>", self.button_backward1)
        pw.add(Button_backward1)

        self.img_play_stop = tkinter.PhotoImage(file="../design/playstop.png")
        Button_play_scene = ttk.Button(text=u"", width=85, image=self.img_play_stop)
        Button_play_scene.bind("<Button-1>", self.play_scene)
        pw.add(Button_play_scene)

        self.img_forward1 = tkinter.PhotoImage(file="../design/forward1.png")
        Button_forward1 = ttk.Button(text=u"", width=85, image=self.img_forward1)
        Button_forward1.bind("<Button-1>", self.button_forward1)
        pw.add(Button_forward1)

        self.img_forward10 = tkinter.PhotoImage(file="../design/forward10.png")
        Button_forward10 = ttk.Button(text=u"", width=85, image=self.img_forward10)
        Button_forward10.bind("<Button-1>", self.button_forward10)
        pw.add(Button_forward10)

        self.img_forward100 = tkinter.PhotoImage(file="../design/forward100.png")
        Button_forward100 = ttk.Button(text="", width=85, image=self.img_forward100)
        Button_forward100.bind("<Button-1>", self.button_forward100)
        pw.add(Button_forward100)

    def create_button_play(self, pw):

        Button_score_image = ttk.Button(text=u"ScoreImage", width=8)
        Button_score_image.bind("<Button-1>", self.score_image_all)
        pw.add(Button_score_image)

        Button_score_text = ttk.Button(text=u"ScoreText", width=8)
        Button_score_text.bind("<Button-1>", self.score_text)
        pw.add(Button_score_text)

        Button_score_text = ttk.Button(text=u"CalcScore", width=8)
        Button_score_text.bind("<Button-1>", self.calc_score)
        pw.add(Button_score_text)

    def create_button_server(self):
        if self.score.firstServer == 0:
            self.label_firstServer = ttk.Label(
                text="1stServer:" + self.score.playerA
            )
        else:
            self.label_firstServer = ttk.Label(
                text="1stServer:" + self.score.playerB
            )

        self.pw1_3.add(self.label_firstServer)

        self.pw1_3_1 = tkinter.PanedWindow(
            self.pw_left, orient="vertical"
        )  # ラジオボタン whichポイント
        self.pw1_3.add(self.pw1_3_1)

        self.winner.set(self.score.winner)
        self.radio1 = tkinter.Radiobutton(
            text=self.score.playerA,
            variable=self.winner,
            value=0,
            command=self.change_state,
        )
        self.pw1_3_1.add(self.radio1)
        self.radio2 = tkinter.Radiobutton(
            text=self.score.playerB,
            variable=self.winner,
            value=1,
            command=self.change_state,
        )
        self.pw1_3_1.add(self.radio2)

        label1 = tkinter.Label(text=u"のポイント")
        self.pw1_3.add(label1)

        self.Button_fault = ttk.Button(text=u"フォルト", width=10)
        self.Button_fault.bind("<Button-1>", self.buttonFault_clicked)
        self.pw1_3.add(self.Button_fault)
        Button_end = ttk.Button(text=u"終了フレーム", width=10)
        Button_end.bind("<Button-1>", self.button_end)
        self.pw1_3.add(Button_end)

    def create_button_pointpattern(self, pw):
        self.pw1_4_1 = tkinter.PanedWindow(self.pw1_4, orient="vertical")
        pw.add(self.pw1_4_1)
        self.pw1_4_2 = tkinter.PanedWindow(self.pw1_4, orient="vertical")
        self.pw1_4.add(self.pw1_4_2)
        self.pw1_4_3 = tkinter.PanedWindow(self.pw1_4, orient="vertical")
        self.pw1_4.add(self.pw1_4_3)

        self.Button1 = ttk.Button(text=u"サービスエース(1)", width=20)
        # self.Button1 = ttk.Button(self.pw1_4_1, text=u"サービスエース(1)", width=20)
        self.Button1.bind("<Button-1>", self.button1_clicked)
        self.pw1_4_1.add(self.Button1)
        self.Button4 = ttk.Button(text=u"リターンエラー(4)", width=20)
        self.Button4.bind("<Button-1>", self.button4_clicked)
        self.pw1_4_1.add(self.Button4)

        self.Button2 = ttk.Button(text=u"ストロークウィナー(2)", width=20)
        self.Button2.bind("<Button-1>", self.button2_clicked)
        self.pw1_4_2.add(self.Button2)
        self.Button5 = ttk.Button(text=u"ストロークエラー(5)", width=20)
        self.Button5.bind("<Button-1>", self.button5_clicked)
        self.pw1_4_2.add(self.Button5)

        self.Button3 = ttk.Button(text=u"ボレーウィナー(3)", width=20)
        self.Button3.bind("<Button-1>", self.button3_clicked)
        self.pw1_4_3.add(self.Button3)

        self.Button6 = ttk.Button(text=u"ボレーエラー(6)", width=20)
        self.Button6.bind("<Button-1>", self.button6_clicked)
        self.pw1_4_3.add(self.Button6)

    def updata_button(self):
        self.radio1["text"] = self.score.playerA
        self.radio2["text"] = self.score.playerB

    def create_shot_tree(self, pw):
        self.shot_tree = ttk.Treeview(self.master, selectmode="browse", takefocus=1)
        self.shot_tree["columns"] = (1, 2, 3, 4, 5, 6)
        self.shot_tree["show"] = "headings"
        self.shot_tree.column(1, width=30)
        self.shot_tree.column(2, width=35)
        self.shot_tree.column(3, width=40)
        self.shot_tree.column(4, width=40)
        self.shot_tree.column(5, width=40)
        self.shot_tree.column(6, width=40)
        self.shot_tree.heading(1, text="No")
        self.shot_tree.heading(2, text="Rally")
        self.shot_tree.heading(3, text="Frame")
        self.shot_tree.heading(4, text="Player")
        self.shot_tree.heading(5, text="Bce/Hit")
        self.shot_tree.heading(6, text="Fr/Bc")

        vscrollbar = ttk.Scrollbar(
            self.master, orient=tkinter.VERTICAL, command=self.shot_tree.yview
        )
        pw1 = tkinter.PanedWindow(
            pw, orient="horizontal")
        pw1.add(self.shot_tree)
        
        self.shot_tree.configure(yscroll=vscrollbar.set)

        pw2 = tkinter.PanedWindow(
            pw, orient="horizontal")
        pw2.add(vscrollbar)
        pw.add(pw2)
        pw.add(pw1)


        # pw.add(self.shot_tree)
        self.create_right_menu_tree_point()
        self.shot_tree.bind("<Button-3>", self.show_popup_tree_point)

    def create_tree(self, pw):
        self.tree = ttk.Treeview(self.master, selectmode="browse", takefocus=1)
        self.tree["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)  # , 12, 13, 14
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
        # self.tree.column(12, width=75)
        # self.tree.column(13, width=40)
        # self.tree.column(14, width=40)
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
        # self.tree.heading(12, text="FrBc")
        # self.tree.heading(13, text="X")
        # self.tree.heading(14, text="Y")

        vscrollbar = ttk.Scrollbar(
            self.master, orient=tkinter.VERTICAL, command=self.tree.yview
        )
        pw1 = tkinter.PanedWindow(
            pw, orient="horizontal")
        pw1.add(self.tree)
        
        self.tree.configure(yscroll=vscrollbar.set)

        pw2 = tkinter.PanedWindow(
            pw, orient="horizontal")
        pw2.add(vscrollbar)
        pw.add(pw2)
        pw.add(pw1)

        self.create_right_menu_tree()  # 右クリックのメニュー
        self.tree.bind("<Button-3>", self.show_popup_tree)

    def create_right_menu(self):
        self.menu_top = Menu(self, tearoff=False)
        self.menu_2nd = Menu(self.menu_top, tearoff=0)
        self.menu_3rd = Menu(self.menu_top, tearoff=0)
        self.menu_top.add_cascade(label="Change Mode", menu=self.menu_2nd, under=5)
        self.menu_top.add_cascade(label="Fix Position", menu=self.menu_3rd, under=5)

        self.menu_top.add_separator()

        self.menu_2nd.add_command(
            label="Select Ball Position", under=4, command=self.select_ball_position
        )
        self.menu_2nd.add_command(
            label="Select Score Range", under=4, command=self.select_score_range
        )

        self.menu_3rd.add_command(label="PlayerA", under=4, command=self.selectPlayerA)
        self.menu_3rd.add_command(label="PlayerB", under=4, command=self.selectPlayerB)
        self.menu_3rd.add_command(
            label="CourtRightUp", under=4, command=self.selectCourtRightUp
        )
        self.menu_3rd.add_command(
            label="CourtLeftUp", under=4, command=self.selectCourtLeftUp
        )
        self.menu_3rd.add_command(
            label="CourtLeftDown", under=4, command=self.selectCourtLeftDown
        )
        self.menu_3rd.add_command(
            label="CourtRightDown", under=4, command=self.selectCourtRightDown
        )

    def create_right_menu_tree(self):
        """データ画面で右クリックしたときのメニュー画面"""
        self.menu_top_tree = Menu(self, tearoff=False)

        self.menu_top_tree.add_command(
            label="Delete", underline=5, command=self.delete_tree_point
        )

        self.menu_top_tree.add_command(
            label="Auto Score 1 Point", underline=5, command=self.score_image2text_one
        )

        self.menu_top_tree.add_command(
            label="Auto Score All", underline=5, command=self.score_image2text_all
        )

    def create_right_menu_tree_point(self):
        self.menu_top_tree_point = Menu(self, tearoff=False)

        self.menu_top_tree_point.add_command(
            label="データ削除", underline=5, command=self.delete_tree_shot
        )

        self.menu_top_tree_point.add_command(
            label="Endフレーム以降のデータ削除",
            underline=5,
            command=self.delete_tree_shot_after_end,
        )

        self.menu_top_tree_point.add_command(
            label="No Bounce", underline=5, command=self.no_bound
        )

        self.menu_top_tree_point.add_command(
            label="Detete Last Shot", underline=5, command=self.delete_last_shot
        )

    def buttonFault_clicked2(self, event):
        if self.score.faultFlug == 0:
            self.score.faultFlug = 1
            self.score.arrayFirstSecond[self.score.number] = 1  # 1stフォルト
            self.score.arrayPointPattern[self.score.number] = self.score.patternString[
                6
            ]
            self.score.arrayPointWinner[self.score.number] = ""
            self.score.pointWin[0][self.score.number] = 2
            self.score.pointWin[1][self.score.number] = 2

            self.score.calcScore()

        elif self.score.faultFlug == 1:
            self.score.faultFlug = 0
            self.score.arrayFirstSecond[self.score.number] = 2  # 2ndフォルト=ダブルフォルト
            self.score.arrayPointPattern[self.score.number] = self.score.patternString[
                7
            ]
            self.score.pointWin[(self.score.firstServer + self.score.totalGame) % 2][
                self.score.number
            ] = 0
            self.score.pointWin[
                (self.score.firstServer + self.score.totalGame + 1) % 2
            ][self.score.number] = 1
            self.score.arrayPointWinner[self.score.number] = self.score.playerName[
                (self.score.firstServer + self.score.totalGame + 1) % 2
            ]

            self.score.calcScore()  # arrayScoreにスコアを格納
        self.score.arrayServer[self.score.number] = self.score.playerName[
            (self.score.firstServer + self.score.totalGame) % 2
        ]
        self.set_tree()

    def buttonFault_clicked(self, event):
        """calc when button fault clicked
        if pre point is fault,2nd fault


        """

        if self.score.number == 0:
            self.first_fault()
        else:
            if self.score.arrayFault[self.score.number - 1] == 1:  # 前のポイントが1stフォルト
                self.second_fault()
            else:
                self.first_fault()

        self.calc_fault_all()
        self.score.calcScore()
        self.set_tree()

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

        # todo Noneや""の場合は、飛ばして次の計算をするようにしたい
        print("self.score.arrayFault:", self.score.arrayFault)
        pre = None
        current = None
        for i in range(len(self.score.arrayFault)):
            if i > 0:
                if self.score.arrayFault[i - 1] != None:
                    pre = self.score.arrayFault[i - 1]
                if self.score.arrayFault[i] != None:
                    current = self.score.arrayFault[i]
                if pre != None and current != None:
                    if pre == 1:  # 前のポイントがフォルト
                        if current == 0:  # 現在ポイントがフォルト以外
                            # print("1")
                            self.score.arrayFirstSecond[i] = 1  # 0じゃない？
                        # else:  # 現在ポイントがフォルトorダブルフォルト
                        elif current > 0:  # 現在ポイントがフォルトorダブルフォルト
                            # print("2")
                            self.score.arrayFault[i] = 2  # ダブルフォルトにする
                    else:  # 前のポイントがフォルト以外
                        if current == 0:  # 現在ポイントがフォルト以外
                            print("3")
                        # else:  # 現在ポイントがフォルトorダブルフォルト
                        elif current > 0:  # 現在ポイントがフォルトorダブルフォルト
                            # print("4")
                            self.score.arrayFault[i] = 1
                else:
                    if self.score.arrayFault[i - 1] == None:
                        self.score.arrayFirstSecond[i - 1] = 0
                    if self.score.arrayFault[i] == None:
                        self.score.arrayFirstSecond[i] = 0

    def first_fault(self):
        print("firstFault")
        self.score.arrayFault[self.score.number] = 1  # 2⇒ダブルフォルト 1⇒フォルト 0⇒フォルトなし
        self.score.arrayFirstSecond[self.score.number] = 1
        # self.score.arrayServer[self.score.number] =
        self.score.arrayPointWinner[self.score.number] = ""
        self.score.pointWin[0][self.score.number] = 2
        self.score.pointWin[1][self.score.number] = 2
        self.score.arrayPointPattern[self.score.number] = self.score.patternString[6]
        self.score.calcScore()
        if self.score.number == (len(self.score.arrayFault) - 1):
            self.score.faultFlug = 1

    def second_fault(self):
        print("secondFault")
        self.score.arrayFault[self.score.number] = 2  # 2⇒ダブルフォルト 1⇒フォルト 0⇒フォルトなし
        self.score.arrayFirstSecond[self.score.number] = 2
        self.score.arrayPointPattern[self.score.number] = self.score.patternString[7]
        self.score.pointWin[(self.score.firstServer + self.score.totalGame) % 2][
            self.score.number
        ] = 0
        self.score.pointWin[(self.score.firstServer + self.score.totalGame + 1) % 2][
            self.score.number
        ] = 1
        self.score.arrayPointWinner[self.score.number] = self.score.playerName[
            (self.score.firstServer + self.score.totalGame + 1) % 2
        ]
        if self.score.number == (len(self.score.arrayFault) - 1):
            self.score.faultFlug = 0

    def button_end(self, event):
        if self.pos_seek.get() > self.score.array_frame_start[self.score.number]:
            end = self.score.array_frame_end[
                self.score.number
            ]  # 次のフレームに行く前に終了フレームを一時記憶
            self.score.array_frame_end[self.score.number] = int(
                self.pos_seek.get() - 1
            )  # 終了フレーム
            # normalPatternButton()
            if self.score.faultFlug == 1:
                self.Button_fault["text"] = "ダブルフォルト"
            else:
                self.Button_fault["text"] = "フォルト"

            # number.set(number.get() + 1)  # 次のシーン
            self.score.number += 1
            self.score.array_frame_start.insert(
                self.score.number, int(self.pos_seek.get())
            )  # 開始フレーム
            self.score.array_frame_end.insert(self.score.number, end)
            self.score.arrayPointPattern.insert(self.score.number, "")  # パターン
            self.score.arrayPointWinner.insert(self.score.number, "")  # ポイント勝者+
            self.score.pointWin[0].insert(self.score.number, 2)
            self.score.pointWin[1].insert(self.score.number, 2)
            self.score.arraySet.insert(self.score.number, "")  # スコア
            self.score.arrayGame.insert(self.score.number, "")  # スコア
            self.score.arrayScore.insert(self.score.number, "")  # スコア
            self.score.arrayScoreResult.insert(self.score.number, "")  # スコア
            self.score.arrayFirstSecond.insert(self.score.number, 0)  # 1st2nd
            self.score.arrayServer.insert(self.score.number, "")  # サーバー
            # self.score.arrayForeBack.insert(self.score.number, "")  # フォアバック
            self.score.arrayCourt[0].insert(self.score.number, [0, 0])
            self.score.arrayCourt[1].insert(self.score.number, [0, 0])
            self.score.arrayCourt[2].insert(self.score.number, [0, 0])
            self.score.arrayCourt[3].insert(self.score.number, [0, 0])
            self.score.arrayContactServe.insert(self.score.number, [0, 0])
            print(
                "self.score.array_ball_position_shot:",
                self.score.array_ball_position_shot,
            )
            self.score.arrayFault.insert(self.score.number, 0)
            self.score.nextAppend()
            self.setButtonFault()

            self.score.mode = 1

            self.set_tree()

    def change_state(self):
        self.score.winner = self.winner.get()
        # score.firstServer = self.firstServer.get()
        if self.score.winner != (self.score.firstServer + self.score.totalGame + 1) % 2:
            self.Button1.configure(state="normal")
            self.Button4.configure(state="normal")
        elif (
            self.score.winner == (self.score.firstServer + self.score.totalGame + 1) % 2
        ):
            self.Button1.configure(state="disabled")
            self.Button4.configure(state="disabled")

    def key_activate(self):
        self.focus_set()

    def button1_clicked(self, event):  # Ace
        self.setPattern(0)

    def button2_clicked(self, event):  # STW
        self.setPattern(1)

    def button3_clicked(self, event):  # VlW
        self.setPattern(2)
        # self.after(5000,self.setPattern(2))
        # self.master.after(1000,self.showerror())
        # self.Button3.configure(relief="raised")

    def button4_clicked(self, event):  # RtE
        self.setPattern(3)

    def button5_clicked(self, event):  # StE
        self.setPattern(4)

    def button6_clicked(self, event):  # VlE
        self.setPattern(5)

    def button_forward10(self, event):
        self.pos_seek.set(self.pos_seek.get() + 10)

    def button_backward10(self, event):
        self.pos_seek.set(self.pos_seek.get() - 10)

    def button_forward1(self, event):
        self.pos_seek.set(self.pos_seek.get() + 1)
        self.focus_set()

    def play(self, event):
        self.vid.set_start_frame(self.pos_seek.get())
        self.vid.set_end_frame(self.frame_count)
        self.mode = True
        self.update()

    def keyA(self, event):
        print("test!")

    def key(self, event):
        print("pressed", repr(event.keysym))

    def stop(self, event):
        # self.vid.set_start_frame(self.myval.get())
        # self.vid.set_end_frame(score.array_frame_end[score.number])
        self.mode_play = False
        # self.update()

    def play_scene(self, event):
        if self.vid:
            if self.mode_play:
                self.mode_play = False
            else:
                self.vid.set_start_frame(self.pos_seek.get())
                self.vid.set_end_frame(self.score.array_frame_end[self.score.number])
                self.mode_play = True
                self.update()

    def button_backward1(self, event):
        self.pos_seek.set(self.pos_seek.get() - 1)

    def button_forward100(self, event):
        self.pos_seek.set(self.pos_seek.get() + 100)

    def button_backward100(self, event):
        self.pos_seek.set(self.pos_seek.get() - 100)

    def button_delete_tree_point(self, event):
        self.delete_tree_point()

    def delete_last_shot(self):
        print("delete_last_shot")
        if self.score.rally > 0:
            self.score.rally = self.score.rally - 1
            self.score.array_ball_position_shot[self.score.number].pop(-1)
            self.score.arrayPlayerAPosition[self.score.number].pop(-1)
            self.score.arrayPlayerBPosition[self.score.number].pop(-1)
            self.score.arrayHitPlayer[self.score.number].pop(-1)
            self.score.arrayBounceHit[self.score.number].pop(-1)
            self.score.arrayForeBack[self.score.number].pop(-1)
            self.score.arrayDirection[self.score.number].pop(-1)
            self.set_shot_tree()
            self.disp_track_data_court_all()

    def no_bound(self):
        self.score.position_data2array(
            "", "", "", "", "", "", 1, "NoBounce", "", "", self.pos_seek.get()
        )
        self.score.rally = self.score.rally + 1
        self.set_shot_tree()

    def score_image2text_one(self):
        i = self.score.number
        self.score_image_one(i)  # image
        self.score_text_one(i)  # image->score
        self.set_tree()

    def score_image_one(self, i):
        """
        save trim bounding box image at one start_frame to png file
        """
        start_list = self.score.array_frame_start

        self.ds.frame2oneimage(i, start_list, self.vid.videoFileName)
        game_a, game_b, score_a, score_b = self.ds.image2onescore(i)
        print(game_a, game_b, score_a, score_b)
        self.score.arrayGame[i] = str(game_a) + "-" + str(game_b)
        self.score.arrayScore[i] = str(score_a) + "-" + str(score_b)

    def score_text_one(self, i):
        game_a, game_b, score_a, score_b = self.ds.image2onescore(i)
        self.score.arrayGame[i] = str(game_a) + "-" + str(game_b)
        self.score.arrayScore[i] = str(score_a) + "-" + str(score_b)

    def score_image2text_all(self):
        self.score_image_all()  # image
        start_list = self.score.array_frame_start[0:10]
        for i in range(len(start_list)):
            self.score_image_one(i)

        # game_a_array,game_b_array,score_a_array,score_b_array=self.ds.image2scores()#image->score

        # ここにしたをかく
        # game_a,game_b,score_a,score_b=self.ds.image2onescore(i)
        # self.score.arrayGame[i]=str(game_a)+"-"+str(game_b)
        # self.score.arrayScore[i]=str(score_a)+"-"+str(score_b)

        self.set_tree()

    def score_image_all(self, event):
        """save trim bounding box image at all start_frame to png file"""
        # start_list=[0,800,1031,1672,2564,3346,2350,3862,4180,6028,6738,7091,7969,7981,8564,9080,9796,
        #             10172,11097,11498,11900]
        # start_list=[0,800,1031,1672,2564]
        start_list = self.score.array_frame_start[0:10]
        self.ds.frame2images(start_list, self.vid.videoFileName)

    def score_image_all(self):
        """save trim bounding box image at all start_frame to png file"""
        # start_list=[0,800,1031,1672,2564,3346,2350,3862,4180,6028,6738,7091,7969,7981,8564,9080,9796,
        #             10172,11097,11498,11900]
        # start_list=[0,800,1031,1672,2564]
        start_list = self.score.array_frame_start[0:10]
        self.ds.frame2images(start_list, self.vid.videoFileName)

    def score_text(self, event):

        (
            game_a_array,
            game_b_array,
            score_a_array,
            score_b_array,
        ) = self.ds.image2scores()
        print(game_a_array)
        print(game_b_array)
        print(score_a_array)
        print(score_b_array)

        for i in range(len(game_a_array)):
            self.score.arrayGame[i] = str(game_a_array[i]) + "-" + str(game_b_array[i])
            self.score.arrayScore[i] = (
                str(score_a_array[i]) + "-" + str(score_b_array[i])
            )
        print(self.score.arrayGame)
        print(self.score.arrayScore)
        self.set_tree()

    def calc_score(self, event):
        winner_list = self.score.get_winner_list(self.score.arrayScore)
        print(winner_list)
        (
            point_winner_array,
            first_second_array,
            self.score.arrayPointPattern,
        ) = self.score.winner2player_fault(
            winner_list, self.score.playerName, self.score.arrayPointPattern
        )
        self.score.arrayPointWinner = point_winner_array
        self.score.arrayFirstSecond = first_second_array
        print(point_winner_array)
        print(first_second_array)
        self.set_tree()

    def show_pattern_message(self, pattern):
        print("show_pattern_message")
        msg = tkinter.messagebox.askyesno("data", "データを上書きしますか？")
        if msg == 1:
            self.master.after(1, self.setPattern2(pattern))
            # self.setPattern2(pattern)

    def setPattern(self, pattern):
        # self.setScore()
        if self.score.arrayPointPattern[self.score.number] == "":
            self.setPattern2(pattern)
        else:
            msg = tkinter.messagebox.askyesno("data", "データを上書きしますか？")
            if msg == 1:
                # self.master.after(1 ,self.show_pattern_message(pattern))
                self.setPattern2(pattern)

    def setPattern2(self, pattern):
        self.score.pointWin[self.score.winner][self.score.number] = 1
        self.score.pointWin[(self.score.winner + 1) % 2][self.score.number] = 0
        self.score.calcScore()  # arrayScoreにスコアを格納

        # 勝者の名前を格納
        self.score.arrayPointWinner[self.score.number] = self.score.playerName[
            self.score.winner
        ]
        # パターンを格納
        self.score.arrayPointPattern[self.score.number] = self.score.patternString[
            pattern
        ]
        if self.score.number == 0:
            self.firstPattern()
        else:
            if self.score.arrayFault[self.score.number - 1] == 1:  # 前のポイントが1stフォルト
                self.secondPattern()
            else:
                self.firstPattern()

        self.set_tree()
        # self.master.after(1,self.setTree())

        print("number", self.score.number)
        print("arrayFault", self.score.arrayFault)
        print("arrayFirstSecond", self.score.arrayFirstSecond)
        print("arrayScore", self.score.arrayScore)

    def setButtonFault(self):
        print("setButtonFault")
        print("arrayFault", self.score.arrayFault)
        print("score.number", self.score.number)

        if self.score.number == 0:
            self.score.faultFlug = 0
        elif self.score.number == 1:
            if self.score.arrayFault[0] == 0:
                self.score.faultFlug = 0
            else:
                self.score.faultFlug = 1
        else:
            if (
                self.score.arrayFault[self.score.number - 1]
                - self.score.arrayFault[self.score.number - 2]
            ) == 1:
                print("ダブルフォルト")
                self.score.faultFlug = 1  # ダブルフォルト
            else:
                print("フォルト")
                self.score.faultFlug = 0  # フォルト

        print("score.faultFlug", self.score.faultFlug)
        if self.score.faultFlug == 1:
            print("ダブルフォルト")
            self.Button_fault["text"] = "ダブルフォルト"
        else:
            print("フォルト")
            self.Button_fault["text"] = "フォルト"

    def firstPattern(self):
        print("firstPattern")
        self.score.arrayFault[self.score.number] = 0
        self.score.arrayFirstSecond[self.score.number] = 1
        if self.score.number == (len(self.score.arrayFault) - 1):
            self.score.faultFlug = 0

    def secondPattern(self):
        print("secondPattern")
        self.score.arrayFault[self.score.number] = 0
        self.score.arrayFirstSecond[self.score.number] = 2
        if self.score.number == (len(self.score.arrayFault) - 1):
            self.score.faultFlug = 1

    def setPattern22(self, pattern):
        self.score.pointWin[self.score.winner][self.score.number] = 1
        self.score.pointWin[(self.score.winner + 1) % 2][self.score.number] = 0
        self.score.calcScore()  # arrayScoreにスコアを格納

        # 勝者の名前を格納
        self.score.arrayPointWinner[self.score.number] = self.score.playerName[
            self.score.winner
        ]
        # パターンを格納
        self.score.arrayPointPattern[self.score.number] = self.score.patternString[
            pattern
        ]
        if self.score.faultFlug == 1:  # 前のポイントでフォルトをしていた場合
            self.score.arrayFirstSecond[self.score.number] = 2

        elif self.score.faultFlug == 0:
            self.score.arrayFirstSecond[self.score.number] = 1
            if self.score.number == (len(self.score.arrayFault) - 1):
                self.score.faultFlug = 0
        self.set_tree()

    def set_shot_tree(self):
        print("self.score.number:", self.score.number)
        # print("len(self.score.array_ball_position_shot[self.score.number]):",len(self.score.array_ball_position_shot[self.score.number]))
        for i, t in enumerate(self.shot_tree.get_children()):
            self.shot_tree.delete(t)
        for i in range(len(self.score.array_ball_position_shot[self.score.number])):
            print("i", i)
            self.shot_tree.insert(
                "",
                i,
                values=(
                    self.score.number,
                    (i + 1),
                    self.score.array_ball_position_shot[self.score.number][i][1],
                    self.score.arrayHitPlayer[self.score.number][i],
                    self.score.arrayBounceHit[self.score.number][i],
                    self.score.arrayForeBack[self.score.number][i],
                ),
            )  # self.score.arrayDirection[self.score.number][i]

    def set_tree(self):

        for i, t in enumerate(self.tree.get_children()):
            self.tree.delete(t)
        for i in range(len(self.score.array_frame_start)):
            self.tree.insert(
                "",
                i,
                values=(
                    i,
                    self.score.array_frame_start[i],
                    self.score.array_frame_end[i],
                    self.score.arraySet[i],
                    self.score.arrayGame[i],
                    self.score.arrayScore[i],
                    self.score.arrayScoreResult[i],
                    self.score.firstSecondString[self.score.arrayFirstSecond[i]],
                    self.score.arrayServer[i],
                    self.score.arrayPointWinner[i],
                    self.score.arrayPointPattern[i],
                ),
            )
        self.tree.selection_set(self.tree.get_children()[self.score.number])

    def button_select_up(self, event):
        self.score.number -= 1
        curItem = self.tree.get_children()[score.number]
        self.tree.selection_set(curItem)
        self.pos_seek.set(int(self.tree.item(curItem)["values"][1]))
        self.key_activate()
        self.set_shot_tree()  # 追加
        self.disp_edit_tree(self.score.number)

    def button_select_down(self, event):
        self.score.number += 1
        curItem = self.tree.get_children()[score.number]
        self.tree.selection_set(curItem)
        self.pos_seek.set(int(self.tree.item(curItem)["values"][1]))
        self.key_activate()
        self.set_shot_tree()  # 追加
        self.disp_edit_tree(self.score.number)

    def select(self, event):
        print("tree_select")
        curItem = self.tree.focus()
        self.score.number = int(self.tree.item(curItem)["values"][0])
        print(self.score.number)
        self.pos_seek.set(int(self.tree.item(curItem)["values"][1]))  # フレーム位置変更
        self.key_activate()
        self.set_shot_tree()  # 追加
        self.disp_edit_tree(self.score.number)

    def active_select(self):
        curItem = self.tree.get_children()[score.number]
        self.pos_seek.set(int(self.tree.item(curItem)["values"][1]))
        self.key_activate()
        self.set_shot_tree()  # 追加
        self.disp_edit_tree(self.score.number)

    def shift_select(self, event):
        print("shift")
        # tree = event.widget

        i = self.num_shot
        cur_item = self.shot_tree.focus()
        j = int(self.shot_tree.item(cur_item)["values"][1]) - 1
        self.start_shot = min(i, j)
        self.end_shot = max(i, j)
        for i in range(self.start_shot, self.end_shot):
            self.shot_tree.selection_add(self.shot_tree.get_children()[i])

    def select_shot(self, event):
        """
        when select shot tree
        """
        curItem = self.shot_tree.focus()
        self.pos_seek.set(int(self.shot_tree.item(curItem)["values"][2]))
        self.num_shot = int(self.shot_tree.item(curItem)["values"][1]) - 1

        self.start_shot = self.num_shot
        self.end_shot = self.num_shot

        # disp 4 corner points
        # search match frame
        risized_image = self.read_resized_image(self.pos_seek.get())
        resized_image_copy = np.copy(risized_image)

        kx = self.w / self.vid.width
        ky = self.h / self.vid.height
        i = self.score.number
        j = self.num_shot

        # コート座標が4つ存在するときに計算　コート座標⇒変換行列⇒コート座標に変換
        # 保存されているデータがコート中心座標なので、
        if (
            self.score.array_x1[i][j]
            or self.score.array_x2[i][j]
            or self.score.array_x3[i][j]
            or self.score.array_x4[i][j]
        ):
            self.score.arrayPointXY[0] = [
                self.score.array_x1[i][j] * kx,
                self.score.array_y1[i][j] * ky,
            ]
            self.score.arrayPointXY[1] = [
                self.score.array_x2[i][j] * kx,
                self.score.array_y2[i][j] * ky,
            ]
            self.score.arrayPointXY[2] = [
                self.score.array_x3[i][j] * kx,
                self.score.array_y3[i][j] * ky,
            ]
            self.score.arrayPointXY[3] = [
                self.score.array_x4[i][j] * kx,
                self.score.array_y4[i][j] * ky,
            ]
            self.array2invM()
            self.draw_court_line(
                self.pts, resized_image_copy, self.inv_M
            )  # テニスコートラインを描画

            # #xy2leftup　コート中心座標をコート左上座標に変換
            print(
                self.score.arrayPlayerAPosition[i][j],
                self.score.arrayPlayerAPosition[i][j],
            )
            print(
                self.score.arrayPlayerBPosition[i][j],
                self.score.arrayPlayerBPosition[i][j],
            )
            self.xa_c, self.ya_c = self.track_data.xy2leftup(
                self.score.arrayPlayerAPosition[i][j][2],
                self.score.arrayPlayerAPosition[i][j][3],
            )
            self.xb_c, self.yb_c = self.track_data.xy2leftup(
                self.score.arrayPlayerBPosition[i][j][2],
                self.score.arrayPlayerBPosition[i][j][3],
            )

            # コート座標を映像座標に変換する
            pts = np.array([[[float(self.xa_c), float(self.ya_c)]]])
            dst = cv2.perspectiveTransform(pts, self.inv_M)  # self.M
            hx = dst[0][0][0]
            hy = dst[0][0][1]
            self.xa = hx
            self.ya = hy

            pts = np.array([[[float(self.xb_c), float(self.yb_c)]]])
            dst = cv2.perspectiveTransform(pts, self.inv_M)  # self.M
            hx = dst[0][0][0]
            hy = dst[0][0][1]
            self.xb = hx
            self.yb = hy

            self.disp_position_on_image_court(resized_image_copy)

    def disp_edit_tree(self, i):
        self.entry_edit_start.delete(0, tkinter.END)
        self.entry_edit_end.delete(0, tkinter.END)
        self.entry_edit_set_a.delete(0, tkinter.END)
        self.entry_edit_set_b.delete(0, tkinter.END)
        self.entry_edit_game_a.delete(0, tkinter.END)
        self.entry_edit_game_b.delete(0, tkinter.END)
        self.entry_edit_score_a.delete(0, tkinter.END)
        self.entry_edit_score_b.delete(0, tkinter.END)

        print(self.score.arraySet[i])

        self.entry_edit_start.insert(tkinter.END, self.score.array_frame_start[i])
        self.entry_edit_end.insert(tkinter.END, self.score.array_frame_end[i])

        if self.score.arraySet[i] is not None:
            text_set = self.score.arraySet[i]
            left = re.findall(r"([0-9a-zA-Z]*)-", text_set)
            right = re.findall(r"-([0-9a-zA-Z]*)", text_set)
            if len(left):
                self.entry_edit_set_a.insert(tkinter.END, left[0])
            if len(right):
                self.entry_edit_set_b.insert(tkinter.END, right[0])

        if self.score.arrayGame[i] is not None:
            text_game = self.score.arrayGame[i]
            left = re.findall(r"([0-9a-zA-Z]*)-", text_game)
            right = re.findall(r"-([0-9a-zA-Z]*)", text_game)
            if len(left):
                self.entry_edit_game_a.insert(tkinter.END, left[0])
            if len(right):
                self.entry_edit_game_b.insert(tkinter.END, right[0])

        if self.score.arrayScore[i] is not None:
            text_score = self.score.arrayScore[i]
            left = re.findall(r"([0-9a-zA-Z]*)-", text_score)
            right = re.findall(r"-([0-9a-zA-Z]*)", text_score)
            if len(left):
                self.entry_edit_score_a.insert(tkinter.END, left[0])
            if len(right):
                self.entry_edit_score_b.insert(tkinter.END, right[0])

        self.variable_serve.set(
            self.score.firstSecondString[self.score.arrayFirstSecond[i]]
        )
        self.variable_which_server.set(self.score.arrayServer[i])
        self.variable_winner.set(self.score.arrayPointWinner[i])
        self.variable_pattern.set(self.score.arrayPointPattern[i])

    def close(self):
        if self.vid:
            self.vid.close()


if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        if args[1] == "predict":
            mode_predict_court = True
            mode_predict_player = True
            mode_detect_score = True
    else:
        mode_predict_court = False
        mode_predict_player = False
        mode_detect_score = False

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    settings = setting.Setting()  # settings.json

    score = score.Score(settings.firstServer)
    score.setPlayerName(settings.playerA, settings.playerB)

    print(score.playerA, score.playerB)

    root = tkinter.Tk()
    root.title("Tennis Video Analytics")

    x1 = settings.sx1
    y1 = settings.sy1
    x2 = settings.sx2
    y2 = settings.sy2

    app = Application(
        score, mode_predict_court, mode_predict_player, mode_detect_score, master=root
    )
    app.create_widgets()  # 640, 360

    print("videoFile:", settings.videoFile)
    if settings.videoFile != "":
        videoFile = settings.videoFile
        vid = video.Video(videoFile)
        app.load_video(vid)
        if mode_detect_score:
            if app.ds:
                app.sx1 = int(x1 * app.w / app.vid.width)
                app.sy1 = int(y1 * app.h / app.vid.height)
                app.sx2 = int(x2 * app.w / app.vid.width)
                app.sy2 = int(y2 * app.h / app.vid.height)
                app.ds.set_xy(app.sx1, app.sy1, app.sx2, app.sy2)

        app.image_show()
        app.sc.configure(to=app.frame_count)

    if settings.dataFile != "":
        print(settings.dataFile)
        filename = settings.dataFile
        # "../data/add_track.db"
        app.fld = filename
        app.load_data()

    if mode_detect_score:
        filename = "../data/ball-pos-000000-020000.csv"
        app.load_track_ball_data(filename)

        filename = "../data/track-data2.csv"
        app.load_track_data(filename)

    app.delete_tree_shot_after_end_all()

    app.bind("<Right>", app.button_forward1)  # 右矢印をクリックしたらフレーム+1
    app.bind("<Control-Right>", app.button_forward10)  # ctrf+右矢印をクリックしたらフレーム+10
    app.bind("<Shift-Right>", app.button_forward100)  # shift+右矢印をクリックしたらフレーム+100
    app.bind("<Left>", app.button_backward1)  # 左矢印をクリックしたらフレーム+1
    app.bind("<Control-Left>", app.button_backward10)  # ctrf+左矢印をクリックしたらフレーム+10
    app.bind("<Shift-Left>", app.button_backward100)
    app.bind("p", app.play)
    app.bind("s", app.stop)
    app.bind("<Delete>", app.button_delete_tree_point)
    app.bind("<Up>", app.button_select_up)
    app.bind("<Down>", app.button_select_down)
    app.focus_set()
    app.pack()
    app.mainloop()
