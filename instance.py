# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

os.chdir('/home/chad/Documents/UT Stuff/Research/Diesel TE/TE_Model')

# User Defined Modules
# In this directory
import hx

print "Beginning execution..."

hx = hx.HX()
hx.tem.Ntype.material = 'ideal BiTe n-type'
hx.tem.Ptype.material = 'ideal BiTe p-type'
hx.type = 'parallel'
hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.
#hx.tem = tem.TECarnot()
hx.solve_hx()

print "\nProgram finished."
print "\nPlotting..."

# Plot configuration
FONTSIZE = 20
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

mpl.figure()
mpl.plot(hx.x_dim * 100., hx.exh.T_nodes, '-r', label='Exhaust')
mpl.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
mpl.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
mpl.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

mpl.xlabel('Distance Along HX (cm)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance, '+hx.type)
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/temp '+hx.type+'.png')
mpl.savefig('Plots/temp '+hx.type+'.pdf')

mpl.figure()
mpl.plot(hx.tem.Ntype.T, hx.tem.Ntype.q, label=hx.tem.Ntype.material)
mpl.plot(hx.tem.Ptype.T, hx.tem.Ptype.q, label=hx.tem.Ptype.material)
mpl.xlabel('Temperature (K)')
mpl.ylabel(r'Heat Flux ($\frac{W}{m^2K}$)')
mpl.title('Heat Flux v Temperature')
mpl.grid()
mpl.legend()

mpl.show()

