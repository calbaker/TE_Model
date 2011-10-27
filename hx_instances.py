# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os

#
# User Defined Modules
# In this directory
import hx
reload(hx)

print "Beginning execution..."

length = 1. * 0.001
current = 3.5
area = (0.002)**2
area_ratio = 0.69 # n-type area per p-type area, consistent with
                  # Sherman.
fill_fraction = 50.                  

hx = hx.HX()
hx.tem.method = 'analytical'
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.cool.mdot = 1.
hx.length = 1.
hx.tem.I = 4.5
hx.tem.length = length
hx.tem.Ptype.material = 'HMS'
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ptype.area = area
hx.tem.Ntype.area = hx.tem.Ptype.area * area_ratio
hx.tem.area_void = 25. * area
hx.type = 'parallel'
# hx.exh.enhancement = 'straight fins'
# hx.exh.fins = 15

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.set_mdot_charge()
hx.solve_hx()

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

plt.close()



# plt.show()

