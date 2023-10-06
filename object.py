#imports ...

from stl import mesh
import numpy as np

class Object():
    def __init__(self,obj):
        self.mesh = mesh.Mesh.from_file(obj)
        self.obj = self.setObj()
        self.vectors = self.mesh.vectors
        
    def setObj(self):
        x = self.mesh.x.flatten()
        y = self.mesh.y.flatten()
        z = self.mesh.z.flatten()
        
        obj = np.array([x.T,y.T,z.T,np.ones(x.size)])
        
        return obj
        
    