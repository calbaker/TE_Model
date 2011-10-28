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
tem.T_props = 0.5 * (tem.T_h + tem.T_c)
tem.set_eta_max()
tem.set_power_max()
tem.set_A_opt()

res = 80
length1d = np.linspace(0.01, 2, res) * 0.001
current1d = np.linspace(0.01, 10, res+1)

length_current, current_length = np.meshgrid(length1d, current1d)
eta_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
p_length_current = np.empty([np.size(length1d), np.size(current1d)])
R_load = np.empty([np.size(length1d), np.size(current1d)])

for i in range(np.size(length1d)):
    tem.length = length1d[i]
    for j in range(np.size(current1d)):
        tem.I = current1d[j]
        tem.set_constants()
        tem.solve_tem()
        eta_length_current[i,j] = tem.eta
        p_length_current[i,j] = tem.P
        R_load[i,j] = tem.R_load

eta_length_R_load = eta_length_current[:,::-1]
p_length_R_load = p_length_current[:,::-1]

print "elapsed time:", time.clock() - t0

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

high = tem.eta_max * 100.
dummy = ( high - np.logspace(np.log10(high), -1, 10) )
LEVELS_eta = np.empty(np.size(dummy)+1)
LEVELS_eta[-1] = high
LEVELS_eta[0:-1] = dummy

high = p_length_current.max() * 1000.
# high = 1.6
dummy = ( high - np.logspace(np.log10(high), -1, 10) )
LEVELS_p = np.empty(np.size(dummy)+1)
LEVELS_p[-1] = high
LEVELS_p[0:-1] = dummy
LEVELS_p = np.linspace(0,high,15) 

fig1 = plt.figure()
FCS = plt.contourf(current_length, length_current * 1000.,
                   eta_length_current.T * 100., levels=LEVELS_eta)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("Current (A)")
fig1.savefig('Plots/' + tem.method + '/eta_length_current.pdf')
fig1.savefig('Plots/' + tem.method + '/eta_length_current.png')

fig1p = plt.figure()
FCS = plt.contourf(current_length, length_current * 1000.,
                   p_length_current.T * 1000., levels=LEVELS_p)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Power (W)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("Current (A)")
fig1p.savefig('Plots/' + tem.method + '/p_length_current.pdf')
fig1p.savefig('Plots/' + tem.method + '/p_length_current.png')

fig1r = plt.figure()
FCS = plt.contourf(R_load.T, length_current * 1000.,
                   eta_length_R_load.T * 100., levels=LEVELS_eta)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel(r"R_load ($\Omega$)")
fig1r.savefig('Plots/' + tem.method + '/eta_length_R_load.pdf')
fig1r.savefig('Plots/' + tem.method + '/eta_length_R_load.png')

fig1pr = plt.figure()
FCS = plt.contourf(R_load.T, length_current * 1000.,
                   p_length_R_load.T * 1000., levels=LEVELS_p)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Power (W)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("R_load ($\Omega$)")
fig1pr.savefig('Plots/' + tem.method + '/p_length_R_load.pdf')
fig1pr.savefig('Plots/' + tem.method + '/p_length_R_load.png')

# plt.show()

