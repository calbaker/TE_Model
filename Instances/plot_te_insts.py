# distribution modules
import matplotlib.pyplot as plt
import numpy as np


load_dir = "../data/te_insts/"

U = np.load(load_dir + 'U.npy')
lengths = np.load(load_dir + 'lengths.npy')
fill_fractions = np.load(load_dir + 'fill_fractions.npy')
currents = np.load(load_dir + 'currents.npy')
area_ratios = np.load(load_dir + 'area_ratios.npy')
P = np.load(load_dir + 'P.npy')

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3, 3

plt.close('all')

plt.figure()
x_2d, y_2d = np.meshgrid(U, U)
# TICKS = 
# LEVELS = 
FCS = plt.contourf(x_2d, y_2d, P.T)
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f')
CB.set_label(r'Power')
plt.grid()
plt.xlabel('?Cold? Side U')
plt.ylabel('?Hot? Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/P.pdf')

plt.figure()
x_2d, y_2d = np.meshgrid(U, U)
# TICKS = 
# LEVELS = 
FCS = plt.contourf(x_2d, y_2d, lengths.T)
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f')
CB.set_label(r'Length')
plt.grid()
plt.xlabel('?Cold? Side U')
plt.ylabel('?Hot? Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/length.pdf')

plt.figure()
x_2d, y_2d = np.meshgrid(U, U)
# TICKS = 
# LEVELS = 
FCS = plt.contourf(x_2d, y_2d, fill_fractions.T)
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f')
CB.set_label(r'fill_fraction')
plt.grid()
plt.xlabel('?Cold? Side U')
plt.ylabel('?Hot? Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/fill_fraction.pdf')

plt.figure()
x_2d, y_2d = np.meshgrid(U, U)
# TICKS = 
# LEVELS = 
FCS = plt.contourf(x_2d, y_2d, currents.T)
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f')
CB.set_label(r'Current')
plt.grid()
plt.xlabel('?Cold? Side U')
plt.ylabel('?Hot? Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/current.pdf')

