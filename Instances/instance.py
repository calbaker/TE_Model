# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import hx

area = (0.002)**2
length = 5.e-3

hx = hx.HX()
hx.te_pair.I = 2.
hx.te_pair.length = length
hx.te_pair.Ntype.material = 'MgSi'
hx.te_pair.Ntype.area = area
hx.te_pair.Ptype.material = 'HMS'
hx.te_pair.Ptype.area = area * 2. 
hx.te_pair.area_void = 10. * area
hx.type = 'parallel'
hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.
#hx.te_pair = te_pair.TECarnot()
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

plt.figure()
plt.plot(hx.x_dim * 100., hx.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx.x_dim * 100., hx.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx.x_dim * 100., hx.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
plt.title('Temperature v. Distance, '+hx.type)
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/temp '+hx.type+'.png')
plt.savefig('Plots/temp '+hx.type+'.pdf')

plt.figure()
plt.plot(hx.te_pair.Ntype.T, hx.te_pair.Ntype.q, label=hx.te_pair.Ntype.material)
plt.plot(hx.te_pair.Ptype.T, hx.te_pair.Ptype.q, label=hx.te_pair.Ptype.material)
plt.xlabel('Temperature (K)')
plt.ylabel(r'Heat Flux ($\frac{W}{m^2K}$)')
plt.title('Heat Flux v Temperature')
plt.grid()
plt.legend()

plt.show()

