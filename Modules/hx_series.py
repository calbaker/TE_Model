# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
from scipy.optimize import fmin

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

        super(HX_Series, self).__init__()
        
        self.N = 5
        self.nodes = self.N * 25

    def setup(self):
        """not sure what this should do yet.  It's an ad hoc method
        for now.""" 

        self.x = np.linspace(0, self.length, self.nodes)
        self.hx_zone = np.array([hx.HX() for i in range(self.N)])
        self.init_arrays()
    
        try:
            self.exh.enhancement
        except AttributeError:
            self.exh.enhancement = None

        for i in range(self.N):
            self.hx_zone[i].type = self.type
            self.hx_zone[i].length = self.length / self.N
            self.hx_zone[i].width = self.width
            self.hx_zone[i].exh.height = self.exh.height
            self.hx_zone[i].cool.height = self.cool.height
            self.hx_zone[i].te_pair.method = self.te_pair.method
            self.hx_zone[i].nodes = self.nodes / self.N
            if self.exh.enhancement != None:
                self.hx_zone[i].exh.enhancement = self.exh.enhancement
            else:
                self.exh.enhancement = self.hx_zone[i].exh.enhancement

    def solve_hxs(self):
        """ad hoc method for now."""
        
        self.hx_zone[0].exh.T_inlet = self.exh.T_inlet 
        self.hx_zone[0].cool.T_inlet = self.cool.T_inlet
        
        self.hx_zone[0].exh.mdot = self.exh.mdot

        self.hx_zone[0].optimize()

        for i in range(1,self.N):
            print "Solving zone", i, "of", self.N - 1
            self.hx_zone[i].exh.mdot = self.exh.mdot
            self.hx_zone[i].exh.T_inlet = self.hx_zone[i-1].exh.T_outlet  
            self.hx_zone[i].cool.T_inlet = (
        self.hx_zone[i-1].cool.T_outlet ) 
            self.hx_zone[i].x0 = self.hx_zone[i-1].te_pair.I
            self.hx_zone[i].current_only = True

            self.hx_zone[i].te_pair.Ntype.area = (
            self.hx_zone[0].te_pair.Ntype.area )
            self.hx_zone[i].te_pair.Ptype.area = (
            self.hx_zone[0].te_pair.Ptype.area )
            self.hx_zone[i].te_pair.area_void = (
            self.hx_zone[0].te_pair.area_void ) 

            self.hx_zone[i].te_pair.I = ( 
            fmin(self.hx_zone[i].get_inv_power_v_I, self.hx_zone[i-1].te_pair.I) )

        self.cat_zones()

        self.exh.volume = self.exh.height * self.exh.width * self.length
        self.power_density = self.power_net / self.exh.volume 


    def cat_zones(self):
        """Concatenates all the arrays of the hx_zones."""
        
        self.exh.enthalpy_nodes = np.zeros(self.nodes)
        self.exh.entropy_nodes = np.zeros(self.nodes)
        self.exh.availability_flow_nodes = np.zeros(self.nodes)

        self.cool.enthalpy_nodes = np.zeros(self.nodes)
        self.cool.entropy_nodes = np.zeros(self.nodes)
        self.cool.availability_flow_nodes = np.zeros(self.nodes)

        self.power_net_zones = np.zeros(self.N)
        self.te_pair.power_total_zones = np.zeros(self.N)
        self.Wdot_pumping_zones = np.zeros(self.N)

        for i in range(self.N):
            start = i * self.hx_zone[i].nodes
            end = (i + 1.) * self.hx_zone[i].nodes
            
            self.Qdot_nodes[start:end] = self.hx_zone[i].Qdot_nodes
            # storing node heat transfer in array

            self.q_h_nodes[start:end] = self.hx_zone[i].q_h_nodes
            self.q_c_nodes[start:end] = self.hx_zone[i].q_c_nodes
            self.te_pair.q_h_nodes[start:end] = self.hx_zone[i].te_pair.q_h_nodes
            self.te_pair.q_c_nodes[start:end] = self.hx_zone[i].te_pair.q_c_nodes
            self.error_hot_nodes[start:end] = self.hx_zone[i].error_hot_nodes
            self.error_cold_nodes[start:end] = self.hx_zone[i].error_cold_nodes
            
            self.exh.T_nodes[start:end] = self.hx_zone[i].exh.T_nodes
        
            self.exh.Vdot_nodes[start:end] = self.hx_zone[i].exh.Vdot_nodes
            self.exh.f_nodes[start:end] = self.hx_zone[i].exh.f_nodes
            self.exh.deltaP_nodes[start:end] = self.hx_zone[i].exh.deltaP_nodes
            self.exh.Wdot_nodes[start:end] = self.hx_zone[i].exh.Wdot_nodes

            self.exh.Nu_nodes[start:end] = self.hx_zone[i].exh.Nu_nodes
            self.exh.c_p_nodes[start:end] = self.hx_zone[i].exh.c_p_nodes
            self.exh.h_nodes[start:end] = self.hx_zone[i].exh.h_nodes

            self.exh.entropy_nodes[start:end] = self.hx_zone[i].exh.entropy_nodes
            self.exh.enthalpy_nodes[start:end] = self.hx_zone[i].exh.enthalpy_nodes

            self.cool.T_nodes[start:end] = self.hx_zone[i].cool.T_nodes

            self.te_pair.T_h_nodes[start:end] = self.hx_zone[i].te_pair.T_h_nodes
            # hot side temperature (K) of TEM at each node 
            self.te_pair.T_c_nodes[start:end] = self.hx_zone[i].te_pair.T_c_nodes
            # cold side temperature (K) of TEM at each node.  

            self.U_nodes[start:end] = self.hx_zone[i].U_nodes
            self.U_hot_nodes[start:end] = self.hx_zone[i].U_hot_nodes
            self.U_cold_nodes[start:end] = self.hx_zone[i].U_cold_nodes

            self.te_pair.power_nodes[start:end] = (
            self.hx_zone[i].te_pair.power_nodes ) 
            self.te_pair.eta_nodes[start:end] = self.hx_zone[i].te_pair.eta_nodes
            self.te_pair.h_nodes[start:end] = self.hx_zone[i].te_pair.h_nodes

            self.exh.velocity_nodes[start:end] = self.hx_zone[i].exh.velocity_nodes
        
            self.exh.enthalpy_nodes[start:end] = (
            self.hx_zone[i].exh.enthalpy_nodes ) 
            self.exh.entropy_nodes[start:end] = (
            self.hx_zone[i].exh.entropy_nodes ) 
            self.exh.availability_flow_nodes[start:end] = (
            self.hx_zone[i].exh.availability_flow_nodes ) 

            self.cool.enthalpy_nodes[start:end] = (
            self.hx_zone[i].cool.enthalpy_nodes ) 
            self.cool.entropy_nodes[start:end] = (
            self.hx_zone[i].cool.entropy_nodes ) 
            self.cool.availability_flow_nodes[start:end] = (
            self.hx_zone[i].cool.availability_flow_nodes ) 

            self.power_net_zones[i] = ( self.hx_zone[i].power_net ) 
            self.te_pair.power_total_zones[i] = (
            self.hx_zone[i].te_pair.power_total )  
            self.Wdot_pumping_zones[i] = (
            self.hx_zone[i].Wdot_pumping )

        self.power_net = self.power_net_zones.sum()
        self.te_pair.power_total = ( 
        self.te_pair.power_total_zones.sum() ) 
        self.Wdot_pumping = self.Wdot_pumping_zones.sum()

