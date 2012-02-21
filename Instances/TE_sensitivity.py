# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.823
fill_fraction = 2.63e-2
leg_length = 3.55e-4
current = 12.5

hx11 = hx.HX()
hx11.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current]) 

hx11.length = 48.e-2
hx11.width = 73.e-2
hx11.exh.height = 2.8e-2

hx11.te_pair.I = current
hx11.te_pair.length = leg_length

hx11.te_pair.Ntype.material = 'MgSi'
hx11.te_pair.Ptype.material = 'HMS'

hx11.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction) 

hx11.te_pair.method = 'analytical'
hx11.type = 'counter'

hx11.exh.enh = hx11.exh.enh_lib.OffsetStripFin()
hx11.exh.enh.k = 0.02 # approx. thermal conductivity for Ti  
hx11.exh.enh.thickness = 2.e-3
hx11.exh.enh.spacing = 3.19e-3

hx11.plate.k = 0.02 # k for Ti
hx11.plate.thickness = 0.125 * 2.54e-2

hx11.exh.T_inlet = 800.
hx11.cool.T_inlet_set = 300.
hx11.cool.T_outlet = 310.

hx11.set_mdot_charge()
hx11.cool.T_outlet = fsolve(hx11.get_T_inlet_error,
                                  x0=hx11.cool.T_outlet) 

current_array = np.linspace(10, 14, 15)
fill_array = np.linspace(1.5, 3.5, 16) * 1.e-2
leg_height_array = np.linspace(0.1, 1, 20) * 1.e-3

power_net_array = np.zeros([current_array.size, fill_array.size,
                            leg_height_array.size]) 

for i in range(current_array.size):
    hx11.te_pair.I = current_array[i]
    for j in range(fill_array.size):
        fill_fraction = fill_array[j]
        hx11.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)             
        for k in range(leg_height_array.size):
            hx11.te_pair.length = leg_height_array[k]
            hx11.solve_hx()
            
            power_net_array[i,j,k] = hx11.power_net

np.save('../data/TE_sensitivity/power_net_array', power_net_array) 
np.save('../data/TE_sensitivity/current_array', current_array) 
np.save('../data/TE_sensitivity/fill_array', fill_array) 
np.save('../data/TE_sensitivity/leg_height_array', leg_height_array) 

print "\nProgram finished."
print "\nPlotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()

plt.figure()
plt.plot(hx11.x * 100., hx11.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx11.x * 100., hx11.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx11.x * 100., hx11.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx11.x * 100., hx11.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx11.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)

# plt.show()

print "power net:", hx11.power_net * 1000., 'W'
print "power raw:", hx11.te_pair.power_total * 1000., 'W'
print "pumping power:", hx11.Wdot_pumping * 1000., 'W'
hx11.exh.volume = hx11.exh.height * hx11.exh.width * hx11.length
print "exhaust volume:", hx11.exh.volume * 1000., 'L'
print "exhaust power density:", hx11.power_net / hx11.exh.volume, 'kW/m^3'


