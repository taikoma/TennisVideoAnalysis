import cv2
import numpy as np


class View():
    def __init__(self):
        print("init")

    def draw_line(self,img,line,inv_M):
        """Draw a line 
        


        """
        dst_inv=cv2.perspectiveTransform(line,inv_M)
        cv2.line(img, (int(dst_inv[0][0][0]),int(dst_inv[0][0][1])),
            (int(dst_inv[0][1][0]),int(dst_inv[0][1][1])), (0, 255, 0),1)#中央の横ライン



