import vrep
import vrepConst
import math
import time

class Gripper():
    def __init__(self,clientid):

        self.clientID=clientid

        res,self.rollJoint=vrep.simxGetObjectHandle(self.clientID,'RJ',vrep.simx_opmode_blocking)
        res,self.gripperJoint1=vrep.simxGetObjectHandle(self.clientID,'SJ1',vrep.simx_opmode_blocking)
        res,self.gripperJoint2=vrep.simxGetObjectHandle(self.clientID,'SJ2',vrep.simx_opmode_blocking)

        vrep.simxSetJointPosition(self.clientID, self.rollJoint, 0, vrep.simx_opmode_streaming)
        vrep.simxSetJointPosition(self.clientID, self.gripperJoint1, 0, vrep.simx_opmode_streaming)
        vrep.simxSetJointPosition(self.clientID, self.gripperJoint2, 0, vrep.simx_opmode_streaming)

        res,pos1=vrep.simxGetJointPosition(self.clientID, self.gripperJoint1, vrep.simx_opmode_streaming)
        res,pos2=vrep.simxGetJointPosition(self.clientID, self.gripperJoint2, vrep.simx_opmode_streaming)
        res,pos3=vrep.simxGetJointPosition(self.clientID, self.rollJoint, vrep.simx_opmode_streaming)
        

    def initGripper(self):

        res,pos=vrep.simxGetJointPosition(self.clientID, self.rollJoint, vrep.simx_opmode_buffer)
        while pos>-math.pi/2-math.pi/12:
            vrep.simxSetJointPosition(self.clientID, self.rollJoint, pos-math.pi/50, vrep.simx_opmode_oneshot)
            res,pos=vrep.simxGetJointPosition(self.clientID, self.rollJoint, vrep.simx_opmode_buffer)
            time.sleep(0.01)

    def deinitGripper(self):
     
        res,pos=vrep.simxGetJointPosition(self.clientID, self.rollJoint, vrep.simx_opmode_buffer)
        while pos<0:
            vrep.simxSetJointPosition(self.clientID, self.rollJoint, pos+math.pi/50, vrep.simx_opmode_oneshot)
            res,pos=vrep.simxGetJointPosition(self.clientID, self.rollJoint, vrep.simx_opmode_buffer)
            time.sleep(0.01)


    def gripperAtach(self,mode):

        res,pos1=vrep.simxGetJointPosition(self.clientID, self.gripperJoint1, vrep.simx_opmode_buffer)
        res,pos2=vrep.simxGetJointPosition(self.clientID, self.gripperJoint2, vrep.simx_opmode_buffer)
        if mode:
            while pos2<math.pi/6:

                vrep.simxSetJointPosition(self.clientID, self.gripperJoint1, pos1-math.pi/50, vrep.simx_opmode_oneshot)
                vrep.simxSetJointPosition(self.clientID, self.gripperJoint2, pos2+math.pi/50, vrep.simx_opmode_oneshot)

                res,pos1=vrep.simxGetJointPosition(self.clientID, self.gripperJoint1, vrep.simx_opmode_buffer)
                res,pos2=vrep.simxGetJointPosition(self.clientID, self.gripperJoint2, vrep.simx_opmode_buffer)

                time.sleep(0.01)
        else:
            while pos2>0:

                vrep.simxSetJointPosition(self.clientID, self.gripperJoint1, pos1+math.pi/50, vrep.simx_opmode_oneshot)
                vrep.simxSetJointPosition(self.clientID, self.gripperJoint2, pos2-math.pi/50, vrep.simx_opmode_oneshot)

                res,pos1=vrep.simxGetJointPosition(self.clientID, self.gripperJoint1, vrep.simx_opmode_buffer)
                res,pos2=vrep.simxGetJointPosition(self.clientID, self.gripperJoint2, vrep.simx_opmode_buffer)

                time.sleep(0.01)


    def giveBall(self):
        self.gripperAtach(True)
        self.initGripper()
        self.gripperAtach(False)
        self.deinitGripper()

    def brokeBall(self):
        self.initGripper()
        self.gripperAtach(True)
        self.deinitGripper()
        self.gripperAtach(False)
        