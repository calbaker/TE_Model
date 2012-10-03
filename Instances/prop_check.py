"""Script that checks material property curve fitting by plotting
curves and raw data."""

# distribution modules
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import leg
reload(leg)

prop_check = leg.Leg()

prop_check.material = 'HMS'

prop_check.T_array = np.linspace(300, 900, 100.)
prop_check.alpha_T = np.zeros(prop_check.T_array.size)
prop_check.k_T = np.zeros(prop_check.T_array.size)
prop_check.sigma_T = np.zeros(prop_check.T_array.size)

for i in range(prop_check.T_array.size):

    prop_check.set_TEproperties(prop_check.T_array[i])

    prop_check.alpha_T[i] = prop_check.alpha
    prop_check.k_T[i]     = prop_check.k
    prop_check.sigma_T[i] = prop_check.sigma

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.close()

plt.figure('Seebeck')

plt.plot(prop_check.T_array, prop_check.alpha_T * 1.e6)
plt.plot(prop_check.alpha_raw[:, 0], prop_check.alpha_raw[:, 1],
         marker='x')
plt.xlabel('Temperature (K)')
plt.ylabel('Seebeck Coeff (V/K)')
plt.grid()

plt.figure('k')

plt.plot(prop_check.T_array, prop_check.k_T)
plt.plot(prop_check.k_raw[:, 0], prop_check.k_raw[:, 1], marker='x')
plt.xlabel('Temperature (K)')
plt.ylabel(r'Thermal Conductivity ($\frac{W}{mK})')
plt.grid()

plt.figure('Sigma')

plt.plot(prop_check.T_array, prop_check.sigma_T * 1.e-4)
plt.plot(prop_check.sigma_raw[:, 0], prop_check.sigma_raw[:, 1],
         marker='x')
plt.xlabel('Temperature (K)')
plt.ylabel(r'$\sigma$')
plt.grid()

# plt.plot(prop_check.T_array, prop_check.sigma_T * 1.e-4)
# plt.plot(1/prop_check.sigma_raw[:, 0], 1/prop_check.sigma_raw[:, 1],
#          marker='x')
# plt.xlabel('Temperature (K)')
# plt.ylabel(r'$\sigma$')
# plt.grid()

plt.show()
