# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import te_pair
reload(te_pair)

t0 = time.clock()

length = 1. * 0.001
current = 3.5
area = (0.002)**2
area_ratio = 0.69 # n-type area per p-type area, consistent with
                  # Sherman.  

te_pair = te_pair.TE_PAIRodule()
te_pair.I = current
te_pair.Ntype.material = 'MgSi'
te_pair.Ptype.material = 'HMS'
te_pair.T_h_goal = 500.
te_pair.T_c = 300.
te_pair.Ptype.node = 0
te_pair.Ntype.node = 0
te_pair.Ptype.area = area
te_pair.Ntype.area = te_pair.Ptype.area * area_ratio
te_pair.length = length
te_pair.area_void = 0.
te_pair.method = 'analytical'
te_pair.set_constants()
te_pair.Ptype.area = te_pair.area / (1. + area_ratio)
te_pair.Ntype.area = te_pair.area - te_pair.Ptype.area 
te_pair.Ptype.set_prop_fit()
te_pair.Ntype.set_prop_fit()
te_pair.solve_te_pair()
te_pair.T_props = 0.5 * (te_pair.T_h + te_pair.T_c)
te_pair.set_eta_max()
te_pair.set_power_max()
te_pair.set_A_opt()

res = 80
length1d = np.linspace(0.01, 2, res) * 0.001
current1d = np.linspace(0.5, 20, res+1)

length_current, current_length = np.meshgrid(length1d, current1d)
eta_length_current = np.empty([np.size(length1d), np.size(current1d)]) 
p_length_current = np.empty([np.size(length1d), np.size(current1d)])
R_load = np.empty([np.size(length1d), np.size(current1d)])
R_internal = np.empty([np.size(length1d), np.size(current1d)])

for i in range(np.size(length1d)):
    te_pair.length = length1d[i]
    for j in range(np.size(current1d)):
        te_pair.I = current1d[j]
        te_pair.set_constants()
        te_pair.solve_te_pair()
        eta_length_current[i,j] = te_pair.eta
        p_length_current[i,j] = te_pair.P
        R_load[i,j] = te_pair.R_load
        R_internal[i,j] = te_pair.R_internal

eta_length_R_load = eta_length_current.copy()
p_length_R_load = p_length_current.copy()

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

high = te_pair.eta_max * 100.
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
fig1.savefig('Plots/' + te_pair.method + '/eta_length_current.pdf')
fig1.savefig('Plots/' + te_pair.method + '/eta_length_current.png')

fig1p = plt.figure()
FCS = plt.contourf(current_length, length_current * 1000.,
                   p_length_current.T * 1000., levels=LEVELS_p)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Power (W)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("Current (A)")
fig1p.savefig('Plots/' + te_pair.method + '/p_length_current.pdf')
fig1p.savefig('Plots/' + te_pair.method + '/p_length_current.png')

fig1r = plt.figure()
FCS = plt.contourf(R_load.T, length_current * 1000.,
                   eta_length_R_load.T * 100., levels=LEVELS_eta)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel(r"R_load ($\Omega$)")
fig1r.savefig('Plots/' + te_pair.method + '/eta_length_R_load.pdf')
fig1r.savefig('Plots/' + te_pair.method + '/eta_length_R_load.png')

fig1pr = plt.figure()
FCS = plt.contourf(R_load.T, length_current * 1000.,
                   p_length_R_load.T * 1000., levels=LEVELS_p)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Power (W)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("R_load ($\Omega$)")
fig1pr.savefig('Plots/' + te_pair.method + '/p_length_R_load.pdf')
fig1pr.savefig('Plots/' + te_pair.method + '/p_length_R_load.png')

fig_R_load = plt.figure()
FCS = plt.contourf(current_length, length_current * 1000.,
                   R_load.T)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label(r'Load Resistance ($\Omega$)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel("Current (A)")
plt.savefig('Plots/' + te_pair.method + '/R_load.pdf')
plt.savefig('Plots/' + te_pair.method + '/R_load.png')

R_ratio = R_load / R_internal

fig1ropt = plt.figure()
FCS = plt.contourf(R_ratio.T, length_current * 1000.,
                   eta_length_R_load.T * 100., levels=LEVELS_eta)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Thermal Efficiency (%)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel(r"$\frac{R_{load}}{R_{internal}}$")
plt.subplots_adjust(left=0.12)
plt.subplots_adjust(right=0.78)
plt.subplots_adjust(bottom=0.14)
plt.subplots_adjust(top=0.95)
plt.savefig('Plots/' + te_pair.method + '/eta_length_R_ratio.pdf')
plt.savefig('Plots/' + te_pair.method + '/eta_length_R_ratio.png')

fig1propt = plt.figure()
FCS = plt.contourf(R_ratio.T, length_current * 1000.,
                   p_length_R_load.T * 1000., levels=LEVELS_p)
CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
CB.set_label('TE Power (W)')
plt.grid()
plt.ylabel("Leg Height (mm)")
plt.xlabel(r"$\frac{R_{load}}{R_{internal}}$")
plt.subplots_adjust(left=0.12)
plt.subplots_adjust(right=0.78)
plt.subplots_adjust(bottom=0.14)
plt.subplots_adjust(top=0.95)
plt.savefig('Plots/' + te_pair.method + '/p_length_R_ratio.pdf')
plt.savefig('Plots/' + te_pair.method + '/p_length_R_ratio.png')

# fig1ropt = plt.figure()
# FCS = plt.contourf(R_ratio.T, length_current * 1000.,
#                    eta_length_R_load.T * 100., levels=LEVELS_eta)
# CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
# CB.set_label('TE Thermal Efficiency (%)')
# plt.grid()
# plt.ylabel("Leg Height (mm)")
# plt.xlabel(r"$\frac{R_{load}}{R_{internal}}$")
# plt.subplots_adjust(left=0.12)
# plt.subplots_adjust(right=0.78)
# plt.subplots_adjust(bottom=0.14)
# plt.subplots_adjust(top=0.95)
# plt.savefig('Plots/' + te_pair.method + '/eta_length_R_ratio.pdf')
# plt.savefig('Plots/' + te_pair.method + '/eta_length_R_ratio.png')

# fig1propt = plt.figure()
# FCS = plt.contourf(R_ratio.T, length_current * 1000.,
#                    p_length_R_load.T * 1000., levels=LEVELS_p)
# CB = plt.colorbar(FCS, orientation='vertical', format="%.2f")
# CB.set_label('TE Power (W)')
# plt.grid()
# plt.ylabel("Leg Height (mm)")
# plt.xlabel(r"$\frac{R_{load}}{R_{internal}}$")
# plt.subplots_adjust(left=0.12)
# plt.subplots_adjust(right=0.78)
# plt.subplots_adjust(bottom=0.14)
# plt.subplots_adjust(top=0.95)
# plt.savefig('Plots/' + te_pair.method + '/p_length_R_ratio.pdf')
# plt.savefig('Plots/' + te_pair.method + '/p_length_R_ratio.png')

# plt.show()

