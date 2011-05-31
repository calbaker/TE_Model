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
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 2.5
hx.cool.T_inlet = 300.
#hx.tem.set_ZT()

hx.exh.fin_array = sp.arange(1., 6., 1.)
# array for varied exhaust duct height (m)
array_size = sp.size(hx.exh.fin_array)
hx.power_net_array = sp.zeros(array_size)
hx.Wdot_pumping_array = sp.zeros(array_size)
hx.Qdot_array = sp.zeros(array_size)
hx.tem.power_array = sp.zeros(array_size)

for i in sp.arange(sp.size(hx.exh.fin_array)):
    hx.exh.fins = hx.exh.fin_array[i]
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
mpl.plot(hx.exh.fin_array, hx.power_net_array,
         label='Net')  
mpl.plot(hx.exh.fin_array, hx.Wdot_pumping_array,
         label='Pumping')
mpl.plot(hx.exh.fin_array, hx.tem.power_array,
         label='TEM')
mpl.plot(hx.exh.fin_array, hx.Qdot_array,
         label=r'$\dot{Q}$') 
mpl.grid()
mpl.xlabel('Number of Fins')
mpl.ylabel('Power (kW)')
mpl.ylim(ymin=0)
mpl.title('Power v. Number of Fins')
mpl.legend(loc='best')
mpl.savefig('Plots/power v fins.pdf')
mpl.savefig('Plots/power v fins.png')

mpl.show()
