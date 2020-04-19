import json
import collections as cl

class Setting():  # 設定ファイル読込
    def __init__(self):
        
        fileName="settings.json"
        jsonFile=open(fileName,'r')
        self.jsonDict=json.load(jsonFile)

        self.playerA=self.jsonDict["playerA"]
        self.playerB=self.jsonDict["playerB"]
        self.firstServer=self.jsonDict["firstServer"]
        self.videoFile=self.jsonDict["videoFile"]
        self.dataFile=self.jsonDict["database"]

    def save_data(self,playerA,playerB,firstServer):
        self.playerA=playerA
        self.playerB=playerB
        self.firstServer=firstServer

        fileName="settings.json"
        jsonFile=open(fileName,'w')

        ys=cl.OrderedDict()
        ys["playerA"]=self.playerA
        ys["playerB"]=self.playerB
        ys["firstServer"]=self.firstServer
        ys["videoFile"]=self.videoFile
        ys["database"]=self.dataFile
        json.dump(ys,jsonFile,indent=4)

        
        
        