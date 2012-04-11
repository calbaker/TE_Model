# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time, os, sys
from scipy.optimize import fsolve

# local user modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

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

T_guess = np.array([700., 350.])

class _Exh(object):

    def __init__(self):
        self.T = 800.
        self.h = 0.5


class _Cool(object):
    
    def __init__(self):
        self.T = 300.
        self.h = 0.5

exh = _Exh()
cool = _Cool()

def get_error(T_arr):
    T_h = T_arr[0]
    exh.q = exh.h * (T_h - exh.T)
    te_pair.T_h_goal = T_h
    te_pair.solve_te_pair()
    error_hot = (exh.q - te_pair.q_h) / te_pair.q_h
    
    T_c = T_arr[1]
    cool.q = cool.h * (cool.T - T_c)
    te_pair.T_c = T_c
    te_pair.solve_te_pair()
    error_cold = (exh.q - te_pair.q_c) / te_pair.q_c
    
    te_pair.error = np.array([error_hot, error_cold]).reshape(2)  
    return te_pair.error

T_arr = fsolve(get_error, x0=T_guess) 

print "T_h:", T_arr[0]
print "T_c:", T_arr[1]

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
