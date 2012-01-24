# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import te_pair
reload(te_pair)

I = .22 # current (amps)
area = (0.002)**2

T_h_goal = 650.
T_c = 310.

TE_PAIR = te_pair.TE_PAIRodule()
TE_PAIR.I = I
TE_PAIR.Ntype.area = area
TE_PAIR.Ntype.material = 'MgSi'
TE_PAIR.Ntype.set_prop_fit()
TE_PAIR.Ptype.area = area * 2.
TE_PAIR.Ptype.material = 'HMS'
TE_PAIR.Ptype.set_prop_fit()

TE_PAIR.T_h_goal = T_h_goal
TE_PAIR.T_c = T_c
TE_PAIR.solve_te_pair()

TE_PAIR.lengths = sp.linspace(0., 10., 30) * 1e-3
TE_PAIR.currents = sp.linspace(0.1, 30., 30) * TE_PAIR.I
TE_PAIR.etas = sp.zeros([sp.size(TE_PAIR.lengths), sp.size(TE_PAIR.currents)])
for i in sp.arange(sp.size(TE_PAIR.lengths)):
    print "length = ", TE_PAIR.length * 1.e3
    for j in sp.arange(sp.size(TE_PAIR.currents)):
        TE_PAIR.length = TE_PAIR.lengths[i]
        TE_PAIR.I = TE_PAIR.currents[j]
        TE_PAIR.solve_te_pair()
        TE_PAIR.etas[i,j] = TE_PAIR.eta

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

LEVELS = sp.linspace(0., 5., 15)

fig = plt.figure()
length, currents = sp.meshgrid(TE_PAIR.lengths, TE_PAIR.currents)
FCS = plt.contourf(length * 1000., currents, TE_PAIR.etas.T *
                   100., LEVELS)  
CB = plt.colorbar(FCS, orientation='horizontal', format='%0.1f')
plt.xlabel('TE Leg Length (mm)')
plt.ylabel('Current (A)')
# plt.title(r'Efficiency v. Leg Length and Current $T_h$=' +
#           str(TE_PAIR.T_h_goal) + ' K')
fig.savefig('Plots/eta v length and current te_pair ' + str(TE_PAIR.T_h_goal) +
            ' K.pdf')
fig.savefig('Plots/eta v length and current te_pair ' + str(TE_PAIR.T_h_goal) +
            ' K.png')

plt.show()
