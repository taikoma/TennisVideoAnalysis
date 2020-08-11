import tkinter
import cv2
import PIL.Image,PIL.ImageTk
import time

class App:#動画再生用のアプリケーションクラス
    def __init__(self,window,window_title,start_frame,end_frame,video_source=0):
        self.window=window
        self.window.title(window_title)
        self.video_source=video_source

        self.vid=MyVideoCapture(video_source)#videoクラスの読み込み　

        #canvasエリアに動画データサイズに合わせて動画データをセット
        self.canvas=tkinter.Canvas(window,width=self.vid.width,height=self.vid.height)
        self.canvas.pack()

        self.vid.set_start_frame(start_frame)
        self.vid.set_end_frame(end_frame)

        #一定時間毎に画像更新することで動画を再生する
        self.vid.set_frame()
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source

        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)
        

class MyVideoCapture:#
    def __init__(self,video_source=0):
        self.vid=cv2.VideoCapture(video_source)#videoデータを読み込む
        if not self.vid.isOpened():#videoを読み込めないとき
            raise ValueError("Unable to open source",video_source)

        self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps=self.vid.get(cv2.CAP_PROP_FPS)
        self.start_frame=0
        self.end_frame=self.vid.get(cv2.CAP_PROP_FRAME_COUNT)

    def __del__(self):#
        if self.vid.isOpened():
            self.vid.release()
        #self.window.mainloop()

    def set_start_frame(self,start_frame):#再生開始フレームの値をセット
        if(start_frame<=self.end_frame):
            self.start_frame=start_frame

    def set_end_frame(self,end_frame):#再生終了フレームの値をセット
        if(end_frame>=self.start_frame):
            self.end_frame=end_frame
    
    def set_frame(self):#再生開始フレーム位置をセット
        if self.vid.isOpened():
            self.vid.set(1,self.start_frame)
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return(ret,None)
        else:
            return(ret,None)

    def get_frame(self):#再生するフレームを読み込む
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame_no = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_no<=self.end_frame:
                if ret:
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return(ret,None)
            else:
                return(False,None)
        else:
            return(ret,None)
if __name__ == "__main__":
    videofile="box.mp4"
    start_frame=100
    end_frame=200
    App(tkinter.Tk(),"Tkinter and OpenCV",start_frame,end_frame,videofile)

