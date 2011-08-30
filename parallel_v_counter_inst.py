# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os


# User Defined Modules
# In this directory
import hx

print "Beginning execution..."

hx_parallel = hx.HX()
hx_parallel.tem.Ntype.material = 'ideal BiTe n-type'
hx_parallel.tem.Ptype.material = 'ideal BiTe p-type'
hx_parallel.type = 'parallel'
hx_parallel.exh.T_inlet = 800.
hx_parallel.exh.P = 100.
hx_parallel.cool.T_inlet = 300.
#hx_parallel.tem = tem.TECarnot()
hx_parallel.solve_hx()

hx_counter = hx.HX()
hx_counter.tem.Ntype.material = 'ideal BiTe n-type'
hx_counter.tem.Ptype.material = 'ideal BiTe p-type'
hx_counter.exh.porous = 'no'
hx_counter.type = 'counter'
hx_counter.exh.T_inlet = 800.
hx_counter.exh.P = 100.
hx_counter.cool.T_outlet = 306.
#hx_counter.tem = tem = tem.TECarnot()
hx_counter.solve_hx()

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
mpl.plot(hx_parallel.x_dim * 100., hx_parallel.exh.T_nodes, '-r', label='Exhaust')
mpl.plot(hx_parallel.x_dim * 100., hx_parallel.tem.T_h_nodes, '-g', label='TEM Hot Side')
mpl.plot(hx_parallel.x_dim * 100., hx_parallel.tem.T_c_nodes, '-k', label='TEM Cold Side')
mpl.plot(hx_parallel.x_dim * 100., hx_parallel.cool.T_nodes, '-b', label='Coolant')

mpl.xlabel('Distance Along HX (cm)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance, '+hx_parallel.type)
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/temp '+hx_parallel.type+'.png')
mpl.savefig('Plots/temp '+hx_parallel.type+'.pdf')

mpl.figure()
mpl.plot(hx_counter.x_dim * 100., hx_counter.exh.T_nodes, '-r', label='Exhaust')
mpl.plot(hx_counter.x_dim * 100., hx_counter.tem.T_h_nodes, '-g', label='TEM Hot Side')
mpl.plot(hx_counter.x_dim * 100., hx_counter.tem.T_c_nodes, '-k', label='TEM Cold Side')
mpl.plot(hx_counter.x_dim * 100., hx_counter.cool.T_nodes, '-b', label='Coolant')

mpl.xlabel('Distance Along HX (cm)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance, '+hx_counter.type)
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/temp '+hx_counter.type+'.png')
mpl.savefig('Plots/temp '+hx_counter.type+'.pdf')

mpl.show()

