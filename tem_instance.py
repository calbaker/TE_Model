# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl

# local user modules
import tem

TEM = tem.TEModule()
TEM.T_h_goal = 600.
TEM.T_c = 300.
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
mpl.plot(x, TEM.Ntype.T, label='N-type leg')
mpl.plot(x, TEM.Ptype.T, label='P-type leg')
mpl.title('TEM Temperature Profile')
mpl.ylabel('Temperature (K)')
mpl.xlabel(r'Position ($\mu m$)')
mpl.grid()
mpl.savefig('Plots/TEM temperature profile.pdf')
mpl.savefig('Plots/TEM temperature profile.png')

mpl.show()
