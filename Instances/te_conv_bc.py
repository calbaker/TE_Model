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
te_pair.T_h_conv = 800.
te_pair.T_c_conv = 300.
te_pair.Ptype.node = 0
te_pair.Ntype.node = 0
te_pair.Ptype.area = area
te_pair.Ntype.area = te_pair.Ptype.area * area_ratio
te_pair.length = length
te_pair.area_void = 0.
te_pair.method = 'analytical'
te_pair.set_constants()

def get_minpar(apar):
    te_pair.fill_fraction = apar[0]
    te_pair.length = apar[0]
    te_pair.I = apar[0]
    te_pair.area_ratio = apar[0]
    
    te_pair.solve_te_pair()
    minpar = 1. / te_pair.P

    return minpar

U_hot = np.linspace(0.1, 2, 15)
U_cold = np.linspace(1., 10, 16)

power = np.zeros([U_hot.size,U_cold.size])
R_thermal = np.zeros([U_hot.size,U_cold.size])
fill_fraction = np.zeros([U_hot.size,U_cold.size])
length = np.zeros([U_hot.size,U_cold.size])
I = np.zeros([U_hot.size,U_cold.size])
area_ratio = np.zeros([U_hot.size,U_cold.size])

x0 = np.array([0.03, 0.001, 10., 0.7]) 

te_pair.T_h_goal = te_pair.T_h_conv
te_pair.T_c = te_pair.T_c_conv
te_pair.T_guess = np.array([te_pair.T_h_goal,te_pair.T_c])
te_pair.T_guess = te_pair.T_guess.reshape(2) 

for i in range(U_hot.size):
    te_pair.U_hot = U_hot[i]
    for j in range(U_cold.size):
        print "Solving", i, ",", j, 'of', U_hot.size, ',', U_cold.size
        te_pair.U_cold = U_cold[j]
        
        fmin(get_minpar, x0=x0)

        power[i,j]         = te_pair.P
        R_thermal[i,j]     = te_pair.R_thermal
        fill_fraction[i,j] = te_pair.fill_fraction
        length[i,j]        = te_pair.length
        I[i,j]             = te_pair.I         
        area_ratio[i,j]    = te_pair.area_ratio

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

R_hot = 1. / U_hot
R_cold = 1. / U_cold
R_hot2d, R_cold2d = np.meshgrid(R_hot, R_cold)
#TICKS = np.linspace(800, power_net_array.max() * 1.e3, 12)
#LEVELS = np.linspace(800, power_net_array.max() * 1.e3, 12)

plt.figure()
FCS = plt.contourf(R_hot2d, R_cold2d, R_thermal.T) 
CB = plt.colorbar(FCS, orientation='vertical')
# CB = plt.colorbar(FCS, orientation='vertical', format='%.0f', ticks=TICKS)
CB.set_label('TE Thermal Resistance')
plt.grid()
plt.xlabel(r'R$_{hot}$')
plt.ylabel(r'R$_{cold}$')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)

plt.show()
