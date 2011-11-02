# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import numpy as np
import xlrd
import time

# User Defined Modules
# In this directory
import hx
reload(hx)

t0 = time.clock()

length = 1. * 0.001
current = 4.5
area = (0.002)**2
area_ratio = 0.69 # p-type area per n-type area
fill_fraction = 0.025

hx = hx.HX()
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.nodes = 2.
hx.length = 0.04
hx.tem.I = current
hx.tem.length = length

hx.tem.Ntype.material = 'MgSi'
hx.tem.Ptype.material = 'HMS'

hx.tem.Ptype.area = area                           
hx.tem.Ntype.area = hx.tem.Ptype.area * area_ratio
hx.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx.tem.Ptype.area +
                            hx.tem.Ntype.area) )  

hx.tem.method = 'analytical'
hx.type = 'parallel'

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.set_mdot_charge()
hx.solve_hx() # solving once to initialize variables that are used
              # later 

res = 100
length1d = np.linspace(0.2, 2, res) / 1000.
current1d = np.linspace(1, 15, res+1)
fill_fraction1d = np.linspace(0.005, 0.1, res+2)

length_current, current_length = np.meshgrid(length1d, current1d)
current_fill, fill_current = np.meshgrid(current1d, fill_fraction1d)
length_fill, fill_length = np.meshgrid(length1d, fill_fraction1d)

P_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
P_current_fill = np.empty([np.size(current1d), np.size(fill_fraction1d)]) 
P_length_fill = np.empty([np.size(length1d),
                          np.size(fill_fraction1d)])
print "base camp"

for i in range(np.size(length1d)):
    hx.tem.length = length1d[i]
    for j in range(np.size(current1d)):
        hx.tem.I = current1d[j]
        hx.tem.set_constants()
        hx.solve_hx()
        P_length_current[i,j] = hx.tem.power_total * 1000.

hx.tem.length = length
print "finished first for loop."

for i in range(np.size(current1d)):
    hx.tem.I = current1d[i]
    for j in range(np.size(fill_fraction1d)):
        hx.tem.area_void = ( (1. - fill_fraction1d[j]) / fill_fraction1d[j] *
                           (hx.tem.Ptype.area + hx.tem.Ntype.area) )
        hx.solve_hx()
        P_current_fill[i,j] = hx.tem.power_total * 1000.

hx.tem.I = current
print "finished second for loop."

for i in range(np.size(length1d)):
    hx.tem.length = length1d[i]
    for j in range(np.size(fill_fraction1d)):
        hx.tem.area_void = ( (1. - fill_fraction1d[j]) / fill_fraction1d[j] *
                           (hx.tem.Ptype.area + hx.tem.Ntype.area) )   
        hx.solve_hx()
        P_length_fill[i,j] = hx.tem.power_total * 1000.

print "finished third for loop."
print "summit"

elapsed = time.clock() - t0
print "Elapsed time:", elapsed

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.formatter.limits'] = -3,3

plt.close('all')

max_array = np.array([P_length_current.max(), P_current_fill.max(),
                      P_length_fill.max()]) 

high = max_array.max()
dummy = ( high - np.logspace(np.log10(high), -1, 10) )
LEVELS = np.empty(np.size(dummy)+1)
LEVELS[-1] = high
LEVELS[0:-1] = dummy
# LEVELS = np.linspace(0,high,15) 

fig1 = plt.figure()
FCS = plt.contourf(length_current * 1000., current_length,
                   P_length_current.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Power (W)')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Current (A)")
fig1.savefig('Plots/HX Optimization/length_current.pdf')
fig1.savefig('Plots/HX Optimization/length_current.png')

fig3 = plt.figure()
FCS = plt.contourf(current_fill, fill_current, P_current_fill.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Power (W)')
plt.grid()
plt.xlabel("Current (A)")
plt.ylabel("Fill Fraction")
fig3.savefig('Plots/HX Optimization/current_fill.pdf')
fig3.savefig('Plots/HX Optimization/current_fill.png')

fig2 = plt.figure()
FCS = plt.contourf(length_fill * 1000., fill_length, P_length_fill.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label('TE Power (W)')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Fill Fraction")
fig2.savefig('Plots/HX Optimization/length_fill.pdf')
fig2.savefig('Plots/HX Optimization/length_fill.png')

plt.show()
