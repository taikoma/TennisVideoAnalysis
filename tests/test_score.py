import unittest
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
import src.score as score
import src.const as const

class TestScore(unittest.TestCase):
    def setUp(self):#設定 save_temp_db
        self.score=score.Score(0)

    def test_convert_set(self):
        game_a,game_b=6,4
        set_a,set_b=0,0
        self.assertEqual((0,0,1,0),self.score.convert_set(game_a,game_b,set_a,set_b))
        
        game_a,game_b=4,6
        set_a,set_b=0,0
        self.assertEqual((0,0,0,1),self.score.convert_set(game_a,game_b,set_a,set_b))

        game_a,game_b=7,6
        set_a,set_b=0,0
        self.assertEqual((0,0,1,0),self.score.convert_set(game_a,game_b,set_a,set_b))
        
        game_a,game_b=6,7
        set_a,set_b=0,0
        self.assertEqual((0,0,0,1),self.score.convert_set(game_a,game_b,set_a,set_b))

        game_a,game_b=6,5
        set_a,set_b=0,0
        self.assertEqual((6,5,0,0),self.score.convert_set(game_a,game_b,set_a,set_b))
        
        game_a,game_b=5,6
        set_a,set_b=0,0
        self.assertEqual((5,6,0,0),self.score.convert_set(game_a,game_b,set_a,set_b))



    def test_convert_score(self):#score計算にエラーがないかテスト total_gameの変化が含まれていてステートレスになっていない
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

    def test_devide_left_right(self):
        text_score = "15-30"
        l,r=self.score.divide_left_right(text_score)
        self.assertEqual("15",l)
        self.assertEqual("30",r)
        
        text_score = ""
        l,r=self.score.divide_left_right(text_score)
        self.assertEqual("",l)
        self.assertEqual("",r)


    def test_get_winner(self):
        winner=self.score.get_winner(0,0,0,0)
        self.assertEqual(2,winner)
        winner=self.score.get_winner(0,1,0,0)
        self.assertEqual(0,winner)
        

    def test_get_winner_list(self):
        array_score=["0-0","0-15","0-15","15-15","15-30","15-40","30-40","40-40","40-A","40-40"]
        winner_array=self.score.get_winner_list(array_score)
        self.assertEqual([1,2,0,1,1,0,0,1,0,3],winner_array)

        array_score=["0-0","0-15","0-15","","15-15","15-30","15-40","30-40","40-40","40-A","40-40"]
        winner_array=self.score.get_winner_list(array_score)
        self.assertEqual([1,2,3,0,1,1,0,0,1,0,3],winner_array)

        array_score=["0-0","0-15","0-15","","","15-15","15-30","15-40","30-40","40-40","40-A","40-40"]
        winner_array=self.score.get_winner_list(array_score)
        self.assertEqual([1,2,3,3,0,1,1,0,0,1,0,3],winner_array)

        array_score=["0-0","0-15","0-15","","","0-15","15-15","15-30","15-40","30-40","40-40","40-A","40-40"]
        winner_array=self.score.get_winner_list(array_score)
        self.assertEqual([1,2,3,3,2,0,1,1,0,0,1,0,3],winner_array)


    def test_score2count(self):
        score="0"
        self.assertEqual(0,self.score.score2count(score))
        score="15"
        self.assertEqual(1,self.score.score2count(score))
        score="30"
        self.assertEqual(2,self.score.score2count(score))
        score="40"
        self.assertEqual(3,self.score.score2count(score))
        score="A"
        self.assertEqual(4,self.score.score2count(score))
        score="fasdf"
        self.assertEqual(-1,self.score.score2count(score))

    def test_winner2player_fault(self):
        player_name=["a","b"]
        winner_array=[0,1,1,2,2,3,0,2]
        point_pattern=["","","","","","","",""]
        point_winner_array,first_second_array,point_pattern=self.score.winner2player_fault(winner_array,player_name,point_pattern)
        self.assertEqual(["a","b","b","","","","a",""],point_winner_array)
        self.assertEqual([1,1,1,1,2,0,1,1],first_second_array)#0:not point 1:1st 2:2nd
        self.assertEqual(["","","",const.PATTERN[6],const.PATTERN[7],"","",const.PATTERN[6]],point_pattern)#0:not point 1:1st 2:2nd

    def test_position_data2array(self):
        self.score.playerName=["A","B"]
        self.score.firstServer=0
        self.score.totalGame=1
        
        self.score.arrayBallPosition=[[],[],[],[]]
        self.score.arrayPlayerAPosition=[[],[],[],[]]
        self.score.arrayPlayerBPosition=[[],[],[],[]]
        self.score.arrayHitPlayer=[[],[],[],[]]
        self.score.arrayBounceHit=[[],[],[],[]]
        self.score.arrayForeBack=[[],[],[],[]]
        self.score.arrayDirection=[[],[],[],[]]
        
        num=2
        self.score.number=num
        pos_seek=100
        xball=10
        yball=20
        self.score.position_data2array(xball,yball,3,4,5,6,0,"Hit","Fore","Cross",pos_seek)
        self.assertEqual([[],[],[[num,pos_seek,xball,yball]],[]],self.score.arrayBallPosition)
        self.assertEqual([[],[],["B"],[]],self.score.arrayHitPlayer)

    def test_position_data2array_fix(self):
        self.score.playerName=["A","B"]
        self.score.firstServer=0
        self.score.totalGame=1
        
        self.score.arrayBallPosition=[[],[],[[1,11,1,2],[2,51,3,4]],[]]
        self.score.arrayPlayerAPosition=[[],[],[[11,12],[13,14]],[]]
        self.score.arrayPlayerBPosition=[[],[],[[21,22],[23,24]],[]]
        self.score.arrayHitPlayer=[[],[],["A","A"],[]]
        self.score.arrayBounceHit=[[],[],["Bounce","Hit"],[]]
        self.score.arrayForeBack=[[],[],["Fore","Back"],[]]
        self.score.arrayDirection=[[],[],["Cross","Cross"],[]]
        
        num=2
        self.score.number=num
        rally=2
        self.score.rally=rally
        pos_seek=100
        xball=10
        yball=20
        self.score.position_data2array_fix(xball,yball,3,4,5,6,0,"Hit","Fore","Cross",pos_seek)
        self.assertEqual([[],[],[[1,11,1,2],[rally,pos_seek,xball,yball]],[]],self.score.arrayBallPosition)
        self.assertEqual([[],[],["A","B"],[]],self.score.arrayHitPlayer)

    def test_delete_position_data(self):
        #delete middle
        self.score.arrayBallPosition=[[],[],[[1,11,1,2],[2,51,3,4],[3,101,5,6]],[]]
        self.score.arrayPlayerAPosition=[[],[],[[11,12],[13,14],[15,16]],[]]
        self.score.arrayPlayerBPosition=[[],[],[[21,22],[23,24],[25,26]],[]]
        self.score.arrayHitPlayer=[[],[],["A","A","B"],[]]
        self.score.arrayBounceHit=[[],[],["Bounce","Hit","Bounce"],[]]
        self.score.arrayForeBack=[[],[],["Fore","Back","Back"],[]]
        self.score.arrayDirection=[[],[],["Cross","Cross","Cross"],[]]
        num=2
        self.score.number=num
        i=1
        self.score.delete_position_data(i)
        self.assertEqual([[],[],[[1,11,1,2],[2,101,5,6]],[]],self.score.arrayBallPosition)
        self.assertEqual([[],[],[[11,12],[15,16]],[]],self.score.arrayPlayerAPosition)

        #delete last
        self.score.arrayBallPosition=[[],[],[[1,11,1,2],[2,51,3,4],[3,101,5,6]],[]]
        self.score.arrayPlayerAPosition=[[],[],[[11,12],[13,14],[15,16]],[]]
        self.score.arrayPlayerBPosition=[[],[],[[21,22],[23,24],[25,26]],[]]
        self.score.arrayHitPlayer=[[],[],["A","A","B"],[]]
        self.score.arrayBounceHit=[[],[],["Bounce","Hit","Bounce"],[]]
        self.score.arrayForeBack=[[],[],["Fore","Back","Back"],[]]
        self.score.arrayDirection=[[],[],["Cross","Cross","Cross"],[]]
        num=2
        self.score.number=num
        i=2
        self.score.delete_position_data(i)
        self.assertEqual([[],[],[[1,11,1,2],[2,51,3,4]],[]],self.score.arrayBallPosition)
        self.assertEqual([[],[],[[11,12],[13,14]],[]],self.score.arrayPlayerAPosition)

        #delete first
        self.score.arrayBallPosition=[[],[],[[1,11,1,2],[2,51,3,4],[3,101,5,6]],[]]
        self.score.arrayPlayerAPosition=[[],[],[[11,12],[13,14],[15,16]],[]]
        self.score.arrayPlayerBPosition=[[],[],[[21,22],[23,24],[25,26]],[]]
        self.score.arrayHitPlayer=[[],[],["A","A","B"],[]]
        self.score.arrayBounceHit=[[],[],["Bounce","Hit","Bounce"],[]]
        self.score.arrayForeBack=[[],[],["Fore","Back","Back"],[]]
        self.score.arrayDirection=[[],[],["Cross","Cross","Cross"],[]]
        num=2
        self.score.number=num
        i=0
        self.score.delete_position_data(i)
        self.assertEqual([[],[],[[1,51,3,4],[2,101,5,6]],[]],self.score.arrayBallPosition)
        self.assertEqual([[],[],[[13,14],[15,16]],[]],self.score.arrayPlayerAPosition)


    def test_divide_track_data(self):
        self.score.arrayBallPosition=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayPlayerAPosition=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayPlayerBPosition=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayHitPlayer=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayBounceHit=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayForeBack=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayDirection=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        self.score.arrayBounceHit=[[],[],[],[],[],[],[],[],[],[],[],[]]#num12
        start_frame=[0,40,70,120,1000]
        track_frame=[15,20,30,50,100,115,120,130,150,200]
        bx=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
        by=[11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]
        xa=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
        ya=[11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]
        xb=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
        yb=[11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]
        hit_bounce=["Front_Hit","Front_Bounce","Back_Hit","Back_Bounce","Front_Hit","Front_Bounce","Back_Hit","Back_Bounce","Front_Hit","Front_Bounce"]
        self.score.divide_track_data(start_frame,track_frame,bx,by,xa,ya,xb,yb,hit_bounce)
        # print(self.score.arrayBallPosition)
        self.assertEqual([[[0,15,1.0,11.0],[0,20,2.0,12.0],[0,30,3.0,13.0]],[[1,50,4.0,14.0]],[[2,100,5.0,15.0],[2,115,6.0,16.0]],[[3,120,7.0,17.0],[3,130,8.0,18.0],[3,150,9.0,19.0],[3,200,10.0,20.0]], [], [], [], [], [], [], [], []],self.score.arrayBallPosition)
        self.assertEqual([[[0,15,1.0,11.0],[0,20,2.0,12.0],[0,30,3.0,13.0]],[[1,50,4.0,14.0]],[[2,100,5.0,15.0],[2,115,6.0,16.0]],[[3,120,7.0,17.0],[3,130,8.0,18.0],[3,150,9.0,19.0],[3,200,10.0,20.0]], [], [], [], [], [], [], [], []],self.score.arrayPlayerAPosition)
        self.assertEqual([["Hit","Bounce","Hit"],["Bounce"],["Hit","Bounce"],["Hit","Bounce","Hit","Bounce"],[], [], [], [], [], [], [], []],self.score.arrayBounceHit)


