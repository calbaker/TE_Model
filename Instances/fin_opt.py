
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

area_ratio = 0.721
fill_fraction = 2.98e-2
leg_length = 3.45e-4
current = 13.5

hx_fins_opt = hx.HX()
hx_fins_opt.width = 0.3
hx_fins_opt.exh.height = 3.5e-2
hx_fins_opt.length = 1.
hx_fins_opt.te_pair.I = current
hx_fins_opt.te_pair.length = leg_length

hx_fins_opt.te_pair.Ntype.material = 'MgSi'
hx_fins_opt.te_pair.Ptype.material = 'HMS'

hx_fins_opt.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx_fins_opt.te_pair.method = 'analytical'
hx_fins_opt.type = 'counter'
hx_fins_opt.exh.enh = hx_fins_opt.exh.enh_lib.IdealFin()
hx_fins_opt.exh.enh.thickness = 1.e-3
hx_fins_opt.exh.enh.N = 60

hx_fins_opt.exh.T_inlet = 800.
hx_fins_opt.cool.T_inlet_set = 300.
hx_fins_opt.cool.T_outlet = 310.

hx_fins_opt.set_mdot_charge()
hx_fins_opt.cool.T_outlet = fsolve(hx_fins_opt.get_T_inlet_error,
                                x0=hx_fins_opt.cool.T_outlet)
def get_minpar(apar):
    """Returns parameter to be minimized as a function of apar.
    apar[0] : number of fins"""
    
    hx_fins_opt.exh.enh.N = apar[0]
    hx_fins_opt.solve_hx()

    if hx_fins_opt.power_net < 0:
        minpar = np.abs(hx_fins_opt.power_net)
    else:
        minpar = 1. / hx_fins_opt.power_net
    
    return minpar

x0 = np.array([59])
xmin = fmin(get_minpar, x0)

print "fins:", hx_fins_opt.exh.enh.N

print "power net:", hx_fins_opt.power_net * 1000., 'W'
print "power raw:", hx_fins_opt.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_fins_opt.Wdot_pumping * 1000., 'W'
hx_fins_opt.exh.volume = hx_fins_opt.exh.height * hx_fins_opt.exh.width * hx_fins_opt.length
print "exhaust volume:", hx_fins_opt.exh.volume * 1000., 'L'
print "exhaust power density:", hx_fins_opt.power_net / hx_fins_opt.exh.volume, 'kW/m^3'
