"""Plots results from heat exchanger experiments."""

import numpy as np
import matplotlib.pyplot as plt


# from ~/Documents/Python
import properties as prop

DIR = '../Heat Exchanger Experiments/gen2/'
FILE = '2012-09-04.csv'

data = np.recfromcsv(DIR + FILE)

class DataPoint(object):
    pass

exh = prop.ideal_gas()
exh.P = 101.325
cool = DataPoint()

exh.T_in = data['hx_exh_in_t'] + 273.15  # K
exh.T_out = data['hx_exh_out_t'] + 273.15  # K
exh.mdot = data['exh_mdot_kgmin'] / 60.  # kg/s

cool.T_in = 0.5 * (data['hx_cool_1_in_t'] + data['hx_cool_2_in_t'])

exh.T_mean = 0.5 * (exh.T_in + exh.T_out)
exh.delta_T = exh.T_in - exh.T_out
exh.eta = exh.delta_T / (exh.T_in - cool.T_in) 

exh.c_p = np.zeros(exh.T_in.size)

for i in range(exh.T_in.size):
    exh.T = exh.T_mean[i]
    exh.set_TempPres_dependents()
    exh.c_p[i] = exh.c_p_air

exh.Qdot = exh.mdot * exh.c_p * exh.delta_T

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

TICKS = exh.Qdot.copy()
TICKS.sort()
LEVELS = TICKS

plt.close()

# fig1 = plt.figure()
# FCS = plt.contourf(
#     exh.T_in.reshape(2, 2), exh.mdot.reshape(2, 2),
#     exh.Qdot.reshape(2, 2), levels=LEVELS
#     )
# CB = plt.colorbar(
#     FCS, orientation='vertical', format='%.2f', ticks=TICKS
#     )
# CB.set_label(r'$\dot{Q}$ (kW)')
# plt.grid()
# plt.xlabel('Charge Flow (kg/s)')
# plt.ylabel('Exh Inlet Temp (K)')

# plt.savefig('Plots/plot_exp/Qdot.pdf')

dx = (exh.mdot.max() - exh.mdot.min()) / 10.
dy = (exh.T_in.max() - exh.T_in.min()) / 10.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(exh.mdot, exh.T_in, np.zeros(exh.Qdot.size), dx, dy, exh.Qdot)

ax.set_xlabel(r'$\dot{m}$ (kg/s)')
ax.set_ylabel(r'$T_{exh,in}$ (K)')
ax.set_zlabel(r'$\dot{Q}$')

plt.show()
