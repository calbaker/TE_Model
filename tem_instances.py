# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import tem
reload(tem)

t0 = time.clock()

length = 1. * 0.001
current = 3.5
area = (0.002)**2
area_ratio = 0.69 # n-type area per p-type area, consistent with
                  # Sherman.  

tem = tem.TEModule()
tem.I = current
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 500.
tem.T_c = 300.
tem.Ptype.node = 0
tem.Ntype.node = 0
tem.Ptype.area = area
tem.Ntype.area = tem.Ptype.area * area_ratio
tem.length = length
tem.area_void = 0.
tem.method = 'analytical'
tem.set_constants()
tem.Ptype.area = tem.area / (1. + area_ratio)
tem.Ntype.area = tem.area - tem.Ptype.area 
tem.Ptype.set_prop_fit()
tem.Ntype.set_prop_fit()
tem.solve_tem()
tem.set_eta_max()
tem.set_A_opt()

length1d = np.linspace(0.01, 3, 95) * 0.001
current1d = np.linspace(0.01, 10, 96)
area_ratio1d = np.linspace(0.1, 2, 97)

length_current, current_length = np.meshgrid(length1d, current1d)
current_area, area_current = np.meshgrid(current1d, area_ratio1d)
length_area, area_length = np.meshgrid(length1d, area_ratio1d)

eta_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
eta_current_area = np.empty([np.size(current1d), np.size(area_ratio1d)]) 
eta_length_area = np.empty([np.size(length1d), np.size(area_ratio1d)]) 

a, b, c = tem.set_xi()
L_opt = tem.xi / current1d * 1000.

for i in range(np.size(length1d)):
    tem.length = length1d[i]
    for j in range(np.size(current1d)):
        tem.I = current1d[j]
        tem.set_constants()
        tem.solve_tem()
        eta_length_current[i,j] = tem.eta

tem.length = length
tem.I = current
print "finished first for loop."

for i in range(np.size(current1d)):
    tem.I = current1d[i]
    for j in range(np.size(area_ratio1d)):
        tem.Ptype.area = tem.area / (1. + area_ratio1d[j])
        tem.Ntype.area = tem.area - tem.Ptype.area 
        tem.set_constants()
        tem.solve_tem()
        eta_current_area[i,j] = tem.eta

tem.length = length
tem.I = current
tem.Ptype.area = tem.area / (1. + area_ratio)
tem.Ntype.area = tem.area - tem.Ptype.area 
print "finished second for loop."

for i in range(np.size(length1d)):
    tem.length = length1d[i]
    for j in range(np.size(area_ratio1d)):
        tem.Ptype.area = tem.area / (1. + area_ratio1d[j])
        tem.Ntype.area = tem.area - tem.Ptype.area 
        tem.set_constants()
        tem.solve_tem()
        eta_length_area[i,j] = tem.eta

tem.length = length
tem.I = current
tem.Ptype.area = tem.area / (1. + area_ratio)
tem.Ntype.area = tem.area - tem.Ptype.area 
print "finished third for loop."

print "elapsed time:", time.clock() - t0

print "plotting"

plt.close('all')

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3,3

LEVELS1 = ( tem.eta_max * 105. - np.logspace(np.log10(tem.eta_max *
                                                      100), -1, 10) )
fig1 = plt.figure()
FCS = plt.contourf(current_length, length_current * 1000.,
                   eta_length_current.T * 100., levels = LEVELS1)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.plot(current1d, L_opt, '-c',label=r'Optimal $\xi$')
plt.legend(loc='upper right')
plt.ylim(ymax=length1d.max()*1000.)
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("Current (A)")
fig1.savefig('Plots/TE Optimization/length_current.pdf')
fig1.savefig('Plots/TE Optimization/length_current.png')

LEVELS2 = LEVELS1
fig2 = plt.figure()
FCS = plt.contourf(area_length, length_area * 1000., 
                   eta_length_area.T * 100., levels=LEVELS2)   
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("P-type to N-type Area Ratio")
fig2.savefig('Plots/TE Optimization/length_area.pdf')
fig2.savefig('Plots/TE Optimization/length_area.png')

LEVELS3 = LEVELS1
fig3 = plt.figure()
FCS = plt.contourf(area_current, current_area, eta_current_area.T * 100.,
                   levels=LEVELS3) 
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Current (A)")
plt.xlabel("P-type to N-type Area Ratio")
fig3.savefig('Plots/TE Optimization/current_area.pdf')
fig3.savefig('Plots/TE Optimization/current_area.png')

plt.show()

