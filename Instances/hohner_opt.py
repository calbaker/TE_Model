# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve, fmin_tnc, fmin

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import harmonica
reload(harmonica)

hohner = harmonica.Harmonica()
hohner.hx1.te_pair.method = 'analytical'
hohner.hx2.te_pair.method = 'analytical'


def optim(apar):
    """Function for returning parameter to be minimized."""
hohner.solve_harmonica()

def optim(apar):
    """Returns power_net as a function of the optimization parameters
    of interest.

    Arguments
    ------------"""

    apar = np.asarray(apar)

    hohner.height = apar[0]
    hohner.length = apar[1]
    hohner.hx1.width = apar[2]
    hohner.hx2.length = apar[3]
    hohner.hx2.exh.fins = apar[4]

    hohner.solve_harmonica()
    
    # if hohner.power_net <= 0: 
    #     minpar = 1.e3 
    #     # arbitrarily large number to scare it away from here! 
    # else:
    minpar = 1. / hohner.power_net
    
    print hohner.power_net
        
    return minpar

def fprime():
    """dummy function"""
    return 1

x0 = np.array([1.e-2, 1., 20.e-2, 5.e-2, 60]) 

# initial guess for fmin

# xb = [

# xmin1 = fmin_tnc(optim,x0,fprime,approx_grad=True,bounds=xb,xtol=0.01)

xmin = fmin(optim, x0) 


