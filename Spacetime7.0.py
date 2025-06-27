import sys, math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider,
    QHBoxLayout, QVBoxLayout,QDoubleSpinBox,QSpinBox, QDial
)
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

def add_slider(label_text, min_val, max_val, initial_val, callback, layout):
    row = QHBoxLayout()  
    row.setSpacing(1)
    row.setContentsMargins(0, 0, 0, 0)
    
    label = QLabel(label_text)
    label.setFixedWidth(70)
    slider = QSlider(Qt.Horizontal)
    slider.setRange(min_val, max_val)
    slider.setValue(initial_val)
    value_label = QLabel(str(initial_val))
    #value_label.setFixedWidth(40)

    def update(val):
        value_label.setText(str(val))
        callback(val)
    slider.valueChanged.connect(update)
    row.addWidget(label)
    row.addWidget(slider)
    row.addWidget(value_label)

    layout.addLayout(row)

    
def add_spinbox(label_text, min_val, max_val, step, initial_val, callback, layout):
    column = QVBoxLayout()
    label = QLabel(label_text)
    label.setAlignment(Qt.AlignCenter)
    spinbox = QSpinBox()
    spinbox.setRange(min_val, max_val)
    spinbox.setSingleStep(step)
    spinbox.setValue(initial_val)
    spinbox.valueChanged.connect(callback)
    column.addWidget(label)
    column.addWidget(spinbox)
    layout.addLayout(column)


class GLWidget(QGLWidget):
    def __init__(self):
        super().__init__()
        #Initiates the mass
        self.mass = 10
        self.mass2 = 10
        self.exponent = 10
        self.exponent2 = 10
        self.spacing = 100
        self.zoomX = 5000
        self.zoomY = 5000
        self.test = 0
        self.mass2 = 10
        self.positionX = 10
        self.positionY = 10
        self.positionX1 = 10
        self.positionY1 = 10
        self.radius1 = 15   # in grid‐units
        self.radius2 = 15
        self.height = 1e9

    #Makes mass global
    def set_mass(self, val):
        self.mass = val
        
    def set_mass2(self,val):
        self.mass2 = val
        
    def set_radius1(self,val):
        self.radius1 = val
        
    def set_radius2(self,val):
        self.radius2 = val
        
    def set_height(self,val):
        self.height = val
        
    def set_positionX(self,val):
        self.positionX = val
        
    def set_positionY(self,val):
        self.positionY = val
    
    def set_positionX1(self,val):
        self.positionX1 = val
        
    def set_positionY1(self,val):
        self.positionY1 = val
        
    def set_massTotal(self, val):
        self.massTotal = val
        
    def set_exponent(self,val):
        self.exponent = val

    def set_exponent2(self,val):
        self.exponent2 = val
        
    def set_spacing(self,val):
        self.spacing = val
        
    def set_zoomX(self,val):
        self.zoomX = val
        
    def set_zoomY(self,val):
        self.zoomY = val
        
    def set_test(self,val):
        self.test = val


    def initializeGL(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)  

    def resizeGL(self, w, h):
        if h == 0: 
            h = 1 #This just makes sure there are no infinities
        glViewport(0, 0, w, max(1, h))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / float(h), 0.1, 1000000000000000)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        #global massSlider
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #gluLookAt(200000, 300000, 0, 0, 10, 0,  0, 1, 0)
        #gluLookAt(self.zoomX, self.zoomY, 0, 0, 0, 0,  0, 1, 0)
        #gluLookAt(self.set_zoomX, 5000, 0, 0, 0, 0,  0, 1, 0)
        gluLookAt(self.zoomX, self.zoomY, 0, 0, 0, 0,  0, 1, 0)
        glColor3f(0, 1, 0)
        
        # simple 1/r gravity well. Might try to make this with constants. This is just m/r not Gm/r
        #Edit I added G and a mass that makes sense
        massTotal = self.mass * 10**(self.exponent)  #this changes the mass of the object
        massTotal2 = self.mass2 * 10**self.exponent2
        zoom = self.spacing
        G = 6.67e-11
        for i in range(-128, 129): #the loop can be changed depending on how big the well is. It changes the length and the width
            glBegin(GL_LINE_STRIP)
            for j in range(-128,129): #also has to be changed if the i is changed. 
                r1 = math.hypot(i + self.positionX1, j+self.positionY1) + .1 #Just the magnitude and the +.1 makes it so there's no division by 0
                r2 = math.hypot(i + self.positionX,j+ self.positionY)+.1
                x = i*zoom #This is just the view in the x direction
                z = j *zoom #The z direciton view
                # compute raw distances
                R1 = self.radius1
                R2 = self.radius2
                # outside vs inside potential for mass1
                if r1 > R1:
                    V1 = -G*massTotal/r1
                else:
                    V1 = G*massTotal*(r1*r1-3*R1*R1)/(2*R1**3)
                
                
                if r2 > R2:
                    V2 = -G*massTotal2/r2
                else:
                    V2 = G*massTotal2*((r2*r2-3*R2*R2) )/(2*R2**3)
                
                y = (V1 + V2)
                glVertex3f(x, y, z)
                #glVertex3f(x,y_2,z)

            glEnd()

        self.update()  #It just updates every frame
        
    

# Main app
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Spacetime")
window.setGeometry(100, 100, 800, 600)

main_layout = QHBoxLayout(window)

# Left panel
gl_widget = GLWidget()
#main_layout.addWidget(gl_widget, 3)

# Right panel
slider_layout = QVBoxLayout()
slider_layout.setSpacing(2)
slider_layout.setContentsMargins(5, 5, 5, 5)

label_row = QHBoxLayout()
maxRange = 250

#main_layout.addLayout(slider_layout, 1)
main_layout.setStretch(0,5)
main_layout.setStretch(1,2)
main_layout.addWidget(gl_widget, 5)
main_layout.addLayout(slider_layout, 2)


maxCamera = 1000000000

add_spinbox("Mass 1:", 0, 250, 1, 0, gl_widget.set_mass, slider_layout)
add_spinbox("Mass 2:", 0, 250, 1, 0, gl_widget.set_mass2, slider_layout)
add_spinbox("Exponent of mass 1:",0,100,1,10,gl_widget.set_exponent,slider_layout)
add_spinbox("Exponent of mass 2:",0,100,1,10,gl_widget.set_exponent2,slider_layout)
add_spinbox("Radius 1",0,100,1,15,gl_widget.set_radius1,slider_layout)
add_spinbox("Radius 2",0,100,1,15,gl_widget.set_radius2,slider_layout)
add_spinbox("spacing:",10,1000000,10,100,gl_widget.set_spacing,slider_layout)
#add_spinbox("Height", 0, 10000, 1, 1, gl_widget.set_height, slider_layout)
add_spinbox("P1 x:", -10000, 10000, 10, 10, gl_widget.set_positionY1, slider_layout)
add_spinbox("P1 y:", -10000, 10000, 10, 10, gl_widget.set_positionX1, slider_layout)
add_spinbox("P2 x:", -10000, 10000, 10, 10, gl_widget.set_positionY, slider_layout)
add_spinbox("P2 y:", -10000, 10000, 10, 10, gl_widget.set_positionX, slider_layout)
add_spinbox("Camera 1:",0,300000,1000,5000,gl_widget.set_zoomX,slider_layout)
add_spinbox("Camera 2:",0,300000,1000,5000,gl_widget.set_zoomY,slider_layout)
add_slider("Mass 1:", 0,250,50,gl_widget.set_mass,slider_layout)
add_slider("Mass 2:", 0,250,50,gl_widget.set_mass2,slider_layout)
add_slider("Camera 1:",0,300000,5000,gl_widget.set_zoomX,slider_layout)
add_slider("Camera 2:",0,300000,5000,gl_widget.set_zoomY,slider_layout)



window.show()
sys.exit(app.exec_())



