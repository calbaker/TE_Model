# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
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
area_ratio = 0.719
fill_fraction = 2.84e-2
leg_length = 3.5e-4
current = 13.3

hx_osf = hx.HX()
hx_osf.width = 0.3
hx_osf.exh.height = 3.5e-2
hx_osf.length = 1.
hx_osf.te_pair.I = current
hx_osf.te_pair.length = leg_length

hx_osf.te_pair.Ntype.material = 'MgSi'
hx_osf.te_pair.Ptype.material = 'HMS'

hx_osf.te_pair.Ptype.area = leg_area
hx_osf.te_pair.Ntype.area = hx_osf.te_pair.Ptype.area * area_ratio
hx_osf.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_osf.te_pair.Ptype.area +
                            hx_osf.te_pair.Ntype.area) )  

hx_osf.te_pair.method = 'analytical'
hx_osf.type = 'counter'
hx_osf.exh.enh = enh_lib.OffsetStripFin()
hx_osf.exh.enh.t = 0.5e-3
hx_osf.exh.enh.s = 0.001

hx_osf.exh.T_inlet = 800.
hx_osf.cool.T_inlet_set = 300.
hx_osf.cool.T_outlet = 310.

hx_osf.set_mdot_charge()
hx_osf.cool.T_outlet = fsolve(hx_osf.get_T_inlet_error, x0=hx_osf.cool.T_outlet)

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
plt.plot(hx_osf.x * 100., hx_osf.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_osf.x * 100., hx_osf.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx_osf.x * 100., hx_osf.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx_osf.x * 100., hx_osf.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_osf.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)

# plt.show()

print "power net:", hx_osf.power_net * 1000., 'W'
print "power raw:", hx_osf.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_osf.Wdot_pumping * 1000., 'W'
hx_osf.exh.volume = hx_osf.exh.height * hx_osf.exh.width * hx_osf.length
print "exhaust volume:", hx_osf.exh.volume * 1000., 'L'
print "exhaust power density:", hx_osf.power_net / hx_osf.exh.volume, 'kW/m^3'


