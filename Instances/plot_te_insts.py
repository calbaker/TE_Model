# distribution modules
import matplotlib.pyplot as plt
import numpy as np


load_dir = "../data/te_insts/"

U_hot = np.load(load_dir + 'U_hot.npy')
U_cold = np.load(load_dir + 'U_cold.npy')
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

x_2d, y_2d = np.meshgrid(U_hot, U_cold)

plt.figure()
TICKS = np.linspace(0., P.max(), 8)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, P.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(r'Power')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/P.pdf')

plt.figure()
TICKS = np.linspace(0., lengths.max() * 1000., 8)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, lengths.T * 1000., levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label('Length (mm)')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/length.pdf')

plt.figure()
TICKS = np.linspace(0, fill_fractions.max(), 8)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, fill_fractions.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label(r'fill_fraction')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/fill_fraction.pdf')

plt.figure()
TICKS = np.linspace(0., currents.max(), 8)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, currents.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label('Current')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/current.pdf')

plt.figure()
TICKS = np.linspace(0, area_ratios.max(), 8)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, area_ratios.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label(r'fill_fraction')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/fill_fraction.pdf')
