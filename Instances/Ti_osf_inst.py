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

hx_osf_Ti0 = hx.HX()
hx_osf_Ti0.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current]) 

hx_osf_Ti0.length = 48.e-2
hx_osf_Ti0.width = 73.e-2
hx_osf_Ti0.exh.height = 2.8e-2

hx_osf_Ti0.te_pair.I = current
hx_osf_Ti0.te_pair.length = leg_length

hx_osf_Ti0.te_pair.Ntype.material = 'MgSi'
hx_osf_Ti0.te_pair.Ptype.material = 'HMS'

hx_osf_Ti0.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction) 

hx_osf_Ti0.te_pair.method = 'analytical'
hx_osf_Ti0.type = 'counter'

hx_osf_Ti0.exh.enh = hx_osf_Ti0.exh.enh_lib.OffsetStripFin()
hx_osf_Ti0.exh.enh.k = 0.02 # approx. thermal conductivity for Ti  
hx_osf_Ti0.exh.enh.thickness = 2.e-3
hx_osf_Ti0.exh.enh.spacing = 3.19e-3

hx_osf_Ti0.plate.k = 0.02 # k for Ti
hx_osf_Ti0.plate.thickness = 0.125 * 2.54e-2

hx_osf_Ti0.exh.T_inlet = 800.
hx_osf_Ti0.cool.T_inlet_set = 300.
hx_osf_Ti0.cool.T_outlet = 310.

hx_osf_Ti0.set_mdot_charge()
hx_osf_Ti0.cool.T_outlet = fsolve(hx_osf_Ti0.get_T_inlet_error,
                                  x0=hx_osf_Ti0.cool.T_outlet) 

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
plt.plot(hx_osf_Ti0.x * 100., hx_osf_Ti0.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_osf_Ti0.x * 100., hx_osf_Ti0.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx_osf_Ti0.x * 100., hx_osf_Ti0.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx_osf_Ti0.x * 100., hx_osf_Ti0.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_osf_Ti0.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)

# plt.show()

print "power net:", hx_osf_Ti0.power_net * 1000., 'W'
print "power raw:", hx_osf_Ti0.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_osf_Ti0.Wdot_pumping * 1000., 'W'
hx_osf_Ti0.exh.volume = hx_osf_Ti0.exh.height * hx_osf_Ti0.exh.width * hx_osf_Ti0.length
print "exhaust volume:", hx_osf_Ti0.exh.volume * 1000., 'L'
print "exhaust power density:", hx_osf_Ti0.power_net / hx_osf_Ti0.exh.volume, 'kW/m^3'


