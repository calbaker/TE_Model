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

# xmin2 output: 
# 7.556944047800089326e-01
# 1.843479126333371840e-02
# 1.247566990833368561e-03
# 3.945352024826855430e+00

# parameters for TE legs
area = (0.002)**2
length = 1.25e-3
current = 3.95 
area_ratio = 0.756
fill_fraction = 1.83e-2

hx_ducts = hx.HX()
hx_ducts.width = 30.e-2
# hx_ducts.exh.bypass = 0.
hx_ducts.exh.height = 3.5e-2
hx_ducts.length = 1.
hx_ducts.tem.I = current
hx_ducts.tem.length = length

hx_ducts.tem.Ntype.material = 'MgSi'
hx_ducts.tem.Ptype.material = 'HMS'

hx_ducts.tem.Ptype.area = area                           
hx_ducts.tem.Ntype.area = hx_ducts.tem.Ptype.area * area_ratio
hx_ducts.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_ducts.tem.Ptype.area +
                            hx_ducts.tem.Ntype.area) )  

# hx_ducts.tem.method = 'analytical'
hx_ducts.type = 'counter'

hx_ducts.exh.T_inlet = 800.
hx_ducts.exh.P = 100.
hx_ducts.cool.T_outlet = 310.
hx_ducts.cool.T_inlet_set = 300.

hx_ducts.ducts = np.arange(1, 7, 1)

hx_ducts.set_mdot_charge()
hx_ducts.exh.mdot0 = hx_ducts.exh.mdot 

hx_ducts.exh.mdot_array = hx_ducts.exh.mdot0 / hx_ducts.ducts
hx_ducts.cool.mdot_array = hx_ducts.cool.mdot * 2. / (hx_ducts.ducts + 1.) 

hx_ducts.exh.height_array = np.zeros(hx_ducts.ducts.size)
hx_ducts.cool.height_array = np.zeros(hx_ducts.ducts.size)
hx_ducts.height_array = np.zeros(hx_ducts.ducts.size)

# hx_ducts.exh.height_array = 3.5e-2 / hx_ducts.ducts
# hx_ducts.cool.height_array = 2.e-2 / (hx_ducts.ducts + 1.)
# hx_ducts.height_array = ( hx_ducts.ducts * hx_ducts.exh.height_array +  (hx_ducts.ducts + 1) * hx_ducts.cool.height_array )

def get_height(height):
    """solves for duct height such that total height is constrained"""
    hx_ducts.exh.height = np.float(height)
    hx_ducts.cool.height = 2. / 3.5 * hx_ducts.exh.height 

    hx_ducts.height = ( (ducts + 1.) * (2. * hx_ducts.plate.thickness + hx_ducts.cool.height) + ducts * hx_ducts.exh.height )

    total = 5.5e-2 + 6. * hx_ducts.plate.thickness

    error = hx_ducts.height - total

    return error

for i in range(hx_ducts.ducts.size):
    ducts = hx_ducts.ducts[i]
    fsolve(get_height, x0=0.01)
    hx_ducts.exh.height_array[i] = hx_ducts.exh.height
    hx_ducts.cool.height_array[i] = hx_ducts.cool.height
    hx_ducts.height_array[i] = hx_ducts.height

hx_ducts.cool.T_outlet_array = np.zeros(len(hx_ducts.height_array))
hx_ducts.cool.T_inlet_array = np.zeros(len(hx_ducts.height_array))

# Initializing arrays for storing loop results.  
hx_ducts.Qdot_array = np.zeros(hx_ducts.ducts.size)
hx_ducts.tem.power_array = np.zeros(np.size(hx_ducts.ducts)) 
hx_ducts.power_net_array = np.zeros(np.size(hx_ducts.ducts))
hx_ducts.Wdot_pumping_array = np.zeros(np.size(hx_ducts.ducts)) 


for i in np.arange(np.size(hx_ducts.ducts)):
    hx_ducts.exh.height = hx_ducts.exh.height_array[i]
    hx_ducts.cool.height = hx_ducts.cool.height_array[i]

    hx_ducts.exh.mdot = hx_ducts.exh.mdot_array[i]
    hx_ducts.cool.mdot = hx_ducts.cool.mdot_array[i]

    hx_ducts.cool.T_outlet = fsolve(hx_ducts.get_T_inlet_error, x0=hx_ducts.cool.T_outlet)
    hx_ducts.cool.T_outlet_array[i] = hx_ducts.cool.T_outlet
    hx_ducts.cool.T_inlet_array[i] = hx_ducts.cool.T_inlet
    
    print "Finished solving for", hx_ducts.ducts[i], "ducts\n"
    
    hx_ducts.Qdot_array[i] = hx_ducts.Qdot * hx_ducts.ducts[i]
    hx_ducts.tem.power_array[i] = hx_ducts.tem.power_total * hx_ducts.ducts[i]
    hx_ducts.power_net_array[i] = hx_ducts.power_net * hx_ducts.ducts[i]
    hx_ducts.Wdot_pumping_array[i] = hx_ducts.Wdot_pumping * hx_ducts.ducts[i]
    
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

FIGDIM1 = ([0.12, 0.12, 0.75, 0.75])

XTICKS = hx_ducts.exh.height_array.copy() * 100.
XTICKS = list(XTICKS)

for i in range(len(XTICKS)):
    XTICKS[i] = ('{:01.1f}'.format(XTICKS[i])) 

XTICKS[0] = ''

fig = plt.figure()
ax1 = fig.add_axes(FIGDIM1)
ax1.plot(hx_ducts.ducts, hx_ducts.Qdot_array / 10., 'db', label=r'$\dot{Q}/10$') 
ax1.plot(hx_ducts.ducts, hx_ducts.tem.power_array, 'og', label='TEM')
ax1.plot(hx_ducts.ducts, hx_ducts.power_net_array, 'sr', label='$P_{net}$')  
ax1.plot(hx_ducts.ducts, hx_ducts.Wdot_pumping_array, '*k', label='Pumping')
ax1.legend(loc='best')
ax1.grid()
ax1.set_xlabel('Ducts')
ax1.set_ylabel('Power (kW)')
ax1.set_ylim(0,7)
ax1.set_xlim(0,7)
ax1.set_ylim(ymin=0)
ax2 = plt.twiny(ax1)
plt.xticks(np.arange(len(XTICKS)), XTICKS)
ax2.set_xlabel('Exhaust Duct Height (cm)')

fig.savefig('../Plots/power v stacked ducts.pdf')
fig.savefig('../Plots/power v stacked ducts.pdf')

plt.show()

print "\nCurrent =", current
print "Length =", length
print "Fill Fraction", fill_fraction
print "power =", hx_ducts.power_net_array.max()
