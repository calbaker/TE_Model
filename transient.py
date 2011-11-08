# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os

#
# User Defined Modules
# In this directory
import hx
reload(hx)

class transient_hx(hx):
    """Special class for modeling waste heat recovery heat exchanger
    with transient inlet temperature and flow conditions."""

    
