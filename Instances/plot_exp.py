"""Plots results from heat exchanger experiments."""

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
# pychecker will flag this statement, but it is necessary
import numpy as np
import matplotlib.pyplot as plt

FILE = '2012-09-18 copper'

npzfile = np.load('../output/model_validation/' + FILE + '.npz') 
deltaP = npzfile['deltaP']
mdot = npzfile['mdot']
Qdot_arr = npzfile['Qdot_arr']
T_in = npzfile['T_in']
Qdot = npzfile['Qdot']
Qdot_surf = npzfile['Qdot_surf']
deltaP_arr = npzfile['deltaP_arr']
mdot2d = npzfile['mdot2d']
T_in2d = npzfile['T_in2d']
velocity = npzfile['velocity']
rho = npzfile['rho']
Re_D = npzfile['Re_D']

# Plot configuration
FONTSIZE = 12
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.close()
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    mdot, T_in, Qdot
    )
ax.scatter(
    mdot, T_in, Qdot_arr, color='r',
    )
ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')
plt.savefig('../Plots/plot_exp/' + FILE + '/Qdot.pdf')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    mdot, T_in, deltaP
    )
ax.scatter(
    mdot, T_in, deltaP_arr,
    color='r'
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\Delta P$')
plt.savefig('../Plots/plot_exp/' + FILE + '/deltaP.pdf')

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(
    mdot, T_in, Qdot
    )
surf = ax.plot_surface(
    mdot2d, T_in2d, Qdot_surf, alpha=0.4, rstride=1,
    cstride=1, cmap=cm.jet, linewidth=0, antialiased=False
    )
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')
plt.savefig('../Plots/plot_exp/' + FILE + '/Qdot_fit.pdf')

fig = plt.figure()
dimless_P_mod = deltaP_arr / (0.5 * rho * velocity ** 2.)
dimless_P_exp = deltaP / (0.5 * rho * velocity ** 2.)
plt.plot(
    Re_D, dimless_P_mod * 1e3, linestyle='', marker='s', color='b',
    label='model'
    )
plt.plot(
    Re_D, dimless_P_exp * 1e3, linestyle='', marker='s', color='r',
    label='experiment'
    )
plt.xlabel(r'Re$_D$')
plt.ylabel(r'$\frac{\Delta P}{1/2 \rho U^2}$ x 1x10$^3$')
plt.grid()
plt.legend()
plt.savefig('../Plots/plot_exp/' + FILE + '/dimless_P.pdf')

plt.show()
