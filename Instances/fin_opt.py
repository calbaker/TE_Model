
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
import enhancement
reload(enhancement)

leg_area = (0.002)**2

area_ratio = 0.703
fill_fraction = 3.12e-2
leg_length = 6.01e-4
current = 7.77

hx_fins0 = hx.HX()
hx_fins0.width = 0.3
hx_fins0.exh.height = 3.5e-2
hx_fins0.length = 1.
hx_fins0.te_pair.I = current
hx_fins0.te_pair.length = leg_length

hx_fins0.te_pair.Ntype.material = 'MgSi'
hx_fins0.te_pair.Ptype.material = 'HMS'

hx_fins0.te_pair.Ptype.area = leg_area                           
hx_fins0.te_pair.Ntype.area = hx_fins0.te_pair.Ptype.area * area_ratio
hx_fins0.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_fins0.te_pair.Ptype.area +
                            hx_fins0.te_pair.Ntype.area) )  

hx_fins0.te_pair.method = 'analytical'
hx_fins0.type = 'counter'
hx_fins0.exh.enhancement = enhancement.IdealFin()
hx_fins0.exh.enhancement.thickness = 1.e-3
hx_fins0.exh.enhancement.N = 17

hx_fins0.exh.T_inlet = 800.
hx_fins0.cool.T_inlet_set = 300.
hx_fins0.cool.T_outlet = 310.

hx_fins0.set_mdot_charge()
hx_fins0.cool.T_outlet = fsolve(hx_fins0.get_T_inlet_error, x0=hx_fins0.cool.T_outlet)

def get_minpar(param):
    """Returns parameter to be minimized as a function of apar.
    apar[0] : number of fins
    apar[1] : fin thickness (m)"""
    
    hx_fins0.exh.enhancement.N = apar[0]
    hx_fins0.exh.enhancement.thickness = apar[1]
    hx_fins0.exh.solve_hx()

    if hx_fins0.power_net < 0:
        minpar = np.abs(hx_fins0.power_net)
    else:
        minpar = 1. / hx_fins0.power_net
    
    return minpar

x0 = np.array([45, 0.001])
xmin = fmin(get_minpar, x0)
