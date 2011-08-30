# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import hx
reload(hx)

print "Beginning execution..."

# parameters for TE legs
area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.tem.I = 5.
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 150. * area
hx.type = 'parallel'
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 5.e-3
hx.exh.fins = 22 # 22 fins seems to be best.  

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.ducts = 8.
hx.exh.height = 3.5e-2 / hx.ducts
hx.cool.height = 2.e-2 / (hx.ducts + 1.)
hx.height = ( hx.exh.height * hx.ducts + hx.cool.height * (hx.ducts +
                                                           1.) )
hx.exh.bypass = 1. - 1./hx.ducts
hx.cool.mdot = hx.cool.mdot / hx.ducts

hx.solve_hx() # solving once to initialize variables that are used

hx.power_net = hx.power_net * hx.ducts
hx.tem.power = hx.tem.power * hx.ducts
hx.Qdot = hx.Qdot * hx.ducts
hx.Wdot_pumping = hx.Wdot_pumping * hx.ducts
    
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
plt.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/temp '+hx.type+str(hx.ducts)+'.png')
plt.savefig('Plots/temp '+hx.type+str(hx.ducts)+'.pdf')

plt.show()

