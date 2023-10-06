#imports ...

from stl import mesh
import numpy as np

class Object():
    def __init__(self,obj):
        self.mesh = mesh.Mesh.from_file(obj)
        self.obj = self.setObj()

        # Get the vectors that define the triangular faces that form the 3D object
        self.vectors = self.mesh.vectors 
    

    def setObj(self):
        x = self.mesh.x.flatten()
        y = self.mesh.y.flatten()
        z = self.mesh.z.flatten()
        
        """
        Create the 3D object from the x,y,z coordinates and add 
        the additional array of ones to represent the object 
        using homogeneous coordinates
        """
        obj = np.array([x.T,y.T,z.T,np.ones(x.size)])
        
        return obj
        




def set_axes_equal(ax):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    