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

area_ratio = 0.719
fill_fraction = 2.84e-2
leg_length = 3.5e-4
current = 13.3

hx_fins0 = hx.HX()

hx_fins0.length = 1.
hx_fins0.width = 0.3
hx_fins0.exh.height = 3.5e-2

hx_fins0.footprint = hx_fins0.length * hx_fins0.width

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
hx_fins0.cool.T_outlet = fsolve(hx_fins0.get_T_inlet_error,
                                x0=hx_fins0.cool.T_outlet)
hx_fins0.optimize()

def get_minpar(apar):
    """Returns parameter to be minimized as a function of apar.
    apar[0] : number of fins
    apar[1] : fin thickness (m)"""
    
    hx_fins0.exh.enhancement.N = apar[0]
    # hx_fins0.exh.enhancement.thickness = apar[1]
    hx_fins0.solve_hx()

    if hx_fins0.power_net < 0:
        minpar = np.abs(hx_fins0.power_net)
    else:
        minpar = 1. / hx_fins0.power_net
    
    return minpar

x0 = np.array([45])

length_array = np.linspace(0.2, 2, 15)
width_array = hx_fins0.footprint / length_array 
aspect_array = length_array / width_array
P_net = np.zeros(aspect_array.size)
P_raw = np.zeros(aspect_array.size)
P_pumping = np.zeros(aspect_array.size)

for i in range(aspect_array.size):
    hx_fins0.width = width_array[i]
    hx_fins0.length = length_array[i]
    hx_fins0.optimize()
    xmin = fmin(get_minpar, x0)
    P_net[i] = hx_fins0.power_net
    P_raw[i] = hx_fins0.te_pair.power_total
    P_pumping[i] = hx_fins0.Wdot_pumping

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

plt.figure()
plt.plot(aspect_array, P_net * 1000., label=r"P$_{net}$")
plt.plot(aspect_array, P_raw * 1000., label=r"P$_{raw}$")
plt.plot(aspect_array, P_pumping * 1000., label=r"P$_{pump}$")
plt.xlabel("Aspect Ratio")
plt.ylabel("Net Power (W)")
plt.grid()
plt.legend()

plt.savefig("../Plots/power v. aspect ratio.pdf")
plt.savefig("../Plots/power v. aspect ratio.png")
