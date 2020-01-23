import json

class Setting():  # 設定ファイル読込
    def __init__(self):
        
        fileName="settings.json"
        jsonFile=open(fileName,'r')
        jsonDict=json.load(jsonFile)
        self.playerA=jsonDict["playerA"]
        self.playerB=jsonDict["playerB"]
        self.firstServer=jsonDict["firstServer"]