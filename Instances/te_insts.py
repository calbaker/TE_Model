# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time, os, sys

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
te_pair.method = 'numerical'
te_pair.set_constants()
te_pair.solve_te_pair()

T_h_goal = np.linspace(400, 600., 100)
T_props = (T_h_goal + T_h_goal[0]) / 2.

A_opt = np.zeros(np.size(T_props))
xi_opt = np.zeros(np.size(T_props))
eta_max = np.zeros(np.size(T_props))
abc = np.zeros([np.size(T_props),3])

for i in range(np.size(T_props)):
    te_pair.T_props = T_props[i]
    te_pair.set_A_opt()
    A_opt[i] = te_pair.A_opt

for i in range(np.size(T_h_goal)):
    te_pair.T_h_goal = T_h_goal[i]
    te_pair.set_eta_max()
    eta_max[i] = te_pair.eta_max

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
plt.plot(T_props, A_opt, '-k')
plt.xlabel('Property Evaluation Temperature (K)')
plt.ylabel(r'Optimal $\frac{A_n}{A_p}$')
plt.ylim(0,0.75)
plt.grid()
plt.subplots_adjust(left=0.15)
plt.savefig('../Plots/area_ratio_v_T.pdf')
plt.savefig('../Plots/area_ratio_v_T.png')

fig3 = plt.figure()
plt.plot(T_h_goal, eta_max*100., '-k')
plt.xlabel('TE Hot Side Temperature (K)')
plt.ylabel(r'$\eta_{max}$(%)')
plt.grid()
plt.subplots_adjust(left=0.15)
plt.savefig('../Plots/eta_max_v_T.pdf')
plt.savefig('../Plots/eta_max_v_T.png')

