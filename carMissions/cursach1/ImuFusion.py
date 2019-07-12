
import math 


class compliment():
    def __init__(self):

        self.roll=0
        self.pitch=0
        self.yaw=0

        self.K=0.7
        

    def filter(self,acc,gyro,dt):

        accX=math.pi/2-math.acos(acc[0])
        accY=math.pi/2-math.acos(acc[1])
        #accZ=math.pi/2-math.acos(acc[2])
        

        self.roll=(1-self.K)*(self.roll+gyro[0]*dt)+self.K*accX
        self.pitch=(1-self.K)*(self.pitch+gyro[1]*dt)+self.K*accY
        #self.yaw=(1-self.K)*(self.yaw+gyro[2]*dt)+self.K*accZ

        #print(self.roll,self.pitch)



