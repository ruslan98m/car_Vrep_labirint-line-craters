import math

class sKalman():

    def __init__(self,vv,vp):
        self.varVolt = vv
        self.varProcess = vp #cкорость реакции 
        self.Pc = 0.0
        self.G = 0.0
        self.P = 1.0
        self.Xp = 0.0
        self.Zp = 0.0
        self.Xe = 0.0


    def filter(val): 
        self.Pc = self.P + self.varProcess
        self.G = self.Pc/(self.Pc + self.varVolt)
        self.P = (1-self.G)*self.Pc
        self.Xp = self.Xe
        self.Zp = self.Xp
        self.Xe = self.G*(val-self.Zp)+self.Xp
        return self.Xe
