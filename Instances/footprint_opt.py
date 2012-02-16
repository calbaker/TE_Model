# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve, fminbound, fmin

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.721
fill_fraction = 3.13e-2
leg_length = 3.45e-4
current = 13.5

hx2 = hx.HX()
hx2.width = 0.3
hx2.exh.height = 3.5e-2
hx2.length = 1.
hx2.te_pair.I = current
hx2.te_pair.length = leg_length

hx2.te_pair.Ntype.material = 'MgSi'
hx2.te_pair.Ptype.material = 'HMS'

hx2.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx2.te_pair.method = 'analytical'
hx2.type = 'counter'
hx2.exh.enh = hx2.exh.enh_lib.IdealFin()
hx2.exh.enh.thickness = 1.e-3
hx2.exh.enh.N = 60

hx2.exh.T_inlet = 800.
hx2.cool.T_inlet_set = 300.
hx2.cool.T_outlet = 310.

hx2.set_mdot_charge()
hx2.cool.T_outlet = fsolve(hx2.get_T_inlet_error,
                                x0=hx2.cool.T_outlet)

hx2.footprint = hx2.width * hx2.length

def get_minpar(apar):
    """Returns parameter to be minimized as a function of apar.
    apar : fin spacing"""
    
    hx2.exh.enh.spacing = apar[0]
    hx2.aspect_ratio = apar[1]
    
    hx2.width = np.sqrt(hx2.footprint / hx2.aspect_ratio)
    hx2.length = hx2.aspect_ratio * hx2.width

    hx2.solve_hx()

    if hx2.power_net < 0:
        minpar = np.abs(hx2.power_net)
    else:
        minpar = 1. / hx2.power_net
    
    print "fins:", hx2.exh.enh.N
    print "length:", hx2.length
    print "width:", hx2.width
    print "power net:", hx2.power_net * 1000., 'W'

    return minpar

x0 = np.array([2.72e-3, 1.])

xmin = fmin(get_minpar, x0)

print "fins:", hx2.exh.enh.N
print "length:", hx2.length
print "width:", hx2.width

print "power net:", hx2.power_net * 1000., 'W'
print "power raw:", hx2.te_pair.power_total * 1000., 'W'
print "pumping power:", hx2.Wdot_pumping * 1000., 'W'
hx2.exh.volume = hx2.exh.height * hx2.exh.width * hx2.length
print "exhaust volume:", hx2.exh.volume * 1000., 'L'
print "exhaust power density:", hx2.power_net / hx2.exh.volume, 'kW/m^3'
