# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time, os, sys
from scipy.optimize import fmin

# local user modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

t0 = time.clock()

length = 1.e-3
current = 3.5
area = (2.e-3)**2
area_ratio = 0.69 

te_pair = te_pair.TE_Pair()
te_pair.I = current
te_pair.Ntype.material = 'MgSi'
te_pair.Ptype.material = 'HMS'
te_pair.T_h_goal = 500.
te_pair.T_c = 300.
te_pair.Ptype.node = 0
te_pair.Ntype.node = 0
te_pair.Ptype.area = area
te_pair.Ntype.area = te_pair.Ptype.area * area_ratio
te_pair.length = length
te_pair.area_void = 0.
te_pair.method = 'analytical'
te_pair.set_constants()
te_pair.Ptype.set_prop_fit()
te_pair.Ntype.set_prop_fit()
te_pair.solve_te_pair()

def get_minpar(apar):
    """Function for returning parameter to be minimized."""
    te_pair.I = apar[0]
    te_pair.area_ratio = apar[1]

    te_pair.set_area()
    te_pair.solve_te_pair()

    if te_pair.P > 0:
        minpar = 1. / te_pair.P
    else:
        minpar = -te_pair.P
    return minpar

T_h_goal = np.linspace(400, 600., 100)
T_props = (T_h_goal + T_h_goal[0]) / 2.

A_opt = np.zeros(np.size(T_props))
I_opt = np.zeros(np.size(T_props))
eta_opt = np.zeros(np.size(T_props))

x0 = np.array([5., 0.7])

for i in range(np.size(T_props)):
    te_pair.T_props = T_props[i]
    te_pair.T_h_goal = T_h_goal[i]
    xmin = fmin(get_minpar, x0)
    I_opt[i] = te_pair.I
    A_opt[i] = te_pair.area_ratio
    eta_opt[i] = te_pair.eta
    if i%5 == 0:
        print "Solved", i, "of", np.size(T_props)

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3,3

plt.close('all')

fig1 = plt.figure()
plt.plot(T_h_goal, I_opt)
plt.xlabel(r'$T_h$ (K)')
plt.ylabel("I (A)")
plt.grid()

fig2 = plt.figure()
plt.plot(T_h_goal, A_opt)
plt.xlabel(r"$T_h$ (K)")
plt.ylabel("N/P Area Ratio")
plt.grid()

fig3 = plt.figure()
plt.plot(T_h_goal, eta_opt)
plt.xlabel(r"$T_h$ (K)")
plt.ylabel("Efficiency")
plt.grid()
