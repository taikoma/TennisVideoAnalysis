import json
import collections as cl
import logging

class Setting():  # 設定ファイル読込
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info('init Setting()')
        self.fileName="../settings.json"
        jsonFile=open(self.fileName,'r')

        try:
            self.jsonDict=json.load(jsonFile)
        except:
            self.playerA="playerA"
            self.playerB="playerB"
            self.firstServer=0
            self.videoFile=""
            self.dataFile=""

            self.sx1=0
            self.sy1=0
            self.sx2=0
            self.sy2=0
        else:
            self.playerA=self.jsonDict["playerA"]
            self.playerB=self.jsonDict["playerB"]
            self.firstServer=self.jsonDict["firstServer"]
            self.videoFile=self.jsonDict["videoFile"]
            self.dataFile=self.jsonDict["database"]

            self.sx1=self.jsonDict["sx1"]
            self.sy1=self.jsonDict["sy1"]
            self.sx2=self.jsonDict["sx2"]
            self.sy2=self.jsonDict["sy2"]
            



    def save_data(self,playerA,playerB,firstServer,videoFile,x1,y1,x2,y2):
        print("savedata")
        logging.info('save_data')
        self.playerA=playerA
        self.playerB=playerB
        self.firstServer=firstServer
        self.videoFile=videoFile

        self.sx1=x1
        self.sy1=y1
        self.sx2=x2
        self.sy2=y2

        jsonFile=open(self.fileName,'w')

        ys=cl.OrderedDict()
        ys["playerA"]=self.playerA
        ys["playerB"]=self.playerB
        ys["firstServer"]=self.firstServer
        ys["videoFile"]=self.videoFile
        ys["database"]=self.dataFile

        ys["sx1"]=self.sx1
        ys["sy1"]=self.sy1
        ys["sx2"]=self.sx2
        ys["sy2"]=self.sy2
        logging.info('settings.json : %s %s %s %s %s',ys["playerA"],ys["playerB"],ys["firstServer"],ys["videoFile"],ys["database"])
        json.dump(ys,jsonFile,indent=4)

        
        
        