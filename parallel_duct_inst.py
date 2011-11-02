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

# parameters for TE legs
area = (0.002)**2
length = 1.e-3
current = 5. # this is really close to max for these params
area_ratio = 0.69
fill_fraction = 1. / 75. # this is still about right so fill_fraction
                         # may be independent of current.  

hx_ducts0 = hx.HX()
hx_ducts0.width = 30.e-2
# hx_ducts0.exh.bypass = 0.
hx_ducts0.exh.height = 3.5e-2
hx_ducts0.length = 1.
hx_ducts0.tem.I = current
hx_ducts0.tem.length = length

hx_ducts0.tem.Ntype.material = 'MgSi'
hx_ducts0.tem.Ptype.material = 'HMS'

hx_ducts0.tem.Ptype.area = area                           
hx_ducts0.tem.Ntype.area = hx_ducts0.tem.Ptype.area * area_ratio
hx_ducts0.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_ducts0.tem.Ptype.area +
                            hx_ducts0.tem.Ntype.area) )  

hx_ducts0.tem.method = 'analytical'
hx_ducts0.type = 'parallel'

hx_ducts0.exh.T_inlet = 800.
hx_ducts0.exh.P = 100.
hx_ducts0.cool.T_inlet = 300.

ducts = 7

hx_ducts0.exh.height = 3.5e-2 / ducts
hx_ducts0.cool.height = 2.e-2 / (ducts + 1.)

hx_ducts0.set_mdot_charge()
hx_ducts0.exh.mdot0 = hx_ducts0.exh.mdot 

hx_ducts0.exh.mdot = hx_ducts0.exh.mdot0 / ducts
hx_ducts0.cool.mdot = hx_ducts0.cool.mdot * 2. / (ducts + 1.) 

hx_ducts0.height = ( ducts * hx_ducts0.exh.height + (ducts + 1) *
                     hx_ducts0.cool.height )  

hx_ducts0.solve_hx()
    
hx_ducts0.Qdot = hx_ducts0.Qdot * ducts
hx_ducts0.tem.power = hx_ducts0.tem.power_total * ducts
hx_ducts0.power_net = hx_ducts0.power_net * ducts
hx_ducts0.Wdot_pumping = hx_ducts0.Wdot_pumping * ducts

print "\nProgram finished."
print "Plotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

plt.figure()
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_ducts0.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/temp '+hx_ducts0.type+str(ducts)+'.png')
plt.savefig('Plots/temp '+hx_ducts0.type+str(ducts)+'.pdf')

# plt.show()

print hx_ducts0.power_net

