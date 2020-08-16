import TennisCourtNet
import math
import cv2
import matplotlib.cm
import numpy as np
from scipy.ndimage.filters import gaussian_filter, maximum_filter
from scipy.ndimage.morphology import generate_binary_structure
import os.path as osp
import torch

class Predict():
    def __init__(self,filepath):
        self.net = TennisCourtNet.TennisCourtNet()
        net_weights = torch.load(filepath, map_location={'cuda:0': 'cpu'})
        keys = list(net_weights.keys())
        weights_load = {}

        for i in range(len(keys)):
            weights_load[list(self.net.state_dict().keys())[i]
                         ] = net_weights[list(keys)[i]]

        state = self.net.state_dict()
        state.update(weights_load)
        self.net.load_state_dict(state)
        

    def predict(self,oriImg):
        oriImg = cv2.cvtColor(oriImg, cv2.COLOR_BGR2RGB)# BGRをRGBにして表示

        size = (368, 368)# 画像のリサイズ
        img = cv2.resize(oriImg, size, interpolation=cv2.INTER_CUBIC)
        img = img.astype(np.float32) / 255.# 画像の前処理
        color_mean = [0.485, 0.456, 0.406]# 色情報の標準化
        color_std = [0.229, 0.224, 0.225]
        preprocessed_img = img.copy()[:, :, ::-1]  # BGR→RGB
        for i in range(3):
            preprocessed_img[:, :, i] = preprocessed_img[:, :, i] - color_mean[i]
            preprocessed_img[:, :, i] = preprocessed_img[:, :, i] / color_std[i]
        img = preprocessed_img.transpose((2, 0, 1)).astype(np.float32)# （高さ、幅、色）→（色、高さ、幅）
        img = torch.from_numpy(img)# 画像をTensorに
        x = img.unsqueeze(0)# ミニバッチ化：torch.Size([1, 3, 368, 368])
        self.net.eval()
        predicted_outputs, _ = self.net(x)

        pafs = predicted_outputs[0][0].detach().numpy().transpose(1, 2, 0)
        heatmaps = predicted_outputs[1][0].detach().numpy().transpose(1, 2, 0)

        pafs = cv2.resize(pafs, size, interpolation=cv2.INTER_CUBIC)
        heatmaps = cv2.resize(heatmaps, size, interpolation=cv2.INTER_CUBIC)

        pafs = cv2.resize(
            pafs, (oriImg.shape[1], oriImg.shape[0]), interpolation=cv2.INTER_CUBIC)
        heatmaps = cv2.resize(
            heatmaps, (oriImg.shape[1], oriImg.shape[0]), interpolation=cv2.INTER_CUBIC)

        return pafs,heatmaps

    def find_peaks(self,param, img):
        peaks_binary = (maximum_filter(img, footprint=generate_binary_structure(
            2, 1)) == img) * (img > param['thre1'])
        return np.array(np.nonzero(peaks_binary)[::-1]).T    

    def predictPoints(self,oriImg):
        pafs,heatmaps = self.predict(oriImg)
        param = {'thre1': 0.1, 'thre2': 0.05, 'thre3': 0.5}
        points=[]
        for i in range(4):
            heat_map = heatmaps[:, :, i]
            map_orig=heat_map
            peak_coords = self.find_peaks(param, map_orig)
            if(len(peak_coords)>0):
                points.append(peak_coords[0])
        points=np.array(points)
        return points
