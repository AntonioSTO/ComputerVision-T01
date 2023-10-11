#imports ...
from math import pi,cos,sin
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Transform:
    def __init__(self, reference):
        self.reference = reference
    
    def move (self,dx,dy,dz):
        T = np.eye(4)
        T[0,-1] = dx
        T[1,-1] = dy
        T[2,-1] = dz
        return T

    def z_rotation(self,angle):
        angle = pi*(angle/180)
        rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
        return rotation_matrix

    def x_rotation(self,angle):
        angle = pi*(angle/180)
        rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
        return rotation_matrix

    def y_rotation(self,angle):
        angle = pi*(angle/180)
        rotation_matrix=np.array([[cos(angle),0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])
        return rotation_matrix
    
    def projectionModel(intrinsic,extrinsic,ref):
        #Operações de modelo de projeção
        pass
        #return matriz modelo de projeção
    
    