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
hx_exp.file = '2012-09-04 gypsum.csv'
hx_exp.import_data()

hx_mod = real_hx.get_hx()
k_gypsum = 0.17e-3
# thermal conductivity (kW / (m * K)) of gypsum board from Incropera
# and DeWitt Intro. to Heat Transfer 5th ed., Table A.3
thickness_gypsum = 0.25 * 2.54e-2
# thickness (m) of gypsum board
hx_mod.R_extra = thickness_gypsum / k_gypsum

hx_mod = real_hx.solve_hx(hx_exp, hx_mod)

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
    np.zeros(hx_exp.exh.Qdot.size), dx, dy, hx_exp.exh.Qdot
    )
ax.bar3d(
    hx_exp.exh.mdot, hx_exp.exh.T_in,
    np.zeros(hx_exp.exh.Qdot.size), -dx, -dy,
    hx_mod.Qdot_arr, color='r'
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')

plt.show()