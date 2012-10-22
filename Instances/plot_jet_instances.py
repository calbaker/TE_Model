# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import numpy as np


power_net_H = np.load("../output/jet_instances/power_net_H.npy")
power_net_D = np.load("../output/jet_instances/power_net_D.npy")
power_net_X = np.load("../output/jet_instances/power_net_X.npy")

H_array = np.load("../output/jet_instances/H_array.npy")
D_array = np.load("../output/jet_instances/D_array.npy")
X_array = np.load("../output/jet_instances/X_array.npy")


# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['figure.subplot.left'] = 0.15
plt.rcParams['figure.subplot.right'] = 0.85
plt.rcParams['figure.subplot.bottom'] = 0.15
plt.rcParams['figure.subplot.top'] = 0.9

plt.close('all')

plt.figure()
plt.plot(H_array * 100., power_net_H)
plt.xlabel('Annular Duct Height (cm)')
plt.ylabel('Net Power')
plt.grid()
plt.savefig("../Plots/jet_instances/power_net_H.pdf")

plt.figure()
plt.plot(D_array * 1000., power_net_D)
plt.xlabel('Jet Orifice Diameter (mm)')
plt.ylabel('Net Power')
plt.grid()
plt.savefig("../Plots/jet_instances/power_net_D.pdf")

plt.figure()
plt.plot(X_array * 100., power_net_X)
plt.xlabel('Jet Spacing (cm)')
plt.ylabel('Net Power')
plt.grid()
plt.savefig("../Plots/jet_instances/power_net_X.pdf")

# plt.show()

