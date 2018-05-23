import math

class Complex:
    def __init__(self , R , I):
        self.real = R
        self.img = I
    def _add_(self,z1):
        self.real += z1.real
        self.img += z1.img
    def _sub_(self,z1):
        self.real -= z1.real
        self.img -= z1.img
    def _mul_(self,z1):
        self.real = self.real * z1.real - self.img * z1.img
        self.img = self.real * z1.img + self.img * z1.real 
    def get_mag(self,z):
        mag = math.sqrt( ( (z.real)**2 ) + ( (z.img)**2 ))
        return mag
    def get_phase(self,z):
        phase = math.atan2(z.img,z.real) # check for tan-1
        return phase
    def polar(self,z):
        return self.get_mag(z),self.get_phase(z)

def main():
    try:
        N = int(input("Enter N Samples: "))
    except Exception:
        print("ERROR >> Either,You didn't Enter N Samples Or Invalid Entry")       
        return
    #try:
    n = int(input("Enter number of samples of x(n):"))
    x = [float(input()) for i in range(n)]
    x_n = [Complex(float(x[i]),0) for i in range(n)]
    if n <= N:
        for i in range(N-n):
            x_n.append(Complex(float(0),float(0)))
    else :
        print("ERROR >> Number of samples in x(n) Must be less than or equal N Samples")       
        return
    Wn_factor = 2*math.pi/N
    Wn = [[Complex(0,0) for i in range(N)] for i in range(N)]
    Sum = Complex(0,0) 
    X_K = [Complex(0,0) for i in range(N)]
    
    print("Enter multy")
    for i in range(N):
        for j in range(N):
            Wn[i][j].real = math.cos(round((Wn_factor*i*j),2))
            Wn[i][j].img = -1*math.sin(round((Wn_factor*i*j),2))
            #Wn[i][j] = cmath.e ** complex(0.0,-1*Wn_factor*i*j)  #another formula
            mul = Wn[i][j]._mul_(x_n[j])
            Sum._add_(mul)
            #Sum = Complex.add_complex(Sum,Complex(x_n[j] * Wn[i][j].real ,x_n[j] * Wn[i][j].img))
        X_K[i].real = Sum.real
        X_K[i].img = Sum.img
        Sum = Complex(0,0)
    
    print("Exit multy")
    
    X_K_mag = [Complex.get_mag(X_K[i]) for i in range(N)]
    X_K_phase = [Complex.get_phase(X_K[i]) for i in range(N)]
    
    print("Enter str")

    X_K_magnitude = ""
    X_K_phase = ""
    
    for i in range(N):
        X_K_magnitude += str(round((X_K_mag[i]),2)) + "||"
        X_K_phase += str(round((X_K_phase[i])*(180/math.pi),2)) + "||"
 

    print("Magniude : ",X_K_magnitude," Phase : ",X_K_phase)
 
if __name__ == '__main__':
    main()