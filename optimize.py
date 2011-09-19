# Chad Baker
# Nick Malaya
# Created on 2011 August 30th
# using
# http://docs.scipy.org/doc/scipy/reference/optimize.html

# Distribution Modules
import os
import matplotlib.pyplot as plt

from numpy import *
import scipy as sp
from scipy.optimize import fmin
from scipy.optimize import fmin_powell
from scipy.optimize import anneal
from scipy.optimize import fmin_l_bfgs_b

# User Defined Modules
# In this directory
import hx
reload(hx)
import tem

# parameter space -- not varying for optimization!
area = (0.002)**2
length = 5.e-3

hx = hx.HX()
hx.tem.segments = 25
hx.width = 30.e-2
hx.exh.bypass = 0.
hx.exh.height = 3.5e-2
hx.length = 1.
hx.tem.I = 2.
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'parallel'
hx.exh.enhancement = "straight fins"
hx.exh.fin.thickness = 5.e-3
hx.exh.fins = 22

hx.exh.T_inlet = 800.
hx.cool.T_inlet = 300.


# additional variables (as of 9/1/11)
hx.tem.Ptype.area = 10.e-6

# this is our optimization method 
# (what we desire to optimize)
def optim(apar):
    # unpack guess vector
    apar=asarray(apar)
    hx.tem.leg_ratio     = apar[0]
    hx.tem.fill_fraction = apar[1]
    hx.tem.length        = apar[2]
    hx.tem.I             = apar[3]

    # reset surrogate variables
    hx.tem.Ntype.area = hx.tem.leg_ratio*hx.tem.Ptype.area
    hx.tem.area_void  = hx.tem.Ptype.area/hx.tem.fill_fraction

    hx.solve_hx()

    # 1/power_net -- fmin is a minimization routine
    return 1/(hx.power_net)

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
x0 = 1.2, 13.0, .001, 5

# bounds for the parameters {I-IV}:
xb = [(0.2,5.0),(1,100.0),(0.0005,0.01),(.1,10.0)]

# optimization loop
print "Beginning optimization..."

# find min
#xmin1 = fmin(optim,x0)

# find min using L-BFGS-B algorithm
xmin1 = fmin_l_bfgs_b(optim,x0,fprime,approx_grad=True,bounds=xb)

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
