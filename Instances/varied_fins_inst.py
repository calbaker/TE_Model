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

# Output from xmin2
# 6.834534389943245358e-01
# 2.384892371916906562e-02
# 3.267547630355634538e-04
# 1.390419916569227965e+01

# parameters for TE legs
area = (0.002)**2
length = 3.27e-4
current = 13.9
area_ratio = 0.683
fill_fraction = 2.38e-2

hx_fins = hx.HX()
hx_fins.width = 30.e-2
hx_fins.exh.bypass = 0.
hx_fins.exh.height = 3.5e-2
hx_fins.length = 1.
hx_fins.tem.I = current
hx_fins.tem.length = length

hx_fins.tem.Ntype.material = 'MgSi'
hx_fins.tem.Ptype.material = 'HMS'

hx_fins.tem.Ptype.area = area                           
hx_fins.tem.Ntype.area = hx_fins.tem.Ptype.area * area_ratio
hx_fins.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_fins.tem.Ptype.area +
                            hx_fins.tem.Ntype.area) )  

# hx_fins.tem.method = "analytical"
hx_fins.type = 'counter'
hx_fins.exh.enhancement = "straight fins"
hx_fins.exh.fin.thickness = 5.e-3
hx_fins.exh.fins = 10

hx_fins.exh.T_inlet = 800.
hx_fins.exh.P = 100.
hx_fins.cool.T_inlet_set = 300.
hx_fins.cool.T_outlet = 310.

hx_fins.set_mdot_charge()
hx_fins.cool.T_outlet = fsolve(hx_fins.get_T_inlet_error, x0=hx_fins.cool.T_outlet)

hx_fins.exh.fin_array = np.arange(20, 42, 2)
# array for varied exhaust duct height (m)
array_size = np.size(hx_fins.exh.fin_array)
hx_fins.power_net_array = np.zeros(array_size)
hx_fins.Wdot_pumping_array = np.zeros(array_size)
hx_fins.Qdot_array = np.zeros(array_size)
hx_fins.tem.power_array = np.zeros(array_size)
hx_fins.exh.fin.spacings = np.zeros(np.size(hx_fins.exh.fin_array)) 

for i in np.arange(np.size(hx_fins.exh.fin_array)):
    hx_fins.exh.fins = hx_fins.exh.fin_array[i]
    print "\nSolving for", hx_fins.exh.fins, "fins\n"
    hx_fins.solve_hx()
    hx_fins.power_net_array[i] = hx_fins.power_net
    hx_fins.Wdot_pumping_array[i] = hx_fins.Wdot_pumping
    hx_fins.Qdot_array[i] = hx_fins.Qdot
    hx_fins.tem.power_array[i] = hx_fins.tem.power_total
    hx_fins.exh.fin.spacings[i] = hx_fins.exh.fin.spacing

print "\nProgram finished."
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
plt.plot(hx_fins.exh.fin.spacings * 100., hx_fins.Qdot_array / 10., 'db', 
         label=r'$\dot{Q}/10$') 
plt.plot(hx_fins.exh.fin.spacings * 100., hx_fins.tem.power_array, 'og',
         label='TEM')
plt.plot(hx_fins.exh.fin.spacings * 100., hx_fins.power_net_array, 'sr', 
         label='$P_{net}$')  
plt.plot(hx_fins.exh.fin.spacings * 100., hx_fins.Wdot_pumping_array, '*k',
         label='Pumping')
plt.grid()
plt.xticks(rotation=40)
plt.xlabel('Fin Spacing (cm)')
plt.ylabel('Power (kW)')
plt.ylim(0,3)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig('../Plots/power v fin spacing.pdf')
plt.savefig('../Plots/power v fin spacing.png')

plt.figure()
plt.plot(hx_fins.exh.fin_array, hx_fins.Qdot_array / 10., 'db', label=r'$\dot{Q}/10$') 
plt.plot(hx_fins.exh.fin_array, hx_fins.tem.power_array, 'og', label='TEM')
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
