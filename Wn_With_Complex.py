from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import *
from os import path
import sys
import math
import cmath
import matplotlib.pyplot as plt
from pylab import *

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

class Complex:
    def __init__(self , R , I):
        self.real = R
        self.img = I
    def add_complex(self,z1,z2):
        Z.real = z1.real + z2.real
        Z.img = z1.img + z2.img
        return Z
    def sub_complex(self,z1,z2):
        Z.real = z1.real - z2.real
        Z.img = z1.img - z2.img
        return Z
    def multiply_complex(self,z1,z2):
        Z.real = z1.real * z2.real - z1.img * z2.img
        Z.img = z1.real * z2.img + z1.img * z2.real 
        return Z
    def get_mag(self):
        mag = math.sqrt( ( (self.real)**2 ) + ( (self.img)**2 ))
        return mag
    def get_phase(self):
        phase = math.atan2(self.img,self.real) # check for tan-1
        return phase
    def polar(self,z):
        return self.get_mag(z),self.get_phase(z)

class MainApp(QtWidgets.QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui()
        self.handle_btns()
        
    def handle_btns(self):
        self.Wn_calc.clicked.connect(self.Get_Wn)
        self.btn_clear.clicked.connect(self.Clear)
        self.btn_plot_phase.clicked.connect(self.Plot_phase)
        self.btn_plot_mag.clicked.connect(self.Plot_mg)
 
    def Get_Wn(self):
        try:
            N = int(self.in_N.text())
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter N Samples Or Invalid Entry")       
            return
        try:
            x_n_str = self.in_x_n.text().split(',')
            x_n = [Complex(float(i),0) for i in x_n_str]
            n = len(x_n)
            if n <= N:
                for i in range(N-n):
                    x_n.append(Complex(float(0),0))
            else :
                QtWidgets.QMessageBox.warning(self,"ERROR","Number of samples in x(n) Must be less than or equal N Samples")       
                return
            Wn_factor = 2*math.pi/N
            Wn = [[Complex(0,0) for i in range(N)] for i in range(N)]
            Sum = Complex(0,0) 
            X_K = [Complex(0,0) for i in range(N)]
            
            for i in range(N):
                for j in range(N):
                    Wn[i][j].real = math.cos(round((Wn_factor*i*j),2))
                    Wn[i][j].img = -1*math.sin(round((Wn_factor*i*j),2))
                    #Wn[i][j] = cmath.e ** complex(0.0,-1*Wn_factor*i*j)  #another formula
                    Sum.real += x_n[j].real * Wn[i][j].real
                    Sum.img += x_n[j].real * Wn[i][j].img
                    #Sum = Complex.add_complex(Sum,Complex(x_n[j] * Wn[i][j].real ,x_n[j] * Wn[i][j].img))
                X_K[i].real = Sum.real
                X_K[i].img = Sum.img
                Sum = Complex(0,0)
            
            X_K_mag = [X_K[i].get_mag() for i in range(N)]
            X_K_ph = [X_K[i].get_phase() for i in range(N)]
            
            X_K_magnitude = " "
            X_K_phase = " "
            
            for i in range(N):
                X_K_magnitude += str(round((X_K_mag[i]),2)) + "||"
                X_K_phase += str(round((X_K_ph[i])*(180/math.pi),2)) + "||"

            self.out_magnitude.setText(X_K_magnitude)
            self.out_phase.setText(X_K_phase)           
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter x(n) values Or Invaid Entry")
            return
        
    def Clear(self):
        self.out_magnitude.setText('')
        self.out_phase.setText('')
        self.in_x_n.setText('')
        self.in_N.setText('')
            
    def handle_ui(self):
        QtWidgets.QMainWindow.setWindowTitle(self,"Discrete Fourier Transform Calculator")
        QtWidgets.QMainWindow.setFixedSize(self,415,361 )
    def Plot_mg(self):
        if self.in_N.text() == None or self.in_N.text() == '':
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Enter N Samples")
        elif self.in_x_n.text() == None or self.in_x_n.text() == '' :
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Enter x(n) values")
        elif (self.out_magnitude.text() == None or self.out_magnitude.text() == '' ) and (self.out_phase.text() == None or self.out_phase.text() == '' ):
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Click Calculate X(K)")
        else:
            x = [i+1 for i in range(int(self.in_N.text()))]
            y_mag = self.out_magnitude.text().split('||')
            y_m = [float(y_mag[i]) for i in range(int(self.in_N.text()))]
            
            plt.figure(1)
            stem(x, y_m, '-.', bottom=0)
            plt.xlabel('K')
            plt.ylabel('Magnitude')
            #plt.grid(True)
            show()            
        return

    def Plot_phase(self):
        if self.in_N.text() == None or self.in_N.text() == '' :
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Enter N Samples")
        elif self.in_x_n.text() == None or self.in_x_n.text() == '':
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Enter x(n) values")
        elif (self.out_magnitude.text() == None or self.out_magnitude.text() == '' ) and (self.out_phase.text() == None or self.out_phase.text() == '' ):
            QtWidgets.QMessageBox.warning(self,"ERROR","You didn't Click Calculate X(K)")
        else:
            x = [i+1 for i in range(int(self.in_N.text()))]
            y_phase = self.out_phase.text().split('||')
            y_p = [float(y_phase[i]) for i in range(int(self.in_N.text()))]

            plt.figure(2)
            stem(x, y_p, '-.', bottom=0)
            plt.xlabel('K')
            plt.ylabel('Phase')
            plt.grid(True)
            show()
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    