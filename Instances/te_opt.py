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
te_pair.T_h_goal = 633.
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
    te_pair.set_constants()
    te_pair.solve_te_pair()

    if te_pair.P > 0:
        minpar = 1. / te_pair.P
    else:
        minpar = -te_pair.P
    return minpar

T_h_goal = np.linspace(500, 750., 25)
T_props = (T_h_goal + T_h_goal[0]) / 2.

A_opt = np.zeros(T_props.size)
A_opt_theory = np.zeros(T_props.size)
I_opt = np.zeros(T_props.size)
eta_opt = np.zeros(T_props.size)
eta_opt_theory = np.zeros(T_props.size)

x0 = np.array([5., 0.7])

for i in range(T_props.size):
    te_pair.T_props = T_props[i]
    te_pair.T_h_goal = T_h_goal[i]
    xmin = fmin(get_minpar, x0)
    I_opt[i] = xmin[0]
    A_opt[i] = xmin[1]
    eta_opt[i] = te_pair.eta

    te_pair.set_eta_max()
    eta_opt_theory[i] = te_pair.eta_max

    te_pair.set_A_opt()
    A_opt_theory[i] = te_pair.A_opt

    if i%5 == 0:
        print "Solved", i, "of", T_props.size

# Plot configuration
FONTSIZE = 25
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 3.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3,3

plt.close('all')

fig1 = plt.figure()
plt.plot(T_h_goal, I_opt)
plt.xlabel(r'T$_h$ (K)')
plt.ylabel(r"I$_{opt}$ (A)")
plt.ylim(ymin=0)
plt.grid()
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.savefig("../Plots/te_opt/current.pdf")
plt.savefig("../Plots/te_opt/current.png")

fig2 = plt.figure()
plt.plot(T_h_goal, A_opt, label='numerical')
plt.plot(T_h_goal, A_opt_theory, label='theoretical')
plt.xlabel(r"T$_h$ (K)")
plt.ylabel("N/P Area Ratio")
plt.ylim(0.6, 0.8)
plt.grid()
plt.legend(loc='lower right')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.savefig("../Plots/te_opt/area.pdf")
plt.savefig("../Plots/te_opt/area.png")

fig3 = plt.figure()
plt.plot(T_h_goal, eta_opt * 100., label='numerical')
plt.plot(T_h_goal, eta_opt_theory * 100., label='theoretical')
plt.xlabel(r"T$_h$ (K)")
plt.ylabel("Efficiency (%)")
plt.ylim(0,5)
plt.grid()
plt.legend(loc='lower right')
plt.subplots_adjust(bottom=0.15)
plt.savefig("../Plots/te_opt/eta.pdf")
plt.savefig("../Plots/te_opt/eta.png")
