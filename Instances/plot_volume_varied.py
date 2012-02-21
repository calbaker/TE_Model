# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt

dirpath = '../data/volume_varied/'

length_array = np.load(dirpath + 'length_array')
width_array = np.load(dirpath + 'width_array')
spacing_array = np.load(dirpath + 'spacing_array')
power_net_array = np.load(dirpath + 'power_net_array')

print "\nPlotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

plt.figure()
x_2d, y_2d = np.meshgrid(length_array * 100., width_array * 100.)
TICKS = np.linspace(800, power_net_array.max() * 1.e3, 12)
LEVELS = np.linspace(800, power_net_array.max() * 1.e3, 12)
FCS = plt.contourf(x_2d, y_2d, power_net_array.T * 1.e3, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.0f', ticks=TICKS)
CB.set_label(r'Power')
plt.grid()
plt.xlabel('Length (cm)')
plt.ylabel('Width (cm)')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/volume_varied/power_net.pdf')

plt.figure()
# TICKS = np.linspace(800, power_net_array.max() * 1.e3, 12)
# LEVELS = np.linspace(800, power_net_array.max() * 1.e3, 12)
FCS = plt.contourf(x_2d, y_2d, spacing_array.T * 1.e3)#, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f', ticks=TICKS)
CB.set_label(r'Fin Spacing (mm)')
plt.grid()
plt.xlabel('Length (cm)')
plt.ylabel('Width (cm)')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/volume_varied/fin spacing.pdf')

# plt.show()
