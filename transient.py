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

    def get_error_hot(self,T_h):
        """Returns hot side and cold side heat flux values in an
        array.  The first entry is hot side heat flux and the second
        entry is cold side heat flux."""
        self.q_h = ( self.R_contact * (T_h - self.plate.T) )
        self.tem.T_h_goal = T_h
        self.tem.solve_tem()
        self.error_hot = (self.q_h - self.tem.q_h) / self.tem.q_h
        return self.error_hot

    def get_error_cold(self,T_c):
        """Returns cold side and cold side heat flux values in an
        array.  The first entry is cold side heat flux and the second
        entry is cold side heat flux."""
        self.q_c = self.U_cold * (self.cool.T - T_c)
        self.tem.T_c = T_c
        self.tem.solve_tem()
        self.error_cold = (self.q_c - self.tem.q_c) / self.tem.q_c
        return self.error_cold

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
            
    def solve_hx(self,**kwargs): # solve parallel flow heat exchanger
        """solves for performance of entire HX based on transient.
        Supercedes same function in hx.py"""
        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']
        else:
            self.verbose = False
        self.set_constants()
        self.exh.T = self.exh.T_inlet
        # T_inlet and T_outlet correspond to the temperatures going
        # into and out of the heat exchanger.
        if self.type == 'parallel':
            self.cool.T = self.cool.T_inlet
        elif self.type == 'counter':
            self.cool.T = self.cool.T_outlet  

        self.tem.Ptype.set_prop_fit()
        self.tem.Ntype.set_prop_fit()

        # initializing arrays for tracking variables at nodes
        ZEROS = np.zeros(self.nodes)
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
        
        # for loop iterates of nodes of HX in streamwise direction
        for i in np.arange(self.nodes):
            if self.verbose == True:
                print "\nSolving node", i
            if self.transient == True:
                self.solve_node_transient(i)
            else:
                self.solve_node(i)

            self.Qdot_nodes[i] = self.Qdot_node
            # storing node heat transfer in array
            if self.thermoelectrics_on == True:
                self.q_h_nodes[i] = self.q_h
                self.q_c_nodes[i] = self.q_c
                self.tem.q_h_nodes[i] = self.tem.q_h
                self.tem.q_c_nodes[i] = self.tem.q_c
                self.error_hot_nodes[i] = self.error_hot
                self.error_cold_nodes[i] = self.error_cold

            self.exh.T_nodes[i] = self.exh.T
            self.exh.h_nodes[i] = self.exh.h
            self.exh.f_nodes = self.exh.f
            self.exh.Nu_nodes = self.exh.Nu_D

            self.cool.h_nodes[i] = self.cool.h
            self.cool.T_nodes[i] = self.cool.T
            self.cool.f_nodes = self.cool.f
            self.cool.Nu_nodes = self.cool.Nu_D
            self.tem.T_h_nodes[i] = self.tem.T_h
            # hot side temperature (K) of TEM at each node 
            self.tem.T_c_nodes[i] = self.tem.T_c
            # cold side temperature (K) of TEM at each node.  
            self.U_nodes[i] = self.U
            self.U_hot_nodes[i] = self.U_hot
            self.U_cold_nodes[i] = self.U_cold
            self.tem.power_nodes[i] = self.tem.P * self.leg_pairs
            self.tem.eta_nodes[i] = self.tem.eta
            self.tem.h_nodes[i] = self.tem.h

            if self.thermoelectrics_on == True:
                # redefining temperatures (K) for next node
                self.exh.T = ( self.exh.T + self.tem.q_h * self.area /
                    self.exh.C )   
                if self.type == 'parallel':
                    self.cool.T = ( self.cool.T - self.tem.q_c * self.area
                        / self.cool.C )  
                elif self.type == 'counter':
                    self.cool.T = ( self.cool.T + self.tem.q_c * self.area
                        / self.cool.C )
            else:
                self.exh.T = ( self.exh.T - self.Qdot_node / self.exh.C )
                if self.type == 'parallel':
                    self.cool.T = ( self.cool.T + self.Qdot_node /
            self.cool.C )    
                elif self.type == 'counter':
                    self.cool.T = ( self.cool.T + self.Qdot_node /
            self.cool.C ) 
                
        # defining HX outlet/inlet temperatures (K)
        self.exh.T_outlet = self.exh.T
        if self.type == 'parallel':
            self.cool.T_outlet = self.cool.T
        elif self.type == 'counter':
            self.cool.T_inlet = self.cool.T

        self.Qdot = self.Qdot_nodes.sum()
        self.effectiveness = ( self.Qdot / (self.exh.C *
        (self.exh.T_inlet - self.cool.T_inlet)) )
        # heat exchanger effectiveness
        self.tem.power_total = self.tem.power_nodes.sum()
        # total TE power output (kW)
        self.Wdot_pumping = ( self.exh.Wdot_pumping +
        self.cool.Wdot_pumping ) 
        # total pumping power requirement (kW) 
        self.power_net = self.tem.power_total - self.Wdot_pumping 
        self.eta_1st = self.power_net / self.Qdot
        
        
        
        
    
