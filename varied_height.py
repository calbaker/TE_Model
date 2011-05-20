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

hx = hx.HX()
hx.type = 'parallel'
hx.tem = tem.TECarnot()
hx.exh.T_inlet = 700.
hx.exh.P = 100.
hx.cool.T_inlet = 300.
#hx.tem.set_ZT()

hx.exh.height_array = sp.arange(1., 5., 0.05) * 1.e-2
# array for varied exhaust duct height (m)
array_size = sp.size(hx.exh.height_array)
hx.power_net_array = sp.zeros(array_size)
hx.Wdot_pumping_array = sp.zeros(array_size)
hx.Qdot_array = sp.zeros(array_size)
hx.tem.power_array = sp.zeros(array_size)

for i in sp.arange(sp.size(hx.exh.height_array)):
    hx.exh.height = hx.exh.height_array[i]
    hx.solve_hx()
    hx.power_net_array[i] = hx.power_net
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping
    hx.Qdot_array[i] = hx.Qdot
    hx.tem.power_array[i] = hx.tem.power

print "\nProgram finished."
print "\nPlotting..."

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

mpl.figure()
mpl.plot(hx.exh.height_array * 100., hx.power_net_array,
         label='Net')  
mpl.plot(hx.exh.height_array * 100., hx.Wdot_pumping_array,
         label='Pumping')
mpl.plot(hx.exh.height_array * 100., hx.tem.power_array,
         label='TEM')
mpl.plot(hx.exh.height_array * 100., hx.Qdot_array,
         label=r'$\dot{Q}$') 
mpl.grid()
mpl.xlabel('Exhaust Duct Height (cm)')
mpl.ylabel('Power (kW)')
mpl.title('Power v. Exhaust Duct Height')
mpl.legend()
mpl.savefig('Plots/power v height.pdf')
mpl.savefig('Plots/power v height.png')

mpl.show()
