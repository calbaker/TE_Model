# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl

# local user modules
import tem

tem = tem.TEModule()
tem.I = 1.
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 550.
tem.T_c = 350.
tem.Ptype.node = 0
tem.Ntype.node = 0
tem.Ntype.area = (0.002)**2
tem.Ptype.area = tem.Ntype.area * 2.
tem.length = 2.e-3
tem.area_void = 0.
tem.set_constants()
tem.Ptype.set_prop_fit()
tem.Ntype.set_prop_fit()
tem.solve_tem()

# Plot configuration
FONTSIZE = 20
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

x = sp.arange(tem.Ntype.segments) * tem.Ntype.segment_length * 1.e6
# x position (micron)

fig1 = mpl.figure()
mpl.plot(x*1e-3, tem.Ntype.T, label=tem.Ntype.material)
mpl.plot(x*1e-3, tem.Ptype.T, label=tem.Ptype.material)
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
mpl.plot(tem.Ntype.T, tem.Ntype.q * 1e-3, label=tem.Ntype.material)
mpl.plot(tem.Ptype.T, tem.Ptype.q * 1e-3, label=tem.Ptype.material)
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
mpl.plot(x*1e-3, tem.Ntype.q * 1e-3, label=tem.Ntype.material)
mpl.plot(x*1e-3, tem.Ptype.q * 1e-3, label=tem.Ptype.material)
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
