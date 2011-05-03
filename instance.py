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

HX2 = HX.HX()
HX2.exh.porous = 'no'
HX2.type = 'counter'
HX2.exh.T_inlet = 600.
HX2.exh.P = 100.
HX2.cool.T_outlet = 306.
HX2.solve_HX()

print "\nProgram finished."
print "\nPlotting..."

x = sp.arange(HX2.nodes) * HX2.node_length * 100

mpl.figure()
mpl.plot(x, HX2.cool.T_nodes,
         label='Coolant')
mpl.plot(x, HX2.TEM.T_cool,
         label='TEM Cold Side')
mpl.plot(x, HX2.TEM.T_hot,
         label='TEM Hot Side')
mpl.plot(x, HX2.exh.T_nodes,
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
# mpl.plot(x, HX2.cool.T_nodes,
#          label='Coolant')
# mpl.plot(x, HX2.cool.T_nodes + HX2.Qdot_nodes / ((HX2.cool.h**-1 +
#          HX2.plate.h**-1)**-1 * HX2.A), label='TEM Cold Side') 
# mpl.plot(x, HX2.cool.T_nodes + HX2.Qdot_nodes / ((HX2.cool.h**-1 +
#          HX2.plate.h**-1 + HX2.TEM.h**-1)**-1 * HX2.A), label='TEM' +
#          ' Hot Side') 
# mpl.plot(x, HX2.cool.T_nodes + HX2.Qdot_nodes / ((HX2.cool.h**-1 +
#          HX2.plate.h**-1 + HX2.TEM.h**-1 + HX2.plate.h**-1 +
#          HX2.exh.h**-1)**-1 * HX2.A), label='Exhaust') 

# mpl.xlabel('Distance Along HX (m)')
# mpl.ylabel('Temperature (K)')
# mpl.title('Temperature v. Distance Along HX')
# mpl.grid()
# mpl.legend()
# mpl.savefig('Plots/convection temp.png')
# mpl.savefig('Plots/convection temp.pdf')

mpl.show()

DUDh_exh = HX2.exh.h**-2 * HX2.U**-2 # derivative of overall heat
                                     # transfer w.r.t. exhaust heat
                                     # transfer coefficient  
DUDh_plate = HX2.plate.h**-2 * HX2.U**-2 # derivative of overall heat
                                     # transfer w.r.t. plate heat
                                     # transfer coefficient 
