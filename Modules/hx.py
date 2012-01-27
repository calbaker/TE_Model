# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import time
import numpy as np
import matplotlib.pyplot as mpl
from scipy.optimize import fsolve,fmin

# User Defined Modules
# In this directory
import engine
import te_pair
reload(te_pair)
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
        self.width = 10.e-2
        # width (cm*10**-2) of HX duct. This model treats duct as
        # parallel plates for simpler modeling. 
        self.length = 20.e-2
        # length (m) of HX duct
        self.nodes = 25 # number of nodes for numerical heat transfer
                        # model
        self.x = np.linspace(0, self.length, self.nodes)
        self.xtol = 0.01
        self.x0 = np.array([.7,0.02,0.001,4.])
        self.xmin_file = 'xmin'
        self.T0 = 300.
        # temperature (K) at restricted dead state

        # initialization of sub classes
        self.cool = coolant.Coolant()
        self.exh = exhaust.Exhaust()
        self.te_pair = te_pair.TE_Pair()
        self.plate = platewall.PlateWall()
        self.cummins = engine.Engine()

        self.arrangement = 'single'

        self.fix_geometry()

    def init_arrays(self):
        """Initializes a whole bunch of arrays for storing node
        values."""

        ZEROS = np.zeros(self.nodes)
        self.Qdot_nodes = ZEROS.copy()
        # initialize array for storing heat transfer (kW) in each node 
        
        self.exh.Vdot_nodes = ZEROS.copy()

        self.exh.T_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.exh.h_nodes = ZEROS.copy()
        self.exh.f_nodes = ZEROS.copy()
        self.exh.deltaP_nodes = ZEROS.copy()
        self.exh.Wdot_nodes = ZEROS.copy()
        self.exh.Nu_nodes = ZEROS.copy()
        self.exh.c_p_nodes = ZEROS.copy()
        self.exh.entropy_nodes = ZEROS.copy()
        self.exh.enthalpy_nodes = ZEROS.copy()

        self.cool.T_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.cool.entropy_nodes = ZEROS.copy()
        self.cool.enthalpy_nodes = ZEROS.copy()

        self.U_nodes = ZEROS.copy()
        self.U_hot_nodes = self.U_nodes.copy()
        self.U_cold_nodes = self.U_nodes.copy()
        self.q_h_nodes = ZEROS.copy()
        self.q_c_nodes = self.q_h_nodes.copy()
        self.te_pair.q_h_nodes = self.q_h_nodes.copy()
        self.te_pair.q_c_nodes = self.q_h_nodes.copy()

        self.error_hot_nodes = ZEROS.copy()
        self.error_cold_nodes = ZEROS.copy()

        self.te_pair.T_c_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.te_pair.T_h_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.te_pair.h_nodes = self.U_nodes.copy()

        self.te_pair.power_nodes = ZEROS.copy()
        self.te_pair.eta_nodes = ZEROS.copy()

        self.exh.velocity_nodes = ZEROS.copy()
        self.exh.mdot_nodes = ZEROS.copy()

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
        self.area = self.node_length * self.width * self.cool.ducts 
        # area (m^2) through which heat flux occurs in each node
        self.te_pair.set_constants()
        self.leg_pairs = int(self.area / self.te_pair.area)
        # Number of TEM leg pairs per node
        self.x_dim = np.arange(self.node_length/2, self.length +
        self.node_length/2, self.node_length)   
        # x coordinate (m)
        self.fix_geometry()
        self.exh.set_flow_geometry(self.exh.width) 
        self.cool.set_flow_geometry(self.cool.width)

    def fix_geometry(self):
        """Makes sure that common geometry like width and length is
        the same between exh, cool, and the overal heat exchanger.

        Notes: Exhaust duct length is equal to node_length because
        everything about the exhaust is evaluated in each node, but
        coolant duct length is equal to total length because the
        coolant has constant properties throughout the hx."""

        self.cool.width = self.width
        self.cool.length = self.length
        self.exh.width = self.width
        self.exh.length = self.length / self.nodes 

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
        self.plate.R_contact + self.te_pair.R_thermal + self.plate.R_contact +
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

    def get_error(self,T_arr):
        """Returns hot and cold side error.  This doc string needs
        work.""" 
        T_h = T_arr[0]
        T_h = T_h
        self.q_h = self.U_hot * (T_h - self.exh.T)
        self.te_pair.T_h_goal = T_h
        self.te_pair.solve_tem()
        self.error_hot = (self.q_h - self.te_pair.q_h) / self.te_pair.q_h

        T_c = T_arr[1]
        T_c = T_c
        self.q_c = self.U_cold * (self.cool.T - T_c)
        self.te_pair.T_c = T_c
        self.te_pair.solve_tem()
        self.error_cold = (self.q_c - self.te_pair.q_c) / self.te_pair.q_c

        self.error = np.array([self.error_hot, self.error_cold])
        return self.error

    def solve_node(self,i):
        """Solves for performance of streamwise slice of HX.  The
        argument i is an indexing variable from a for loop within the
        function solve_hx."""
        self.te_pair.Ntype.node = i # used within tem.py
        self.te_pair.Ptype.node = i
        if self.te_pair.method == 'numerical':
            print "Solving node", i
        
        if i == 0:
            self.te_pair.T_c = self.cool.T
            # guess at cold side tem temperature (K)
            self.te_pair.T_h_goal = self.exh.T
            # guess at hot side TEM temperature (K)
            self.te_pair.solve_tem()
            self.set_convection()
            self.q = self.U * (self.cool.T - self.exh.T)
            self.te_pair.T_h_goal = self.q / self.U_hot + self.exh.T
            self.te_pair.T_c = -self.q / self.U_cold + self.cool.T
        else:
            self.set_convection()
            self.te_pair.T_c = self.te_pair.T_c_nodes[i-1]
            self.te_pair.T_h_goal = self.te_pair.T_h_nodes[i-1] 

        self.T_guess = np.array([self.te_pair.T_h_goal,self.te_pair.T_c])
        self.T_guess = self.T_guess.reshape(2)
        self.T_arr = fsolve(self.get_error, x0=self.T_guess,
        xtol=self.xtol) 
        self.te_pair.T_h_goal = self.T_arr[0]
        self.te_pair.T_c = self.T_arr[1]
        self.Qdot_node = -self.q_h * self.area
        # heat transfer on hot side of node, positive values indicates
        # heat transfer from hot to cold
            
    def solve_hx(self,**kwargs): # solve parallel flow heat exchanger
        """solves for performance of entire HX"""

        self.init_arrays()
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
            
        self.te_pair.Ptype.set_prop_fit()
        self.te_pair.Ntype.set_prop_fit()

        if self.arrangement == 'harmonica':
            self.exh.mdot_nodes = np.arange(self.nodes, 0, self.nodes
            + 1) / self.nodes * self.exh.mdot

        # for loop iterates of nodes of HX in streamwise direction
        for i in np.arange(self.nodes):
            if self.verbose == True:
                print "\nSolving node", i
            if self.arrangement == 'harmonica':
                self.exh.mdot = self.exh.mdot[i]
            self.solve_node(i)
            self.store_node_values(i)

            # redefining temperatures (K) for next node
            self.exh.T = ( self.exh.T + self.te_pair.q_h * self.area /
                self.exh.C )   
            if self.type == 'parallel':
                self.cool.T = ( self.cool.T - self.te_pair.q_c * self.area
                    / self.cool.C )  
            elif self.type == 'counter':
                self.cool.T = ( self.cool.T + self.te_pair.q_c * self.area
                    / self.cool.C )
                
        # defining HX outlet/inlet temperatures (K)
        self.exh.T_outlet = self.exh.T
        if self.type == 'parallel':
            self.cool.T_outlet = self.cool.T
        elif self.type == 'counter':
            self.cool.T_inlet = self.cool.T

        self.Qdot_total = self.Qdot_nodes.sum()
        self.effectiveness = ( self.Qdot_total / (self.exh.C *
        (self.exh.T_inlet - self.cool.T_inlet)) )
        # heat exchanger effectiveness
        self.te_pair.power_total = self.te_pair.power_nodes.sum()
        # total TE power output (kW)
        self.exh.Wdot_total = self.exh.Wdot_nodes.sum()
        self.Wdot_pumping = ( self.exh.Wdot_pumping +
        self.cool.Wdot_pumping ) 
        # total pumping power requirement (kW) 
        self.power_net = self.te_pair.power_total - self.Wdot_pumping 
        
        self.set_availability()

    def set_availability(self):
        """Runs at end of analysis to determine availability of
        coolant and exhaust everywhere."""

        # Availability analysis
        self.exh.enthalpy0 = self.exh.get_enthalpy(self.T0)
        # enthalpy (kJ/kg) of exhaust at restricted dead state
        self.exh.entropy0 = self.exh.get_entropy(self.T0)
        # entropy (kJ/kg*K) of exhuast at restricted dead state

        self.exh.availability_flow_nodes = ( (self.exh.enthalpy_nodes
        - self.exh.enthalpy0 - self.T0 * (self.exh.entropy_nodes -
        self.exh.entropy0)) * self.exh.mdot ) 
        # availability (kJ/kg) of exhaust

        self.cool.enthalpy_nodes = ( self.cool.c_p_nodes *
        (self.cool.T_nodes - self.T0) + self.cool.enthalpy0) 
        # enthalpy (kJ/kg*K) of coolant
        self.cool.entropy_nodes = ( self.cool.c_p_nodes *
        np.log(self.cool.T_nodes / self.T0) + self.cool.entropy0 ) 

        self.cool.availability_flow_nodes = (
        (self.cool.enthalpy_nodes - self.cool.enthalpy0 - self.T0 *
        (self.cool.entropy_nodes - self.cool.entropy0)) *
        self.cool.mdot) 
        # availability (kJ/kg) of coolant

    def store_node_values(self,i):
        """Storing solved values in array to keep track of what
        happens in every node."""
        self.Qdot_nodes[i] = self.Qdot_node
        # storing node heat transfer in array

        self.q_h_nodes[i] = self.q_h
        self.q_c_nodes[i] = self.q_c
        self.te_pair.q_h_nodes[i] = self.te_pair.q_h
        self.te_pair.q_c_nodes[i] = self.te_pair.q_c
        self.error_hot_nodes[i] = self.error_hot
        self.error_cold_nodes[i] = self.error_cold

        self.exh.T_nodes[i] = self.exh.T

        self.exh.Vdot_nodes[i] = self.exh.Vdot
        self.exh.f_nodes[i] = self.exh.f
        self.exh.deltaP_nodes[i] = self.exh.deltaP
        self.exh.Wdot_nodes[i] = self.exh.Wdot_pumping

        self.exh.Nu_nodes[i] = self.exh.Nu_D
        self.exh.c_p_nodes[i] = self.exh.c_p 
        self.exh.h_nodes[i] = self.exh.h

        self.exh.entropy_nodes[i] = self.exh.entropy
        self.exh.enthalpy_nodes[i] = self.exh.enthalpy

        self.cool.T_nodes[i] = self.cool.T

        self.te_pair.T_h_nodes[i] = self.te_pair.T_h
        # hot side temperature (K) of TEM at each node 
        self.te_pair.T_c_nodes[i] = self.te_pair.T_c
        # cold side temperature (K) of TEM at each node.  

        self.U_nodes[i] = self.U
        self.U_hot_nodes[i] = self.U_hot
        self.U_cold_nodes[i] = self.U_cold

        self.te_pair.power_nodes[i] = self.te_pair.P * self.leg_pairs
        self.te_pair.eta_nodes[i] = self.te_pair.eta
        self.te_pair.h_nodes[i] = self.te_pair.h

        self.exh.velocity_nodes[i] = self.exh.velocity

    def get_inv_power(self,apar):
	"""Method for returning inverse of net power as a function of
	leg ratio, fill fraction, length, and current.  Use with
	scipy.optimize.fmin to find optimal set of input parameters."""
	# unpack guess vector
	apar=np.asarray(apar)
	self.te_pair.leg_ratio     = apar[0]
	self.te_pair.fill_fraction = apar[1]
	self.te_pair.length        = apar[2]
	self.te_pair.I             = apar[3]

	# reset surrogate variables
	self.te_pair.Ntype.area = self.te_pair.leg_ratio * self.te_pair.Ptype.area
	self.te_pair.area_void = ( (1. - self.te_pair.fill_fraction) /
	self.te_pair.fill_fraction * (self.te_pair.Ptype.area + self.te_pair.Ntype.area)
	)
	self.set_constants()
	self.solve_hx()

	# 1/power_net 
	return 1. / (self.te_pair.power_total)

    def optimize(self):
	"""Uses fmin to find optimal set of:
	I) tem.leg_ratio
	II) tem.fill_fraction
	III) hx.te_pair.length
	IV) hx.te_pair.I
	based on minimizing the inverse of power.  This may be a bad
	method if net power is negative.

	self.x0 must be defined elsewhere"""
	
	time.clock()

	self.te_pair.method = 'analytical'
	self.xmin1 = fmin(self.get_inv_power, self.x0)
	t1 = time.clock() 
	print """xmin1 found. Switching to numerical model.
	Elapsed time solving xmin1 =""", t1

	self.te_pair.method = 'numerical'
	self.xmin2 = fmin(self.get_inv_power, self.xmin1)
	t2 = time.clock() - t1
	print """xmin2 found.
	Elapsed time solving xmin2 =""", t2

	t = time.clock()
	print """Total elapsed time =""", t 

	print """Writing to output/optimize/xmin1 and output/optimize/xmin2"""

	np.savetxt('output/optimize/'+self.xmin_file+'1', self.xmin1)
	np.savetxt('output/optimize/'+self.xmin_file+'2', self.xmin2)

    def get_T_inlet_error(self, T_outlet):
	"""Returns error for coolant inlet temperature from desired
	setpoint for the counter flow configuration in which the
	outlet coolant temperaure is specified.  Should be used with
	fsolve to determine the correct inlet temperature for the
	coolant.

	Inputs: hx instance and outlet coolant temperature"""

	self.cool.T_outlet = np.float(T_outlet)
	self.solve_hx()
	error = self.cool.T_inlet_set - self.cool.T_inlet
	return error
