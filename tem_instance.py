# distribution modules
import scipy as sp

# local user modules
import tem

leg = tem.Leg()
leg.material = 'HMS'
leg.solve_leg()

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

for i in sp.arange(4,sp.size(leg.q_c)):
    mpl.plot(sp.absolute(leg.q_c[i]), leg.T_h_guess[i], 'o', label=str(i))
mpl.plot(sp.absolute(leg.q_c), leg.T_h_guess, '-k')    

mpl.ylim(500,600)
mpl.xlabel(r'$q_c$')
mpl.ylabel(r'$T_h$')
mpl.legend(loc='right')
mpl.legend
mpl.grid()

mpl.show()
