# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve, fmin

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.740
fill_fraction = 3.01e-2
leg_length = 3.18e-4
current = 14.1

hx_osf_opt = hx.HX()
hx_osf_opt.width = 0.55
hx_osf_opt.exh.height = 3.5e-2
hx_osf_opt.length = 0.55
hx_osf_opt.te_pair.I = current
hx_osf_opt.te_pair.length = leg_length

hx_osf_opt.te_pair.Ntype.material = 'MgSi'
hx_osf_opt.te_pair.Ptype.material = 'HMS'

hx_osf_opt.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction) 

hx_osf_opt.te_pair.method = 'analytical'
hx_osf_opt.type = 'counter'
hx_osf_opt.exh.enh = hx_osf_opt.exh.enh_lib.OffsetStripFin()
hx_osf_opt.exh.enh.thickness = 0.5e-3
hx_osf_opt.exh.enh.spacing = 0.001

hx_osf_opt.exh.T_inlet = 800.
hx_osf_opt.cool.T_inlet_set = 300.
hx_osf_opt.cool.T_outlet = 310.

hx_osf_opt.set_mdot_charge()
hx_osf_opt.cool.T_outlet = fsolve(hx_osf_opt.get_T_inlet_error, x0=hx_osf_opt.cool.T_outlet)

def get_minpar(apar):
    """Returns parameter to be minimized as a function of apar.
    apar[0] : number of fins"""
    
    hx_osf_opt.exh.enh.s = apar[0]
    hx_osf_opt.solve_hx()

    if hx_osf_opt.power_net < 0:
        minpar = np.abs(hx_osf_opt.power_net)
    else:
        minpar = 1. / hx_osf_opt.power_net
    
    return minpar

x0 = np.array([0.005])
xmin = fmin(get_minpar, x0)

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
plt.plot(hx_osf_opt.x * 100., hx_osf_opt.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_osf_opt.x * 100., hx_osf_opt.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx_osf_opt.x * 100., hx_osf_opt.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx_osf_opt.x * 100., hx_osf_opt.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_osf_opt.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)

# plt.show()

print "\npower net:", hx_osf_opt.power_net * 1000., 'W'
print "power raw:", hx_osf_opt.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_osf_opt.Wdot_pumping * 1000., 'W'
hx_osf_opt.exh.volume = hx_osf_opt.exh.height * hx_osf_opt.exh.width * hx_osf_opt.length
print "exhaust volume:", hx_osf_opt.exh.volume * 1000., 'L'
print "exhaust power density:", hx_osf_opt.power_net / hx_osf_opt.exh.volume, 'kW/m^3'


