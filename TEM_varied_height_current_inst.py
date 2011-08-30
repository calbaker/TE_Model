# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import tem
reload(tem)

I = .22 # current (amps)
area = (0.002)**2

T_h_goal = 650.
T_c = 310.

TEM = tem.TEModule()
TEM.I = I
TEM.Ntype.area = area
TEM.Ntype.material = 'MgSi'
TEM.Ntype.set_prop_fit()
TEM.Ptype.area = area * 2.
TEM.Ptype.material = 'HMS'
TEM.Ptype.set_prop_fit()

TEM.T_h_goal = T_h_goal
TEM.T_c = T_c
TEM.solve_tem()

TEM.lengths = sp.linspace(0., 10., 30) * 1e-3
TEM.currents = sp.linspace(0.1, 30., 30) * TEM.I
TEM.etas = sp.zeros([sp.size(TEM.lengths), sp.size(TEM.currents)])
for i in sp.arange(sp.size(TEM.lengths)):
    print "length = ", TEM.length * 1.e3
    for j in sp.arange(sp.size(TEM.currents)):
        TEM.length = TEM.lengths[i]
        TEM.I = TEM.currents[j]
        TEM.solve_tem()
        TEM.etas[i,j] = TEM.eta

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
length, currents = sp.meshgrid(TEM.lengths, TEM.currents)
FCS = plt.contourf(length * 1000., currents, TEM.etas.T *
                   100., LEVELS)  
CB = plt.colorbar(FCS, orientation='horizontal', format='%0.1f')
plt.xlabel('TE Leg Length (mm)')
plt.ylabel('Current (A)')
# plt.title(r'Efficiency v. Leg Length and Current $T_h$=' +
#           str(TEM.T_h_goal) + ' K')
fig.savefig('Plots/eta v length and current tem ' + str(TEM.T_h_goal) +
            ' K.pdf')
fig.savefig('Plots/eta v length and current tem ' + str(TEM.T_h_goal) +
            ' K.png')

plt.show()
