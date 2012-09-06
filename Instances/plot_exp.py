"""Plots results from heat exchanger experiments."""

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

mod_data.Qdot_arr = np.zeros(exp_data.exh.T_in.size)

for i in range(exp_data.exh.T_in.size):
    mod_data.exh.T_inlet = exp_data.exh.T_in[i]
    mod_data.exh.mdot = exp_data.exh.mdot[i]
    mod_data.cool.mdot = exp_data.cool.Vdot[i] * mod_data.cool.rho
    mod_data.cool.T_outlet = exp_data.cool.T_out[i]

    mod_data.solve_hx()

    mod_data.Qdot_arr[i] = mod_data.Qdot_total

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

TICKS = exp_data.exh.Qdot.copy()
TICKS.sort()
LEVELS = TICKS

plt.close()

# fig1 = plt.figure()
# FCS = plt.contourf(
#     exp_data.exh.T_in.reshape(2, 2), exp_data.exh.mdot.reshape(2, 2),
#     exp_data.exh.Qdot.reshape(2, 2), levels=LEVELS
#     )
# CB = plt.colorbar(
#     FCS, orientation='vertical', format='%.2f', ticks=TICKS
#     )
# CB.set_label(r'$\dot{Q}$ (kW)')
# plt.grid()
# plt.xlabel('Charge Flow (kg/s)')
# plt.ylabel('Exh Inlet Temp (K)')

# plt.savefig('Plots/plot_exp/Qdot.pdf')

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
    np.zeros(exp_data.exh.Qdot.size), dx * 0.5, dy * 0.5,
    mod_data.Qdot_arr, color='r'
    )

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')

plt.show()
