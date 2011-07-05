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

print "Beginning execution..."

# parameters for TE legs
area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.tem.I = 5.
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 150. * area
hx.type = 'parallel'
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 5.e-3
hx.exh.fins = 22 # 22 fins seems to be best.  

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.solve_hx() # solving once to initialize variables that are used
              # later 

ducts = sp.linspace(1, 15, 30)
hx.Qdot_array = sp.zeros(sp.size(ducts))
hx.tem.power_array = sp.zeros(sp.size(ducts)) 
hx.power_net_array = sp.zeros(sp.size(ducts))
hx.Wdot_pumping_array = sp.zeros(sp.size(ducts)) 
hx.exh.height_array = 3.5e-2 / ducts
hx.cool.height_array = 1.e-2 / ducts
hx.exh.bypass_array = 1. - 1./ducts
hx.cool.mdot_array = hx.cool.mdot / ducts

for i in sp.arange(sp.size(ducts)):
    hx.exh.height = hx.exh.height_array[i]
    hx.cool.height = hx.cool.height_array[i]
    hx.exh.bypass = hx.exh.bypass_array[i]
    hx.cool.mdot = hx.cool.mdot_array[i]

    hx.solve_hx()
    
    hx.Qdot_array[i] = hx.Qdot * ducts[i]
    hx.tem.power_array[i] = hx.tem.power * ducts[i]
    hx.power_net_array[i] = hx.power_net * ducts[i]
    hx.Wdot_pumping_array[i] = hx.Wdot_pumping * ducts[i]
    
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

FIGDIM1 = ([0.12, 0.12, 0.75, 0.75])

XTICKS = list()

for i in sp.arange(sp.size(hx.exh.height_array)):
    if i % 3 == 0:
        XTICKS.append('{:01.1f}'.format(hx.exh.height_array[i] * 1.e2))

XTICKS[0] = ''
fig = plt.figure()
ax1 = fig.add_axes(FIGDIM1)
ax1.plot(ducts, hx.Qdot_array / 10., label=r'$\dot{Q}/10$') 
ax1.plot(ducts, hx.tem.power_array, label='TEM')
ax1.plot(ducts, hx.power_net_array, label='$P_{net}$')  
ax1.plot(ducts, hx.Wdot_pumping_array, label='Pumping')
ax1.legend(loc='best')
ax1.grid()
ax1.set_xlabel('Ducts')
ax1.set_ylabel('Power (kW)')
ax1.set_ylim(0,7)
ax1.set_ylim(ymin=0)
ax2 = plt.twiny(ax1)
plt.xticks(sp.arange(len(XTICKS)), XTICKS)
ax2.set_xlabel('Exhaust Duct Height (cm)')

fig.savefig('Plots/power v || ducts.pdf')
fig.savefig('Plots/power v || ducts.png')

plt.show()

