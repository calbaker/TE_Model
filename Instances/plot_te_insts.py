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
TICKS = np.linspace(0., P.max() * 0.5, 12)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, P.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label('Power')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.title('Power')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/P.pdf')

plt.figure()
TICKS = np.linspace(0., 2., 12)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, lengths.T * 1000., levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label('Length (mm)')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.title('Length')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/length.pdf')

plt.figure()
TICKS = np.linspace(fill_fractions.min(), 0.1, 12)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, fill_fractions.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label('fill fraction')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.title('Fill Fraction')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/fill_fraction.pdf')

plt.figure()
TICKS = np.linspace(0., 30, 12)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, currents.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label('Current')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.title('Current')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/current.pdf')

plt.figure()
TICKS = np.linspace(area_ratios.min(), area_ratios.max(), 12)
LEVELS = TICKS
FCS = plt.contourf(x_2d, y_2d, area_ratios.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS) 
CB.set_label('Area Ratio')
plt.grid()
plt.xlabel('Hot Side U')
plt.ylabel('Cold Side U')
plt.title('Area Ratio')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/te_insts/fill_fraction.pdf')
