import unittest
from pathlib import Path
import sys
import tkinter
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.TennisVideoAnalysis as TennisVideoAnalysis
import src.video as video
import src.score as score

class TestTennisVideoAnalysis(unittest.TestCase):
    def setUp(self):#設定
        self.root = tkinter.Tk()
        self.score = score.Score(0)
        mode_predict_court=False
        mode_predict_player=False
        mode_detect_score=False
        self.app=TennisVideoAnalysis.Application(self.score,mode_predict_court,mode_predict_player,mode_detect_score, master=self.root)
        self.app.create_widgets(360, 640)

    # def test_loadVideo(self):
    #     videoFile="./video/nishioka-nakashima.mp4"
    #     vid = video.Video(videoFile)
    #     self.app.loadVideo(vid)

    


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



        
                    


