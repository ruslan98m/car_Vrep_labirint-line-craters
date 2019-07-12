import vrep
import vrepConst
import random

class OpticalSensor():
     def __init__(self,clientid):

        self.clientID=clientid
        self.sensErr=0.01
        self.movement=0
        
        res,self.sensorHandle=vrep.simxGetObjectHandle(self.clientID,'LineTracer', vrep.simx_opmode_blocking)

        res,self.startPosition=vrep.simxGetObjectPosition(self.clientID, self.sensorHandle, -1, vrep.simx_opmode_streaming)

        while self.startPosition[1]==0:
             res,self.startPosition=vrep.simxGetObjectPosition(self.clientID, self.sensorHandle, -1, vrep.simx_opmode_buffer)



     def getSensorMovement(self):

         res,pos=vrep.simxGetObjectPosition(self.clientID, self.sensorHandle, -1, vrep.simx_opmode_buffer)

         self.movementX=pos[0]-self.startPosition[0]
         self.movementY=pos[1]-self.startPosition[1]

         self.movementX*random.uniform(1-self.sensErr, 1+self.sensErr)
         self.movementY*random.uniform(1-self.sensErr, 1+self.sensErr)

         self.startPosition=pos

        