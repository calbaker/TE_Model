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
            self.hx_zone[i].exh.mdot = self.exh.mdot
            self.hx_zone[i].exh.T_inlet = self.hx_zone[0].exh.T_outlet  
            self.hx_zone[i].cool.T_inlet = (
        self.hx_zone[0].cool.T_outlet ) 
            self.hx_zone[i].optimize()

        self.store_zone_values()

        # def store_zone_values(self):
        #     """Concatenates all the zone values to make it look like a
        #     single heat exchanger."""

        #     self.power_net = np.array(hx_zone[:].power_net).sum()
        #     self.te_pair.power_total = np.array(hx_zone[:]

        
        # self.Qdot_nodes = ZEROS.copy()
        # # initialize array for storing heat transfer (kW) in each node 
        
        # self.exh.Vdot_nodes = ZEROS.copy()

        # self.exh.T_nodes = ZEROS.copy()
        # # initializing array for storing temperature (K) in each node 
        # self.exh.h_nodes = ZEROS.copy()
        # self.exh.f_nodes = ZEROS.copy()
        # self.exh.deltaP_nodes = ZEROS.copy()
        # self.exh.Wdot_nodes = ZEROS.copy()
        # self.exh.Nu_nodes = ZEROS.copy()
        # self.exh.c_p_nodes = ZEROS.copy()
        # self.exh.entropy_nodes = ZEROS.copy()
        # self.exh.enthalpy_nodes = ZEROS.copy()

        # self.cool.T_nodes = ZEROS.copy()
        # # initializing array for storing temperature (K) in each node 
        # self.cool.entropy_nodes = ZEROS.copy()
        # self.cool.enthalpy_nodes = ZEROS.copy()

        # self.U_nodes = ZEROS.copy()
        # self.U_hot_nodes = self.U_nodes.copy()
        # self.U_cold_nodes = self.U_nodes.copy()
        # self.q_h_nodes = ZEROS.copy()
        # self.q_c_nodes = self.q_h_nodes.copy()
        # self.te_pair.q_h_nodes = self.q_h_nodes.copy()
        # self.te_pair.q_c_nodes = self.q_h_nodes.copy()

        # self.error_hot_nodes = ZEROS.copy()
        # self.error_cold_nodes = ZEROS.copy()

        # self.te_pair.T_c_nodes = ZEROS.copy()
        # # initializing array for storing temperature (K) in each node 
        # self.te_pair.T_h_nodes = ZEROS.copy()
        # # initializing array for storing temperature (K) in each node 
        # self.te_pair.h_nodes = self.U_nodes.copy()

        # self.te_pair.power_nodes = ZEROS.copy()
        # self.te_pair.eta_nodes = ZEROS.copy()

        # self.exh.velocity_nodes = ZEROS.copy()
