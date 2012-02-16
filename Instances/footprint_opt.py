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

hx1 = hx.HX()
hx1.width = 0.3
hx1.exh.height = 3.5e-2
hx1.length = 1.
hx1.te_pair.I = current
hx1.te_pair.length = leg_length

hx1.te_pair.Ntype.material = 'MgSi'
hx1.te_pair.Ptype.material = 'HMS'

hx1.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx1.te_pair.method = 'analytical'
hx1.type = 'counter'
hx1.exh.enh = hx1.exh.enh_lib.IdealFin()
hx1.exh.enh.thickness = 1.e-3
hx1.exh.enh.N = 60

hx1.exh.T_inlet = 800.
hx1.cool.T_inlet_set = 300.
hx1.cool.T_outlet = 310.

hx1.set_mdot_charge()
hx1.cool.T_outlet = fsolve(hx1.get_T_inlet_error,
                                x0=hx1.cool.T_outlet)

hx1.footprint = hx1.width * hx1.length

def get_minpar(apar):
    """Returns parameter to be minimized as a function of apar.
    apar : fin spacing"""
    
    hx1.exh.enh.spacing = apar[0]
    hx1.aspect_ratio = apar[1]
    
    hx1.width = np.sqrt(hx1.footprint / hx1.aspect_ratio)
    hx1.length = hx1.aspect_ratio * hx1.width

    hx1.solve_hx()

    if hx1.power_net < 0:
        minpar = np.abs(hx1.power_net)
    else:
        minpar = 1. / hx1.power_net
    
    print "fins:", hx_fins_opt.exh.enh.N
    print "length:", hx_fins_opt.length
    print "width:", hx_fins_opt.width
    print "power net:", hx_fins_opt.power_net * 1000., 'W'

    return minpar

x0 = np.array([2.72e-3, 1.])

xmin = fmin(get_minpar, x0)

print "fins:", hx_fins_opt.exh.enh.N
print "length:", hx_fins_opt.length
print "width:", hx_fins_opt.width

print "power net:", hx_fins_opt.power_net * 1000., 'W'
print "power raw:", hx_fins_opt.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_fins_opt.Wdot_pumping * 1000., 'W'
hx_fins_opt.exh.volume = hx_fins_opt.exh.height * hx_fins_opt.exh.width * hx_fins_opt.length
print "exhaust volume:", hx_fins_opt.exh.volume * 1000., 'L'
print "exhaust power density:", hx_fins_opt.power_net / hx_fins_opt.exh.volume, 'kW/m^3'
