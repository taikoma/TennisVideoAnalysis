import cv2  # OpenCVライブラリ
import torch
from utils.ssd_model import SSD
from utils.ssd_model import DataTransform
from utils.ssd_predict_show import SSDPredictShow

class playerDetect():
    def __init__(self,filepath):
        voc_classes = ['PlayerBack', 'PlayerFront', 'ball', 'ballperson',
                    'linesman', 'umpire']
        ssd_cfg = {
            'num_classes': 6,  # 背景クラスを含めた合計クラス数
            'input_size': 300,  # 画像の入力サイズ
            'bbox_aspect_num': [4, 6, 6, 6, 4, 4],  # 出力するDBoxのアスペクト比の種類
            'feature_maps': [38, 19, 10, 5, 3, 1],  # 各sourceの画像サイズ
            'steps': [8, 16, 32, 64, 100, 300],  # DBOXの大きさを決める
            'min_sizes': [30, 60, 111, 162, 213, 264],  # DBOXの大きさを決める
            'max_sizes': [60, 111, 162, 213, 264, 315],  # DBOXの大きさを決める
            'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
        }
        net = SSD(phase="inference", cfg=ssd_cfg)
        # net_weights = torch.load('../weights/ssd300_300.pth',
        #                         map_location={'cuda:0': 'cpu'})
        net_weights = torch.load('../weights/ssd300_300.pth')
        net.load_state_dict(net_weights)
        self.ssd = SSDPredictShow(eval_categories=voc_classes, net=net)
    
    def predict(self,img):
        predict_bbox, pre_dict_label_index, scores=self.ssd.ssd_predict(img, data_confidence_level=0.4)
        x1_1,y1_1,x1_2,y1_2,x2_1,y2_1,x2_2,y2_2=0,0,0,0,0,0,0,0
        for i,b in enumerate(pre_dict_label_index):
            if(b==0):
                x1_1,y1_1,x1_2,y1_2=int(predict_bbox[i][0]),int(predict_bbox[i][1]),int(predict_bbox[i][2]),int(predict_bbox[i][3])
            elif(b==1):
                x2_1,y2_1,x2_2,y2_2=int(predict_bbox[i][0]),int(predict_bbox[i][1]),int(predict_bbox[i][2]),int(predict_bbox[i][3])    
    
        return x1_1,y1_1,x1_2,y1_2,x2_1,y2_1,x2_2,y2_2
