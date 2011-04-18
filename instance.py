# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

# User Defined Modules
# In this directory
import HX
# In python directory
import properties as prop

print "Beginning execution..."

# Instantiation
HX1 = HX.HX()
HX1.exh.porous = 'no' 
HX1.exh.T_inlet = 600.
HX1.exh.P = 100.
HX1.cool.T_inlet = 300.
HX1.solve_HX()

print "Program finished."
