from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import *
from os import path
import sys
import math 
import cmath
import matplotlib.pyplot as plt
from pylab import *

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

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
        self.btn_FFT.clicked.connect(self.FFT)

    def Get_Wn(self):
        try:
            N = int(self.in_N.text())
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter N Samples Or Invalid Entry")       
            return
        try:
            x_n_str = self.in_x_n.text().split(',')
            x_n = [float(i) for i in x_n_str]
            n = len(x_n)
            if n <= N:
                for i in range(N-n):
                    x_n.append(float(0))
            else :
                QtWidgets.QMessageBox.warning(self,"ERROR","Number of samples in x(n) Must be less than or equal N Samples")       
                return
            Wn_factor = 2*math.pi/N
            Wn = [[0 for i in range(N)] for i in range(N)]
            Sum = 0 
            X_K = [0 for i in range(N)]
            
            for i in range(N):
                for j in range(N):
                    #Wn[i][j] = complex(math.cos(round((Wn_factor*i*j),2)),-1*math.sin(round((Wn_factor*i*j),2))) 
                    Wn[i][j] = cmath.e ** complex(0.0,-1*Wn_factor*i*j)  #another formula
                    Sum += Wn[i][j] * x_n[j] 
                X_K[i] = Sum
                Sum = 0
            
            X_K_mag_phase = [cmath.polar(X_K[i]) for i in range(N)]
            
            X_K_magnitude = ""
            X_K_phase = ""
            
            for i in range(N):
                X_K_magnitude += str(round((X_K_mag_phase[i][0]),2)) + "||"
                X_K_phase += str(round((X_K_mag_phase[i][1])*(180/math.pi),2)) + "||"

            self.out_magnitude.setText(X_K_magnitude)
            self.out_phase.setText(X_K_phase)           
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter x(n) values Or Invaid Entry")
            return
    
    def FFT(self):
        try:
            N = int(self.in_N.text())
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter N Samples Or Invalid Entry")       
            return
        try:
            x_n_str = self.in_x_n.text().split(',')
            x_n = [float(i) for i in x_n_str]
            n = len(x_n)
            if n <= N:
                for i in range(N-n):
                    x_n.append(float(0))
            else :
                QtWidgets.QMessageBox.warning(self,"ERROR","Number of samples in x(n) Must be less than or equal N Samples")       
                return
        except Exception:
            QtWidgets.QMessageBox.warning(self,"ERROR","Either,You didn't Enter x(n) values Or Invaid Entry")
            return
        self.test.setText(test_txt)
        log = math.log2(len(x_n))
        test_txt = ''
        # print(float(log))
        # print(float(int(log)))
        if float(log) - int(log) == 0:
            self.test.setText("success with " + str(log))
        else:
            test_txt = str(float(log)) + "|" + str(float(int(log)))
            self.test.setText(test_txt)
            QtWidgets.QMessageBox.warning(self,"ERROR","Can't Use FFT algorithm on x(n)")
            self.test.setText("")

        Wn_factor = 2*math.pi/N

    def radix2_dit(self,xn,N): # recursion function 
        if len(xn) == 2:
            pass

        else:
            f1 = [xn[i] for i in range(len(xn)) if i % 2 == 0]
            f2 = [xn[i] for i in range(len(xn)) if i % 2 != 0]
            radix2_dit(f1,N/2)
            radix2_dit(f2,N/2)

    def Clear(self):
        self.out_magnitude.setText(' ')
        self.out_phase.setText(' ')
        self.in_x_n.setText(' ')
        self.in_N.setText(' ')
            
    def handle_ui(self):
        QtWidgets.QMainWindow.setWindowTitle(self,"Discrete Fourier Transform Calculator")
        QtWidgets.QMainWindow.setFixedSize(self,415,361 )

    def Plot_mg(self):
        x = [i+1 for i in range(int(self.in_N.text()))]
        y_mag = self.out_magnitude.text().split('||')
        y_m = [float(y_mag[i]) for i in range(int(self.in_N.text()))]
        
        plt.figure(1)
        stem(x, y_m, '-.', bottom=0)
        plt.xlabel('K')
        plt.ylabel('Magnitude')
        plt.grid(True)
        show()

    def Plot_phase(self):

        x = [i+1 for i in range(int(self.in_N.text()))]
        y_phase = self.out_phase.text().split('||')
        y_p = [float(y_phase[i]) for i in range(int(self.in_N.text()))]

        plt.figure(2)
        stem(x, y_p, '-.', bottom=0)
        plt.xlabel('K')
        plt.ylabel('Phase')
        plt.grid(True)
        show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()