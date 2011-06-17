import matplotlib.pyplot as mpl
import scipy as sp

# init values
Tc = 400.
Th = 750.
#J = 36e4
n = 100 # number of segments
m = 50 # number of currents
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
    Jp[p] = J
    T = sp.zeros(n)
    q = sp.zeros(n)
    Ti = Tc
    #J = 0 #-1.0e4
    while sp.absolute(Ti - Th) > err:
        T0 = Tc
        q0 = qc
        sum1 = 0
        sum2 = 0
    
        for i in range(n):
            Ap0 = (0.15*T0 + 211.)*10**(-6)
            Pp0 = 0.01*1/25 
            Kp0 = 100*3.194/T0         
            Ti = T0 + (dx/Kp0)*(J*T0*Ap0 - q0)
            dq = (Pp0*J*J*(1 + Ap0*Ap0*T0/(Pp0*Kp0)) - J*Ap0*q0/Kp0) 
            qi = q0 + dq * dx
            q[i] = qi
            T[i] = Ti
            dT = Ti - T0
            sum1 = sum1 + Ap0*dT
            sum2 = Pp0*dx + sum2
            if p == 10: 
                print "\nPrem"
                print "J =", J
                print "T0 =", T0
                print "Ap0 =", Ap0
                print "Pp0 =", Pp0
                print "Kp0 =", Kp0
                print "V_segment =", Ap0 * dT
                print "sum1 =", sum1
                print "sum2 =", sum2
                print "qi =", qi
                print "qc =", qc
                         
            T0 = Ti
            q0 = qi
    
        eta = J*(sum1 + J*sum2)*100./qi
        eta_heat = (qi - qc) / qc * 100.
        if p == 10:
            print "eta =", eta
            print "eta_heat = ", eta_heat
        qc = qc*(1 + (Th-Ti)/Th)
    if p == 10:
        fig1 = mpl.figure()
        mpl.plot(T, q)
        mpl.title("q v T")
        mpl.xlabel('T (K)')
        mpl.ylabel(r'q ($\frac{W}{m^2 K}$)')
        mpl.grid()
        
    eff[p] = eta

fig2 = mpl.figure()
mpl.plot(Jp / 100.**2,eff)
mpl.xlabel(r'Current Density (A/$cm^2$)')
mpl.ylabel('Efficiency (#)')
mpl.title('p-type leg')
mpl.grid()

#disp(['efficiency = ', num2str(eta)])
