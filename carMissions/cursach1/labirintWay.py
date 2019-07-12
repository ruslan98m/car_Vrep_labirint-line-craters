import vrep
import vrepConst
import numpy as np
import cv2
import time
import math


class Map():
    def __init__(self, clientid):
        self.clientID=clientid
        #self.resolution=[32,16]
        self.img=0
        res,self.cameraHandle=vrep.simxGetObjectHandle(self.clientID,'Vision_sensor',vrep.simx_opmode_blocking)
       
        res,self.resolution, image =  vrep.simxGetVisionSensorImage(self.clientID, self.cameraHandle, 0, vrep.simx_opmode_streaming)
        time.sleep(1)


    def getCameraImage(self):
        
        err, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.cameraHandle, 0, vrep.simx_opmode_buffer)
        image = np.array(image, dtype=np.uint8)
        image.resize([resolution[1], resolution[0], 3])
        center = (resolution[1] / 2, resolution[0] / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotImg = cv2.warpAffine(image, M, (resolution[0], resolution[1]))
        normImg=cv2.flip(image, 1)
        self.img=np.flip(normImg, axis=2)


    def getMap(self):



        hsv_min = np.array((0, 100, 100), np.uint8)
        hsv_max = np.array((30, 255, 255), np.uint8)
        
        # преобразуем RGB картинку в HSV модель
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV )
        # применяем цветовой фильтр
        self.thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        for i in range(0,16):
            for j in range(0,28):
                if not self.thresh[i][j]==0:
                    self.thresh[i][j]=1

        self.map=self.thresh[2:15,4:24]*(-1)
        self.map=np.flip(np.transpose(self.map),axis=1)
        #print(self.map)
        #resized = cv2.resize(self.thresh, (600,300), interpolation = cv2.INTER_AREA)
        #cv2.imshow('result', resized) 
        # if cv2.waitKey(1) & 0xFF == ord('q'):
           # cv2.destroyAllWindows()



    def showStream(self):
        #resized = cv2.resize(self.img, (600,300), interpolation = cv2.INTER_AREA)
        cv2.imshow('image',self.img )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def spreadRay(self):

        startPosY=19
        startPosX=7

        endPosY=0
        endPosX=11
                       
        chArr=self.map*(-1)
        self.wallArr=self.map*(-1)
        sprArr=self.map
        #print(len(chArr),len(chArr[0]))
        def addone(posX,posY,k):
            try:
                if chArr[posY][posX+1]==0:
                    sprArr[posY][posX+1]=k
                    stepArr[posY][posX+1]=1
            except:
                None
            try:
                if chArr[posY][posX-1]==0:
                    sprArr[posY][posX-1]=k
                    stepArr[posY][posX-1]=1
            except:
                None
            try:
                if chArr[posY+1][posX]==0:
                    sprArr[posY+1][posX]=k
                    stepArr[posY+1][posX]=1
            except:
                None
            try:
                if chArr[posY-1][posX]==0:
                    sprArr[posY-1][posX]=k
                    stepArr[posY-1][posX]=1
            except:
                None
            
            chArr[posY][posX]=1
            
        k=1
        addone(startPosX,startPosY,k)
        
       
        val=True
        while val:
            for i in range(0,len(sprArr)):
                for j in range(0,len(sprArr[0])):
                    if sprArr[i][j]==k:
                        addone(j,i,k+1)
                        #print(sprArr)
                        
                        if i==endPosY and j==endPosX:
                            val=False
            k+=1
            #сhArr=self.map
            #print(stepArr)
            

        
        

        pX = endPosX
        pY = endPosY
        
        stepArr=np.zeros((len(self.map),len(self.map[0])))

        def getNearWay(posY,posX):

            positionX=posX
            positionY=posY
            sig=True
            step=0
            try:
                if sprArr[posY][posX]-sprArr[posY][posX+1]==1 and sig:
                    #np.append(way,1)
                    step=1
                    positionX+=1                   
                    stepArr[posY][posX+1]=3                 
                    sig=False
                    
            except:
                None
            try:
                if sprArr[posY][posX]-sprArr[posY][posX-1]==1 and sig:
                    #np.append(way,2)  
                    step=2 
                    positionX-=1
                    stepArr[posY][posX-1]=3
                    sig=False
                    
            except:
                None
            try:
                if sprArr[posY][posX]-sprArr[posY+1][posX]==1 and sig:
                    #np.append(way,3)
                    step=3
                    positionY+=1
                    stepArr[posY+1][posX]=3
                    sig=False
                    
            except:
                None
            try:
                if sprArr[posY][posX]-sprArr[posY-1][posX]==1 and sig:
                    step=4
                    #np.append(way,4)
                    positionY-=1
                    stepArr[posY-1][posX]=3
                    sig=False
                    
            except:
                None
           
            
            return positionY,positionX,step
        way=[]
        self.carWay=[]
        while not(pX==startPosX and pY==startPosY):
            pY,pX,st=getNearWay(pY,pX)
            #print(st)
            way.append(st)
        #print(stepArr+self.wallArr)        
        way=np.flip(way,axis=0)
        print(way)
        for i in range(1,len(way)):
            if way[i]-way[i-1]==1 or way[i]-way[i-1]==-2:
                self.carWay.append(1)
                #print(way[i]-way[i-1])
                
            elif way[i]-way[i-1]==-1 or way[i]-way[i-1]==2:
                self.carWay.append(3)
                #print(way[i]-way[i-1])
                
        #    else:
                
        #        self.carWay.append(2)
        #print(self.carWay)

        #print(way)

        



