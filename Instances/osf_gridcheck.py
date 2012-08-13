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

hx_osf0 = hx.HX()
hx_osf0.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current]) 

hx_osf0.width = 22. * 2.54e-2
hx_osf0.length = 22. * 2.54e-2

hx_osf0.exh.height = 1.25 * 2.54e-2
hx_osf0.cool.height = 1. * 2.54e-2

hx_osf0.te_pair.I = current
hx_osf0.te_pair.length = leg_length

hx_osf0.te_pair.Ntype.material = 'MgSi'
hx_osf0.te_pair.Ptype.material = 'HMS'

hx_osf0.te_pair.set_leg_areas()

hx_osf0.te_pair.method = 'numerical'
hx_osf0.type = 'counter'

hx_osf0.exh.enh = hx_osf0.exh.enh_lib.OffsetStripFin()
# hx_osf0.exh.enh.thickness = 0.25 * 2.54e-2
# 0.25 inches is too thick to manufacture
hx_osf0.exh.enh.thickness = 0.01 * 2.54e-2 
hx_osf0.exh.enh.spacing = 0.1 * 2.54e-2 
hx_osf0.exh.enh.l = 0.47 * 2.54e-2

hx_osf0.cool.enh = hx_osf0.cool.enh_lib.IdealFin()
hx_osf0.cool.enh.thickness = 0.1 * 2.54e-2 
hx_osf0.cool.enh.spacing = 0.4 * 2.54e-2

hx_osf0.exh.T_inlet = 800.
hx_osf0.cool.T_inlet_set = 300.
hx_osf0.cool.T_outlet = 310.

hx_osf0.set_mdot_charge()
# hx_osf0.cool.T_outlet = fsolve(hx_osf0.get_T_inlet_error,
#                                x0=hx_osf0.cool.T_outlet)

hx_osf0.apar_list.append(['self', 'exh', 'enh', 'l'])
hx_osf0.apar_list.append(['self', 'exh', 'enh', 'spacing'])

# hx_osf0.solve_hx()

print "\nProgram finished."

elapsed = time.clock() - time0

print "elapsed time:", elapsed

print "\nPlotting..."

#hx_osf0.solve_hx()
#print "power net:", hx_osf0.power_net * 1000., 'W'


#hx_osf0.te_pair.nodes = 40
#hx_osf0.solve_hx()
#print "power net:", hx_osf0.power_net * 1000., 'W'


# grid independence check
for x in range(10, 31, 5):

    hx_osf0.te_pair.nodes = x
    hx_osf0.solve_hx()
    print "\ncurrent number of nodes = ", hx_osf0.te_pair.nodes
    print "for", hx_osf0.te_pair.nodes, " nodes, power output is = "
    print "power net:", hx_osf0.power_net * 1000., 'W'
    
