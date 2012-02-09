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
        self.nodes = self.N * 5

        super(HX_Series, self).__init__()
        self.init_arrays()
    
    def setup(self):
        """not sure what this should do yet.  It's an ad hoc method
        for now.""" 
        
        self.hx_zone = np.empty(shape=self.N, dtype='object')

        try:
            self.exh.enhancement
        except AttributeError:
            self.exh.enhancement = None

        for i in range(self.N):
            self.hx_zone[i] = hx.HX()
            self.hx_zone[i].type = self.type
            self.hx_zone[i].length = self.length / self.N
            self.hx_zone[i].width = self.width
            self.hx_zone[i].exh.height = self.exh.height
            self.hx_zone[i].cool.height = self.cool.height
            self.hx_zone[i].te_pair.method = self.te_pair.method
            self.hx_zone[i].nodes = self.nodes / self.N
            if self.exh.enhancement != None:
                self.hx_zone[i].exh.enhancement = self.exh.enhancement

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
            self.hx_zone[i].x0 = self.hx_zone[i-1].te_pair.I
            self.hx_zone[i].current_only = True
            self.hx_zone[i].optimize()

        self.cat_zones()

        self.exh.volume = self.exh.height * self.exh.width * self.length
        self.power_density = self.power_net / self.exh.volume 


    def cat_zones(self):
        """Concatenates all the arrays of the hx_zones."""
        
        self.power_net_zones = np.zeros(self.N)
        self.te_pair.power_total_zones = np.zeros(self.N)
        self.Wdot_pumping_zones = np.zeros(self.N)

        for i in range(self.N):
            start = i * self.hx_zone[i].nodes
            end = (i + 1.) * self.hx_zone[i].nodes
            
            self.Qdot_nodes[start:end] = self.hx_zone[i].Qdot_node
            # storing node heat transfer in array

            self.q_h_nodes[start:end] = self.hx_zone[i].q_h
            self.q_c_nodes[start:end] = self.hx_zone[i].q_c
            self.te_pair.q_h_nodes[start:end] = self.hx_zone[i].te_pair.q_h
            self.te_pair.q_c_nodes[start:end] = self.hx_zone[i].te_pair.q_c
            self.error_hot_nodes[start:end] = self.hx_zone[i].error_hot
            self.error_cold_nodes[start:end] = self.hx_zone[i].error_cold
            
            self.exh.T_nodes[start:end] = self.hx_zone[i].exh.T
        
            self.exh.Vdot_nodes[start:end] = self.hx_zone[i].exh.Vdot
            self.exh.f_nodes[start:end] = self.hx_zone[i].exh.f
            self.exh.deltaP_nodes[start:end] = self.hx_zone[i].exh.deltaP
            self.exh.Wdot_nodes[start:end] = self.hx_zone[i].exh.Wdot_pumping

            self.exh.Nu_nodes[start:end] = self.hx_zone[i].exh.Nu_D
            self.exh.c_p_nodes[start:end] = self.hx_zone[i].exh.c_p 
            self.exh.h_nodes[start:end] = self.hx_zone[i].exh.h

            self.exh.entropy_nodes[start:end] = self.hx_zone[i].exh.entropy
            self.exh.enthalpy_nodes[start:end] = self.hx_zone[i].exh.enthalpy

            self.cool.T_nodes[start:end] = self.hx_zone[i].cool.T

            self.te_pair.T_h_nodes[start:end] = self.hx_zone[i].te_pair.T_h
            # hot side temperature (K) of TEM at each node 
            self.te_pair.T_c_nodes[start:end] = self.hx_zone[i].te_pair.T_c
            # cold side temperature (K) of TEM at each node.  

            self.U_nodes[start:end] = self.hx_zone[i].U
            self.U_hot_nodes[start:end] = self.hx_zone[i].U_hot
            self.U_cold_nodes[start:end] = self.hx_zone[i].U_cold

            self.te_pair.power_nodes[start:end] = ( 
            self.hx_zone[i].te_pair.P * self.hx_zone[i].leg_pairs ) 
            self.te_pair.eta_nodes[start:end] = self.hx_zone[i].te_pair.eta
            self.te_pair.h_nodes[start:end] = self.hx_zone[i].te_pair.h

            self.exh.velocity_nodes[start:end] = self.hx_zone[i].exh.velocity
        
            self.power_net_zones[i] = ( self.hx_zone[i].power_net ) 
            self.te_pair.power_total_zones[i] = (
            self.hx_zone[i].te_pair.power_total )  
            self.Wdot_pumping_zones[i] = (
            self.hx_zone[i].Wdot_pumping )

        self.power_net = self.power_net_zones.sum()
        self.te_pair.power_total = ( 
        self.te_pair.power_total_zones.sum() ) 
        self.Wdot_pumping = self.Wdot_pumping_zones.sum()

