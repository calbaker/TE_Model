# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl

# local user modules
import te_pair

TE_PAIR = te_pair.TE_PAIRodule()
TE_PAIR.Ntype.material = 'ex1 n-type'
TE_PAIR.Ptype.material = 'ex1 p-type'
TE_PAIR.Ptype.area = TE_PAIR.Ptype.area * 20.7
TE_PAIR.T_h_goal = 650.
TE_PAIR.T_c = 400.
TE_PAIR.solve_te_pair()

# Plot configuration
FONTSIZE = 20
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

x = sp.arange(TE_PAIR.Ntype.segments) * TE_PAIR.Ntype.segment_length * 1.e6
# x position (micron)

fig1 = mpl.figure()
mpl.plot(x*1e-3, TE_PAIR.Ntype.T, label=TE_PAIR.Ntype.material)
mpl.plot(x*1e-3, TE_PAIR.Ptype.T, label=TE_PAIR.Ptype.material)
mpl.title('TE_PAIR Temperature v Position')
mpl.ylabel('Temperature (K)')
mpl.xlabel('Position (mm)')
mpl.grid()
fig1.subplots_adjust(bottom=0.12)
fig1.subplots_adjust(left=0.18)
mpl.legend(loc='best')
mpl.savefig('Plots/TE_PAIR temp v position.pdf')
mpl.savefig('Plots/TE_PAIR temp v position.png')

fig2 = mpl.figure()

mpl.subplot(211)
mpl.grid()
mpl.plot(TE_PAIR.Ntype.T, TE_PAIR.Ntype.q * 1e-3, label=TE_PAIR.Ntype.material)
mpl.title('TE_PAIR Heat Flux v Temperature')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')

mpl.subplot(212)
mpl.plot(TE_PAIR.Ptype.T, TE_PAIR.Ptype.q * 1e-3, label=TE_PAIR.Ptype.material)
mpl.grid()
mpl.xlabel('T (K)')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')
fig2.subplots_adjust(bottom=0.12)
fig2.subplots_adjust(left=0.22)
mpl.legend(loc='best')
mpl.savefig('Plots/TE_PAIR heat v temp.pdf')
mpl.savefig('Plots/TE_PAIR heat v temp.png')

fig3 = mpl.figure()

mpl.subplot(211)
mpl.grid()
mpl.plot(x*1e-3, TE_PAIR.Ntype.q * 1e-3, label=TE_PAIR.Ntype.material)
mpl.title('TE_PAIR Heat Flux v Position')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')

mpl.subplot(212)
mpl.plot(x*1e-3, TE_PAIR.Ptype.q * 1e-3, label=TE_PAIR.Ptype.material)
mpl.grid()
mpl.xlabel('x (mm)')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')
fig3.subplots_adjust(bottom=0.12)
fig3.subplots_adjust(left=0.22)
mpl.legend(loc='best')
mpl.savefig('Plots/TE_PAIR heat v position.pdf')
mpl.savefig('Plots/TE_PAIR heat v position.png')

mpl.show()
