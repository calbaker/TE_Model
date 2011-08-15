# Chad Baker
# Created on 2011 Feb 10
1
# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os

os.chdir('/home/chad/Documents/UT Stuff/Research/Diesel TE/TE_Model')

# User Defined Modules
# In this directory
import hx
import tem

print "Beginning execution..."

area = (0.002)**2
length = 5.e-3

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
hx.exh.enhancement = "Mancin porous"

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.solve_hx()

hx.exh.PPI_array = sp.array_size([10])
array_size = sp.size(hx.exh.PPI_array)
hx.power_net_array = sp.zeros(array_size)
hx.Wdot_pumping_array = sp.zeros(array_size)
hx.Qdot_array = sp.zeros(array_size)
hx.tem.power_array = sp.zeros(array_size)
hx.exh.porosity = .99

for i in sp.arange(array_size):
    hx.exh.PPI = hx.exh.PPI_array[i]
    hx.solve_hx()
    hx.power_net_array[i] = hx.power_net
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping
    hx.Qdot_array[i] = hx.Qdot
    hx.tem.power_array[i] = hx.tem.power
    
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
plt.plot(hx.exh.PPI_array, hx.Qdot_array / 10.,
         label=r'$\dot{Q}/10$') 
plt.plot(hx.exh.PPI_array, hx.tem.power_array,
         label='TEM')
plt.plot(hx.exh.PPI_array, hx.power_net_array,
         label='$P_{net}$')  
plt.plot(hx.exh.PPI_array, hx.Wdot_pumping_array,
         label='Pumping')
plt.grid()
plt.xlabel('Pores Per Inch (#/in)')
plt.ylabel('Power (kW)')
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.title('Power v. Pore Size')
plt.legend(loc='best')
plt.savefig('Plots/power v pore size.pdf')
plt.savefig('Plots/power v pore size.png')

plt.show()
