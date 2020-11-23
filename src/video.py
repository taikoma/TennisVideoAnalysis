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
import score


class Video():  # ビデオファイルの読み込み
    def __init__(self, videoFileName):
        self.videoFileName = videoFileName
        self.video = cv2.VideoCapture(self.videoFileName)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width=self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(self.width,self.height)

        print(self.frame_count)

        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        
        self.start_frame = 0
        self.end_frame = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.start_frame

    def close(self):
        self.video.release()

    def set_start_frame(self, start_frame):  # 再生開始フレームの値をセット
        if(start_frame <= self.end_frame):
            self.start_frame = start_frame

    def set_end_frame(self, end_frame):  # 再生終了フレームの値をセット
        if(end_frame >= self.start_frame):
            self.end_frame = end_frame

    def set_frame(self):  # 再生開始フレーム位置をセット
        if self.video.isOpened():
            self.video.set(1, self.start_frame)
            ret, frame = self.video.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return(ret, None)
        else:
            return(ret, None)

    def get_frame(self):  # 再生するフレームを読み込む
        if self.video.isOpened():
            ret, frame = self.video.read()
            self.frame_no = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))

            if self.frame_no <= self.end_frame:
                if ret:
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return(ret, None)
            else:
                return(False, None)
        else:
            return(ret, None)