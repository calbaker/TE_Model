# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl

# User Defined Modules
# In this directory
import HX
reload(HX)

print "Beginning execution..."

HX1 = HX.HX()
HX1.exh.porous = 'no'
HX1.type = 'parallel'
HX1.exh.T_inlet = 600.
HX1.exh.P = 100.
HX1.cool.T_inlet = 300.
HX1.solve_HX()

print "\nProgram finished."
print "\nPlotting..."

x = sp.arange(HX1.nodes) * HX1.node_length * 100

mpl.figure()
mpl.plot(x, HX1.cool.T_nodes,
         label='Coolant')
mpl.plot(x, HX1.TEM.T_cool,
         label='TEM Cold Side')
mpl.plot(x, HX1.TEM.T_hot,
         label='TEM Hot Side')
mpl.plot(x, HX1.exh.T_nodes,
         label='Exhaust')

mpl.xlabel('Distance Along HX (m)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance Along HX')
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/flow temp.png')
mpl.savefig('Plots/flow temp.pdf')

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

DUDh_exh = HX1.exh.h**-2 * HX1.U**-2
DUDh_plate = HX1.plate.h**-2 * HX1.U**-2 
