# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import numpy as np
import xlrd

# User Defined Modules
# In this directory
import hx
reload(hx)

print "Beginning execution..."

area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.thermoelectrics_on = False
hx.width = 9.e-2
hx.length = 0.195
hx.exh.bypass = 0.
hx.exh.height = 1.e-2
mdot_cool = 4. * hx.cool.rho # coolant flow rate (GPM) 
hx.cool.mdot = mdot_cool / 60. * 3.8
hx.cool.height = 0.5e-2
hx.tem.I = 4.5
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'counter'
hx.exh.P = 100.

hx.cool.T_outlet = 300.
hx.exh.T_inlet = 500.
hx.set_mdot_charge()
hx.solve_hx()

print "\nProgram finished."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5



