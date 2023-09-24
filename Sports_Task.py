import sys
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from sports import Ui_MainWindow,MplCanvas 
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QMainWindow , QApplication , QLabel 

import matplotlib



class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        self.u=MplCanvas()
        self.ui = Ui_MainWindow()
        uic.loadUi("sports.ui",self)
        self.ui.setupUi(self)
############## GUI FOR CHOOSE THE DOMAIN ###############
        self.ui.horizontalSlider.setMaximum(200)
        self.ui.horizontalSlider.setMinimum(100)
        self.ui.horizontalSlider.setTickInterval(5)
        self.ui.horizontalSlider.valueChanged.connect(self.valuechange)
        self.ui.fig.clf()
        self.u.axes = self.ui.fig.gca()
        self.data_start = 100
        self.data_end = 300
        self.data_points = 40
        self.data = np.linspace(self.data_start, self.data_end, self.data_points)
        self.mean = 160
        self.std = 20
       
        self.Distance = 0
        self.Angle = 0
        self.Velocity = 0
        self.ui.Distance_lineEdit.textChanged.connect(lambda: self.Calc_Height())
        self.ui.Angle_lineEdit.textChanged.connect(lambda: self.Calc_Height())
        self.ui.velocity_lineEdit.textChanged.connect(lambda: self.Calc_Height())

        self.probability_cdf = norm.cdf(self.data, loc=self.mean, scale=self.std)
        
        print("the probabilty of the mean= ",self.probablity(self.mean))


        
        self.u.axes.plot(self.data,self.probability_cdf)  
        
        self.u.axes.vlines(self.mean, 0, self.probablity(self.mean), colors='k', linestyles='--')
        self.ui.image_canvas.draw() 
        self.ui.image_canvas.flush_events()

    def probablity (self,x):
        probability_cdf = norm.cdf(x, loc=self.mean, scale=self.std)
        return probability_cdf

    def valuechange(self):
        self.ui.fig.clf()
        self.u.axes = self.ui.fig.gca()
        self.speed = self.ui.horizontalSlider.value()
        probability_pdf2 = norm.cdf(self.speed, loc=self.mean, scale=self.std)
        print("the probabilty of the velocity = ",probability_pdf2)
        self.ui.textEdit.setText("the probabilty =  "+ str(probability_pdf2))
        self.u.axes.plot(self.data,self.probability_cdf)  
        self.u.axes.vlines(self.mean, 0, self.probablity(self.mean), colors='k', linestyles='--')
        self.u.axes.vlines(self.speed, 0, self.probablity(self.speed), colors='r', linestyles='dotted',label='velocity')
        self.ui.image_canvas.draw() 
        self.ui.image_canvas.flush_events()

         ##########################################################################################
        
    def get_DistanceFromGoal(self):
            if self.ui.Distance_lineEdit.text() != "":
                    self.Distance = self.ui.Distance_lineEdit.text()
            return float(self.Distance)

    def get_FiringAngle(self):
            if self.ui.Angle_lineEdit.text() != "":
                    self.Angle = self.ui.Angle_lineEdit.text()
            return float(self.Angle)

    def get_FiringVelocity(self):
            if self.ui.velocity_lineEdit.text() != "":
                    self.Velocity = self.ui.velocity_lineEdit.text()
            return float(self.Velocity)

    def Calc_Height(self):
            if (self.ui.Distance_lineEdit.text() != "" and self.ui.velocity_lineEdit.text() != ""):
                    D = self.get_DistanceFromGoal()
                    theta = self.get_FiringAngle()
                    ##print(np.sin(theta * np.pi/180))
                    Vo = self.get_FiringVelocity()
                    g = 9.8
                    ## Rising Phase ##
                    self.T1 = (Vo * np.sin(theta * np.pi / 180)) / g                                        ## the ball reaches the top at time T1
                    # print(self.T1)
                    self.h = (Vo * self.T1 * np.sin(theta * np.pi / 180)) - (0.5 * g * (self.T1) ** 2)       ## Corresponding Elevation
                    self.ui.Max_Height.setText(" " + str(self.h))
                    self.S = Vo * self.T1 * np.cos(theta * np.pi / 180)                                    ## Horizontal Distance from Firing Point
                    ## Falling Phase ##
                    self.S_dash = D - self.S
                    self.T2 = self.S_dash / (Vo * np.cos(theta * np.pi / 180))
                    self.h_dash = self.h - (0.5 * g * (self.T2) ** 2)
                    self.ui.HeightAtGoal.setText(" " + str(self.h_dash))


def main():
    app = QApplication(sys.argv)
    main = UI()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()