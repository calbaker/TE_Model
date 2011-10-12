# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import tem

t0 = time.clock()

length = 0.002
current = 1.
area = (0.002)**2
area_ratio = 2 # p-type area per n-type area

tem = tem.TEModule()
tem.I = current
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 550.
tem.T_c = 350.
tem.Ptype.node = 0
tem.Ntype.node = 0
tem.Ntype.area = area
tem.Ptype.area = tem.Ntype.area * area_ratio
tem.length = length
tem.area_void = 0.
tem.set_constants()
tem.Ptype.set_prop_fit()
tem.Ntype.set_prop_fit()
tem.solve_tem()

length1d = np.linspace(0.5, 5, 25) / 1000.
current1d = np.linspace(0.1, 5, 25)
area_ratio1d = np.linspace(0.5, 5, 25)

length_current, current_length = np.meshgrid(length1d, current1d)
current_area, area_current = np.meshgrid(current1d, area_ratio1d)
length_area, area_length = np.meshgrid(length1d, area_ratio1d)

P_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
P_current_area = np.empty([np.size(current1d), np.size(area_ratio1d)]) 
P_length_area = np.empty([np.size(length1d), np.size(area_ratio1d)]) 

for i in range(np.size(length1d)):
    tem.length = length1d[i]
    for j in range(np.size(current1d)):
        tem.I = current1d[j]
        tem.set_constants()
        tem.solve_tem()
        P_length_current[i,j] = tem.P

tem.length = length
tem.current = current
print "finished first for loop."

for i in range(np.size(current1d)):
    tem.I = current1d[i]
    for j in range(np.size(area_ratio1d)):
        tem.Ntype.area = tem.area / (1. + area_ratio1d[j])
        tem.Ptype.area = tem.area - tem.Ntype.area 
        tem.set_constants()
        tem.solve_tem()
        P_current_area[i,j] = tem.P

tem.current = current
tem.area_ratio = area_ratio
tem.Ntype.area = tem.area / (1. + area_ratio)
tem.Ptype.area = tem.area - tem.Ntype.area 
print "finished second for loop."

for i in range(np.size(length1d)):
    tem.length = length1d[i]
    for j in range(np.size(area_ratio1d)):
        tem.Ntype.area = tem.area / (1. + area_ratio1d[j])
        tem.Ptype.area = tem.area - tem.Ntype.area 
        tem.set_constants()
        tem.solve_tem()
        P_length_area[i,j] = tem.P

tem.length = length
tem.current = current
tem.set_constants()
tem.solve_tem()
print "finished third for loop."
print "plotting"

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3,3

fig1 = plt.figure()
FCS = plt.contourf(length_current * 1000., current_length, P_length_current.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("Current (A)")
fig1.savefig('Plots/TE Optimization/length_current.pdf')
fig1.savefig('Plots/TE Optimization/length_current.png')

fig2 = plt.figure()
FCS = plt.contourf(length_area * 1000., area_length, P_length_area.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Leg Height (mm)")
plt.ylabel("P-type to N-type Area Ratio")
fig2.savefig('Plots/TE Optimization/length_area.pdf')
fig2.savefig('Plots/TE Optimization/length_area.png')

fig3 = plt.figure()
FCS = plt.contourf(current_area, area_current, P_current_area.T) 
CB = plt.colorbar(FCS, orientation='vertical')
plt.grid()
plt.xlabel("Current (A)")
plt.ylabel("P-type to N-type Area Ratio")
fig3.savefig('Plots/TE Optimization/current_area.pdf')
fig3.savefig('Plots/TE Optimization/current_area.png')

print "elapsed time:", time.clock()

plt.show()

