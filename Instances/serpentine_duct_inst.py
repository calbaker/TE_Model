# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys

# User Defined Modules
# In this directory
# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx

# parameters for TE legs
area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.te_pair.I = 5.
hx.te_pair.length = length
hx.te_pair.Ntype.material = 'MgSi'
hx.te_pair.Ntype.area = area
hx.te_pair.Ptype.material = 'HMS'
hx.te_pair.Ptype.area = area * 2. 
hx.te_pair.area_void = 150. * area
hx.te_pair.method = 'analytical'
hx.type = 'parallel'
# hx.exh.enhancement = "straight fins"
# hx.exh.fin.thickness = 5.e-3
# hx.exh.fins = 22 # 22 fins seems to be best.  

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.set_mdot_charge()
hx.solve_hx() # solving once to initialize variables that are used
              # later 

ducts = np.array([2.])
hx.Qdot_array = np.zeros(np.size(ducts))
hx.te_pair.power_array = np.zeros(np.size(ducts)) 
hx.power_net_array = np.zeros(np.size(ducts))
hx.Wdot_pumping_array = np.zeros(np.size(ducts)) 

hx.exh.height_array = 3.5e-2 / ducts
hx.cool.height_array = 1.e-2 / ducts
hx.length_array = hx.length * ducts

for i in np.arange(np.size(ducts)):
    hx.exh.height = hx.exh.height_array[i]
    hx.cool.height = hx.cool.height_array[i]
    hx.length = hx.length_array[i]

    hx.solve_hx()
    
    hx.Qdot_array[i] = hx.Qdot_total 
    hx.te_pair.power_array[i] = hx.te_pair.power_total
    hx.power_net_array[i] = hx.power_net 
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping 
    
# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

print "power net:", hx.power_net * 1000., 'W'
print "power raw:", hx.te_pair.power_total * 1000., 'W'
print "pumping power:", hx.Wdot_pumping * 1000., 'W'
hx.exh.volume = hx.exh.height * hx.exh.width * hx.length
print "exhaust volume:", hx.exh.volume * 1000., 'L'
print "exhaust power density:", hx.power_net / hx.exh.volume, 'kW/m^3'


