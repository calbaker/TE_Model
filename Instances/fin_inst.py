# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve
from scimath.units import * 
from scimath.units.api import *

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

area = UnitScalar((0.002)**2, units=length.m**2)
leg_length = UnitScalar(3.27e-4, units=length.m)
current = UnitScalar(13.9, units=SI.ampere)
area_ratio = 0.683
fill_fraction = 2.38e-2

hx_fins0 = hx.HX()
hx_fins0.width = UnitScalar(30.e-2, units=length.m)
hx_fins0.exh.height = UnitScalar(3.5e-2, units=length.m)
hx_fins0.length = UnitScalar(1., units=length.m)
hx_fins0.tem.I = current
hx_fins0.tem.length = leg_length

hx_fins0.tem.Ntype.material = 'MgSi'
hx_fins0.tem.Ptype.material = 'HMS'

hx_fins0.tem.Ptype.area = area                           
hx_fins0.tem.Ntype.area = hx_fins0.tem.Ptype.area * area_ratio
hx_fins0.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_fins0.tem.Ptype.area +
                            hx_fins0.tem.Ntype.area) )  

hx_fins0.tem.method = 'analytical'
hx_fins0.type = 'counter'
hx_fins0.exh.enhancement = "straight fins"
hx_fins0.exh.fin.thickness = UnitScalar(5.e-3, units=length.m)
hx_fins0.exh.fins = 32

hx_fins0.exh.T_inlet = UnitScalar(800., units=temperature.K)
hx_fins0.cool.T_inlet_set = UnitScalar(300., units=temperature.K)
hx_fins0.cool.T_outlet = UnitScalar(310., units=temperature.K)

hx_fins0.set_mdot_charge()
hx_fins0.cool.T_outlet = fsolve(hx_fins0.get_T_inlet_error, x0=hx_fins0.cool.T_outlet)

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

plt.figure()
plt.plot(hx_fins0.x_dim * 100., hx_fins0.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_fins0.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/temp '+hx_fins0.type+str(hx_fins0.exh.fins)+'.png')
plt.savefig('../Plots/temp '+hx_fins0.type+str(hx_fins0.exh.fins)+'.pdf')

# plt.show()

print hx_fins0.power_net
