import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

T_h = 500.
T_c = 300.
delta_T = T_h - T_c

alpha_p = 150.e-6
alpha_n = -125.e-6
alpha_pn = alpha_p - alpha_n
k_p = 3.
k_n = 3. 
sigma_p = 5.e4
sigma_n = 15.e4
rho_p = 1. / sigma_p
rho_n = 1. / sigma_n

def get_eta(x):
    """Return thermoelectric device efficiency assuming average
    material properties."""
    A = x[0]
    I = x[1]
    L = x[2]

    R = ( alpha_pn * delta_T / I - (rho_p + rho_n / A) * L ) 
    
    eta = ( I**2 * R / (alpha_pn * T_h * I + delta_T / L * (k_p + A
    * k_n) - I**2 * L * 0.5 * (rho_p + rho_n / A)) )  

    return eta

A = np.linspace(0.1,1.5,50)
I = np.linspace(60,110,51) * 1000.
L = np.linspace(5,25,52) * 0.001

A0 = 0.577
I0 = 83.e3
L0 = 1. * 0.01

A2d_I, I2d_A = np.meshgrid(A,I / 1000.)
A2d_L, L2d_A = np.meshgrid(A,L * 1000.)
I2d_L, L2d_I = np.meshgrid(I / 1000.,L * 1000.)

eta_ij = np.empty([np.size(A), np.size(I)])
eta_jk = np.empty([np.size(I), np.size(L)])
eta_ik = np.empty([np.size(A), np.size(L)])

for i in range(np.size(A)):
    for j in range(np.size(I)):
        x = np.array([A[i], I[j], L0])
        eta_ij[i,j] = get_eta(x)

for j in range(np.size(I)):
    for k in range(np.size(L)):
        x = np.array([A0, I[j], L[k]])
        eta_jk[j,k] = get_eta(x)

for i in range(np.size(A)):
    for k in range(np.size(L)):
        x = np.array([A[i], I0, L[k]])
        eta_ik[i,k] = get_eta(x)

Z = ( (alpha_pn / ((rho_p * k_p)**0.5 + (rho_n * k_n)**0.5))**2. ) 
T_bar = 0.5 * (T_h + T_c)
eta_max = ( delta_T / T_h * ((1. + T_bar * Z)**0.5 - 1.) / ((1. + T_bar * Z)**0.5 + T_c / T_h) )

plt.close('all')

LEVELS = np.linspace(0,eta_max,15)

fig1 = plt.figure()
FCS = plt.contourf(A2d_I, I2d_A, eta_ij.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("N:P Area Ratio")
plt.ylabel(r"Current * 10$^{-3}$ (A)")
fig1.savefig('Plots/Analytical/nparea_current.pdf')
fig1.savefig('Plots/Analytical/nparea_current.png')

fig2 = plt.figure()
FCS = plt.contourf(I2d_L, L2d_I, eta_jk.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel(r"Current * 10$^{-3}$ (A)")
plt.ylabel("Leg Length (mm)")
fig2.savefig('Plots/Analytical/current_length.pdf')
fig2.savefig('Plots/Analytical/current_length.png')

fig3 = plt.figure()
FCS = plt.contourf(A2d_L, L2d_A, eta_ik.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("N:P Area Ratio")
plt.ylabel("Leg Length (mm)")
fig3.savefig('Plots/Analytical/nparea_length.pdf')
fig3.savefig('Plots/Analytical/nparea_length.png')

plt.show()
