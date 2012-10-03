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

hx_fins = hx.HX()

hx_fins.width = 0.6
hx_fins.length = 0.6 
hx_fins.exh.height = 1.5e-2
hx_fins.cool.height = 1.2e-2

hx_fins.te_pair.Ntype.material = 'MgSi'
hx_fins.te_pair.Ptype.material = 'HMS'

hx_fins.te_pair.set_leg_areas()

hx_fins.te_pair.method = 'numerical'
hx_fins.type = 'counter'

hx_fins.exh.set_enhancement('IdealFin')
# hx_fins.exh.enh.thickness = 0.25 * 2.54e-2
# 0.25 inches is too thick to manufacture

hx_fins.cool.enh = hx_fins.cool.set_enhancement('IdealFin')

OPT_PAR_DIR = "../output/fin_opt/"
hx_fins.te_pair.fill_fraction = (
    np.load(OPT_PAR_DIR + 'te_pair.fill_fraction.npy')
    )
hx_fins.te_pair.I = (
    np.load(OPT_PAR_DIR + 'te_pair.I.npy')
    )
hx_fins.te_pair.leg_area_ratio = (
    np.load(OPT_PAR_DIR + 'te_pair.leg_area_ratio.npy')
    )
hx_fins.te_pair.length = (
    np.load(OPT_PAR_DIR + 'te_pair.length.npy')
    )
hx_fins.exh.enh.spacing = (
    np.load(OPT_PAR_DIR + 'exh.enh.spacing.npy')
    )

hx_fins.exh.T_inlet = 800.
hx_fins.cool.T_inlet_set = 300.
hx_fins.cool.T_outlet = 310.

hx_fins.set_mdot_charge()

array_size = 50

hx_fins.exh.enh.spacings = (
    np.linspace(0.2, 5, 25) * hx_fins.exh.enh.spacing
    )

hx_fins.power_net_array = np.zeros(array_size)
hx_fins.Wdot_pumping_array = np.zeros(array_size)
hx_fins.Qdot_array = np.zeros(array_size)
hx_fins.te_pair.power_array = np.zeros(array_size)

for i in np.arange(np.size(hx_fins.exh.fin_array)):
    hx_fins.exh.enh.spacing = hx_fins.exh.enh.spacings[i]

    hx_fins.solve_hx()

    hx_fins.power_net_array[i] = hx_fins.power_net
    hx_fins.Wdot_pumping_array[i] = hx_fins.Wdot_pumping
    hx_fins.Qdot_array[i] = hx_fins.Qdot_total
    hx_fins.te_pair.power_array[i] = hx_fins.te_pair.power_total
    hx_fins.exh.enh.spacings[i] = hx_fins.exh.enh.spacing

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

PLOT_DIR = "../Plots/fins_varied/"

plt.figure()
plt.plot(hx_fins.exh.enh.spacings * 100., hx_fins.Qdot_array / 10., 'db', 
         label=r'$\dot{Q}_{h}$ / 10') 
plt.plot(hx_fins.exh.enh.spacings * 100., hx_fins.te_pair.power_array, 'og',
         label=r'$P_{raw}$')
plt.plot(hx_fins.exh.enh.spacings * 100., hx_fins.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_fins.exh.enh.spacings * 100., hx_fins.Wdot_pumping_array, '*k',
         label='Pumping')
plt.grid()
plt.xticks(rotation=40)
plt.xlabel('Fin Spacing (cm)')
plt.ylabel('Power (kW)')
# plt.ylim(0,3)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig(PLOT_DIR + 'p_v_spacing.pdf')

# plt.show()
