import cv2
import mediapipe as mp
import time
import serial
import save_image
from diff import *

class human_tracking:
    def __init__(self):
        self.ser = serial.Serial('com5', 9600)
        time.sleep(2)
        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose()
        self.cap = cv2.VideoCapture(0)
        self.old_state = 0
        self.new_state = 0
        self.image1 = None
        self.image2 = self.cap.read()[1]
        self.flag = 0
        pTime = 0

    def newfun(self):
        while True:
            begin_tracking

    def begin_tracking(self,path):
        success, img = self.cap.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = self.pose.process(imgRGB)
        self.old_state = self.new_state
        if result.pose_landmarks:
            self.new_state = 1 #This is when human detect

            self.mpDraw.draw_landmarks(img,result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
            xavg = 0
            yavg = 0
            counter = 0
            for id,lm in enumerate(result.pose_landmarks.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if lm.visibility>0.9:
                    xavg = xavg + int(lm.x*w)
                    yavg = yavg + int(lm.y*h)
                    counter = counter +1
            if counter != 0:
                xavg = xavg/counter
                yavg = yavg/counter
            else :
                xavg = 0
                yavg = 0
            cv2.circle(img, (int(xavg), int(yavg)), 10, (255, 0, 0), cv2.FILLED)
            h, w, c = img.shape
            xcenter = w/2;
            ycenter = h/2;
            if xavg > xcenter+50:
                self.ser.write('2'.encode('utf-8'))
                print('sent 2')

            if xavg < xcenter - 50:
                self.ser.write('1'.encode('utf-8'))
                print('sent 1')

            if yavg > ycenter + 50:
                self.ser.write('3'.encode('utf-8'))
                print('sent 3')

            if yavg < ycenter - 50:
                self.ser.write('4'.encode('utf-8'))
                print('sent 4')
        else:
            self.new_state = 0

        if self.new_state - self.old_state == 0:
            print("no change")

        if self.new_state - self.old_state == 1:
            print("human coming")
            self.image1 = self.image2
            self.image2 = img
        if self.new_state - self.old_state == -1:
            print("human leaving")
            self.image1 = self.image2
            self.image2 = img
            self.flag = 1

        if self.flag == 1:
            extractItem(path, self.image1, self.image2)
            self.flag = 0
            print("ectracing")

        cv2.imshow("image",img)
        cv2.waitKey(1)

    def Move_to_Origin(self):
        self.ser.write('5'.encode('utf-8'))
        time.sleep(5)

    #def return_img(self):
        # return the image


