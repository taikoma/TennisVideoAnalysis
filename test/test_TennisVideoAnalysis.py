import unittest
import TennisVideoAnalysis
import video
import score
import tkinter

class TestTennisVideoAnalysis(unittest.TestCase):
    def setUp(self):
        self.root = tkinter.Tk()
        self.score = score.Score(0)
        self.app=TennisVideoAnalysis.Application(self.score, master=self.root)
        self.app.create_widgets(360, 640)

    def test_loadVideo(self):
        videoFile="./video/nishioka-nakashima.mp4"
        vid = video.Video(videoFile)
        self.app.loadVideo(vid)
