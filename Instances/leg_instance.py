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

leg = leg.Leg()
leg.length = 3.56e-4
leg.I = 13.
leg.material = 'HMS'
leg.nodes = 10
leg.t_array = np.linspace(0, 1, 20)

leg.T_h_conv = 570.
leg.U_hot = 54e3
leg.T_c_conv = 300.
leg.U_cold = 253e3

leg.set_constants()

leg.solve_leg()

leg.T_h_conv += 100.

leg.solve_leg_transient()

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

plt.figure()

for i in range(leg.t_array.size):
    plt.plot(leg.x * 1e3, leg.T_xt[i, :])

plt.grid()
plt.xlabel('Position (mm)')
plt.ylabel('Temperature (K)')
plt.ylim(leg.T_c_conv, leg.T_h_conv)
plt.subplots_adjust(left=0.15)

plt.show()
    
