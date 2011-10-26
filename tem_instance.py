# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import tem
reload(tem)

t0 = time.clock()

length = 1. * 0.001
current = 3.5
area = (0.002)**2
area_ratio = 0.69 # n-type area per p-type area, consistent with
                  # Sherman.  

tem = tem.TEModule()
tem.I = current
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 500.
tem.T_c = 300.
tem.Ptype.node = 0
tem.Ntype.node = 0
tem.Ntype.area = area
tem.Ptype.area = tem.Ntype.area * area_ratio
tem.length = length
tem.area_void = 0.
tem.method = 'analytical'
tem.set_constants()
tem.Ptype.set_prop_fit()
tem.Ntype.set_prop_fit()
tem.solve_tem()

T_props = np.linspace(300,450.,100)
T_h_goal = np.linspace(300,600.,100)
A_opt = np.empty(np.size(T_props))
xi_opt = np.empty(np.size(T_props))
eta_max = np.empty(np.size(T_props))

for i in range(np.size(T_props)):
    tem.T_props = T_props[i]
    tem.set_A_opt()
    A_opt[i] = tem.A_opt

for i in range(np.size(T_h_goal)):
    tem.T_h_goal = T_h_goal[i]
    tem.set_xi()
    xi_opt[i] = tem.xi
    tem.set_eta_max()
    eta_max[i] = tem.eta_max

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
plt.savefig('Plots/area_ratio_v_T.pdf')
plt.savefig('Plots/area_ratio_v_T.png')

fig2 = plt.figure()
plt.plot(T_h_goal, xi_opt, '-k')
plt.xlabel('TE Hot Side Temperature (K)')
plt.ylabel(r'Optimal $\xi=IL$')
plt.grid()
plt.subplots_adjust(left=0.15)
plt.savefig('Plots/xi_v_T.pdf')
plt.savefig('Plots/xi_v_T.png')

fig3 = plt.figure()
plt.plot(T_h_goal, eta_max*100., '-k')
plt.xlabel('TE Hot Side Temperature (K)')
plt.ylabel(r'$\eta_{max}$(%)')
plt.grid()
plt.subplots_adjust(left=0.15)
plt.savefig('Plots/eta_max_v_T.pdf')
plt.savefig('Plots/eta_max_v_T.png')

