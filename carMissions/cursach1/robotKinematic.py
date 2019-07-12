import vrep
import vrepConst
import math
import time

#from cursach1 import application as app 

class Robot():

    def __init__(self,clientid,radiusWheel):

        self.clientID=clientid
        self.positionX=0
        self.positionY=0
        self.direction=0
        self.position=0
        self.radWheel=0.03
        self.distBetweenWheel=0.1

        res,self.leftMotor=vrep.simxGetObjectHandle(self.clientID,'DynamicLeftJoint',vrep.simx_opmode_blocking)
        res,self.rightMotor=vrep.simxGetObjectHandle(self.clientID,'DynamicRightJoint',vrep.simx_opmode_blocking)

        vrep.simxSetJointTargetVelocity(self.clientID,self.leftMotor, 0, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientID,self.rightMotor, 0, vrep.simx_opmode_streaming)

    def move(self,leftVel,rightVel,err,dt):

        vrep.simxSetJointTargetVelocity(self.clientID,self.leftMotor, leftVel/self.radWheel, vrep.simx_opmode_oneshot)
        vrep.simxSetJointTargetVelocity(self.clientID,self.rightMotor, rightVel/self.radWheel, vrep.simx_opmode_oneshot)

        
        self.positionX+=math.cos(self.direction)*(leftVel+rightVel)/2*dt
        self.positionY+=math.sin(self.direction)*(leftVel+rightVel)/2*dt

        self.position+=(leftVel+rightVel)/2*dt
        self.direction+=(rightVel-leftVel)*dt/self.distBetweenWheel

        #app.ui.label.setText(_translate("MainWindow", str(self.positionX)))
        #app.ui.label_2.setText(_translate("MainWindow", str(self.positionY)))
        #app.ui.label_3.setText(_translate("MainWindow", str(self.direction)))
    def moveDir(self,num):
        t=0
        position=0
        dt=0.001  
        dist=num*0.2
        self.position=0
        velocity=0.3
        t=dist/velocity
        
        #while(math.fabs(self.position)<dist):
        #    ts=vrep.simxGetLastCmdTime(self.clientID)
        self.move(velocity,velocity,0,dt)       
        #    dt=vrep.simxGetLastCmdTime(self.clientID)-ts
        time.sleep(t)  
        self.stop()
        


    def rotate(self,angle):
        t=0
        dt=0.001  
        realPos=0
        vel=0.05
        targetPos=self.distBetweenWheel/2*angle*math.pi/180
        if angle>0:
            vel=-vel        
        while(math.fabs(realPos)<math.fabs(targetPos)):
            ts=time.time() 
            realPos+=vel*dt
            self.move(vel, -vel, 0, dt)
            dt=time.time()-ts

        #self.direction+=angle*math.pi/180
        self.stop()

  

    def stop(self):
        vrep.simxSetJointTargetVelocity(self.clientID,self.leftMotor, 0, vrep.simx_opmode_oneshot)
        vrep.simxSetJointTargetVelocity(self.clientID,self.rightMotor, 0, vrep.simx_opmode_oneshot)
