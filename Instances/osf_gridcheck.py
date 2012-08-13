# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
import time

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
current = 34.3

time0 = time.clock()

hx_osf_gridcheck = hx.HX()
hx_osf_gridcheck.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current]) 

hx_osf_gridcheck.width = 22. * 2.54e-2
hx_osf_gridcheck.length = 22. * 2.54e-2

hx_osf_gridcheck.exh.height = 1.25 * 2.54e-2
hx_osf_gridcheck.cool.height = 1. * 2.54e-2

hx_osf_gridcheck.te_pair.I = current
hx_osf_gridcheck.te_pair.length = leg_length

hx_osf_gridcheck.te_pair.Ntype.material = 'MgSi'
hx_osf_gridcheck.te_pair.Ptype.material = 'HMS'

hx_osf_gridcheck.te_pair.set_leg_areas()

hx_osf_gridcheck.te_pair.method = 'numerical'
hx_osf_gridcheck.type = 'counter'

hx_osf_gridcheck.exh.enh = hx_osf_gridcheck.exh.enh_lib.OffsetStripFin()
# hx_osf_gridcheck.exh.enh.thickness = 0.25 * 2.54e-2
# 0.25 inches is too thick to manufacture
hx_osf_gridcheck.exh.enh.thickness = 0.01 * 2.54e-2 
hx_osf_gridcheck.exh.enh.spacing = 0.1 * 2.54e-2 
hx_osf_gridcheck.exh.enh.l = 0.47 * 2.54e-2

hx_osf_gridcheck.cool.enh = hx_osf_gridcheck.cool.enh_lib.IdealFin()
hx_osf_gridcheck.cool.enh.thickness = 0.1 * 2.54e-2 
hx_osf_gridcheck.cool.enh.spacing = 0.4 * 2.54e-2

hx_osf_gridcheck.exh.T_inlet = 800.
hx_osf_gridcheck.cool.T_inlet_set = 300.
hx_osf_gridcheck.cool.T_outlet = 310.

hx_osf_gridcheck.set_mdot_charge()
# hx_osf_gridcheck.cool.T_outlet = fsolve(hx_osf_gridcheck.get_T_inlet_error,
#                                x0=hx_osf_gridcheck.cool.T_outlet)

hx_osf_gridcheck.apar_list.append(['self', 'exh', 'enh', 'l'])
hx_osf_gridcheck.apar_list.append(['self', 'exh', 'enh', 'spacing'])

hx_osf_gridcheck.solve_hx()

# grid independence check
for i in np.arange(5, 40, 5):

    hx_osf_gridcheck.te_pair.nodes = i
    hx_osf_gridcheck.solve_hx()

    print "for", hx_osf_gridcheck.te_pair.nodes, " nodes, power output is = "
    print "power net:", hx_osf_gridcheck.power_net * 1000., 'W'
    
