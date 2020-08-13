import unittest
import sys
import TennisVideoAnalysis
import video
import score
import tkinter

class TestTennisVideoAnalysis(unittest.TestCase):
    def setUp(self):#設定
        self.root = tkinter.Tk()
        self.score = score.Score(0)
        self.app=TennisVideoAnalysis.Application(self.score, master=self.root)
        self.app.create_widgets(360, 640)

    # def test_loadVideo(self):
    #     videoFile="./video/nishioka-nakashima.mp4"
    #     vid = video.Video(videoFile)
    #     self.app.loadVideo(vid)

    def test_score_convert_score(self):
        #ゲームに変化がない場合
        g=[0,0]
        s=[0,0]
        ps=[[0,0],[1,0],[2,0],[3,0],[0,1],[1,1],[2,1],[3,1],#,[4,0],[4,1]
            [0,2],[1,2],[2,2],[3,2],[0,3],[1,3],[2,3],[3,3],#,[4,2],[4,3] Ad
            [4,3],[4,4],[5,4],[5,5],[6,5],[6,6],[7,6],[7,7]]
        for i,p in enumerate(ps):
            # p=[0,1]
            correct_score=[['0','0'],['15','0'],['30','0'],['40','0'],['0','15'],['15','15'],['30','15'],['40','15'],#,['0','0'],['0','0']
                        ['0','30'],['15','30'],['30','30'],['40','30'],['0','40'],['15','40'],['30','40'],['40','40'],#,['0','0'],['0','0']
                        ['Ad','40'],['40','40'],['Ad','40'],['40','40'],['Ad','40'],['40','40'],['Ad','40'],['40','40']]
            scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
            self.assertEqual([scoreA,scoreB],correct_score[i])
            self.assertEqual([gameA,gameB],g)
            self.assertEqual([setA,setB],s)
            


