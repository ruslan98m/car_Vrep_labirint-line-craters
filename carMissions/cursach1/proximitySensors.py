import vrep
import vrepConst
import random

class ProxSensor():
    def __init__(self,clientid):

        self.clientID=clientid
        self.sensErr=0.03

        self.drsVal=0
        self.dlsVal=0
        self.rsVal=0
        self.rsVal=0
        self.crsVal=0
        self.clsVal=0

        res,self.dirRightSens=vrep.simxGetObjectHandle(self.clientID,'DRS9930',vrep.simx_opmode_blocking)
        res,self.dirLeftSens=vrep.simxGetObjectHandle(self.clientID,'DLS9930',vrep.simx_opmode_blocking)
        res,self.rightSens=vrep.simxGetObjectHandle(self.clientID,'RS9930',vrep.simx_opmode_blocking)
        res,self.leftSens=vrep.simxGetObjectHandle(self.clientID,'LS9930',vrep.simx_opmode_blocking)
        res,self.cornRightSens=vrep.simxGetObjectHandle(self.clientID,'CRS9930',vrep.simx_opmode_blocking)
        res,self.cornLeftSens=vrep.simxGetObjectHandle(self.clientID,'CLS9930',vrep.simx_opmode_blocking)

        res, ds,DrsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.dirRightSens,vrep.simx_opmode_streaming)
        res, ds,DlsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.dirLeftSens,vrep.simx_opmode_streaming)
        res, ds,RsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.rightSens,vrep.simx_opmode_streaming)
        res, ds,LsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.leftSens,vrep.simx_opmode_streaming)
        res, ds,CrsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.cornRightSens,vrep.simx_opmode_streaming)
        res, ds,ClsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.cornLeftSens,vrep.simx_opmode_streaming)
    def updateAllSensors(self):

        res, ds,DrsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.dirRightSens,vrep.simx_opmode_oneshot)
        res, ds,DlsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.dirLeftSens,vrep.simx_opmode_oneshot)
        res, ds,RsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.rightSens,vrep.simx_opmode_oneshot)
        res, ds,LsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.leftSens,vrep.simx_opmode_oneshot)
        res, ds,CrsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.cornRightSens,vrep.simx_opmode_oneshot)
        res, ds,ClsVal,oh,dnv=vrep.simxReadProximitySensor(self.clientID,self.cornLeftSens,vrep.simx_opmode_oneshot)

        #add noise
        self.drsVal=DrsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal
        self.dlsVal=DlsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal
        self.rsVal=RsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal
        self.lsVal=LsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal
        self.crsVal=CrsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal
        self.clsVal=ClsVal[2]*random.uniform(1-self.sensErr, 1+self.sensErr)+random.uniform(-0.02, 0.03)*self.drsVal



       
