# Chad Baker
# Created on 2012 Jan 26

# Distribution Modules
import time
import numpy as np
import matplotlib.pyplot as mpl
from scipy.optimize import fmin

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
        self.height : height (m) of harmonica hx
        self.length : overall length (m) of harmonica hx
        self.hx2.length : length (m) of side-flow hx
        self.hx2.nodes : number of nodes in hx2"""
    
        self.hx1 = hx.HX()
        self.hx2 = hx.HX()
        self.hx1.arrangement = 'harmonica'
        self.hx2.arrangement = 'harmonica2'

        self.height = 1.e-2
        self.length = 1. 
        self.hx1.exh.T_inlet = 800.
        self.hx1.cool.T_inlet = 300. 
        self.hx2.cool.T_inlet = 300. 
        
        self.hx1.type = 'parallel'
        self.hx2.type = 'parallel'

        self.hx2.length = 0.05
        self.hx2.nodes = 5
        

    def fix_geometry(self):
        """Makes sure that geometry for the two heat exchangers is the
        same where appropriate."""  
        
        self.hx1.height = self.height
        self.hx1.exh.height = self.height
        self.hx1.length = self.length
        self.hx2.width = self.hx1.length
        self.hx2.height = self.hx1.height
        self.hx2.exh.height = self.hx1.height

    def solve_harmonica(self):
        """Solves both hx instances and sums the result."""
        
        self.hx1.set_mdot_charge()
        self.hx1.solve_hx()

        self.width = self.hx1.width + 2. * self.hx2.length 

        self.hx2.exh.T_inlet = self.hx1.exh.T_nodes.mean()
        self.hx2.set_mdot_charge()
        self.hx2.solve_hx()

        self.Qdot = ( self.hx1.Qdot_total + 2. * self.hx2.Qdot_total )  
        self.Wdot_pumping = ( self.hx1.Wdot_pumping +
                              2. * self.hx2.Wdot_pumping ) 
        self.power_total = ( self.hx1.te_pair.power_total +
                             2. * self.hx2.te_pair.power_total ) 
        self.power_net = self.power_total - self.Wdot_pumping
        
