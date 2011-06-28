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
Ntype.material = 'MgSi'
Ntype.set_prop_fit()
Ntype.area = (0.01)**2
Ntype.T_h_goal = 750.
Ntype.T_c = 400.
Ntype.I = 34.

Ptype = tem.Leg()
Ptype.material = 'HMS'
Ptype.set_prop_fit()
Ptype.area = (0.01)**2
Ptype.T_h_goal = 750.
Ptype.T_c = 400.
Ptype.I = -34

Ntype.lengths = sp.arange(1., 15., 0.5) * 1e-3
Ntype.etas = sp.zeros(sp.size(Ntype.lengths))
for i in sp.arange(sp.size(Ntype.lengths)):
    Ntype.length = Ntype.lengths[i]
    Ntype.solve_leg()
    Ntype.etas[i] = Ntype.eta
print "n-type current density =", Ntype.J / 100.**2, "A/cm^2"

Ptype.lengths = sp.arange(1., 15., 0.5) * 1e-3
Ptype.etas = sp.zeros(sp.size(Ptype.lengths))
for i in sp.arange(sp.size(Ptype.lengths)):
    Ptype.length = Ptype.lengths[i]
    Ptype.solve_leg()
    Ptype.etas[i] = Ptype.eta
print "p-type current density =", Ptype.J / 100.**2, "A/cm^2"

# Plot configuration
FONTSIZE = 18
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5

fig1 = mpl.figure()
mpl.plot(Ntype.lengths * 1e3, Ntype.etas * 100.,
         label=Ntype.material)
mpl.plot(Ptype.lengths * 1e3, Ptype.etas * 100.,
         label=Ptype.material)
mpl.grid()
mpl.xlabel('Leg Length (mm)')
mpl.ylabel(r'$\eta$ (%)')
mpl.title('Efficiency v. Leg Length')
mpl.legend(loc='best')
fig1.subplots_adjust(bottom=0.12)
fig1.subplots_adjust(top=0.88)
mpl.savefig('Plots/eta v length.pdf')
mpl.savefig('Plots/eta v length.png')

# fig2 = mpl.figure()
# mpl.plot(Ptype.lengths * 1e3, Ptype.etas * 100.,
#          label='P type')
# mpl.grid()
# mpl.xlabel('Leg Length (mm)')
# mpl.ylabel(r'$\eta$ (%)')
# mpl.title('Efficiency v. Leg Length\n' + Ptype.material)
# mpl.legend(loc='best')
# fig2.subplots_adjust(bottom=0.12)
# fig2.subplots_adjust(top=0.88)
# mpl.savefig('Plots/eta v length ' + Ptype.material + '.pdf')
# mpl.savefig('Plots/eta v length ' + Ptype.material + '.png')

mpl.show()
