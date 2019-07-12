import vrep
import vrepConst
import time
import array
import numpy as np
import math

from regulator import pidControl
from imuSensor import IMU
from lidarSensor import Lidar
from lineSensor import IRSensors
from robotKinematic import Robot
from proximitySensors import ProxSensor



def lineFollow():

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
    regulator=pidControl(0.0006,0.0001,0.0001)
    car=Robot(clientID,0.04)

    dt=0.0001
    greenSignal=False

    while not lineSensors.greenSignal:
        
        velocity=0.3
        timeStart=vrep.simxGetLastCmdTime(clientID)
        lineSensors.getGreenColorSignal()
        imu.upgrateIMU()
        sens.updateAllSensors()
        lineSensors.updateLineSensors()

        try:
            err=lineSensors.getErrSensorsSignal()
        except:
            err=0
        sens.updateAllSensors()
        regulator.pid(err,dt)
        car.move(velocity+regulator.U, velocity-regulator.U,0, dt)
        
        if (sens.drsVal<0.2 and sens.drsVal >0.03) and (sens.dlsVal<0.2 and sens.drsVal>0.03):

             print(sens.dlsVal,sens.drsVal)
             radius=(sens.drsVal+sens.dlsVal)/2+0.2
             sens.updateAllSensors()
             car.stop()
             car.rotate(-70)
             wl=2*math.pi*(radius-car.distBetweenWheel/2)/10
             wr=2*math.pi*(radius+car.distBetweenWheel/2)/10


             cl=False
             cr=False

             while (not cl and not cr):
                 sens.updateAllSensors()
                 if lineSensors.getSensorSignal(lineSensors.leftSensor)<100:
                     cl=True
                 if lineSensors.getSensorSignal(lineSensors.rightSensor)<100:
                     cr=True

                 car.move(wl,wr,0,dt)
             time.sleep(0.35)

             blackTrig=False
             whiteTrig=False
             while (not blackTrig and not whiteTrig):
                sens.updateAllSensors()
                car.rotate(4)
                if lineSensors.getSensorSignal(lineSensors.rightSensor)<100:
                     blackTrig=True
                elif lineSensors.getSensorSignal(lineSensors.rightSensor)>100 and blackTrig:
                     whiteTrig=True
             car.stop()
             time.sleep(0.2)
        
        dt=(vrep.simxGetLastCmdTime(clientID)-timeStart)/1000

    car.stop()
    time.sleep(1)
    vrep.simxFinish(clientID)