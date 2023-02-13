import cv2
import mediapipe as mp
import time
import serial
import save_image
from diff import *

class human_tracking:
    def __init__(self, port = None, baudrate = None, servo = None):
        self.port = port
        self.baudrate = baudrate
        self.servo = servo
        if self.port is None and self.baudrate is None:
            self.ser = None
        else:
            self.ser = serial.Serial(port, baudrate)
        time.sleep(2)
        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose()
        self.cap = cv2.VideoCapture(0)
        self.old_state = 0
        self.new_state = 0
        self.image1 = None
        self.image2 = None
        self.flag = 0
        self.pTime = 0
        self.cTime = 0


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
            if self.port:
                if xavg > xcenter+50:
                    self.ser.write('d'.encode('utf-8'))
                    #print('sent d')

                if xavg < xcenter - 50:
                    self.ser.write('i'.encode('utf-8'))
                    #print('sent i')

                if yavg > ycenter + 50:
                    self.ser.write('3'.encode('utf-8'))
                    #print('sent 3')

                if yavg < ycenter - 50:
                    self.ser.write('4'.encode('utf-8'))
                    #print('sent 4')
        else:
            self.new_state = 0

        #if self.new_state - self.old_state == 0:
            #print("no change")
        if self.new_state == 1:
            self.pTime = 0

        if self.new_state - self.old_state == 1:
            print("human coming")
            #self.image1 = self.image2
            #self.image2 = img

        if self.new_state - self.old_state == -1:
            print("human leaving")
            #time.sleep(2)
            
            if self.port == None:
                self.flag = 1
            self.pTime = time.time()

        #if self.flag == 1:   #control extract item function
            #self.cTime = time.time()
            #if (self.cTime - self.pTime) > 2 and self.pTime != 0 and self.port == None:
                #extract_item(path, self.image1, self.image2)
                #self.flag = 0
                #self.pTime = 0
                #print("extracting")

        self.cTime = time.time()
        #print("current time")
        #print(self.cTime)
        #print("leave time")
        #print(self.pTime)

        if (self.cTime - self.pTime) > 3 and self.pTime != 0 and self.port: #send back to origin command to arduino after human leave 3 sec
            print("back to origin")
            self.ser.write('o'.encode('utf-8'))
            time.sleep(5)
            self.image1 = self.image2
            self.image2 = img
            if self.flag > 0:
                extract_item(path, self.image1, self.image2)
                cv2.imwrite(path+'image1.jpg',self.image1)
                cv2.imwrite(path+'image2.jpg',self.image2)
            self.flag = self.flag +1
            print(self.flag)
            self.pTime = 0
            print('servo extracted')
            print('image1')
            #print(self.image1)
            print('image2')
            #print(self.image2)


        cv2.imshow("image",img)
        cv2.waitKey(1)



    def Move_to_Origin(self):
        self.ser.write('o'.encode('utf-8'))
        print("back to origin")
        time.sleep(5)

    #def return_img(self):
        # return the image


