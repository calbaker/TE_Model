# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as mpl
import scipy.optimize as spopt

# User Defined Modules
# In this directory
import engine
import tem
reload(tem)
import exhaust
reload(exhaust)
import coolant
reload(coolant)
import platewall
reload(platewall)


class HX(object):
    """class for handling HX system"""

    def __init__(self):
        """Geometry and constants"""
        self.loop_count = 0
        self.width = 10.e-2 # width (cm*10**-2) of HX duct. This model treats
            # duct as parallel plates for simpler modeling.
        self.length = 20.e-2 # length (m) of HX duct
        self.nodes = 25 # number of nodes for numerical heat transfer
                        # model
        self.xtol = 0.01

        # initialization of sub classes
        self.cool = coolant.Coolant()
        self.exh = exhaust.Exhaust()
        self.tem = tem.TEModule()
        self.plate = platewall.PlateWall()
        self.cummins = engine.Engine()

        self.fix_geometry()
        self.init_arrays()

    def init_arrays(self):
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

        self.exh.velocity_nodes = ZEROS.copy()

    def setup(self):
        """Sets up variables that must be defined before running
        model.  Useful for terminal.  Not necessary elsewhere."""
        self.exh.T = 800.
        self.cool.T = 300. 
        self.set_mdot_charge()
        self.set_constants()

    def set_constants(self):
        """Sets constants used at the HX level."""
        self.node_length = self.length / self.nodes
        # length (m) of each node
        self.area = self.node_length * self.width * self.cool.ducts # area (m^2)
                                        # through which heat flux
                                        # occurs in each node
        self.tem.set_constants()
        self.leg_pairs = int(self.area / self.tem.area)
        # Number of TEM leg pairs per node
        self.x_dim = np.arange(self.node_length/2, self.length +
        self.node_length/2, self.node_length)   
        # x coordinate (m)
        self.fix_geometry()
        self.exh.set_flow_geometry(self.exh.width) 
        self.cool.set_flow_geometry(self.cool.width)

    def fix_geometry(self):
        """Makes sure that common geometry like width and length is
        the same between exh, cool, and the overal heat exchanger."""
        self.cool.width = self.width
        self.cool.length = self.length
        self.exh.width = self.width
        self.exh.length = self.length

    def set_mdot_charge(self):
        """Sets exhaust mass flow rate. Eventually, this should be a
        function of speed, load, and EGR fraction.  Also, it should
        come from experimental data.  Also, it should probably go
        within the exhaust module."""
        self.cummins.set_mdot_charge() # mass flow rate (kg/s) of exhaust
        self.exh.mdot = self.cummins.mdot_charge 

    def set_convection(self):
        """Sets values for convection coefficients."""
        # Exhaust stuff
        self.exh.set_flow()
        # Coolant stuff
        self.cool.set_flow()
        # Wall stuff
        self.plate.set_h()
        # The previous three commands need only execute once per
        # node.  
        # TE stuff

        self.U = ( (self.exh.R_thermal + self.plate.R_thermal +
        self.plate.R_contact + self.tem.R_thermal + self.plate.R_contact +
        self.plate.R_thermal + self.cool.R_thermal )**-1 )    
        # overall heat transfer coefficient (kW/m^2-K)
        self.U_hot = ( (self.exh.R_thermal + self.plate.R_thermal +
        self.plate.R_contact)**-1 )
        # heat transfer coefficient (kW/m^-K) between TE hot side and
        # exhaust  
        self.U_cold = ( (self.cool.R_thermal +
        self.plate.R_thermal + self.plate.R_contact)**-1 )
        # heat transfer coefficient (kW/m^-K) between TE cold side and
        # coolant  
        
    def get_error_hot(self,T_h):
        """Returns hot side and cold side heat flux values in an
        array.  The first entry is hot side heat flux and the second
        entry is cold side heat flux."""
        self.q_h = self.U_hot * (T_h - self.exh.T)
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

    def solve_node(self,i):
        """Solves for performance of streamwise slice of HX.  The
        argument i is an indexing variable from a for loop within the
        function solve_hx."""
        self.tem.Ntype.node = i # used within tem.py
        self.tem.Ptype.node = i
        
        if i == 0:
            self.tem.T_c = self.cool.T
            # guess at cold side tem temperature (K)
            self.tem.T_h_goal = self.exh.T
            # guess at hot side TEM temperature (K)
            self.tem.solve_tem()
            self.set_convection()
            self.q = self.U * (self.cool.T - self.exh.T)
            self.tem.T_h_goal = self.q / self.U_hot + self.exh.T
            self.tem.T_c = -self.q / self.U_cold + self.cool.T
        else:
            self.tem.T_c = (self.tem.T_c_nodes[i-1])
            self.tem.T_h_goal = (self.tem.T_h_nodes[i-1])

        self.error_hot = 100. # really big number to start while loop

        self.loop_count = 0
        while ( np.absolute(self.error_hot) > self.xtol or
    np.absolute(self.error_cold) > self.xtol ): 
            self.tem.T_h_goal = spopt.fsolve(self.get_error_hot,
    x0=self.tem.T_h_goal)
            # self.tem.solve_tem()
            self.tem.T_c = spopt.fsolve(self.get_error_cold,
    x0=self.tem.T_c) 
            self.error_cold = self.get_error_cold(self.tem.T_c)
            self.error_hot = self.get_error_hot(self.tem.T_h)
            self.loop_count = self.loop_count + 1
            self.Qdot_node = -self.q_h * self.area
            # heat transfer on hot side of node, positive values indicates
            # heat transfer from hot to cold
            
    def solve_hx(self,**kwargs): # solve parallel flow heat exchanger
        """solves for performance of entire HX"""
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

        # for loop iterates of nodes of HX in streamwise direction
        for i in np.arange(self.nodes):
            if self.verbose == True:
                print "\nSolving node", i
            self.solve_node(i)
            self.store_node_values(i)

            # redefining temperatures (K) for next node
            self.exh.T = ( self.exh.T + self.tem.q_h * self.area /
                self.exh.C )   
            if self.type == 'parallel':
                self.cool.T = ( self.cool.T - self.tem.q_c * self.area
                    / self.cool.C )  
            elif self.type == 'counter':
                self.cool.T = ( self.cool.T + self.tem.q_c * self.area
                    / self.cool.C )
                
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

    def store_node_values(self,i):
        """Storing solved values in array to keep track of what
        happens in every node."""
        self.Qdot_nodes[i] = self.Qdot_node
        # storing node heat transfer in array
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

        self.exh.velocity_nodes[i] self.exh.velocity
