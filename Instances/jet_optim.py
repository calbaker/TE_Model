# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fsolve, fmin
import numpy as np
import time

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
# parameters from xmin2
# 7.049488398024472691e-01
# 2.074354421989454272e-02
# 1.033370547666811676e-03
# 4.634972529966798760e+00

leg_area = (0.002)**2
leg_length = 1.03e-3
current = 4.63
area_ratio = 0.705
fill_fraction = 2.07e-2

hx_jets = hx.HX()
hx_jets.exh.enhancement = 'jet array'
hx_jets.te_pair.method = 'analytical'
hx_jets.width = 30.e-2
hx_jets.exh.height = 3.5e-2
hx_jets.cool.mdot = 1.
hx_jets.length = 1.
hx_jets.te_pair.I = current
hx_jets.te_pair.length = leg_length

hx_jets.te_pair.Ptype.material = 'HMS'
hx_jets.te_pair.Ntype.material = 'MgSi'

hx_jets.te_pair.Ptype.area = leg_area                           
hx_jets.te_pair.Ntype.area = hx_jets.te_pair.Ptype.area * area_ratio
hx_jets.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_jets.te_pair.Ptype.area +
                            hx_jets.te_pair.Ntype.area) )  

hx_jets.type = 'counter'

hx_jets.exh.T_inlet = 800.
hx_jets.cool.T_inlet_set = 300.
hx_jets.cool.T_outlet = 310.

hx_jets.set_mdot_charge()

def optim(apar):
    """Returns power_net as a function of the optimization parameters
    of interest.

    Arguments
    -------------
    apar[0] : hx_jets.exh.jets.H, height annulus between jet and
    impinging surface
    apar[1] : hx_jets.exh.jets.D, jet diameter
    apar[2] : hx_jets.exh.jets.spacing, distance between adjacent jets 
    """
    apar = np.asarray(apar)

    hx_jets.exh.jets.H = apar[0] 
    hx_jets.exh.jets.D = apar[1]
    hx_jets.exh.jets.spacing = apar[2]

    hx_jets.set_constants()
    hx_jets.solve_hx()

    if hx_jets.power_net <= 0:
        minpar = 1.e3
    else:
        minpar = 1. / hx_jets.power_net

    return minpar

def fprime():
    """dummy function"""
    return 1

x0 = np.array([5.5e-2, 2.e-3, 1.6e-2]) 
# initial guess for fmin

xb = [(2.0e-2, 7.e-2),(2.0e-3, 4.e-3), (5.e-3, 1.5e-2)]

t0 = time.clock()

# Find min using downhill simplex algorithm
xmin1 = fmin(optim, x0)
# xmin1 = fmin_tnc(optim,x0,fprime,approx_grad=True,bounds=xb,xtol=0.01)

t1 = time.clock() - t0

print "xmin1 =", xmin1
print "power_net =", hx_jets.power_net 

print "Switching to numerical model."
print "Elapsed time solving xmin1:", t1 

# Find min again using the numerical model.  The analytical model
# should run first to provide a better initial guess.
# hx.te_pair.method = 'numerical'

# xmin2 = fmin(optim, xmin1)
# t2 = time.clock() - t1

# print "xmin2 =", xmin2
# print "power_net =", hx_jets.power_net 

# print "Elapsed time solving xmin2:", t2

# t = time.clock() - t0

# print """Total elapsed time =""", t


