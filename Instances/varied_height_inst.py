# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

os.chdir('/home/chad/Documents/UT Stuff/Research/Diesel TE/TE_Model')      

# User Defined Modules
# In this directory
import hx
import te_pair

area = (0.002)**2
length = 5.e-3

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.te_pair.I = 2.
hx.te_pair.length = length
hx.te_pair.Ntype.material = 'MgSi'
hx.te_pair.Ntype.area = area
hx.te_pair.Ptype.material = 'HMS'
hx.te_pair.Ptype.area = area * 2. 
hx.te_pair.area_void = 25. * area
hx.type = 'parallel'

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.
#hx.te_pair.set_ZT()

hx.exh.height_array = sp.linspace(1., 5., 10) * 1.e-2
# array for varied exhaust duct height (m)
array_size = sp.size(hx.exh.height_array)
hx.power_net_array = sp.zeros(array_size)
hx.Wdot_pumping_array = sp.zeros(array_size)
hx.Qdot_array = sp.zeros(array_size)
hx.te_pair.power_array = sp.zeros(array_size)

for i in sp.arange(sp.size(hx.exh.height_array)):
    hx.exh.height = hx.exh.height_array[i]
    hx.solve_hx()
    hx.power_net_array[i] = hx.power_net
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping
    hx.Qdot_array[i] = hx.Qdot
    hx.te_pair.power_array[i] = hx.te_pair.power

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
mpl.plot(hx.exh.height_array * 100., hx.te_pair.power_array,
         label='TE_PAIR')
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
