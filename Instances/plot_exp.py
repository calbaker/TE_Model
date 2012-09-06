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

exp_data = exp_data.ExpData()
exp_data.folder = '../ExpData/'
exp_data.file = '2012-09-04 gypsum.csv'
exp_data.import_data()

mod_data = real_hx.get_hx()
k_gypsum = 0.17e-3
# thermal conductivity (kW / (m * K)) of gypsum board from Incropera
# and DeWitt Intro. to Heat Transfer 5th ed., Table A.3
thickness_gypsum = 0.25 * 2.54e-2
# thickness (m) of gypsum board
mod_data.R_extra = thickness_gypsum / k_gypsum
mod_data.Qdot_arr = np.zeros(exp_data.exh.T_in.size)

for i in range(exp_data.exh.T_in.size):
    mod_data.exh.T_inlet = exp_data.exh.T_in[i]
    mod_data.exh.mdot = exp_data.exh.mdot[i]
    mod_data.cool.mdot = exp_data.cool.Vdot[i] * mod_data.cool.rho
    mod_data.cool.T_outlet = exp_data.cool.T_out[i]

    mod_data.solve_hx()

    mod_data.Qdot_arr[i] = mod_data.Qdot_total

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

dx = (exp_data.exh.mdot.max() - exp_data.exh.mdot.min()) / 10.
dy = (exp_data.exh.T_in.max() - exp_data.exh.T_in.min()) / 10.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(
    exp_data.exh.mdot, exp_data.exh.T_in,
    np.zeros(exp_data.exh.Qdot.size), dx, dy, exp_data.exh.Qdot
    )
ax.bar3d(
    exp_data.exh.mdot, exp_data.exh.T_in,
    np.zeros(exp_data.exh.Qdot.size), -dx, -dy,
    mod_data.Qdot_arr, color='r'
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')

plt.show()
