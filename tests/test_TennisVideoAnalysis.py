import unittest
import sys
import tkinter
sys.path.append('../src')
import TennisVideoAnalysis
import video
import score

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

    def test_score_convert_score(self):#score計算にエラーがないかテスト
        #ゲームに変化がない場合
        g=[0,0]
        s=[0,0]
        for i in range(0,1):
            s[0]=i
            for j in range(0,1):
                s[1]=j
                for k in range(0,6):
                    g[0]=k
                    for l in range(0,6):
                        g[1]=l

                        ps=[[0,0],[1,0],[2,0],[3,0],[0,1],[1,1],[2,1],[3,1],#,[4,0],[4,1]
                            [0,2],[1,2],[2,2],[3,2],[0,3],[1,3],[2,3],[3,3],#,[4,2] Ad
                            [4,3],[4,4],[5,4],[5,5],[6,5],[6,6],[7,6],[7,7]]
                        # g_temp=g
                        for m,p in enumerate(ps):
                            correct_score=[['0','0'],['15','0'],['30','0'],['40','0'],['0','15'],['15','15'],['30','15'],['40','15'],#,['0','0'],['0','0']
                                        ['0','30'],['15','30'],['30','30'],['40','30'],['0','40'],['15','40'],['30','40'],['40','40'],#,['0','0'],['0','0']
                                        ['Ad','40'],['40','40'],['Ad','40'],['40','40'],['Ad','40'],['40','40'],['Ad','40'],['40','40']]
                            scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                            self.assertEqual([scoreA,scoreB],correct_score[m])
                            self.assertEqual([gamePointA,gamePointB],p)
                            self.assertEqual([gameA,gameB],g)
                            self.assertEqual([setA,setB],s)
        #ゲームに変化がある場合
        for i in range(0,1):
            s[0]=i
            for j in range(0,1):
                s[1]=j
                for k in range(0,5):
                    g[0]=k
                    for l in range(0,5):
                        g[1]=l

                        ps=[[4,0],[4,1],[4,2],[5,3],[6,4],[7,5],[9,7],[10,8],[11,9],[12,10]]
                        for m,p in enumerate(ps):
                            scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                            self.assertEqual([scoreA,scoreB],['0','0'])
                            self.assertEqual([gamePointA,gamePointB],[0,0])
                            self.assertEqual([gameA,gameB],[g[0]+1,g[1]])
                            self.assertEqual([setA,setB],s)

                        ps=[[0,4],[1,4],[2,4],[3,5],[4,6],[5,7],[7,9],[8,10],[9,11],[10,12]]
                        for m,p in enumerate(ps):
                            scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                            self.assertEqual([scoreA,scoreB],['0','0'])
                            self.assertEqual([gamePointA,gamePointB],[0,0])
                            self.assertEqual([gameA,gameB],[g[0],g[1]+1])
                            self.assertEqual([setA,setB],s)
        #セットに変化がある場合
        for k in range(0,1):
            s[0]=k
            for l in range(0,1):
                s[1]=l

                gs=[[5,0],[5,1],[5,2],[5,3],[5,4],[6,5]]
                p=[4,0]
                for m,g in enumerate(gs):
                    scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                    self.assertEqual([scoreA,scoreB],['0','0'])
                    self.assertEqual([gamePointA,gamePointB],[0,0])
                    self.assertEqual([gameA,gameB],[0,0])
                    self.assertEqual([setA,setB],[s[0]+1,s[1]])

                gs=[[0,5],[1,5],[2,5],[3,5],[4,5],[5,6]]
                p=[0,4]
                for m,g in enumerate(gs):
                    scoreA, scoreB, gamePointA, gamePointB, gameA, gameB, setA, setB = self.score.convert_score(p[0], p[1], g[0], g[1], s[0], s[1])
                    self.assertEqual([scoreA,scoreB],['0','0'])
                    self.assertEqual([gamePointA,gamePointB],[0,0])
                    self.assertEqual([gameA,gameB],[0,0])
                    self.assertEqual([setA,setB],[s[0],s[1]+1])
        #タイブレーク


    # def test_score_convert_set(self):#score計算にエラーがないかテスト
    #     print("test")
        # setA,setB=0,0
        #セットに変化なし
        # g=[0,0]
        # for i in range(0,6):
        #     g[0]=i
        #     for j in range(0,6):
        #         g[1]=j
        #         gameA, gameB, setA, setB = self.score.convert_set(g[0], g[1], setA, setB)
        #         self.assertEqual([gameA,gameB],[g[0],g[1]])
        #         self.assertEqual([setA,setB],[setA,setB])
        # #6-5 5-6
        # gs=[[6,5],[5,6]]
        # for i,g in enumerate(gs):
        #     gameA, gameB, setA, setB = self.score.convert_set(g[0], g[1], setA, setB)
        #     self.assertEqual([gameA,gameB],[0,0])
        #     self.assertEqual([setA,setB],[setA,setB])

        # #セットに変化あり
        # gs=[[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[1,1]]
        # for i,g in enumerate(gs):
        #     gameA, gameB, setA, setB = self.score.convert_set(g[0], g[1], setA, setB)
        #     self.assertEqual([gameA,gameB],[0,0])
        #     self.assertEqual([setA,setB],[setA+1,setB])

if __name__ == "__main__":
    unittest.main()               



        
                    


