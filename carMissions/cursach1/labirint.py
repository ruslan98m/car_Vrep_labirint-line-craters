import vrep
import vrepConst
import time
import array
import numpy as np

import math
from regulator import pidControl
from imuSensor import IMU
from lidarSensor import Lidar
from robotKinematic import Robot
from proximitySensors import ProxSensor
from motionSensor import OpticalSensor
from labirintWay import Map
from lineSensor import IRSensors
def labirintAlgorithm():

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

 
    imu=IMU(clientID)
    regulator=pidControl(0.008,0.01,0.002)
    car=Robot(clientID,0.04)
    sens=ProxSensor(clientID)
    map=Map(clientID)
    lineSensors=IRSensors(clientID)
      

    
    map.getCameraImage()
    map.getMap()
    map.spreadRay()
    
    #lineSensors.getBlackColorSignal()
    i=0
    velocity=0.1
    dt=0.0001
    sens.updateAllSensors()
    time.sleep(2)
    U=0
    while True:
         

        timeStart=vrep.simxGetLastCmdTime(clientID)
        #lineSensors.getBlackColorSignal() 
        sens.updateAllSensors()      
        
        #if(sens.rsVal<0.6 and sens.rsVal>0.35) and (sens.lsVal<0.6 and sens.lsVal>0.35):
        #    regulator.pid(sens.rsVal-sens.lsVal,dt)
        #    U=regulator.U

        #else:
        #    U=0
        

        
        car.move(velocity+U,velocity-U,0,dt)
        #if(i==len(map.carWay)-1):
        #    time.sleep(4)
        #    break
        #print(sens.drsVal)
        if (sens.drsVal<0.4 and sens.drsVal>0.3) and (sens.dlsVal<0.4 and sens.dlsVal>0.3):
            if(map.carWay[i]==1):
                car.rotate(80)
                
            else:
                car.rotate(-80)

            sens.updateAllSensors() 
            time.sleep(0.5)       
            i+=1
        

        dt=(vrep.simxGetLastCmdTime(clientID)-timeStart)/1000

    car.stop()
    time.sleep(1)
    vrep.simxFinish(clientID)

