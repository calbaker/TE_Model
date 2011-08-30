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

Ntype = tem.Leg()
Ntype.material = 'MgSi'
Ntype.set_prop_fit()
Ntype.T_h_goal = 750.
Ntype.T_c = 400.

Ptype = tem.Leg()
Ptype.material = 'HMS'
Ptype.set_prop_fit()
Ptype.area = (0.01)**2 # area (m^2)
Ptype.T_h_goal = 750.
Ptype.T_c = 400.

Ntype.current_density = sp.arange(0., 51., 1.) * 100.**2
Ntype.currents = Ntype.current_density * Ntype.area
Ntype.etas = sp.zeros(sp.size(Ntype.currents))
for i in sp.arange(sp.size(Ntype.currents)):
    Ntype.I = Ntype.currents[i]
    Ntype.solve_leg()
    Ntype.etas[i] = Ntype.eta

Ptype.current_density = sp.arange(0., -25.5, -0.5) * 100.**2
Ptype.currents = Ptype.current_density * Ptype.area
Ptype.etas = sp.zeros(sp.size(Ptype.currents))
for i in sp.arange(sp.size(Ptype.currents)):
    Ptype.I = Ptype.currents[i]
    Ptype.solve_leg()
    Ptype.etas[i] = Ptype.eta

# Plot configuration
FONTSIZE = 12
FIGSIZE = (5.5, 3.5)
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['figure.figsize'] = FIGSIZE

FIGDIM1 = ([0.10, 0.15, 0.38, 0.8])
FIGDIM2 = ([0.58, 0.15, 0.38, 0.8])

fig = plt.figure()
ax1 = fig.add_axes(FIGDIM1)
ax1.plot(Ntype.current_density / 100.**2, Ntype.etas * 100.,
                  label=r'$Mg_2Si_{0.5}Sn_{0.5}$', color='b') 
ax1.set_xlabel(r'Current Density (A/$cm^2$)')
ax1.set_ylabel(r'$\eta$')
ax1.set_ylim(0,6.5)
ax1.legend(loc='lower center')
ax1.grid()

ax2 = fig.add_axes(FIGDIM2)
ax2.plot(Ptype.current_density / 100.**2, Ptype.etas * 100.,
         label=Ptype.material, color='r') 
ax2.set_yticklabels('')
ax2.set_ylim(0,6.5)
ax2.set_xlabel(r'Current Density (A/$cm^2$)')
ax2.legend(loc='lower center')
ax2.grid()

fig.savefig('Plots/eta v current.png')
fig.savefig('Plots/eta v current.pdf')

plt.show()
