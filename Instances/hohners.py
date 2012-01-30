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

hohner.length = 0.5

hohner.hx1.length = hohner.length

hohner.hx1.exh.height = 5.e-2
hohner.hx1.width = 5.e-2

hohner.hx2.width = hohner.hx1.length

hohner.hx2.cool.width = hohner.hx1.cool.width
hohner.hx2.cool.length = hohner.hx1.cool.length

hohner.hx2.length = 35.e-2
hohner.hx2.exh.height = 5.e-2

hohner.hx2.exh.enhancement = 'straight fins'
hohner.hx2.exh.fin.thickness = 0.001
hohner.hx2.exh.fins = 200.

indvar = np.arange(150,250,1) 
power_net = np.zeros(indvar.size)

for i in range(indvar.size):
    if i%5 == 0:
        print "iteration", i, "of", indvar.size
    hohner.hx2.exh.fins = indvar[i]
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
plt.plot(indvar, power_net)
plt.xlabel("Interesting Independent Variable")
plt.ylabel("Net power (kW)")
plt.grid()

plt.show()

