class pidControl():
    def __init__(self,kp,ki,kd):
        self.Kp=kp
        self.Kd=kd
        self.Ki=ki
        self.lastErr=0
        self.lastI=0
        self.U=0

    def pid(self,err,dt):
       P=self.Kp*err
       I=self.Ki*err*dt+self.lastI
       try:
            D=self.Kd/dt*(err-self.lastErr)
       except:
            D=0

       self.lastErr=err
       self.lastI=I
       self.U=P+I+D
class relle():

    def __init__(self,min,max,vel):
        self.U=0
        self.velocity=vel
        self.minErr=min
        self.maxErr=max

    def control(self,err):
        if err<self.minErr:
            self.U=self.velocity
        elif err>self.maxErr:
            self.U=-self.velocity
        else:
            self.U=0
        
