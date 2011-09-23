# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import scipy.optimize as spopt
import time

# User Defined Modules
# In this directory
import engine
import tem
reload(tem)
import exhaust
reload(exhaust)
import coolant
reload(coolant)


class _PlateWall(object):
    """class for modeling metal walls of heat exchanger"""
    k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
    t = 0.005 # thickness (m) of HX plate
    def set_h(self):
        self.h = self.k/self.t
        self.R_thermal = 1 / self.h


class HX(object):
    """class for handling HX system"""

    def __init__(self):
        """Geometry and constants"""
        self.width = 10.e-2 # width (cm*10**-2) of HX duct. This model treats
            # duct as parallel plates for simpler modeling.
        self.length = 20.e-2 # length (m) of HX duct
        self.nodes = 25 # number of nodes for numerical heat transfer
                        # model
        self.error_tol = 0.01 # tolerable percent error in heat flux
        self.R_thermal = 5.
        # thermal contact resistance (m^2*K/kW) between plates
        self.thermoelectrics_on = True
        # if True, the thermoelectric model runs, if false, pure
        # conduction 

        self.fix_geometry()

    # initialization of sub classes
    cool = coolant.Coolant()
    exh = exhaust.Exhaust()
    tem = tem.TEModule()
    plate = _PlateWall()
    cummins = engine.Engine()

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
        self.exh.mdot = self.cummins.mdot_charge * (1. - self.exh.bypass) 

    def get_error_hot(self,T_h):
        """Returns hot side and cold side heat flux values in an
        array.  The first entry is hot side heat flux and the second
        entry is cold side heat flux."""
        self.q_h = self.U_hot * (T_h - self.exh.T)
        self.tem.T_h_goal = T_h
        self.tem.solve_tem()
        error_hot = self.q_h - self.tem.q_h
        return error_hot

    def get_error_cold(self,T_c):
        """Returns cold side and cold side heat flux values in an
        array.  The first entry is cold side heat flux and the second
        entry is cold side heat flux."""
        self.q_c = self.U_cold * (self.cool.T - T_c)
        self.tem.T_c = T_c
        self.tem.solve_tem()
        error_cold = self.q_c - self.tem.q_c
        return error_cold

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
        self.tem.solve_tem()
        # this command needs to execute every time the BC's are
        # changed.  

        self.U = ( (self.exh.R_thermal + self.plate.R_thermal +
        self.R_thermal + self.tem.R_thermal + self.R_thermal +
        self.plate.R_thermal + self.cool.R_thermal )**-1 )  
        # overall heat transfer coefficient (kW/m^2-K)
        self.U_hot = (self.exh.R_thermal + self.plate.R_thermal)**-1
        # heat transfer coefficient (kW/m^-K) between TE hot side and
        # exhaust  
        self.U_cold = (self.cool.R_thermal + self.plate.R_thermal)**-1
        # heat transfer coefficient (kW/m^-K) between TE cold side and
        # coolant  
        
    def solve_node(self,i):
        """Solves for performance of streamwise slice of HX.  The
        argument i is an indexing variable from a for loop within the
        function solve_hx."""
        if i == 0:
            self.tem.T_c = self.cool.T
            # guess at cold side tem temperature (K)
            self.tem.T_h_goal = self.exh.T
            # guess at hot side TEM temperature (K)
        else:
            self.tem.T_c = self.tem.T_c_nodes[i-1]
            self.tem.T_h_goal = self.tem.T_h_nodes[i-1]
        self.set_convection()
        self.error_hot = 100.  
        # amount by which convection model overpredicts hot side heat
        # flux (kW/m^2-K) relative to TE model.  

        if self.thermoelectrics_on == True:
            self.loop_count = 0
            while ( sp.absolute(self.error_hot / self.tem.q_h) >
            self.error_tol ):
                self.tem.T_h_goal = spopt.fsolve(self.get_error_hot,
                                           self.tem.T_h) 
                self.tem.solve_tem()
                self.tem.T_c = spopt.fsolve(self.get_error_cold, self.tem.T_c) 
                self.tem.solve_tem()
                self.error_cold = self.get_error_cold(self.tem.T_c)
                self.error_hot = self.get_error_hot(self.tem.T_h)
                self.loop_count = self.loop_count + 1
                self.Qdot_node = -self.q_h * self.area
                # heat transfer on hot side of node, positive values indicates
                # heat transfer from hot to cold
        else:
            self.tem.Ntype.set_TEproperties()
            self.tem.Ptype.set_TEproperties()
            self.tem.Ntype.R_thermal = ( self.tem.Ntype.length /
            (self.tem.Ntype.k * self.tem.Ntype.area) )
            self.tem.Ptype.R_thermal = ( self.tem.Ptype.length /
            (self.tem.Ptype.k * self.tem.Ptype.area) )
            self.tem.R_thermal = ( (self.tem.Ntype.R_thermal**-1. +
            self.tem.Ptype.R_thermal**-1.)**-1 * (self.tem.area +
            self.tem.area_void) )  
            
            self.set_convection()
            self.q_h = self.U * (self.cool.T - self.exh.T)
            self.Qdot_node = -self.q_h * self.area

        # these need to run out here for the pure conduction case in
        # which the loop is not active
        self.error_hot = self.get_error_hot(self.tem.T_h)
        self.error_cold = self.get_error_cold(self.tem.T_c)
        

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
        self.x_dim = sp.arange(self.node_length/2, self.length +
        self.node_length/2, self.node_length)   
        # x coordinate (m)
        self.fix_geometry()
        self.exh.set_flow_geometry(self.exh.width) 
        self.cool.set_flow_geometry(self.cool.width)

    def solve_hx(self): # solve parallel flow heat exchanger
        """solves for performance of entire HX"""
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
        ZEROS = sp.zeros(self.nodes)
        self.Qdot_nodes = ZEROS.copy() # initialize array for storing
                                    # heat transfer (kW) in each node 
        self.exh.T_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.exh.h_nodes = ZEROS.copy()
        self.cool.T_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.cool.h_nodes = ZEROS.copy() 
        self.U_nodes = ZEROS.copy() 
        self.U_hot_nodes = ZEROS.copy() 
        self.U_cold_nodes = ZEROS.copy()
        self.q_h_nodes = ZEROS.copy()
        self.q_c_nodes = ZEROS.copy()
        self.tem.q_h_nodes = ZEROS.copy()
        self.tem.q_c_nodes = ZEROS.copy()
        self.tem.T_c_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node 
        self.tem.T_h_nodes = ZEROS.copy() # initializing array for storing
                                     # temperature (K) in each node
        self.tem.h_nodes = ZEROS.copy()                                     
        self.tem.power_nodes = ZEROS.copy()
        self.tem.eta_nodes = ZEROS.copy()
        
        # for loop iterates of nodes of HX in streamwise direction
        for i in sp.arange(self.nodes):
            print "\nSolving node", i
            self.solve_node(i)

            self.Qdot_nodes[i] = self.Qdot_node
            # storing node heat transfer in array
            self.exh.T_nodes[i] = self.exh.T
            self.exh.h_nodes[i] = self.exh.h
            self.cool.h_nodes[i] = self.cool.h
            self.q_h_nodes[i] = self.q_h
            self.q_c_nodes[i] = self.q_c
            self.tem.q_h_nodes[i] = self.tem.q_h
            self.tem.q_c_nodes[i] = self.tem.q_c
            self.tem.T_h_nodes[i] = self.tem.T_h
            # hot side temperature (K) of TEM at each node 
            self.cool.T_nodes[i] = self.cool.T
            self.tem.T_c_nodes[i] = self.tem.T_c
            # cold side temperature (K) of TEM at each node.  
            self.U_nodes[i] = self.U
            self.U_hot_nodes[i] = self.U_hot
            self.U_cold_nodes[i] = self.U_cold
            self.tem.power_nodes[i] = self.tem.P * self.leg_pairs
            self.tem.eta_nodes[i] = self.tem.eta
            self.tem.h_nodes[i] = self.tem.h

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

        self.Qdot = sp.sum(self.Qdot_nodes)
        self.effectiveness = ( self.Qdot / (self.exh.C *
        (self.exh.T_inlet - self.cool.T_inlet)) )
        # heat exchanger effectiveness
        self.tem.power = sp.sum(self.tem.power_nodes)
        # total TE power output (kW)
        self.Wdot_pumping = self.exh.Wdot_pumping + self.cool.Wdot_pumping
        # total pumping power requirement (kW) 
        self.power_net = self.tem.power - self.Wdot_pumping 
        self.eta_1st = -self.power_net / self.Qdot

    def setup(self):
        """Sets up variables that must be defined before running
        model.  Useful for terminal.  Not necessary elsewhere."""
        self.exh.T = 800.
        self.cool.T = 300. 
        self.set_mdot_charge()
        self.set_constants()
