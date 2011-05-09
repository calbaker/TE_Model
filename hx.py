# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

# User Defined Modules
# In this directory
import engine
import tem
reload(tem)
from functions import *
import exhaust
import coolant

# definitions of classes for mediums in which heat transfer can occur

class _PlateWall():
    """class for modeling metal walls of heat exchanger"""
    k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
    t = 0.01 # thickness (m) of HX plate
    def set_h(self):
        self.h = self.k/self.t


class HX:
    """class for handling HX system"""
    def __init__(self):
        """Geometry and constants"""
        self.width = 15e-2 # width (cm*10**-2) of HX duct. This model treats
            # duct as parallel plates for simpler modeling.
        self.length = 1. # length (m) of HX duct
        self.nodes = 50 # number of nodes for numerical heat transfer model
        self.node_length = self.length / self.nodes # length (m) of each node
        self.x_dim = sp.arange(self.node_length/2, self.length +
        self.node_length/2, self.node_length)  
        # x coordinate (m)

    # initilization of class instances
    cool = coolant.Coolant()
    exh = exhaust.Exhaust()
    TEM = tem.TEModule()
    plate = _PlateWall()
    Cummins = engine.Engine()

    # More exhaust attributes
    Cummins.set_mdot_charge() # mass flow rate (kg/s) of exhaust
    exh.mdot = Cummins.mdot_charge

    def solve_node(self):
        """solves for performance of streamwise slice of HX"""
        self.exh.T_out = self.exh.T_in - 5 # Guess at exhaust node out temperature (K)

        # Exhaust stuff
        self.exh.set_flow(self.length)
        # Coolant stuff
        self.cool.set_flow(self.length)
        # Wall stuff
        self.plate.set_h()
        # TE stuff
        self.TEM.solve_tem()

        self.exh.R_thermal = 1 / self.exh.h
        self.plate.R_thermal = 1 / self.plate.h
        self.TEM.R_thermal = 1 / self.TEM.h
        self.cool.R_thermal = 1 / self.cool.h

        self.leg_pairs = int(self.area / self.TEM.area) # Number of TEM leg pairs per node
        # Heat exchanger stuff
        if self.exh.C < self.cool.C:
            self.C_min = self.exh.C
            self.C_max = self.cool.C
        else:
            self.C_min = self.cool.C
            self.C_max = self.exh.C
            
        self.R_C = self.C_min / self.C_max

        self.U = ( (self.exh.R_thermal + self.plate.R_thermal + self.TEM.R_thermal +
        self.plate.R_thermal + self.cool.R_thermal )**-1 ) # overall heat transfer
            # coefficient (kW/m^2-K)
        self.NTU = self.U * self.area / self.C_min # number
            # of transfer units
#################### dependent on HX configuration  
        if self.type == 'parallel':                                        
            self.effectiveness = ( (1 - sp.exp(-self.NTU * (1 + self.R_C))) / (1
             + self.R_C) )  # NTU method for parallel flow from Mills Heat
                # Transfer Table 8.3a  
            self.Qdot = ( self.effectiveness * self.C_min * (self.exh.T_in -
             self.cool.T_in)  ) # NTU heat transfer (kW)
            self.cool.T_out = ( self.cool.T_in + self.Qdot / self.cool.C )
            # temperature (K) at coolant outlet

        elif self.type == 'counter':
            self.effectiveness = ( (1 - sp.exp(-self.NTU * (1 - self.R_C))) /
           (1 - self.R_C * sp.exp(-self.NTU * (1 - self.R_C))) )
            self.Qdot = ( (self.effectiveness * self.C_min * (self.exh.T_in -
             self.cool.T_out)) / (1 - self.effectiveness * self.C_min / self.cool.C) ) # NTU heat transfer (kW) 
            self.cool.T_in = ( self.cool.T_out - self.Qdot / self.cool.C )

#################### independent of HX configuration  
        self.exh.T_out = ( self.exh.T_in - self.Qdot / self.exh.C )
            # temperature (K) at exhaust outlet   

    def solve_hx(self): # solve parallel flow heat exchanger
        """solves for performance of entire HX"""
        self.exh.set_flow_geometry(self.width) 
        self.cool.set_flow_geometry(self.width)
        
        self.area = self.node_length*self.width*self.cool.ducts # area (m^2)
                                        # through which heat flux
                                        # occurs in each node
        self.exh.T_in = self.exh.T_inlet # T_in and T_out correspond to the
                                   # temperatures going into and out
                                   # of the node.  The suffix "let"
                                   # means the temperature is
                                   # referring to the HX inlet or
                                   # outlet.   
        if self.type == 'parallel':
            self.cool.T_in = self.cool.T_inlet
        elif self.type == 'counter':
            self.cool.T_out = self.cool.T_outlet  

        # initializing arrays for tracking variables at nodes
        ZEROS = sp.zeros(self.nodes)
        self.Qdot_nodes = ZEROS.copy() # initialize array for storing
                                    # heat transfer (kW) in each node 
        self.effectiveness_nodes = ZEROS.copy() # initialize array for storing
                                    # heat transfer (kW) in each node 
        self.exh.T_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.exh.h_nodes = ZEROS.copy()
        self.cool.T_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.cool.h_nodes = ZEROS.copy() 
        self.U_nodes = ZEROS.copy() 
        self.TEM.T_c_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.TEM.T_h_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.TEM.power_nodes = ZEROS.copy()
        
        # for loop iterates of nodes of HX in streamwise direction
        for i in sp.arange(self.nodes):
            print "\nSolving node", i
            self.TEM.T_c = self.cool.T_in # guess at cold side TEM temperature (K)
            self.TEM.T_h_goal = self.exh.T_in # guess at hot side TEM temperature (K)

            for j in range(3):
                self.solve_node()
                self.TEM.T_h_goal = ( self.exh.T - self.Qdot / ((self.exh.h**-1 +
                self.plate.h**-1)**-1 * self.area) )
                # redefining TEM hot side temperature (K) based on known heat flux 
                self.TEM.T_c = ( self.Qdot * (1 / (self.plate.h * self.area) + 1 /
                (self.cool.h * self.area)) + self.cool.T)
                # redefining TEM cold side temperature (K) based on known heat flux
   
            self.Qdot_nodes[i] = self.Qdot # storing node heat transfer in array
            self.effectiveness_nodes[i] = self.effectiveness # storing node heat transfer in array

            self.exh.T_nodes[i] = (self.exh.T_in + self.exh.T_out)/2.
            self.exh.h_nodes[i] = self.exh.h
            self.cool.h_nodes[i] = self.cool.h
            self.TEM.T_h_nodes[i] = self.TEM.T_h # hot side
                                        # temperature (K) of TEM at
                                        # each node
            self.cool.T_nodes[i] = (self.cool.T_in + self.cool.T_out)/2.
            self.TEM.T_c_nodes[i] = self.TEM.T_c # hot side temperature (K) of
                                       # TEM at each node.  Use
                                       # negative index because this
                                       # is counterflow.    
            self.U_nodes[i] = self.U
            self.TEM.power_nodes[i] = self.TEM.P_heat * self.leg_pairs

            # redefining outlet temperature (K) for next node
            self.exh.T_in = self.exh.T_out
            if self.type == 'parallel':
                self.cool.T_in = self.cool.T_out
            elif self.type == 'counter':
                self.cool.T_out = self.cool.T_in
                
        # redefining HX outlet/inlet temperatures (K)
        self.exh.T_outlet = self.exh.T_out
        if self.type == 'parallel':
            self.cool.T_outlet = self.cool.T_out
        elif self.type == 'counter':
            self.cool.T_inlet = self.cool.T_in

        self.Qdot = sp.sum(self.Qdot_nodes)
        self.available = self.exh.C * (self.exh.T_inlet - self.exh.T_ref)
        self.effectiveness = self.Qdot / self.available # global HX effectiveness                                        
        self.TEM.power = sp.sum(self.TEM.power_nodes)
        # total TE power output (kW)
        self.Wdot_pumping = self.exh.Wdot_pumping + self.cool.Wdot_pumping
        # total pumping power requirement (kW) 
        self.power_net = self.TEM.power - self.Wdot_pumping 
        self.eta_1st = self.power_net / self.Qdot
        self.eta_2nd = self.power_net / self.available

