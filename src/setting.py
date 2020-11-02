import json
import collections as cl
import logging

class Setting():  # 設定ファイル読込
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info('init Setting()')
        self.fileName="../settings.json"
        jsonFile=open(self.fileName,'r')
        self.jsonDict=json.load(jsonFile)

        self.playerA=self.jsonDict["playerA"]
        self.playerB=self.jsonDict["playerB"]
        self.firstServer=self.jsonDict["firstServer"]
        self.videoFile=self.jsonDict["videoFile"]
        self.dataFile=self.jsonDict["database"]

    def save_data(self,playerA,playerB,firstServer,videoFile):
        logging.info('save_data')
        self.playerA=playerA
        self.playerB=playerB
        self.firstServer=firstServer
        self.videoFile=videoFile
        jsonFile=open(self.fileName,'w')

        ys=cl.OrderedDict()
        ys["playerA"]=self.playerA
        ys["playerB"]=self.playerB
        ys["firstServer"]=self.firstServer
        ys["videoFile"]=self.videoFile
        ys["database"]=self.dataFile
        logging.info('settings.json : %s %s %s %s %s',ys["playerA"],ys["playerB"],ys["firstServer"],ys["videoFile"],ys["database"])
        json.dump(ys,jsonFile,indent=4)

        
        
        