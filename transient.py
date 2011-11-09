# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os

# User Defined Modules
# In this directory
import hx
reload(hx)

class transient_hx(hx):
    """Special class for modeling waste heat recovery heat exchanger
    with transient inlet temperature and flow conditions."""

    def __init__(self):
        """initializes variables."""
        super(transient_hx, self).__init__()

    def solve_hx_transient(self):
        """needs a better doc string"""
        self.solve_hx()

        self.power_net_trans = np.empty([np.size(self.exh.T_inlet_array),np.size(self.exh.T_nodes)])

        for i in range(np.size(self.exh.T_inlet_array)):
            
            
    
    def solve_node_transient(self,i):
        """needs a better doc string"""
        self.tem.Ntype.node = i # used within tem.py
        self.tem.Ptype.node = i
        
        self.solve_node(i)
        self.error_hot = 100. # really big number to start while loop

        self.loop_count = 0
        while ( np.absolute(self.error_hot) > self.xtol or
    np.absolute(self.error_cold) > self.xtol ): 

            self.tem.T_h_goal = spopt.fsolve(self.get_error_hot,
    x0=self.tem.T_h_goal)
            # self.tem.solve_tem()

            self.tem.T_c = spopt.fsolve(self.get_error_cold,
    x0=self.tem.T_c) 

        self.Qdot_node = -self.tem.q_h * self.area
            
