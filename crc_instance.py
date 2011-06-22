# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl

# local user modules
import tem

TEM = tem.TEModule()
TEM.I = 10.
TEM.Ntype.material = 'ideal BiTe n-type'
TEM.Ptype.material = 'ideal BiTe p-type'
TEM.T_h_goal = 650.
TEM.T_c = 400.
TEM.solve_tem()

# Plot configuration
FONTSIZE = 20
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

x = sp.arange(TEM.Ntype.segments) * TEM.Ntype.segment_length * 1.e6
# x position (micron)

fig1 = mpl.figure()
mpl.plot(x*1e-3, TEM.Ntype.T, label=TEM.Ntype.material)
mpl.plot(x*1e-3, TEM.Ptype.T, label=TEM.Ptype.material)
mpl.title('TEM Temperature v Position')
mpl.ylabel('Temperature (K)')
mpl.xlabel('Position (mm)')
mpl.grid()
fig1.subplots_adjust(bottom=0.12)
fig1.subplots_adjust(left=0.18)
mpl.legend(loc='best')
mpl.savefig('Plots/TEM temp v position.pdf')
mpl.savefig('Plots/TEM temp v position.png')

fig2 = mpl.figure()
mpl.plot(TEM.Ntype.T, TEM.Ntype.q * 1e-3, label=TEM.Ntype.material)
mpl.plot(TEM.Ptype.T, TEM.Ptype.q * 1e-3, label=TEM.Ptype.material)
mpl.grid()
mpl.xlabel('T (K)')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')
mpl.title('TEM Heat Flux v Temperature')
fig2.subplots_adjust(bottom=0.12)
fig2.subplots_adjust(left=0.22)
mpl.legend(loc='best')
mpl.savefig('Plots/TEM heat v temp.pdf')
mpl.savefig('Plots/TEM heat v temp.png')

fig3 = mpl.figure()
mpl.plot(x*1e-3, TEM.Ntype.q * 1e-3, label=TEM.Ntype.material)
mpl.plot(x*1e-3, TEM.Ptype.q * 1e-3, label=TEM.Ptype.material)
mpl.xlabel('x (mm)')
mpl.ylabel(r'q $\frac{kW}{m^2K}$')
mpl.title('TEM Heat Flux v Position')
fig3.subplots_adjust(bottom=0.12)
fig3.subplots_adjust(left=0.22)
mpl.grid()
mpl.legend(loc='best')
mpl.savefig('Plots/TEM heat v position.pdf')
mpl.savefig('Plots/TEM heat v position.png')

mpl.show()
