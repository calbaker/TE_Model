# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve

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

hx2.exh.enh = hx2.exh.enh_lib.OffsetStripFin()
hx2.exh.enh.thickness = 2.e-3
hx2.exh.enh.spacing = 3.19e-3
hx2.exh.enh.k = 0.02

hx2.plate.k = 0.02 # for Ti
hx2.plate.thickness = .125 * 2.54e-2

hx2.exh.T_inlet = 800.
hx2.cool.T_inlet_set = 300.
hx2.cool.T_outlet = 310.

hx2.set_mdot_charge()
hx2.cool.T_outlet = fsolve(hx2.get_T_inlet_error,
                                x0=hx2.cool.T_outlet)

hx2.footprint = hx2.width * hx2.length
hx2.exh.volume_spec = 10.e-3

width_array = 

for i in range(
    hx2.width = 
    hx2.length = 

    hx2.exh.height = hx2.exh.volume_spec / (hx2.width * hx2.length)  
    
    hx2.solve_hx()

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


# plt.show()
