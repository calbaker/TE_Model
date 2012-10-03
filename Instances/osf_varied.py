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

hx_osf.exh.fin_array = np.arange(30, 102, 4)
# array for varied exhaust duct height (m)
array_size = np.size(hx_osf.exh.fin_array)
hx_osf.power_net_array = np.zeros(array_size)
hx_osf.Wdot_pumping_array = np.zeros(array_size)
hx_osf.Qdot_array = np.zeros(array_size)
hx_osf.te_pair.power_array = np.zeros(array_size)
hx_osf.exh.enh.spacings = np.zeros(np.size(hx_osf.exh.fin_array)) 

for i in np.arange(np.size(hx_osf.exh.fin_array)):
    hx_osf.exh.enh.N = hx_osf.exh.fin_array[i]

    print "Solving for", hx_osf.exh.enh.N, "osf\n"
    # hx_osf.cool.T_outlet = fsolve(hx_osf.get_T_inlet_error,
    # x0=hx_osf.cool.T_outlet)
    hx_osf.solve_hx()

    hx_osf.power_net_array[i] = hx_osf.power_net
    hx_osf.Wdot_pumping_array[i] = hx_osf.Wdot_pumping
    hx_osf.Qdot_array[i] = hx_osf.Qdot_total
    hx_osf.te_pair.power_array[i] = hx_osf.te_pair.power_total
    hx_osf.exh.enh.spacings[i] = hx_osf.exh.enh.spacing

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

plt.figure()
plt.plot(hx_osf.exh.enh.spacings * 100., hx_osf.Qdot_array / 10., 'db', 
         label=r'$\dot{Q}_{h}$ / 10') 
plt.plot(hx_osf.exh.enh.spacings * 100., hx_osf.te_pair.power_array, 'og',
         label=r'$P_{raw}$')
plt.plot(hx_osf.exh.enh.spacings * 100., hx_osf.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_osf.exh.enh.spacings * 100., hx_osf.Wdot_pumping_array, '*k',
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
plt.savefig('../Plots/power v fin spacing.pdf')
plt.savefig('../Plots/power v fin spacing.png')

plt.figure()
plt.plot(hx_osf.exh.fin_array, hx_osf.Qdot_array / 10., 'db', label=r'$\dot{Q}/10$') 
plt.plot(hx_osf.exh.fin_array, hx_osf.te_pair.power_array, 'og', label='TE_PAIR')
plt.plot(hx_osf.exh.fin_array, hx_osf.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_osf.exh.fin_array, hx_osf.Wdot_pumping_array, '*k', 
         label='Pumping')
plt.grid()
plt.xlabel('Osf')
plt.ylabel('Power (kW)')
plt.ylim(0,3)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
#plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig('../Plots/power v osf.pdf')
plt.savefig('../Plots/power v osf.png')

# plt.show()
