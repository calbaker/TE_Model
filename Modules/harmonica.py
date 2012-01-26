# Chad Baker
# Created on 2012 Jan 26

# Distribution Modules
import time
import numpy as np
import matplotlib.pyplot as mpl
from scipy.optimize import fsolve,fmin

# User Defined Modules
# In this directory
import hx
reload(hx)

class Harmonica(object):
    """Class for combining results from two heat exchangers to form
    the harmonica heat exchanger."""
    
    def __init__(self):
    """Initiates hx1 and hx1, classes for dealing with the flow manifold
    (upstream) heat exchanger and the working (downstream) heat
    exchanger in which most of the heat transfer will take place.

    Sets
    ------------------
    self.hx2.exh.enhancement : see self.exh.__doc__
    self.hx2.length : length (m) of side-flow hx
    self.hx2.nodes : number of nodes in hx2"""
    
    self.hx1 = hx.HX()
    self.hx2 = hx.HX()
    
    self.hx2.exh.enhancement = "straight fins"
    self.hx2.length = 0.05
    self.hx2.nodes = 5

    def fix_geometry(self):
        """Makes sure that geometry for the two heat exchangers is the
        same where appropriate."""  
        
        self.hx1.height = self.height
        self.hx1.length = self.length
        self.hx2.width = self.hx1.length
        self.hx2.height = self.hx1.height
        
    def solve_harmonica(self):
        """Solves both hx instances and sums the result."""
        
        self.fix_geometry()
        self.hx1.solve_hx()

        self.hx2.exh.T_inlet = self.hx1.exh.T_nodes.mean()
        self.hx2.exh.fins = 65
        self.set_mdot_charge()
        self.hx2.solve_hx()

        self.Wdot_pumping = ( self.hx1.Wdot_pumping +
        self.hx2.Wdot_pumping ) 
        self.power_total = ( self.hx1.te_pair.power_total +
        self.hx2.te_pair.power_total ) 
        self.power_net = self.power_total - self.Wdot_pumping
        
