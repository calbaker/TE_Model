# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

os.chdir('/home/chad/Documents/UT Stuff/Research/Diesel TE/TE_Model')

# User Defined Modules
# In this directory
import tem
reload(tem)

Ntype = tem.Leg()
Ntype.material = 'ex1 n-type'
Ntype.area = (0.01)**2
Ntype.length = 1.e-3 
Ntype.T_h_goal = 750.
Ntype.T_c = 400.

Ptype = tem.Leg()
Ptype.material = 'ex1 p-type'
Ptype.area = (0.01)**2 # area (m^2)
Ptype.length = 1.e-3 
Ptype.T_h_goal = 750.
Ptype.T_c = 400.

Ntype.current_density = sp.arange(20., 51., 5.) * 100.**2
Ntype.currents = Ntype.current_density * Ntype.area
Ntype.etas = sp.zeros(sp.size(Ntype.currents))
for i in sp.arange(sp.size(Ntype.currents)):
    Ntype.I = Ntype.currents[i]
    Ntype.solve_leg()
    Ntype.etas[i] = Ntype.eta

Ptype.current_density = sp.arange(0., -2.6, -0.1) * 100.**2
Ptype.currents = Ptype.current_density * Ptype.area
Ptype.etas = sp.zeros(sp.size(Ptype.currents))
for i in sp.arange(sp.size(Ptype.currents)):
    Ptype.I = Ptype.currents[i]
    Ptype.solve_leg()
    Ptype.etas[i] = Ptype.eta

# Plot configuration
FONTSIZE = 18
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

fig1 = mpl.figure()
mpl.plot(Ntype.current_density / 100.**2, Ntype.etas * 100., label='N type')
mpl.grid()
mpl.xlabel(r'Current Density ($A/cm^2$)')
mpl.ylabel(r'$\eta$ (%)')
mpl.ylim(ymin=0)
mpl.title('Efficiency v. Current\nfor TE Legs')
mpl.legend(loc='best')
fig1.subplots_adjust(bottom=0.12)
fig1.subplots_adjust(top=0.88)
mpl.savefig('Plots/eta v current.pdf')
mpl.savefig('Plots/eta v current.png')

fig2 = mpl.figure()
mpl.plot(Ptype.current_density / 100.**2, Ptype.etas * 100., label='P type')
mpl.grid()
mpl.xlabel(r'Current Density ($A/cm^2$)')
mpl.ylabel(r'$\eta$ (%)')
mpl.ylim(ymin=0)
mpl.title('Efficiency v. Current\nfor TE Legs')
mpl.legend(loc='best')
fig2.subplots_adjust(bottom=0.12)
fig2.subplots_adjust(top=0.88)
mpl.savefig('Plots/eta v current.pdf')
mpl.savefig('Plots/eta v current.png')

mpl.show()
