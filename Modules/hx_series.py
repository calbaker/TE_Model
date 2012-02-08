# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np

# User Defined Modules
# In this directory
import hx
reload(hx)

class HX_Series(hx.HX):
    """Class for modeling several heat exchanger in series that have
    different properties or parameters."""

    def __init__(self):
        """Initializes the following variables:
        ----------------------
        self.N : number of heat exchangers in series
        self."""
        
        self.N = 5

        super(HX_Series, self).__init__()
    
    def setup(self):
        """not sure what this should do yet.  It's an ad hoc method
        for now.""" 
        
        self.hx_zone = list()

        for i in range(self.N):
            self.hx_zone.append(hx.HX())
            self.hx_zone[i].type = self.type
            self.hx_zone[i].length = self.length / self.N
            self.hx_zone[i].width = self.width
            self.hx_zone[i].exh.height = self.exh.height
            self.hx_zone[i].cool.height = self.cool.height
            self.hx_zone[i].te_pair.method = self.te_pair.method

        self.nodes = self.N * self.nodes

    def solve_hxs(self):
        """ad hoc method for now."""
        
        self.hx_zone[0].exh.T_inlet = self.exh.T_inlet 
        self.hx_zone[0].cool.T_inlet = self.cool.T_inlet
        
        self.hx_zone[0].exh.mdot = self.exh.mdot

        self.hx_zone[0].optimize()
        for i in range(1,self.N):
            print "Solving zone", i, "of", self.N - 1
            self.hx_zone[i].exh.mdot = self.exh.mdot
            self.hx_zone[i].exh.T_inlet = self.hx_zone[0].exh.T_outlet  
            self.hx_zone[i].cool.T_inlet = (
        self.hx_zone[0].cool.T_outlet ) 
            self.hx_zone[i].x0 = self.hx_zone[i-1].xmin[0]
            self.hx_zone[i].optimize()

