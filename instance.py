# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

os.chdir('/home/chad/Documents/UT Stuff/Research/Diesel TE/Model')

# User Defined Modules
# In this directory
import hx
import tem

print "Beginning execution..."

HX1 = hx.HX()
HX1.type = 'parallel'
HX1.TEM = tem.TECarnot()
HX1.exh.T_inlet = 800.
HX1.exh.P = 100.
HX1.cool.T_inlet = 300.
HX1.TEM.set_ZT()
HX1.solve_hx()

# HX2 = hx.HX()
# HX2.exh.porous = 'no'
# HX2.type = 'counter'
# HX2.exh.T_inlet = 600.
# HX2.exh.P = 100.
# HX2.cool.T_outlet = 306.
# HX2.solve_hx()

print "\nProgram finished."
print "\nPlotting..."

x = sp.arange(HX1.nodes) * HX1.node_length * 100


# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

mpl.figure()
mpl.plot(x, HX1.exh.T_nodes, '-r', label='Exhaust')
mpl.plot(x, HX1.TEM.T_h_nodes, '-g', label='TEM Hot Side')
mpl.plot(x, HX1.TEM.T_c_nodes, '-k', label='TEM Cold Side')
mpl.plot(x, HX1.cool.T_nodes, '-b', label='Coolant')

mpl.xlabel('Distance Along HX (m)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance, '+HX1.type)
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/temp '+HX1.type+'.png')
mpl.savefig('Plots/temp '+HX1.type+'.pdf')

# calculates T using resistance network as a check.  
# mpl.figure()
# mpl.plot(x, HX1.cool.T_nodes,
#          label='Coolant')
# mpl.plot(x, HX1.cool.T_nodes + HX1.Qdot_nodes / ((HX1.cool.h**-1 +
#          HX1.plate.h**-1)**-1 * HX1.A), label='TEM Cold Side') 
# mpl.plot(x, HX1.cool.T_nodes + HX1.Qdot_nodes / ((HX1.cool.h**-1 +
#          HX1.plate.h**-1 + HX1.TEM.h**-1)**-1 * HX1.A), label='TEM' +
#          ' Hot Side') 
# mpl.plot(x, HX1.cool.T_nodes + HX1.Qdot_nodes / ((HX1.cool.h**-1 +
#          HX1.plate.h**-1 + HX1.TEM.h**-1 + HX1.plate.h**-1 +
#          HX1.exh.h**-1)**-1 * HX1.A), label='Exhaust') 

# mpl.xlabel('Distance Along HX (m)')
# mpl.ylabel('Temperature (K)')
# mpl.title('Temperature v. Distance Along HX')
# mpl.grid()
# mpl.legend()
# mpl.savefig('Plots/convection temp.png')
# mpl.savefig('Plots/convection temp.pdf')

mpl.show()

DUDh_exh = HX1.exh.h**-2 * HX1.U**-2 # derivative of overall heat
                                     # transfer w.r.t. exhaust heat
                                     # transfer coefficient  
DUDh_plate = HX1.plate.h**-2 * HX1.U**-2 # derivative of overall heat
                                     # transfer w.r.t. plate heat
                                     # transfer coefficient 
