import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

alpha_p = 150.e-6
alpha_n = -125.e-6
T_h = 500.
T_c = 300.
A_p = 1.
A_n = 1.
k_p = 3.
k_n = 3. 
sigma_p = 5.e4
sigma_n = 15.e4
rho_p = 1. / sigma_p
rho_n = 1. / sigma_n
R = 1.

# Need to vary R and solve for I. 

def get_eta(x):
    """Return thermoelectric device efficiency assuming average
    material properties.

    Parameters
    ----------
    x = (R_a,I,L)
    R_a: area ratio of p-type to n-type leg
    I: current (A)
    L: TE leg length (m)

    Returns
    _________
    eta_t: negative efficiency of TE"""

    R_a = x[0]
    I = x[1]
    L = x[2]

    A_p = A_n * R_a
    eta_t = ( I**2 * R / ((alpha_p - alpha_n) * T_h * I + (T_h - T_c) /
    L * (A_p * k_p + A_n * k_n) - I**2 * L * 0.5 * (rho_p / A_p +
    rho_n / A_n)) ) 

    return -eta_t

R_a = np.linspace(0.2,2,50)
I = np.linspace(0.1,5,50)
L = np.linspace(0.1,4,50) * 0.001

R_a2d_I, I2d_R_a = np.meshgrid(R_a,I)
R_a2d_L, L2d_R_a = np.meshgrid(R_a,L)
I2d_L, L2d_I = np.meshgrid(I,L)

eta_t = np.empty([np.size(R_a), np.size(I), np.size(L)]) 

for i in range(np.size(R_a)):
    for j in range(np.size(I)):
        for k in range(np.size(L)):
            x = np.array([R_a[i], I[j], L[k]])
            eta_t[i,j,k] = -get_eta(x)

fig1 = plt.figure()
FCS = plt.contourf(L2d_I * 1000., I2d_L, eta_t[25,:,:].T) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Current (A)")
fig1.savefig('Plots/HX Optimization/length_current anal.pdf')
fig1.savefig('Plots/HX Optimization/length_current anal.png')

fig2 = plt.figure()
FCS = plt.contourf(L2d_R_a * 1000., R_a2d_L, eta_t[:,25,:].T) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Area Ratio")
fig2.savefig('Plots/HX Optimization/length_fill anal.pdf')
fig2.savefig('Plots/HX Optimization/length_fill anal.png')

fig3 = plt.figure()
FCS = plt.contourf(I2d_R_a, R_a2d_I, eta_t[:,:,25].T) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("Current (A)")
plt.ylabel("Area Ratio")
fig3.savefig('Plots/HX Optimization/current_fill anal.pdf')
fig3.savefig('Plots/HX Optimization/current_fill anal.png')

