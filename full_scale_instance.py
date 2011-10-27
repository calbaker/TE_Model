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

area = (0.002)**2
length = 1.e-3

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
hx.tem.Ptype.area = area
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area / 0.69
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

plt.figure()
plt.plot(hx.x_dim * 100., hx.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/' + hx.tem.method + '/' + 'temp.png')
plt.savefig('Plots/' + hx.tem.method + '/' + 'temp.pdf')

plt.figure()
plt.plot(hx.x_dim * 100., hx.tem.power_nodes * 1000., 's', label='Exhaust')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('TEG Power (W)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/' + hx.tem.method + '/' + 'TEG power.png')
plt.savefig('Plots/' + hx.tem.method + '/' + 'TEG power.pdf')

# plt.show()

