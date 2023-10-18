#imports ...
import numpy as np
from transformer import Transform

class Camera(Transform):
    
    def __init__(self):
        
        #Intrinsic Params
        self.focalDist = 50
        self.ccdx = 1
        self.ccdy = 1
        self.widthPixels = 1280
        self.heightPixels = 720
        self.sTheta = 0
        
        #Orientation and Position Matrix 
        self.M = np.eye(4)
        
    def define_ccdx(self, value):
        self.ccdx = value
        
    def define_ccdy(self, value):
        self.ccdy = value
        
    def define_focalDist(self, value):
        self.focalDist = value
        
    def define_sTheta(self, value):
        self.sTheta = value
        
    def define_heightPixels(self, value):
        self.heightPixels = value
        
    def define_widthPixels(self, value):
        self.widthPixels = value
        
    def get_Intrinsic(self):
        intrinsic = np.array([[self.focalDist*(self.widthPixels/self.ccdx), self.focalDist*(self.sTheta), self.widthPixels/2],
                              [0                          , self.focalDist*(self.widthPixels/self.ccdx), self.heightPixels/2],
                              [0                          , 0                                              ,               1]])
        
        return intrinsic
    
    def get_ReductMatrix(self):
        reduct = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])
        
        return reduct
    
    def update_Intrinsic(self,update):
        params_list = [self.widthPixels,self.heightPixels,self.ccdx,self.ccdy,self.focalDist,self.sTheta]
        
        for param in range(len(update)):
            if update[param] != 0:
                params_list[param] = update[param]
        
        self.define_widthPixels(params_list[0])
        self.define_heightPixels(params_list[1])
        self.define_ccdx(params_list[2])
        self.define_ccdy(params_list[3])
        self.define_focalDist(params_list[4])
        self.define_sTheta(params_list[5])