
import vrep
import vrepConst
import random
import math
class IMU():

    def __init__(self,clientid):

        self.clientID=clientid
        self.accelData=(0,0,0)
        self.gyroData=(0,0,0)
        self.sensErr=0.04

        res,self.accelHandle=vrep.simxGetObjectHandle(self.clientID,'Accelerometer',vrep.simx_opmode_blocking)
        res,self.gyroHandle=vrep.simxGetObjectHandle(self.clientID,'GyroSensor',vrep.simx_opmode_blocking)
        res,self.magnHandle=vrep.simxGetObjectHandle(self.clientID,'Magnetometr',vrep.simx_opmode_blocking)

        err,accelX=vrep.simxGetFloatSignal(self.clientID,'accelerometerX',vrep.simx_opmode_streaming)
        err,accelY=vrep.simxGetFloatSignal(self.clientID,'accelerometerY',vrep.simx_opmode_streaming)
        err,accelZ=vrep.simxGetFloatSignal(self.clientID,'accelerometerZ',vrep.simx_opmode_streaming)

        err,gyroX=vrep.simxGetFloatSignal(self.clientID,'gyroX',vrep.simx_opmode_streaming)
        err,gyroY=vrep.simxGetFloatSignal(self.clientID,'gyroY',vrep.simx_opmode_streaming)
        err,gyroZ=vrep.simxGetFloatSignal(self.clientID,'gyroZ',vrep.simx_opmode_streaming)

        res,euler=vrep.simxGetObjectOrientation(self.clientID,self.magnHandle,0,vrep.simx_opmode_streaming)

    def getAccelData(self):
       

        err,accelX=vrep.simxGetFloatSignal(self.clientID,'accelerometerX',vrep.simx_opmode_oneshot)
        err,accelY=vrep.simxGetFloatSignal(self.clientID,'accelerometerY',vrep.simx_opmode_oneshot)
        err,accelZ=vrep.simxGetFloatSignal(self.clientID,'accelerometerZ',vrep.simx_opmode_oneshot)

        accelNormX=accelX/9.81
        accelNormY=accelY/9.81
        accelNormZ=accelZ/9.81

        accelDataNorm=(accelNormX,accelNormY,accelNormZ)

        #added noise
        accelNormX*=random.uniform(1-self.sensErr,1+self.sensErr)
        accelNormY*=random.uniform(1-self.sensErr,1+self.sensErr)
        accelNormZ*=random.uniform(1-self.sensErr,1+self.sensErr)

        self.accelData=accelDataNorm


    def getGyroData(self):
       
        err,gyroX=vrep.simxGetFloatSignal(self.clientID,'gyroX',vrep.simx_opmode_oneshot)
        err,gyroY=vrep.simxGetFloatSignal(self.clientID,'gyroY',vrep.simx_opmode_oneshot)
        err,gyroZ=vrep.simxGetFloatSignal(self.clientID,'gyroZ',vrep.simx_opmode_oneshot)
        #added noise
        gyroX*=random.uniform(1-self.sensErr,1+self.sensErr)
        gyroY*=random.uniform(1-self.sensErr,1+self.sensErr)
        gyroZ*=random.uniform(1-self.sensErr,1+self.sensErr)

        self.gyroData=(gyroX,gyroY,gyroZ)

        
    def getMagnData(self):

        res,euler=vrep.simxGetObjectOrientation(self.clientID,self.magnHandle,0,vrep.simx_opmode_oneshot)

        #magnX=math.cos(euler[2])*math.cos(euler[1])*math.cos(euler[0])
        #magnY=math.sin(euler[2])*math.cos(euler[1])*math.cos(euler[0])
        #magnZ=math.sin(euler[1])*math.sin(euler[0])
        magnX=math.cos(euler[2])
        magnY=math.sin(euler[2])
        magnZ=0
        #added noise
        magnX*=random.uniform(1-self.sensErr,1+self.sensErr)
        magnY*=random.uniform(1-self.sensErr,1+self.sensErr)
        magnZ*=random.uniform(1-self.sensErr,1+self.sensErr)
       
        
        self.magnData=(magnX,magnY,magnZ)
        
        #print(self.magnData)

    def upgrateIMU(self):       

        self.getAccelData()
        self.getGyroData()
        self.getMagnData()

    def getYawAngle(self):
        self.yaw=math.atan2(self.magnData[1],self.magnData[0])

       