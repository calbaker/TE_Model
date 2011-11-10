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
        self.t_step = 1.

    def init_arrays(self):
        # initializing arrays for tracking variables at nodes
        ZEROS = np.zeros(self.t_step, self.nodes)
        self.Qdot_nodes = ZEROS.copy() # initialize array for storing
                                    # heat transfer (kW) in each node 
        self.exh.T_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.exh.h_nodes = ZEROS.copy()
        self.exh.f_nodes = ZEROS.copy()
        self.exh.Nu_nodes = ZEROS.copy()
        self.cool.T_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.cool.f_nodes = ZEROS.copy()
        self.cool.Nu_nodes = ZEROS.copy()
        self.cool.h_nodes = ZEROS.copy() 
        self.U_nodes = ZEROS.copy() 
        self.U_hot_nodes = ZEROS.copy() 
        self.U_cold_nodes = ZEROS.copy()
        self.q_h_nodes = ZEROS.copy()
        self.q_c_nodes = ZEROS.copy()
        self.tem.q_h_nodes = ZEROS.copy()
        self.tem.q_c_nodes = ZEROS.copy()
        self.error_hot_nodes = ZEROS.copy()
        self.error_cold_nodes = ZEROS.copy()
        self.tem.T_c_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.tem.T_h_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node
        self.tem.h_nodes = ZEROS.copy()                                     
        self.tem.power_nodes = ZEROS.copy()
        self.tem.eta_nodes = ZEROS.copy()

    def solve_hx_transient(self):
        """needs a better doc string"""
        self.solve_hx()

        self.power_net_trans = (
        np.zeros([np.size(self.exh.T_inlet_array),
        np.size(self.exh.T_nodes)]) ) 

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

    def store_node_values(self,i,t):
        """Storing solved values in array to keep track of what
        happens in every node."""
        self.Qdot_nodes[i,t] = self.Qdot_node
        # storing node heat transfer in array
        self.q_h_nodes[i,t] = self.q_h
        self.q_c_nodes[i,t] = self.q_c
        self.tem.q_h_nodes[i,t] = self.tem.q_h
        self.tem.q_c_nodes[i,t] = self.tem.q_c
        self.error_hot_nodes[i,t] = self.error_hot
        self.error_cold_nodes[i,t] = self.error_cold

        self.exh.T_nodes[i,t] = self.exh.T
        self.exh.h_nodes[i,t] = self.exh.h
        self.exh.f_nodes = self.exh.f
        self.exh.Nu_nodes = self.exh.Nu_D

        self.cool.h_nodes[i,t] = self.cool.h
        self.cool.T_nodes[i,t] = self.cool.T
        self.cool.f_nodes = self.cool.f
        self.cool.Nu_nodes = self.cool.Nu_D
        self.tem.T_h_nodes[i,t] = self.tem.T_h
        # hot side temperature (K) of TEM at each node 
        self.tem.T_c_nodes[i,t] = self.tem.T_c
        # cold side temperature (K) of TEM at each node.  
        self.U_nodes[i,t] = self.U
        self.U_hot_nodes[i,t] = self.U_hot
        self.U_cold_nodes[i,t] = self.U_cold
        self.tem.power_nodes[i,t] = self.tem.P * self.leg_pairs
        self.tem.eta_nodes[i,t] = self.tem.eta
        self.tem.h_nodes[i,t] = self.tem.h

        
            
