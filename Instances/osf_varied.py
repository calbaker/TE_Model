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

time0 = time.clock()

hx_osf = hx.HX()

hx_osf.width = 0.6
hx_osf.length = 0.6 
hx_osf.exh.height = 1.5e-2
hx_osf.cool.height = 1.2e-2

hx_osf.te_pair.Ntype.material = 'MgSi'
hx_osf.te_pair.Ptype.material = 'HMS'

hx_osf.te_pair.set_leg_areas()

hx_osf.te_pair.method = 'numerical'
hx_osf.type = 'counter'

hx_osf.exh.set_enhancement('OffsetStripFin')
# hx_osf.exh.enh.thickness = 0.25 * 2.54e-2
# 0.25 inches is too thick to manufacture
hx_osf.exh.enh.thickness = 2.5e-3
hx_osf.exh.enh.spacing = 10.e-3

hx_osf.cool.enh = hx_osf.cool.set_enhancement('IdealFin')
hx_osf.cool.enh.thickness = 2.5e-3
hx_osf.cool.enh.spacing = 10.e-3

OPT_PAR_DIR = "../output/osf_opt/"

hx_osf.exh.enh.spacing = (
    np.load(OPT_PAR_DIR + 'exh.enh.spacing.npy')     
    )
hx_osf.te_pair.fill_fraction = (
    np.load(OPT_PAR_DIR + 'te_pair.fill_fraction.npy')
    )
hx_osf.te_pair.I = (
    np.load(OPT_PAR_DIR + 'te_pair.I.npy')            
    )
hx_osf.te_pair.leg_area_ratio = (
    np.load(OPT_PAR_DIR + 'te_pair.leg_area_ratio.npy')
    )
hx_osf.te_pair.length = (
    np.load(OPT_PAR_DIR + 'te_pair.length.npy')       
    )

hx_osf.exh.T_inlet = 800.
hx_osf.cool.T_inlet_set = 300.
hx_osf.cool.T_outlet = 310.

hx_osf.set_mdot_charge()

array_size = 50

hx_osf.exh.enh.spacings = (
    np.linspace(0.2, 5, array_size) * hx_osf.exh.enh.spacing
    )

hx_osf.power_net_array = np.zeros(array_size)
hx_osf.Wdot_pumping_array = np.zeros(array_size)
hx_osf.Qdot_array = np.zeros(array_size)
hx_osf.te_pair.power_array = np.zeros(array_size)

for i in np.arange(array_size):
    if i % 5 == 0:
        print i
    hx_osf.exh.enh.spacing = hx_osf.exh.enh.spacings[i]

    hx_osf.solve_hx()

    hx_osf.power_net_array[i] = hx_osf.power_net
    hx_osf.Wdot_pumping_array[i] = hx_osf.Wdot_pumping
    hx_osf.Qdot_array[i] = hx_osf.Qdot_total
    hx_osf.te_pair.power_array[i] = hx_osf.te_pair.power_total
    hx_osf.exh.enh.spacings[i] = hx_osf.exh.enh.spacing

output_dir = "../output/osf_varied/"
np.save(output_dir + "power_net", hx_osf.power_net_array)
np.save(output_dir + "Wdot_pumping", hx_osf.Wdot_pumping_array)
np.save(output_dir + "Qdot", hx_osf.Qdot_array)
np.save(output_dir + "power_total", hx_osf.te_pair.power_array)
np.save(output_dir + "spacing", hx_osf.exh.enh.spacings)

print "\nPlotting..."

execfile('plot_osf_varied.py')
