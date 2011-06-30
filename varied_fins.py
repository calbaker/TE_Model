# Chad Baker
# Created on 2011 Feb 10

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
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 5.e-3
hx.exh.fins = 10

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.solve_hx()

hx.exh.fin_array = sp.arange(10, 32, 2)
# array for varied exhaust duct height (m)
array_size = sp.size(hx.exh.fin_array)
hx.power_net_array = sp.zeros(array_size)
hx.Wdot_pumping_array = sp.zeros(array_size)
hx.Qdot_array = sp.zeros(array_size)
hx.tem.power_array = sp.zeros(array_size)
hx.exh.fin.spacings = sp.zeros(sp.size(hx.exh.fin_array)) 

for i in sp.arange(sp.size(hx.exh.fin_array)):
    hx.exh.fins = hx.exh.fin_array[i]
    print "\nSolving for", hx.exh.fins, "fins\n"
    hx.solve_hx()
    hx.power_net_array[i] = hx.power_net
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping
    hx.Qdot_array[i] = hx.Qdot
    hx.tem.power_array[i] = hx.tem.power
    hx.exh.fin.spacings[i] = hx.exh.fin.spacing

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
plt.plot(hx.exh.fin.spacings * 100., hx.Qdot_array / 10.,
         label=r'$\dot{Q}/10$') 
plt.plot(hx.exh.fin.spacings * 100., hx.tem.power_array,
         label='TEM')
plt.plot(hx.exh.fin.spacings * 100., hx.power_net_array,
         label='$P_{net}$')  
plt.plot(hx.exh.fin.spacings * 100., hx.Wdot_pumping_array,
         label='Pumping')
plt.grid()
plt.xlabel('Fin Spacing (cm)')
plt.ylabel('Power (kW)')
plt.ylim(0,2.5)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig('Plots/power v fin spacing.pdf')
plt.savefig('Plots/power v fin spacing.png')

plt.figure()
plt.plot(hx.exh.fin_array, hx.Qdot_array / 10., label=r'$\dot{Q}/10$') 
plt.plot(hx.exh.fin_array, hx.tem.power_array,  label='TEM')
plt.plot(hx.exh.fin_array, hx.power_net_array,
         label='$P_{net}$')  
plt.plot(hx.exh.fin_array, hx.Wdot_pumping_array,
         label='Pumping')
plt.grid()
plt.xlabel('Fins')
plt.ylabel('Power (kW)')
plt.ylim(0,2.5)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.title('Power v. Fin Spacing')
plt.legend(loc='best')
plt.savefig('Plots/power v fins.pdf')
plt.savefig('Plots/power v fins.png')

plt.show()
