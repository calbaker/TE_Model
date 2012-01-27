# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import harmonica
reload(harmonica)

hohner = harmonica.Harmonica()
hohner.hx1.te_pair.method = 'analytical'
hohner.hx2.te_pair.method = 'analytical'

hohner.height = 2.e-2
hohner.hx2.length = 0.1
hohner.hx2.exh.fins = 1000.
hohner.hx2.exh.enhancement = 'none'

height = np.linspace(1,5,10) * 1e-2
power_net = np.zeros(height.size)

for i in range(height.size):
    if i%5 == 0:
        print "Solving node", i, "of", height.size
    hohner.height = height[i]
    hohner.solve_harmonica()
    power_net[i] = hohner.power_net

print power_net.max()
    
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
plt.plot(height * 100., power_net)
plt.xlabel("Exhaust duct height (cm)")
plt.ylabel("Net power (kW)")
plt.grid()

plt.show()

