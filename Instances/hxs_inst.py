# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fsolve

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx_series 
reload(hx_series)
import enhancement 
reload(enhancement)
    
leg_area = (0.002)**2

area_ratio = 0.659
fill_fraction = 2.13e-2
leg_length = 1.10e-3
current = 4.10

hxs = hx_series.HX_Series()
hxs.te_pair.method = 'analytical'
hxs.width = 30.e-2
hxs.exh.height = 3.5e-2
hxs.cool.mdot = 1.
hxs.length = 1.

hxs.te_pair.I = current
hxs.te_pair.length = leg_length

hxs.te_pair.Ptype.material = 'HMS'
hxs.te_pair.Ntype.material = 'MgSi'

hxs.te_pair.Ptype.area = leg_area                           
hxs.te_pair.Ntype.area = hxs.te_pair.Ptype.area * area_ratio
hxs.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hxs.te_pair.Ptype.area +
                            hxs.te_pair.Ntype.area) )  

hxs.type = 'parallel'
hxs.setup()
hxs.exh.enhancement = enhancement.IdealFin()
hxs.exh.enhancement.thickness = 1.e-3
hxs.exh.enhancement.N = 60

hxs.exh.T_inlet = 800.
hxs.cool.T_inlet = 300.

hxs.set_mdot_charge()
# hxs.cool.T_outlet = fsolve(hxs.get_T_inlet_error, x0=hxs.cool.T_outlet)
hxs.solve_hxs()

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

plt.close('all')

print "power net:", hxs.power_net * 1000., 'W'
print "power raw:", hxs.te_pair.power_total * 1000., 'W'
print "pumping power:", hxs.Wdot_pumping * 1000., 'W'
hxs.exh.volume = hxs.exh.height * hxs.exh.width * hxs.length
print "exhaust volume:", hxs.exh.volume * 1000., 'L'
print "exhaust power density:", hxs.power_net / hxs.exh.volume, 'kW/m^3'
