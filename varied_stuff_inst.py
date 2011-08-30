# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import hx
import tem

print "Beginning execution..."

area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.tem.I = 2.
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'parallel'
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 5.e-3
hx.exh.fins = 10

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.solve_hx()

currents = sp.linspace(2., 6., 25)
area_voids = sp.linspace(15., 75., 25) * area

hx.power_net_array = sp.zeros([sp.size(currents),
                               sp.size(area_voids)]) 

for i in sp.arange(sp.size(currents)):
    for j in sp.arange(sp.size(area_voids)):
        hx.tem.I = currents[i]
        hx.tem.area_void = area_voids[j]
        hx.solve_hx()
        hx.power_net_array[i,j] = hx.power_net

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

fig = plt.figure()
currents2d, area_voids2d = sp.meshgrid(currents, area_voids *
                                       (1.e3)**2)
LEVELS = sp.linspace(0., 1., 10)
FCS = plt.contourf(currents2d, area_voids2d, hx.power_net_array.T, LEVELS)
CB = plt.colorbar(FCS, orientation='horizontal', format='%0.1f')
plt.xlabel('Current (A)')
plt.ylabel(r'Void Area ($mm^2$)')
plt.title('Net Power v. Current and Void Area')
fig.savefig('Plots/power v current and void hi res.pdf')
fig.savefig('Plots/power v current and void hi res.png')

plt.show()
