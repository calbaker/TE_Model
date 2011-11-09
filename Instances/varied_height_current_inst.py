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

I = 22. # current (amps)
area = (0.02)**2

T_h_goal = 650.
T_c = 310.

Ntype = tem.Leg()
Ntype.material = 'MgSi'
Ntype.set_prop_fit()
Ntype.area = area
Ntype.T_h_goal = T_h_goal
Ntype.T_c = T_c
Ntype.I = I

Ptype = tem.Leg()
Ptype.material = 'HMS'
Ptype.set_prop_fit()
Ptype.area = area * 2.
Ptype.T_h_goal = T_h_goal
Ptype.T_c = T_c
Ptype.I = -I

Ntype.lengths = sp.linspace(3., 10., 10) * 1e-3
Ntype.currents = sp.linspace(0.1, 3.5, 10) * Ntype.I
Ntype.etas = sp.zeros([sp.size(Ntype.lengths), sp.size(Ntype.currents)])
for i in sp.arange(sp.size(Ntype.lengths)):
    print "length = ", Ntype.length * 1.e3
    for j in sp.arange(sp.size(Ntype.currents)):
        Ntype.length = Ntype.lengths[i]
        Ntype.I = Ntype.currents[j]
        Ntype.solve_leg()
        Ntype.etas[i,j] = Ntype.eta
Ntype.Js = Ntype.currents / Ntype.area        

Ptype.lengths = sp.linspace(3., 10., 10) * 1e-3
Ptype.currents = sp.linspace(0.1, 2.0, 10) * Ptype.I
Ptype.etas = sp.zeros([sp.size(Ptype.lengths), sp.size(Ptype.currents)])
for i in sp.arange(sp.size(Ptype.lengths)):
    print "length = ", Ptype.length * 1.e3
    for j in sp.arange(sp.size(Ptype.currents)):
        Ptype.length = Ptype.lengths[i]
        Ptype.I = Ptype.currents[j]
        Ptype.solve_leg()
        Ptype.etas[i,j] = Ptype.eta
Ptype.Js = Ptype.currents / Ptype.area        


# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

LEVELS = sp.linspace(0., 10., 15)

fig = plt.figure()
height, Js = sp.meshgrid(Ntype.lengths, Ntype.Js)
FCS = plt.contourf(height * 1000., Js / 100.**2, Ntype.etas.T * 100., LEVELS) 
CB = plt.colorbar(FCS, orientation='horizontal', format='%0.1f')
plt.xlabel('TE Leg Height (mm)')
plt.ylabel(r'Current Density (A/$cm^2$)')
plt.title('Efficiency v. Leg Height and Current n-type')
fig.savefig('Plots/eta v height and current n' + str(Ntype.T_h_goal) +
            ' K.pdf')
fig.savefig('Plots/eta v height and current n' + str(Ntype.T_h_goal) +
            ' K.png')

fig = plt.figure()
height, Js = sp.meshgrid(Ptype.lengths, Ptype.Js)
FCS = plt.contourf(height * 1000., currents2d, Ptype.etas.T * 100., LEVELS) 
CB = plt.colorbar(FCS, orientation='horizontal', format='%0.1f')
plt.xlabel('TE Leg Height (mm)')
plt.ylabel(r'Negative Current Density (A/$cm^2$)')
plt.title('Efficiency v. Leg Height and Current p-type')
fig.savefig('Plots/eta v height and current p' + str(Ptype.T_h_goal) +
            ' K.pdf')
fig.savefig('Plots/eta v height and current p' + str(Ptype.T_h_goal) +
            ' K.png')

plt.show()
