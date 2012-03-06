"""This script runs the model for designs available from http://www.thermal-solutions.us/extrusions.html"""

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

area_ratio = 0.745
fill_fraction = 3.10e-2
leg_length = 3.56e-4
current = 13.0

hx_exp = hx.HX()
hx_exp.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current]) 
parallel_extrusions = 3.
hx_exp.width = 0.1076 * parallel_extrusions
hx_exp.exh.height = 3.5e-2
hx_exp.length = 0.5
hx_exp.te_pair.I = current
hx_exp.te_pair.length = leg_length

hx_exp.te_pair.Ntype.material = 'MgSi'
hx_exp.te_pair.Ptype.material = 'HMS'

hx_exp.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx_exp.te_pair.method = 'analytical'
hx_exp.type = 'counter'

hx_exp.exh.enh = hx_exp.exh.enh_lib.IdealFin()
hx_exp.exh.enh.thickness = 1.e-3
hx_exp.exh.enh.spacing = 3.24e-3

hx_exp.cool.enh = hx_exp.cool.enh_lib.IdealFin()
hx_exp.cool.enh.thickness = 1.e-3
hx_exp.cool.enh.spacing = 3.24e-3

hx_exp.exh.T_inlet = 800.
hx_exp.cool.T_inlet_set = 300.
hx_exp.cool.T_outlet = 310.

hx_exp.set_mdot_charge()

hx_exp.optimize()

# def get_minpar(length):
#     """Returns inverse of net power for varied length."""
#     hx_exp.length = length
#     hx_exp.solve_hx()
    
#     if hx_exp.power_net > 0:
#         minpar = 1. / hx_exp.power_net
#     else:
#         minpar = np.abs(hx_exp.power_net)

#     return minpar

# length = fmin(get_minpar, x0=1.)

print "\nPreparing plots."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

cost = ( parallel_extrusions * 6. * hx_exp.length * 75. ) 

print "Material cost:", "$" + str(cost)
print "power net:", hx_exp.power_net * 1000., 'W'
print "power raw:", hx_exp.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_exp.Wdot_pumping * 1000., 'W'
hx_exp.exh.volume = hx_exp.exh.height * hx_exp.exh.width * hx_exp.length
print "exhaust volume:", hx_exp.exh.volume * 1000., 'L'
print "exhaust power density:", hx_exp.power_net / hx_exp.exh.volume, 'kW/m^3'


