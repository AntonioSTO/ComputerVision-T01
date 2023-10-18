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