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

HX1 = hx.HX()
HX1.type = 'parallel'
HX1.tem = tem.TECarnot()
HX1.exh.T_inlet = 700.
HX1.exh.P = 100.
HX1.cool.T_inlet = 300.
#HX1.tem.set_ZT()

HX1.exh.height_array = sp.arange(1., 5., 0.05) * 1.e-2
# array for varied exhaust duct height (m)
array_size = sp.size(HX1.exh.height_array)
HX1.power_net_array = sp.zeros(array_size)
HX1.Wdot_pumping_array = sp.zeros(array_size)
HX1.Qdot_array = sp.zeros(array_size)
HX1.tem.power_array = sp.zeros(array_size)

for i in sp.arange(sp.size(HX1.exh.height_array)):
    HX1.exh.height = HX1.exh.height_array[i]
    HX1.solve_hx()
    HX1.power_net_array[i] = HX1.power_net
    HX1.Wdot_pumping_array[i] = HX1.Wdot_pumping
    HX1.Qdot_array[i] = HX1.Qdot
    HX1.tem.power_array[i] = HX1.tem.power

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
mpl.plot(HX1.exh.height_array * 100., HX1.power_net_array,
         label='Net')  
mpl.plot(HX1.exh.height_array * 100., HX1.Wdot_pumping_array,
         label='Pumping')
mpl.plot(HX1.exh.height_array * 100., HX1.tem.power_array,
         label='TEM')
mpl.plot(HX1.exh.height_array * 100., HX1.Qdot_array,
         label=r'$\dot{Q}$') 
mpl.grid()
mpl.xlabel('Exhaust Duct Height (cm)')
mpl.ylabel('Power (kW)')
mpl.title('Power v. Exhaust Duct Height')
mpl.legend()
mpl.savefig('Plots/power v height.pdf')
mpl.savefig('Plots/power v height.png')

mpl.show()
