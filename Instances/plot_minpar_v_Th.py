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

T_h_conv = np.load(data_dir + 'T_h_conv.npy') 

current = np.load(data_dir + 'current.npy') 
fill_fraction = np.load(data_dir + 'fill.npy')
length = np.load(data_dir + 'length.npy')
area_ratio = np.load(data_dir + 'area_ratio.npy')
power = np.load(data_dir + 'power.npy')

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()
save_dir = "../Plots/plot_minpar_v_Th/"

plt.figure('current')
plt.plot(T_h_conv, current)
plt.grid()
plt.xlabel(r'T$_{h,conv}$')
plt.ylabel('Current (A)')
plt.savefig(save_dir + 'current.pdf')

plt.figure('fill fraction')
plt.plot(T_h_conv, fill_fraction * 1e2)
plt.grid()
plt.xlabel(r'T$_{h,conv}$')
plt.ylabel('Fill Fraction (%)')
plt.savefig(save_dir + 'fill_fraction.pdf')

plt.figure('length')
plt.plot(T_h_conv, length * 1e3)
plt.grid()
plt.xlabel(r'T$_{h,conv}$')
plt.ylabel('Length (mm)')
plt.savefig(save_dir + 'length.pdf')

plt.figure('area ratio')
plt.plot(T_h_conv, area_ratio)
plt.grid()
plt.xlabel(r'T$_{h,conv}$')
plt.ylabel(r'Area Ratio ($A_n/A_p$)')
plt.savefig(save_dir + 'area_ratio.pdf')


plt.show()


