import vrep
import vrepConst
import time
import array
import numpy as np
import math

from regulator import pidControl, relle
from imuSensor import IMU
from lidarSensor import Lidar
from lineSensor import IRSensors
from robotKinematic import Robot
from proximitySensors import ProxSensor
from camera import Cam
from ImuFusion import compliment
from gripper import Gripper

def startMission():

    vrep.simxFinish(-1)

    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    while clientID<=-1:

        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

    if clientID!=-1:  
        print ('Successful !!!')
    
    else:
        print ('connection not successful')
        #sys.exit('could not connect')

    print ('connected to remote api server')

    #vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
    sens=ProxSensor(clientID)
    lineSensors=IRSensors(clientID)
    imu=IMU(clientID)
    regulator=pidControl(0.006 ,0.001,0.001)
    cameraAreaControl=relle(10000,10500,0.03)
    cameraPosControl=relle(124,126,0.005)
    car=Robot(clientID,0.04)
    camera=Cam(clientID)
    imuFilter=compliment()
    gripper=Gripper(clientID)

    step=1
    velocity=0.1

    crater1=np.array([3,4])
    crater2=np.array([3,7])

    def moveDir(vel,pos):
        dt=0
        edgeS=False #машинка на склоне
        edgeS2=False#машинка проехала склон

        position=1
        while( position<pos ):
            ts=vrep.simxGetLastCmdTime(clientID)

            
            camera.getCameraImage()
            sign,x,y,area=camera.trackObject('red')
            cameraPosControl.control(y)
            if area>120 and area<140:
                position=3
            elif area>180 and area<200:
                position=4
            elif area>260 and area<300:
                position=5
            elif area>450 and area<550:
                position=6
            elif area>1300 and area<1800:
                position=7
            elif area>2400 and area<3000:
                position=8
            
            if(sign):
                U1=cameraPosControl.U                

            else:
                U1=0.02
                
            car.move(-U1-vel,+U1-vel,0,dt)
            print(area,position)
            #if(position>=pos and y<128 and y>122):             
            #    break

            #sens.updateAllSensors()
            #regulator.pid(sens.lsVal-0.4,dt)
            #imu.upgrateIMU()
            #imuFilter.filter(imu.accelData,imu.gyroData,dt)
            #if(imuFilter.roll>0.2 and not lineSensors.getGreenColorSignal()):
            #    U=0
            #    if not edgeS2 and not edgeS:
            #        edgeS=True
            #else:
            #    #U=regulator.U
            #    U=0
            #if(imuFilter.roll<0.2 and edgeS):
            #    edgeS2=True
            #    car.position=0
            #    edgeS=False
            #if edgeS:
            #    car.position=0

            #car.move(-vel-U,-vel+U,0,dt)
            
            dt=(vrep.simxGetLastCmdTime(clientID)-ts)/1000
        car.stop()
        car.position=0



    def moveWhile(color):
        dt=0.001
        lineSensors.updateLineSensors()
        lineSensors.getBlackColorSignal()
        lineSensors.getGreenColorSignal()  
        signal=False
        while(not signal):
            ts=vrep.simxGetLastCmdTime(clientID)
            lineSensors.getBlackColorSignal()
            lineSensors.getGreenColorSignal()  
            if color=='green':
                signal=lineSensors.greenSignal 
            elif color=='black':
                signal=lineSensors.blackSignal 
                #print(lineSensors.blackSignal )
            car.move(-velocity,-velocity,0,dt)
            dt=(vrep.simxGetLastCmdTime(clientID)-ts)/1000
        time.sleep(2)
        car.stop()
           
    
    
    def getBall():
        dt=0.001
        camera.setCameraPosition(0,0)
        while True:
            ts=vrep.simxGetLastCmdTime(clientID)
            camera.getCameraImage()
            sign,x,y,area=camera.trackObject('blue')
            
            cameraAreaControl.control(area)
            cameraPosControl.control(y)
            if(sign):
                U1=cameraPosControl.U
                U2=cameraAreaControl.U
                #print(y)
            else:
                U1=0.02
                U2=0
            car.move(-U2-U1,-U2+U1,0,dt)
            #print(area)
            if(area>6700 and y<126 and y>122):
                car.stop()
                gripper.giveBall()
                break

            camera.showStream()
            dt=(vrep.simxGetLastCmdTime(clientID)-ts)/1000
    def searchDir(color):
        camera.setCameraPosition(30,0.8)
        dt=0.001
        while True:
            ts=vrep.simxGetLastCmdTime(clientID)
            camera.getCameraImage()
            sign,x,y,area=camera.trackObject(color)
            
            cameraAreaControl.control(area)
            cameraPosControl.control(y)
            if(sign):
                U1=cameraPosControl.U
                U2=cameraAreaControl.U

            else:
                U1=0.02
                U2=0
            car.move(-U2-U1,-U2+U1,0,dt)
            #print(area)
            if(area>1000 and y<128 and y>122):
                car.move(-velocity,-velocity,0,dt)
                break

            camera.showStream()
            dt=(vrep.simxGetLastCmdTime(clientID)-ts)/1000

    def colibrate():
        camera.setCameraPosition(30,0.8)
        dt=0.001
        while True:
            ts=vrep.simxGetLastCmdTime(clientID)
            camera.getCameraImage()
            sign,x,y,area=camera.trackObject('red')
            
            cameraAreaControl.control(area)
            cameraPosControl.control(y)
            if(sign):
                U1=cameraPosControl.U
                U2=cameraAreaControl.U

            else:
                U1=0.02
                U2=0
            car.move(-2*U2-U1,-2*U2+U1,0,dt)
            #print(area)
            if(y<128 and y>122):
                car.stop()
                camera.destroyAllStream()
                break

            camera.showStream()
            dt=(vrep.simxGetLastCmdTime(clientID)-ts)/1000


    
    
    def makeOperation(pos):  
        colibrate()
        moveDir(velocity,pos)
        car.rotate(80) 
        moveWhile('black')
        getBall()
        if pos>5:
            searchDir('blue')
        searchDir('green')
        moveWhile('green')
        gripper.brokeBall()
    
    makeOperation(crater1[1])
    makeOperation(crater2[1])
    
    
    car.stop()
    camera.destroyAllStream()
    time.sleep(1)  
    vrep.simxFinish(clientID)