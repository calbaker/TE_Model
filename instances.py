# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

# User Defined Modules
# In this directory
import HX
# In python directory
import properties as prop

print "Beginning execution..."

# Instantiation
HX1 = HX.HX()
HX1.exh.porous = 'no' 
HX1.exh.T_inlet = 600.
HX1.exh.P = 100.
HX1.cool.T_inlet = 300.
HX1.solve_HX()

HX0 = HX.HX()
HX0.exh.porous = 'no' 
HX0.exh.T_inlet = 600.
HX0.exh.P = 100.
HX0.cool.T_inlet = 300.
HX0.solve_HX()

print "Plotting..."

# Plotting
# Plot configuration
FONTSIZE = 16
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

mpl.figure()

mpl.plot(HX1.x_dim*100, HX1.exh.T_nodes, label='Exhaust (K)')
mpl.plot(HX1.x_dim*100, HX1.cool.T_nodes, label='Coolant (K)')
mpl.plot(HX1.x_dim*100, HX1.TEM.T_hot, label='TE Hot (K)')
mpl.plot(HX1.x_dim*100, HX1.TEM.T_cool, label='TE Cold (K)')

mpl.xlabel('Distance Along HX (cm)')
mpl.ylabel('Temperature (K)')
mpl.title('Temperature v. Distance in HX')
mpl.legend(loc='best')
mpl.grid()
mpl.savefig('Plots/temperature distribution.pdf')
mpl.savefig('Plots/temperature distribution.png')

mpl.figure()

mpl.plot(HX1.x_dim*100, HX1.TEM.I_nodes)

mpl.xlabel('Distance Along HX (cm)')
mpl.ylabel('Current (A)')
mpl.title('Current v. Distance in HX')
mpl.grid()
mpl.savefig('Plots/current distribution.pdf')
mpl.savefig('Plots/current distribution.png')

height = sp.arange(0.5,2.,0.25)*1.e-2
power_net = sp.empty(0)
Wdot_pumping_cool = sp.empty(0)
Wdot_pumping_exh = sp.empty(0)
Qdot = sp.empty(0)
effectiveness = sp.empty(0)
eta_1st = sp.empty(0)
eta_2nd = sp.empty(0)
power_TE = sp.empty(0)

for i in sp.arange(sp.size(height)):
    HX0.exh.height = height[i]
    HX0.solve_HX()
    HX0.solve_HX()
    power_net = sp.append(power_net,HX0.power_net)
    power_TE = sp.append(power_TE,HX0.TEM.power)
    Wdot_pumping_exh = sp.append(Wdot_pumping_exh,HX0.exh.Wdot_pumping)
    Wdot_pumping_cool = sp.append(Wdot_pumping_cool,HX0.cool.Wdot_pumping)
    Qdot = sp.append(Qdot,HX0.Qdot)
    effectiveness = sp.append(effectiveness,HX0.effectiveness)
    eta_2nd = sp.append(eta_2nd,HX0.eta_2nd)
    eta_1st = sp.append(eta_1st,HX0.eta_1st)

mpl.figure()

mpl.plot(height*1e2,power_net,'o',label='Net Power')
mpl.plot(height*1e2,power_TE,'o',label='TE Power')
mpl.plot(height*1e2,Wdot_pumping_exh,'o',label='Exhaust Pumping Power')
mpl.plot(height*1e2,Wdot_pumping_cool,'o',label='Coolant Pumping Power')
mpl.plot(height*1e2,Qdot,'o',label='Heat Transfer')

mpl.title('Power v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
mpl.xlabel('Duct Height (cm)')
mpl.ylabel('(kW)')
mpl.legend()
mpl.grid()
mpl.savefig('Plots/power.pdf')
mpl.savefig('Plots/power.png')

mpl.figure()

mpl.plot(height*1e2,effectiveness,'o',label='Effectiveness')
mpl.plot(height*1e2,eta_1st,'o',label='1st Law Efficiency')
mpl.plot(height*1e2,eta_2nd,'o',label='modified 2nd Law Efficiency')

mpl.title('Effectiveness v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
mpl.xlabel('Duct Height (cm)')
mpl.ylabel('HX Effectiveness')
mpl.legend()
mpl.grid()
mpl.savefig('Plots/effectiveness.pdf')
mpl.savefig('Plots/effectiveness.png')

mpl.show()

print "Program finished."
