import vrep
import vrepConst
import numpy as np
import math 

class Lidar():

    def __init__(self,clientid,velocity,len):

        self.clientID=clientid
        self.lidarVelocity=velocity
        self.arrayLen=len
        self.lidarPosition=0
        self.sig=0
        self.i=0
        self.nearObstacle=np.array([0,0])
        self.distance=2*math.pi
        self.lidarBuffer=np.zeros((len,2))

        res, self.lidarSensor=vrep.simxGetObjectHandle(self.clientID,'LidarSensor',vrep.simx_opmode_blocking)
        res, self.lidarJoint=vrep.simxGetObjectHandle(self.clientID,'LidarJoint',vrep.simx_opmode_blocking)

        vrep.simxSetJointTargetVelocity(self.clientID,self.lidarJoint,self.lidarVelocity,vrep.simx_opmode_oneshot)

    def setLidarVelocity(self,vel):

        self.lidarVelocity=vel
        vrep.simxSetJointTargetVelocity(self.clientID,self.lidarJoint,self.lidarVelocity,vrep.simx_opmode_oneshot)
    
    def updateLidar(self):

        res, self.lidarPosition=vrep.simxGetJointPosition(self.clientID,self.lidarJoint,vrep.simx_opmode_oneshot)
        if(self.lidarPosition<0):
            self.lidarPosition+=2*math.pi

        res, self.ds,self.sig,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.lidarSensor,vrep.simx_opmode_oneshot)
        if(self.ds==True):
            self.lidarBuffer[self.i,0]=self.lidarPosition
            self.lidarBuffer[self.i,1]=self.sig[2]
            self.i+=1
            if(self.i>=self.arrayLen):
                self.i=0

    def getNearObstacle(self):
        for a in range(0,self.arrayLen):
            if self.nearObstacle[1]<self.lidarBuffer[a,1]:
                self.nearObstacle=self.lidarBuffer[a]            
            a+=1

    def getDistance(self,direction):
        for a in range(0,self.arrayLen):
            if self.distance<math.fabs(self.direction-self.lidarBuffer[a,0]):
                self.distance=self.lidarBuffer[a,1]            
            a+=1

    