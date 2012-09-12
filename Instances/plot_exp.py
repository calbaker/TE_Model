"""Plots results from heat exchanger experiments."""

from mpl_toolkits.mplot3d import Axes3D
# pychecker will flag this statement, but it is necessary
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import exp_data
reload(exp_data)
import real_hx
reload(real_hx)

hx_exp = exp_data.ExpData()
hx_exp.folder = '../ExpData/'
hx_exp.file = 'combined gypsum'
hx_exp.import_data()

hx_mod = real_hx.get_hx()
k_gypsum = 0.17e-3
# thermal conductivity (kW / (m * K)) of gypsum board from Incropera
# and DeWitt Intro. to Heat Transfer 5th ed., Table A.3
thickness_gypsum = 0.25 * 2.54e-2
# thickness (m) of gypsum board
hx_mod.R_extra = thickness_gypsum / k_gypsum

hx_mod = real_hx.solve_hx(hx_exp, hx_mod)

np.savez(
    '../output/plot_exp/' + hx_exp.file, 
    hx_exp.exh.mdot, hx_exp.exh.T_in, hx_exp.exh.delta_P,
    hx_mod.exh.delta_P_arr, hx_exp.exh.Qdot, hx_mod.Qdot_arr
    )

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

dx = (hx_exp.exh.mdot.max() - hx_exp.exh.mdot.min()) / 10.
dy = (hx_exp.exh.T_in.max() - hx_exp.exh.T_in.min()) / 10.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(
    hx_exp.exh.mdot, hx_exp.exh.T_in,
    np.zeros(hx_exp.exh.Qdot.size), dx, dy, hx_exp.exh.Qdot,
    alpha=0.5
    )
ax.bar3d(
    hx_exp.exh.mdot, hx_exp.exh.T_in,
    np.zeros(hx_exp.exh.Qdot.size), dx, dy,
    hx_mod.Qdot_arr, color='r', alpha=0.5
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')
plt.savefig('../Plots/plot_exp/' + hx_exp.file + '/Qdot.pdf')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(
    hx_exp.exh.mdot, hx_exp.exh.T_in,
    np.zeros(hx_exp.exh.delta_P.size), dx, dy, hx_exp.exh.delta_P,
    alpha=0.5
    )
ax.bar3d(
    hx_exp.exh.mdot, hx_exp.exh.T_in,
    np.zeros(hx_exp.exh.delta_P.size), dx, dy,
    hx_mod.exh.delta_P_arr, color='r', alpha=0.5
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\Delta P$')
plt.savefig('../Plots/plot_exp/' + hx_exp.file + '/deltaP.pdf')

plt.show()
