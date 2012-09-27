# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
data_dir = '../output/te_design_space/'
current_array = np.load(data_dir + 'current_array.npy') 
fill_array = np.load(data_dir + 'fill_array.npy') * 100.
length_array = np.load(data_dir + 'length_array.npy') * 1.e3
power_I_fill = np.load(data_dir + 'power_I_fill.npy')
power_fill_height = np.load(data_dir + 'power_fill_height.npy')
power_height_I = np.load(data_dir + 'power_height_I.npy')

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()
save_dir = "../Plots/plot_TE_sensitivity/"

length_array *= 1e3

# fig = plt.figure()
# ax = fig.gca(projection='3d')

X1, Y1 = np.meshgrid(current_array, fill_array)
Z1 = power_I_fill.T
# cset = ax.contourf(X1, Y1, Z1, zdir='z', offset=length_array[0])

X2, Y2 = np.meshgrid(fill_array, length_array)
Z2 = power_fill_height.T
# cset = ax.contourf(X2, Y2, Z2, zdir='x', offset=current_array[0])

X3, Y3 = np.meshgrid(length_array, current_array)
Z3 = power_height_I.T
# cset = ax.contourf(X3, Y3, Z3, zdir='x', offset=fill_array[-1])

# ax.set_xlabel('Current (A)')
# ax.set_xlim(current_array[0], current_array[-1])
# ax.set_ylabel('Fill Fraction')
# ax.set_ylim(fill_array[0], fill_array[-1])
# ax.set_zlabel('Leg Height (mm)')
# ax.set_zlim(length_array[0], length_array[-1])

RIGHT = 0.75
BOTTOM = 0.17
FRACTION = 0.15
MAX_ARRAY = np.array([Z1.max(), Z2.max(), Z3.max()])
MAX = MAX_ARRAY.max()
LEVELS = (
    (MAX + 0.1 - np.logspace(np.log10(0.1), np.log10(MAX), 12))[::-1]
    )
TICKS = LEVELS
FORMAT = '%0.1f'

fig1 = plt.figure('Z1')
cset1 = plt.contourf(X1, Y1, Z1, levels=LEVELS)
CB1 = plt.colorbar(
    cset1, orientation='vertical', format=FORMAT, fraction=FRACTION,
    ticks=TICKS
    )
CB1.set_label(r'Power Flux (kW/m$^2$)')
plt.xticks(rotation=40)
plt.xlabel('Current (A)')
plt.ylabel('Fill Fraction')
plt.subplots_adjust(bottom=BOTTOM, right=RIGHT)
plt.grid()
fig1.savefig(save_dir + "power_I_fill.pdf")

fig2 = plt.figure('Z2')
cset2 = plt.contourf(X2, Y2, Z2, levels=LEVELS)
CB2 = plt.colorbar(
    cset2, orientation='vertical', format=FORMAT, fraction=FRACTION,
    ticks=TICKS
    )
CB2.set_label(r'Power Flux (kW/m$^2$)')
plt.xticks(rotation=40)
plt.xlabel('Fill Fraction')
plt.ylabel('Length (mm)')
plt.subplots_adjust(bottom=BOTTOM, right=RIGHT)
plt.grid()
fig2.savefig(save_dir + "power_fill_length.pdf")

fig3 = plt.figure('Z3')
cset3 = plt.contourf(X3, Y3, Z3, levels=LEVELS)
CB3 = plt.colorbar(
    cset3, orientation='vertical', format=FORMAT, fraction=FRACTION,
    ticks=TICKS 
    )
CB3.set_label(r'Power Flux (kW/m$^2$)')
plt.xticks(rotation=40)
plt.xlabel('Length (mm)')
plt.ylabel('Current (A)')
plt.subplots_adjust(bottom=BOTTOM, right=RIGHT)
plt.grid()
fig3.savefig(save_dir + "power_length_I.pdf")

plt.show()


