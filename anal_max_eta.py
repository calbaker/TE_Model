import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

alpha_p = 150.e-6
alpha_n = -125.e-6
T_h = 500.
T_c = 300.
A_n = 1.
k_p = 3.
k_n = 3. 
sigma_p = 5.e4
sigma_n = 15.e4
rho_p = 1. / sigma_p
rho_n = 1. / sigma_n

def get_eta(x):
    """Return thermoelectric device efficiency assuming average
    material properties."""
    pn_area_ratio = x[0]
    I = x[1]
    L = x[2]

    A_p = A_n * pn_area_ratio
    R_load = ( (alpha_p - alpha_n) * (T_h - T_c) / I + (rho_p * A_p +
    rho_n * A_n) * L )
    
    eta_t = ( I**2 * R_load / ((alpha_p - alpha_n) * T_h * I + (T_h - T_c) /
    L * (A_p * k_p + A_n * k_n) - I**2 * L * 0.5 * (rho_p / A_p +
    rho_n / A_n)) ) 

    return eta_t

pn_area_ratio = np.linspace(0.2,20,50)
I = np.linspace(0.1,25,51)
L = np.linspace(0.1,10,52) * 0.001

pn_area_ratio0 = 5.
I0 = 10.
L0 = 5. * 0.001

pn_area_ratio2d_I, I2d_pn_area_ratio = np.meshgrid(pn_area_ratio,I)
pn_area_ratio2d_L, L2d_pn_area_ratio = np.meshgrid(pn_area_ratio,L)
I2d_L, L2d_I = np.meshgrid(I,L)

eta_t_ij = np.empty([np.size(pn_area_ratio), np.size(I)])
eta_t_jk = np.empty([np.size(I), np.size(L)])
eta_t_ik = np.empty([np.size(pn_area_ratio), np.size(L)])

for i in range(np.size(pn_area_ratio)):
    for j in range(np.size(I)):
        x = np.array([pn_area_ratio[i], I[j], L0])
        eta_t_ij[i,j] = get_eta(x)

for j in range(np.size(I)):
    for k in range(np.size(L)):
        x = np.array([pn_area_ratio0, I[j], L[k]])
        eta_t_jk[j,k] = get_eta(x)

for i in range(np.size(pn_area_ratio)):
    for k in range(np.size(L)):
        x = np.array([pn_area_ratio[i], I0, L[k]])
        eta_t_ik[i,j] = get_eta(x)

Z = ( ((alpha_p - alpha_n) / ((rho_p * k_p)**0.5 + (rho_n *
                                                    k_n)**0.5))**2. ) 
T_bar = 0.5 * (T_h + T_c)
eta_max = ( (T_h - T_c) / T_h * ((1. + T_bar * Z) - 1.) / ((1. + T_bar
    * Z)**0.5 + T_c / T_h) )

fig3 = plt.figure()
FCS = plt.contourf(pn_area_ratio2d_I, I2d_pn_area_ratio, eta_t_ij.T) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("Current (A)")
plt.ylabel("Area Ratio")
fig3.savefig('Plots/HX Optimization/current_fill anal.pdf')
fig3.savefig('Plots/HX Optimization/current_fill anal.png')

fig1 = plt.figure()
FCS = plt.contourf(I2d_L, L2d_I * 1000., eta_t_jk.T) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Thermal Efficiency')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Current (A)")
fig1.savefig('Plots/HX Optimization/.pdf')
fig1.savefig('Plots/HX Optimization/.png')

# fig2 = plt.figure()
# FCS = plt.contourf(pn_area_ratio2d_L, L2d_pn_area_ratio * 1000., eta_t_ik.T) 
# CB = plt.colorbar(FCS, orientation='vertical')
# CB.set_label('TE Thermal Efficiency')
# plt.grid()
# plt.xlabel("Leg Height (mm)")
# plt.ylabel("Area Ratio")
# fig2.savefig('Plots/HX Optimization/length_fill anal.pdf')
# fig2.savefig('Plots/HX Optimization/length_fill anal.png')

plt.show()
