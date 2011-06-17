import matplotlib.pyplot as mpl
import scipy as sp

# init values
Tc = 400
Th = 750
#J = 36e4
n = 2000
m = 50
L = .010
i = 0
err = .1
# guess qc
# qc = -361500
#qx = input('Enter guess for qcx10e-5 (in W/m2):\n')
#qc = qx*10**5
qc = -100*3.194*2/(Th+Tc)*(Th-Tc)/(L)
q0 = qc

# init values for loop
dx = L/n

# create arrays for graphing
Jp = sp.zeros(m)
eff = sp.zeros(m)

for p in range(m):
    
    J = (-2.5 + p/20.)*1e4
    print J
    Jp[p] = J
    Ti = Tc
    #J = 0 #-1.0e4
    while sp.absolute(Ti - Th) > err:
        T0 = Tc
        q0 = qc
        sum1 = 0
        sum2 = 0
    
        for i in range(n):
            Ap0 = (0.15*T0 + 211)*10**(-6) 
            Pp0 = 0.01*1/25 
            Kp0 = 100*3.194/T0         
            Ti = T0 + (dx/Kp0)*(J*T0*Ap0 - q0)
            qi = q0 + (Pp0*J*J*(1 + Ap0*Ap0*T0/(Pp0*Kp0)) - J*Ap0*q0/Kp0)*dx
            dT = Ti - T0
            sum1 = sum1 + Ap0*dT
            sum2 = Pp0*dx + sum2
            T0 = Ti
            q0 = qi
    
        eta = J*(sum1 + J*sum2)*100/qi
        qc = qc*(1 + (Th-Ti)/Th)
#        disp(['Ti = ', num2str(Ti)])
 #       disp(['eta = ', num2str(eta)])
        
    eff[p] = eta

mpl.plot(Jp / 100.**2,eff)
mpl.xlabel(r'Current Density (A/$cm^2$)')
mpl.ylabel('Efficiency (#)')
mpl.title('p-type leg')
mpl.grid()

#disp(['efficiency = ', num2str(eta)])
