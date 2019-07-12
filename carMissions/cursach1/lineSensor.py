import vrep
import vrepConst
import array
import random

import numpy as np

class IRSensors():

    def __init__(self,clientid):

        self.clientID=clientid
        self.sensErr=0.03

        res,self.leftSensor=vrep.simxGetObjectHandle(self.clientID,'LeftSensor',vrep.simx_opmode_blocking)
        res,self.colorSensor=vrep.simxGetObjectHandle(self.clientID,'ColorSensor',vrep.simx_opmode_blocking)
        res,self.rightSensor=vrep.simxGetObjectHandle(self.clientID,'RightSensor',vrep.simx_opmode_blocking)

        res, resolutionLeft, self.imageLeft = vrep.simxGetVisionSensorImage(self.clientID, self.leftSensor, 0, vrep.simx_opmode_streaming)
        res, resolutionRight, self.imageRight = vrep.simxGetVisionSensorImage(self.clientID, self.rightSensor, 0, vrep.simx_opmode_streaming)
        res, resolutionRight, self.greenSignal = vrep.simxGetVisionSensorImage(self.clientID, self.colorSensor, 0, vrep.simx_opmode_streaming)

    def getSensorSignal(self,sensorHandle):
        res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, sensorHandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype=np.uint8)

        
        return (int(img[0])+int(img[1])+int(img[2]))//3
       

    def getGreenColorSignal(self):
        res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.colorSensor, 0, vrep.simx_opmode_buffer)
        
        img = np.array(image, dtype=np.uint8)
        
        self.greenSignal=False

       
        if int(img[1])>230:
            self.greenSignal=True
        return self.greenSignal

    def getBlackColorSignal(self):
        self.blackSignal=False
        self.updateLineSensors()
        if (self.leftSignal+self.rightSignal)/2<60:
            self.blackSignal=True
        return self.blackSignal

    def getErrSensorsSignal(self):

        return self.getSensorSignal(self.leftSensor)-self.getSensorSignal(self.rightSensor)

    def updateLineSensors(self):
        self.rightSignal=self.getSensorSignal(self.rightSensor)
        self.leftSignal=self.getSensorSignal(self.leftSensor)