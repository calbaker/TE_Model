# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import numpy as np
import xlrd

# User Defined Modules
# In this directory
import hx
reload(hx)

length = 1 / 1000.
current = 4.5
area = (0.002)**2
area_ratio = 1.25 # p-type area per n-type area

hx = hx.HX()
hx.nodes = 1.  
hx.thermoelectrics_on = True
hx.width = 9.e-2
hx.length = 0.05
hx.exh.bypass = 0.
hx.exh.height = 1.e-2
Vdot_cool = 4. # coolant flow rate (GPM) 
mdot_cool = 4. / 60. * 3.8 / 1000. * hx.cool.rho  
hx.cool.mdot = mdot_cool / 60. * 3.8
hx.cool.height = 0.5e-2
hx.tem.I = current
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * area_ratio
hx.tem.area_void = 25. * area
hx.type = 'counter'
hx.exh.P = 100.
hx.cool.T_outlet = 300.
hx.exh.T_inlet = 500.
hx.set_mdot_charge()

hx.solve_hx()

fill_fraction = ( (hx.tem.Ptype.area + hx.tem.Ntype.area) /
hx.tem.area_void ) 

length1d = np.linspace(0.01, 3, 25) / 1000.
current1d = np.linspace(0.01, 8, 25)
fill_fraction1d = np.linspace(0.5, 3, 25)

length_current, current_length = np.meshgrid(length1d, current1d)
current_fill, fill_current = np.meshgrid(current1d, fill_fraction1d)
length_fill, fill_length = np.meshgrid(length1d, fill_fraction1d)

P_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
P_current_fill = np.empty([np.size(current1d), np.size(fill_fraction1d)]) 
P_length_fill = np.empty([np.size(length1d), np.size(fill_fraction1d)]) 

for i in range(np.size(length1d)):
    hx.tem.length = length1d[i]
    print "\n***************\n"
    print "length =", hx.tem.length
    for j in range(np.size(current1d)):
        hx.tem.I = current1d[j]
        print "current =", hx.tem.I
        hx.tem.set_constants()
        hx.solve_hx()
        print "power =", hx.tem.power
        P_length_current[i,j] = hx.tem.power

hx.tem.length = length
hx.tem.current = current
print "finished first for loop."

for i in range(np.size(current1d)):
    hx.tem.I = current1d[i]
    for j in range(np.size(fill_fraction1d)):
        hx.tem.area_void = hx.tem.area * (1. - fill_fraction1d[j]) 
        hx.tem.Ntype.area = ( hx.tem.area * fill_fraction1d[j] / (1. +
    area_ratio) ) 
        hx.tem.Ptype.area = ( hx.tem.area - fill_fraction1d[j] -
    hx.tem.Ntype.area )
        hx.tem.set_constants()
        hx.solve_hx()
        P_current_fill[i,j] = hx.tem.power

hx.tem.current = current
hx.tem.fill_fraction = fill_fraction
hx.tem.area_void = hx.tem.area * (1. - fill_fraction1d[j])
hx.tem.Ntype.area = ( hx.tem.area * fill_fraction1d[j] / (1. + area_ratio) ) 
hx.tem.Ptype.area = ( hx.tem.area - fill_fraction1d[j] - hx.tem.Ntype.area )
print "finished second for loop."

for i in range(np.size(length1d)):
    hx.tem.length = length1d[i]
    for j in range(np.size(fill_fraction1d)):
        hx.tem.area_void = hx.tem.area * (1. - fill_fraction1d[j]) 
        hx.tem.Ntype.area = ( hx.tem.area * fill_fraction1d[j] / (1. +
    area_ratio) ) 
        hx.tem.Ptype.area = ( hx.tem.area - fill_fraction1d[j] -
    hx.tem.Ntype.area )
        hx.tem.set_constants()
        hx.solve_hx()
        P_length_fill[i,j] = hx.tem.power 

hx.tem.length = length
hx.tem.current = current
hx.tem.fill_fraction = fill_fraction
hx.tem.area_void = hx.tem.area * (1. - fill_fraction1d[j])
hx.tem.Ntype.area = ( hx.tem.area * fill_fraction1d[j] / (1. + area_ratio) ) 
hx.tem.Ptype.area = ( hx.tem.area - fill_fraction1d[j] - hx.tem.Ntype.area )
hx.tem.set_constants()
hx.solve_hx()
print "finished third for loop."
print "plotting"


# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.formatter.limits'] = -3,3

fig1 = plt.figure()
FCS = plt.contourf(length_current * 1000., current_length, P_length_current.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Current (A)")
fig1.savefig('Plots/HX Optimization/length_current.pdf')
fig1.savefig('Plots/HX Optimization/length_current.png')

fig2 = plt.figure()
FCS = plt.contourf(length_fill * 1000., fill_length, P_length_fill.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("P-type to N-type Fill Ratio")
fig2.savefig('Plots/HX Optimization/length_fill.pdf')
fig2.savefig('Plots/HX Optimization/length_fill.png')

fig3 = plt.figure()
FCS = plt.contourf(current_fill, fill_current, P_current_fill.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Current (A)")
plt.ylabel("P-type to N-type Fill Ratio")
fig3.savefig('Plots/HX Optimization/current_fill.pdf')
fig3.savefig('Plots/HX Optimization/current_fill.png')

