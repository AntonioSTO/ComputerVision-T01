import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from object import *
from cam import Camera
from configure import Configure
import math


###### Crie suas funções de translação, rotação, criação de referenciais, plotagem de setas e qualquer outra função que precisar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #definindo as variaveis
        self.set_variables()
        #Ajustando a tela    
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()

    def set_variables(self):
        self.objeto_original = [] #modificar
        self.objeto = self.objeto_original
        self.cam_original = Camera() #modificar
        self.cam = Camera() #modificar
        self.px_base = 1280  #modificar
        self.px_altura = 720 #modificar
        self.dist_foc = 10 #modificar
        self.stheta = 0 #modificar
        self.ox = self.px_base/2 #modificar
        self.oy = self.px_altura/2 #modificar
        self.ccd = [36,24] #modificar
        self.projection_matrix = [] #modificar
        
    def setup_ui(self):
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2  = self.create_cam_widget("Ref camera")
        line_edit_widget3  = self.create_intrinsic_widget("params instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

          # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        
        ##### Falta acertar os limites do eixo X
        self.ax1.set_xlim([0, self.cam.widthPixels])
        self.ax1.xaxis.tick_top()
        
        ##### Falta acertar os limites do eixo Y
        self.ax1.set_ylim([self.cam.heightPixels, 0])
          
        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        # self.object = Object('gengar.stl')
        self.mesh = mesh.Mesh.from_file('gengar.stl')
        self.obj = self.setObj()
        self.obj = (1/2)*self.obj
        self.vectors = self.mesh.vectors

        ##### Você deverá criar a função de projeção 
        object_2d = self.projection_2d()

        ##### Falta plotar o object_2d que retornou da projeção
        self.obj_view = self.ax1.plot(object_2d[0, :], object_2d[1, :], color = (0.2, 0.2, 0.2, 0.9), linewidth = 0.3) 
        # Get the vectors that define the triangular faces that form the 3D object

        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.ax2.plot(self.obj[0,:], self.obj[1,:], self.obj[2,:], 'r')
        set_axes_equal(self.ax2)
        
        Configure.draw_arrows(np.array([0,0,0,1]), np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]]), self.ax2, 10)

        ### Seta os limites do plot 3D
        x_limits = self.ax2.get_xlim3d()
        y_limits = self.ax2.get_ylim3d()
        z_limits = self.ax2.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        plot_radius = 0.7*max([x_range, y_range, z_range])

        self.ax2.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        self.ax2.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        self.ax2.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
        
        plt.ion()
        
        ##### Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo
        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)
        
        self.axis = self.ax2
        self.x_cam, self.y_cam, self.z_cam = Configure.draw_arrows(self.cam.M[:,3], self.cam.M[:,0:3], self.ax2, 5.0)
        
        # Retornar o widget de canvas
        return canvas_widget


    ##### Você deverá criar as suas funções aqui
    
    def update_params_intrinsc(self, line_edits):

        self.cam.update_Intrinsic(line_edits)

        self.update_canvas()
        

    def update_world(self,line_edits):
        new_update = []
        for i in range(len(line_edits)):
            if line_edits[i].text() == '':
                new_update.append(0)
            else:
                new_update.append(float(line_edits[i].text()))
        
        self.cam.M = (self.cam.move(new_update[0],new_update[2],new_update[4]))@self.cam.M
        
        R1 = self.cam.x_rotation(new_update[1])
        R2 = self.cam.y_rotation(new_update[3])
        R3 = self.cam.z_rotation(new_update[5])
        
        self.cam.M = (R3@R2@R1)@self.cam.M
        
        self.update_canvas()

    def update_cam(self,line_edits):
        new_update = []
        for i in range(len(line_edits)):
            if line_edits[i].text() == '':
                new_update.append(0)
            else:
                new_update.append(float(line_edits[i].text()))

        cam_orig = self.cam_original.M
        
        T = self.cam.move(new_update[0],new_update[2],new_update[4])
        self.cam.M = self.cam.M@cam_orig@T
    
        Rx = self.cam.x_rotation(new_update[1])
        self.cam.M = self.cam.M@cam_orig@Rx
        
        Ry = self.cam.y_rotation(new_update[3])
        self.cam.M = self.cam.M@cam_orig@Ry
        
        Rz = self.cam.z_rotation(new_update[5])
        self.cam.M = self.cam.M@cam_orig@Rz
        
        self.update_canvas()
    
    def projection_2d(self):
        project_matrix = self.cam.get_Intrinsic()@self.cam.get_ReductMatrix()@np.linalg.inv(self.cam.M)@self.obj
        
        project_matrix *= 1/project_matrix[2]
        
        
        return project_matrix
    

    def update_canvas(self):
        
        #2d view update
        
        for item in self.obj_view:
            item.remove()
            
        object_2d = self.projection_2d()
        self.obj_view = self.ax1.plot(object_2d[0, :], object_2d[1, :], color = (0.2, 0.2, 0.2, 0.9), linewidth = 0.3)
        
        #Cam plot update
        self.x_cam.remove()
        self.y_cam.remove()
        self.z_cam.remove()
        
        self.x_cam, self.y_cam, self.z_cam = Configure.draw_arrows(self.cam.M[:,3], self.cam.M[:,0:3], self.ax2, 5.0)

        self.ax1.set_xlim([0, self.cam.widthPixels])
        self.ax1.xaxis.tick_top()
        self.ax1.set_ylim([self.cam.heightPixels, 0])
    
    def reset_canvas(self):
        self.cam = Camera()
        self.update_canvas()
    

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
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
