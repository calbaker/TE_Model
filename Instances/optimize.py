# Chad Baker
# Nick Malaya
# Created on 2011 August 30th
# using
# http://docs.scipy.org/doc/scipy/reference/optimize.html

# Distribution Modules
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fmin
from scipy.optimize import fmin_powell
from scipy.optimize import anneal
from scipy.optimize import fmin_l_bfgs_b

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)
    
area = (0.002)**2
length = 1.e-3
current = 4.
area_ratio = 0.69
fill_fraction = 1. / 40.

hx = hx.HX()
hx.tem.method = 'analytical'
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.cool.mdot = 1.
hx.length = 1.
hx.tem.I = current
hx.tem.length = length

hx.tem.Ptype.material = 'HMS'
hx.tem.Ntype.material = 'MgSi'

hx.tem.Ptype.area = area                           
hx.tem.Ntype.area = hx.tem.Ptype.area * area_ratio
hx.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx.tem.Ptype.area +
                            hx.tem.Ntype.area) )  

hx.type = 'parallel'

hx.exh.T_inlet = 800.
hx.exh.P = 100.
hx.cool.T_inlet = 300.

hx.set_mdot_charge()

# this is our optimization method 
# (what we desire to optimize)
def optim(apar):
    # unpack guess vector
    apar=np.asarray(apar)
    hx.tem.leg_ratio     = apar[0]
    hx.tem.fill_fraction = apar[1]
    hx.tem.length        = apar[2]
    hx.tem.I             = apar[3]

    # reset surrogate variables
    hx.tem.Ntype.area = hx.tem.leg_ratio*hx.tem.Ptype.area
    hx.tem.area_void = ( (1. - hx.tem.fill_fraction) / hx.tem.fill_fraction *
                           (hx.tem.Ptype.area + hx.tem.Ntype.area) )
    hx.set_constants()
    hx.solve_hx()

    # 1/power_net -- fmin is a minimization routine
    return 1./(hx.power_net)

# dummy function
def fprime():
    return 1

#
# parameter optimization:
#
#   I) tem.leg_ratio
#  II) tem.fill_fraction
# III) hx.tem.length
#  IV) hx.tem.I
#
# initial guess {I-IV}:
x0 = 0.71, 0.02, .001, 4.5

# bounds for the parameters {I-IV}:
xb = [(0.2,1.5),(0.001,0.05),(0.0005,0.01),(1,10.0)]

# optimization loop
print "Beginning optimization..."

# find min
#xmin1 = fmin(optim,x0)

# find min using L-BFGS-B algorithm
#xmin1 = fmin_l_bfgs_b(optim,x0,fprime,approx_grad=True,bounds=xb)

# Find min using Powell's method
xmin_powell = fmin_powell(optim,x0)

print "Finalizing optimization..."

# output optimal parameters

print "\nProgram finished."
print xmin1


# notes:
#
# define a variable, tem.leg_ratio = tem.Ntype.area / tem.Ptype.area .  
# Keep tem.Ptype.area = 10.e-6 and vary tem.Ntype.area by varying leg_ratio.  
# leg_ratio can be anywhere from 0.2 up to 5.
#
# The next parameter is the leg area to the void area. 
# define tem.fill_fraction = tem.Ptype.area / tem.area_void.   
# vary this between 1 and 100 by changing area_void.  
#
# The next one is leg length or height, hx.tem.length.  
# Vary this between 0.0005 and 0.01.  
#
# The last one is current, hx.tem.I.  Vary this between 0.1 and 10. 
#
