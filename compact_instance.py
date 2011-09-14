# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt

# User Defined Modules
# In this directory
import hx

print "Beginning execution..."

hx = hx.HX()
hx.width = 9.5e-2
hx.exh.bypass = 0.
hx.exh.height = 1.e-2
mdot_cool = 4. * hx.cool.rho # coolant flow rate (GPM) 
hx.cool.mdot = mdot_cool / 60. * 3.8
hx.length = 0.195
hx.tem.I = 4.5
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'parallel'
# hx.exh.enhancement = 'straight fins'
# hx.exh.fins = 15

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

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
plt.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/temp '+hx.type+'.png')
plt.savefig('Plots/temp '+hx.type+'.pdf')

plt.figure()
plt.plot(hx.tem.Ntype.T, hx.tem.Ntype.q, label=hx.tem.Ntype.material)
plt.plot(hx.tem.Ptype.T, hx.tem.Ptype.q, label=hx.tem.Ptype.material)
plt.xlabel('Temperature (K)')
plt.ylabel(r'Heat Flux ($\frac{W}{m^2K}$)')
plt.title('Heat Flux v Temperature')
plt.grid()
plt.legend()

plt.show()

