import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Configure:
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
        
    def set_plot(ax=None,figure = None,lim=[-2,2]):
        if figure ==None:
            figure = plt.figure(figsize=(8,8))
        if ax==None:
            ax = plt.axes(projection='3d')

        ax.set_title("camera referecnce")
        ax.set_xlim(lim)
        ax.set_xlabel("x axis")
        ax.set_ylim(lim)
        ax.set_ylabel("y axis")
        ax.set_zlim(lim)
        ax.set_zlabel("z axis")
        return ax

    #adding quivers to the plot
    def draw_arrows(point,base,axis,length=1.5):
        # The object base is a matrix, where each column represents the vector
        # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)


        # Plot vector of x-axis
        x = axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # Plot vector of y-axis
        y = axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # Plot vector of z-axis
        z = axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

        return x,y,z

    
    