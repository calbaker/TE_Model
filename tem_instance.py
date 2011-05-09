# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl

# local user modules
import tem
reload(tem)

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

q_c = sp.arange(0.1,10.,0.1) * leg.q_c[0]
T_h = sp.zeros(sp.size(q_c))
for i in sp.arange(sp.size(q_c)):
    leg.q[0] = q_c[i]
    leg.solve_leg_once()
    T_h[i] = leg.T[-1]

dTdq = sp.zeros(sp.size(leg.q_c) - 1)    

for j in sp.arange(sp.size(leg.q_c) - 1):
    dTdq[j] = (leg.T_h[j + 1] - leg.T_h[j]) / (leg.q_c[j + 1] - leg.q_c[j])

fig2 = mpl.figure()
mpl.title('TE Hot Side Temp v. Cold Side Heat')
mpl.plot(q_c*1.e-3, T_h)
mpl.xlabel(r'Cold Side $q^{\prime\prime}$ $\left[\frac{kW}{m^2 K}\right]$')
mpl.ylabel('Hot Side Temperature (K)')
mpl.grid()

mpl.show()
