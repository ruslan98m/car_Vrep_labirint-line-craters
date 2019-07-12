import vrep
import vrepConst
import numpy as np
import cv2
import time
import math
#from cursach1 import application as app 

class Cam():
    def __init__(self, clientid):
        self.clientID=clientid
        self.resolution=[256,256]
        self.img=0
        res,self.cameraHandle=vrep.simxGetObjectHandle(self.clientID,'camera',vrep.simx_opmode_blocking)
        res,self.cameraRevolveJoint=vrep.simxGetObjectHandle(self.clientID,'cameraJoint',vrep.simx_opmode_blocking)
        res,self.cameraPrismaticJoint=vrep.simxGetObjectHandle(self.clientID,'PrismaticJoint',vrep.simx_opmode_blocking)

        res,self.resolution, image =  vrep.simxGetVisionSensorImage(self.clientID, self.cameraHandle, 0, vrep.simx_opmode_streaming)
        time.sleep(1)
        #cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        

    def getCameraImage(self):
        
        err, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.cameraHandle, 0, vrep.simx_opmode_buffer)
        image = np.array(image, dtype=np.uint8)
        image.resize([resolution[1], resolution[0], 3])
        center = (resolution[0] / 2, resolution[1] / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotImg = cv2.warpAffine(image, M, (resolution[0], resolution[1]))
        normImg=cv2.flip(rotImg, 1)
        self.img=np.flip(normImg, axis=2)
       # app.ui.convertToQtFormat(self.img,app.ui.)

    def trackObject(self,color):
        if color=='blue':
            hsv_min = np.array((100, 100, 100), np.uint8)
            hsv_max = np.array((140, 255, 255), np.uint8)

        elif color=='green':
            hsv_min = np.array((50, 100, 100), np.uint8)
            hsv_max = np.array((70, 255, 255), np.uint8)

        elif color=='red':
            hsv_min = np.array((0, 100, 100), np.uint8)
            hsv_max = np.array((30, 255, 255), np.uint8)
        
        # преобразуем RGB картинку в HSV модель
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV )
        # применяем цветовой фильтр
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)

        cv2.imshow('result', thresh) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        # вычисляем моменты изображения
        moments = cv2.moments(thresh, 1)

        xMoment = moments['m01']
        yMoment = moments['m10']
        area = moments['m00']

        if area==0:
            area=1

        x = int(xMoment / area)
        y = int(yMoment / area)
        
        sign=0
        if area>40:
            sign=True

        cv2.rectangle(self.img, (x, y), (int(area),int(area)), (255,0,0), 5)
        
        return sign,x,y,area
        
    

    def showStream(self):
        cv2.imshow('image',self.img )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def destroyAllStream(self):
        cv2.destroyAllWindows()


    def setCameraPosition(self,rot,pos):


        vrep.simxSetJointPosition(self.clientID,self.cameraRevolveJoint,-rot/180*math.pi,vrep.simx_opmode_oneshot)
        vrep.simxSetJointPosition(self.clientID,self.cameraPrismaticJoint,pos,vrep.simx_opmode_oneshot)
