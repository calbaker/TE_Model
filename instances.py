# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl

# User Defined Modules
# In this directory
import HX
reload(HX)

print "Beginning execution..."

# Instantiation
HX0 = HX.HX()
HX0.exh.porous = 'no' 
HX0.exh.T_inlet = 600.
HX0.exh.P = 100.
HX0.cool.T_inlet = 300.

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

height = sp.arange(0.5,5.0,0.25)*1.e-2
power_net = sp.empty(0)
Wdot_pumping_cool = sp.empty(0)
Wdot_pumping_exh = sp.empty(0)
Qdot = sp.empty(0)
effectiveness = sp.empty(0)
eta_1st = sp.empty(0)
eta_2nd = sp.empty(0)
power_TE = sp.empty(0)

for i in sp.arange(sp.size(height)):
 print "\niteration",i,"height =",height[i] 
 HX0.exh.height = height[i]
 HX0.solve_HX()
 print "TEM thermal resistance =",HX0.TEM.R_thermal
 power_net = sp.append(power_net,HX0.power_net)
 power_TE = sp.append(power_TE,HX0.TEM.power)
 Wdot_pumping_exh = sp.append(Wdot_pumping_exh,HX0.exh.Wdot_pumping)
 Wdot_pumping_cool = sp.append(Wdot_pumping_cool,HX0.cool.Wdot_pumping)
 Qdot = sp.append(Qdot,HX0.Qdot)
 effectiveness = sp.append(effectiveness,HX0.effectiveness)
 eta_2nd = sp.append(eta_2nd,HX0.eta_2nd)
 eta_1st = sp.append(eta_1st,HX0.eta_1st)

mpl.figure()
mpl.plot(height*1e2,power_net,'-o',label='Net')
mpl.plot(height*1e2,power_TE,'-o',label='TE')
mpl.plot(height*1e2,Wdot_pumping_exh,'-o',label='Exhaust Pumping')
mpl.plot(height*1e2,Wdot_pumping_cool,'-o',label='Coolant Pumping')
mpl.plot(height*1e2,Qdot,'-o',label='Heat')

mpl.title('Power v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
mpl.xlabel('Duct Height (cm)')
mpl.ylabel('(kW)')
mpl.legend(loc='lower right')
mpl.grid()
mpl.savefig('Plots/power.pdf')
mpl.savefig('Plots/power.png')

mpl.figure()
mpl.plot(height*1e2,effectiveness,'-o',label='$\epsilon$')
mpl.plot(height*1e2,eta_1st,'-o',label='$\eta_{1st}$')
mpl.plot(height*1e2,eta_2nd,'-o',label='$\eta_{2nd}$')

mpl.title('Effectiveness v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
mpl.xlabel('Duct Height (cm)')
mpl.ylabel('HX Effectiveness')
mpl.legend(loc='lower right')
mpl.grid()
mpl.savefig('Plots/effectiveness.pdf')
mpl.savefig('Plots/effectiveness.png')

mpl.show() # uncomment this to show the plots after running the code.  

