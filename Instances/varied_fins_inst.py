# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)
import enhancement
reload(enhancement)

# Output from xmin2
# 6.834534389943245358e-01
# 2.384892371916906562e-02
# 3.267547630355634538e-04
# 1.390419916569227965e+01

# parameters for TE legs
leg_area = (0.002)**2

area_ratio = 0.703
fill_fraction = 3.12e-2
leg_length = 6.01e-4
current = 7.77


hx_fins = hx.HX()
hx_fins.width = 30.e-2
hx_fins.exh.bypass = 0.
hx_fins.exh.height = 3.5e-2
hx_fins.length = 1.
hx_fins.te_pair.I = current
hx_fins.te_pair.length = leg_length

hx_fins.te_pair.Ntype.material = 'MgSi'
hx_fins.te_pair.Ptype.material = 'HMS'

hx_fins.te_pair.Ptype.area = leg_area
hx_fins.te_pair.Ntype.area = hx_fins.te_pair.Ptype.area * area_ratio
hx_fins.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_fins.te_pair.Ptype.area +
                            hx_fins.te_pair.Ntype.area) )  

hx_fins.te_pair.method = "analytical"
hx_fins.type = 'counter'
hx_fins.exh.enhancement = enhancement.IdealFin()
hx_fins.exh.enhancement.thickness = 1.e-3
hx_fins.exh.enhancement.N = 10

hx_fins.exh.T_inlet = 800.
hx_fins.exh.P = 100.
hx_fins.cool.T_inlet_set = 300.
hx_fins.cool.T_outlet = 310.

hx_fins.set_mdot_charge()
hx_fins.cool.T_outlet = fsolve(hx_fins.get_T_inlet_error, x0=hx_fins.cool.T_outlet)

hx_fins.exh.fin_array = np.arange(15, 42, 2)
# array for varied exhaust duct height (m)
array_size = np.size(hx_fins.exh.fin_array)
hx_fins.power_net_array = np.zeros(array_size)
hx_fins.Wdot_pumping_array = np.zeros(array_size)
hx_fins.Qdot_array = np.zeros(array_size)
hx_fins.te_pair.power_array = np.zeros(array_size)
hx_fins.exh.enhancement.spacings = np.zeros(np.size(hx_fins.exh.fin_array)) 

for i in np.arange(np.size(hx_fins.exh.fin_array)):
    hx_fins.exh.enhancement.N = hx_fins.exh.fin_array[i]
    print "Solving for", hx_fins.exh.enhancement.N, "fins\n"
    hx_fins.cool.T_outlet = fsolve(hx_fins.get_T_inlet_error, x0=hx_fins.cool.T_outlet)
    hx_fins.power_net_array[i] = hx_fins.power_net
    hx_fins.Wdot_pumping_array[i] = hx_fins.Wdot_pumping
    hx_fins.Qdot_array[i] = hx_fins.Qdot_total
    hx_fins.te_pair.power_array[i] = hx_fins.te_pair.power_total
    hx_fins.exh.enhancement.spacings[i] = hx_fins.exh.enhancement.spacing

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
plt.plot(hx_fins.exh.enhancement.spacings * 100., hx_fins.Qdot_array / 10., 'db', 
         label=r'$\dot{Q}/10$') 
plt.plot(hx_fins.exh.enhancement.spacings * 100., hx_fins.te_pair.power_array, 'og',
         label='TE_PAIR')
plt.plot(hx_fins.exh.enhancement.spacings * 100., hx_fins.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_fins.exh.enhancement.spacings * 100., hx_fins.Wdot_pumping_array, '*k',
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
plt.plot(hx_fins.exh.fin_array, hx_fins.Qdot_array / 10., 'db', label=r'$\dot{Q}/10$') 
plt.plot(hx_fins.exh.fin_array, hx_fins.te_pair.power_array, 'og', label='TE_PAIR')
plt.plot(hx_fins.exh.fin_array, hx_fins.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_fins.exh.fin_array, hx_fins.Wdot_pumping_array, '*k', 
         label='Pumping')
plt.grid()
plt.xlabel('Fins')
plt.ylabel('Power (kW)')
plt.ylim(0,3)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
#plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig('../Plots/power v fins.pdf')
plt.savefig('../Plots/power v fins.png')

# plt.show()
