# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import time
import numpy as np
import matplotlib.pyplot as mpl
import operator
from scipy.optimize import fsolve, fmin#_l_bfgs_b

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
        self.width = 0.55
        # width (cm*10**-2) of HX duct. This model treats duct as
        # parallel plates for simpler modeling. 
        self.length = 0.55
        # length (m) of HX duct
        self.nodes = 25 # number of nodes for numerical heat transfer
                        # model
        self.x0 = np.array([.7,0.02,0.001,4.])
        self.xb = [(0.5,2.), (0.,1.), (1.e-4,20.e-3), (0.1,None)] 
        # initial guess and bounds for x where entries are N/P area,
        # fill fraction, leg length (m), and current (A)
        self.xtol_fmin = 0.01
        self.xmin_file = 'xmin'
        self.T0 = 300.
        # temperature (K) at restricted dead state
        self.equal_width = True

        self.apar_list = [
            ['self','te_pair','leg_area_ratio'],     
            ['self','te_pair','fill_fraction'],
            ['self','te_pair','length'],        
            ['self','te_pair','I']
            ]

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
        self.cool.deltaP_nodes = ZEROS.copy()
        self.cool.Wdot_nodes = ZEROS.copy()

        self.U_nodes = ZEROS.copy()
        self.U_hot_nodes = self.U_nodes.copy()
        self.U_cold_nodes = self.U_nodes.copy()
        self.te_pair.q_h_conv_nodes = ZEROS.copy()
        self.te_pair.q_c_conv_nodes = ZEROS.copy()
        self.te_pair.q_h_nodes = ZEROS.copy()
        self.te_pair.q_c_nodes = ZEROS.copy()

        self.te_pair.error_hot_nodes = ZEROS.copy()
        self.te_pair.error_cold_nodes = ZEROS.copy()

        self.te_pair.T_c_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.te_pair.T_h_nodes = ZEROS.copy()
        # initializing array for storing temperature (K) in each node 
        self.te_pair.h_nodes = self.U_nodes.copy()

        self.te_pair.power_nodes = ZEROS.copy()
        self.te_pair.eta_nodes = ZEROS.copy()

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
        self.x = np.linspace(0, self.length, self.nodes)
        self.node_length = self.length / self.nodes
        # length (m) of each node
        self.area = self.node_length * self.width * self.cool.ducts 
        # area (m^2) through which heat flux occurs in each node
        self.te_pair.set_constants()
        self.leg_pairs = int(self.area / self.te_pair.area)
        # Number of TEM leg pairs per node
        self.x_dim = np.arange(self.node_length / 2, self.length +
        self.node_length / 2, self.node_length)   
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

        if self.equal_width == True:
            self.exh.width = self.width
            self.cool.width = self.width
        self.cool.length = self.length
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

    def solve_node(self,i):
        """Solves for performance of streamwise slice of HX.  The
        argument i is an indexing variable from a for loop within the
        function solve_hx."""

        if self.te_pair.method == 'numerical':
            print "Solving node", i
        
        self.te_pair.T_h_conv = self.exh.T
        self.te_pair.T_c_conv = self.cool.T

        if i == 0:
            self.te_pair.T_c = self.cool.T
            # guess at cold side tem temperature (K)
            self.te_pair.T_h_goal = self.exh.T
            # guess at hot side TEM temperature (K)

            self.te_pair.solve_te_pair_once()

            self.set_convection()
            self.q = self.U * (self.cool.T - self.exh.T)
            
            self.te_pair.T_h_goal = self.q / self.U_hot + self.exh.T
            self.te_pair.T_c = -self.q / self.U_cold + self.cool.T
        else:
            self.set_convection()
            self.te_pair.T_c = self.te_pair.T_c_nodes[i-1]
            self.te_pair.T_h_goal = self.te_pair.T_h_nodes[i-1] 

        self.te_pair.T_guess = np.array([self.te_pair.T_h_goal,self.te_pair.T_c])
        self.te_pair.T_guess = self.te_pair.T_guess.reshape(2) 

        self.te_pair.U_hot = self.U_hot
        self.te_pair.U_cold = self.U_cold

        self.te_pair.solve_te_pair()
        self.q_h = self.te_pair.q_h
        self.q_c = self.te_pair.q_c        

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
        self.exh.node_length = self.node_length
        self.exh.T = self.exh.T_inlet
        # T_inlet and T_outlet correspond to the temperatures going
        # into and out of the heat exchanger.
        if self.type == 'parallel':
            self.cool.T = self.cool.T_inlet
        elif self.type == 'counter':
            self.cool.T = self.cool.T_outlet  
        self.cool.node_length = self.node_length
            
        # for loop iterates of nodes of HX in streamwise direction
        for i in np.arange(self.nodes):
            if self.verbose == True:
                print "\nSolving node", i
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
        self.cool.Wdot_total = self.cool.Wdot_nodes.sum()
        self.Wdot_pumping = ( self.exh.Wdot_total +
                              self.cool.Wdot_total )  
        # total pumping power requirement (kW) 

        self.power_net = ( self.te_pair.power_total -
        self.Wdot_pumping ) 
        
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

        self.cool.enthalpy_nodes = ( self.cool.c_p *
        (self.cool.T_nodes - self.T0) + self.cool.enthalpy0)  
        # enthalpy (kJ/kg*K) of coolant
        self.cool.entropy_nodes = ( self.cool.c_p *
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

        self.te_pair.q_h_conv_nodes[i] = self.q_h
        self.te_pair.q_c_conv_nodes[i] = self.q_c
        self.te_pair.q_h_nodes[i] = self.te_pair.q_h
        self.te_pair.q_c_nodes[i] = self.te_pair.q_c
        self.te_pair.error_hot_nodes[i] = self.te_pair.error_hot
        self.te_pair.error_cold_nodes[i] = self.te_pair.error_cold

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
        self.cool.deltaP_nodes[i] = self.cool.deltaP
        self.cool.Wdot_nodes[i] = self.cool.Wdot_pumping

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

    def get_minpar(self, apar):
	"""Method for returning inverse of net power as a function of
	leg ratio, fill fraction, length, and current.  Use with
	scipy.optimize.fmin to find optimal set of input parameters."""
	# unpack guess vector
        self.opt_iter = self.opt_iter + 1
        if self.opt_iter % 15 == 0:
            print "optimizaton iteration", self.opt_iter
            print "net power", self.power_net
	apar = np.array(apar)

        for i in range(apar.size):
            setattr(operator.attrgetter('.'.join(self.apar_list[i][1:-1]))(self),
            self.apar_list[i][-1], apar[i]) 

        # reset surrogate variables
        self.te_pair.set_all_areas(self.te_pair.Ptype.area,
        self.te_pair.leg_area_ratio, self.te_pair.fill_fraction) 

	self.solve_hx()

        if apar.any() <= 0.: 
            minpar = np.abs(self.power_net)**3 + 100.  
            # penalizes negative parameters

        elif self.power_net <= 0.:
            minpar = np.abs(self.power_net)**3 + 100.
            # penalizes negative power

        else:
            minpar = 1. / self.power_net

	return minpar

    def optimize(self):
	"""Uses fmin to find optimal set of:
	I) tem.leg_area_ratio
	II) tem.fill_fraction
	III) hx.te_pair.length
	IV) hx.te_pair.I
        V) fin spacing if value for initial guess is given in kwarg
        ...maybe some others as determined by kwargs

	This is based on minimizing the inverse of power.  This may be
	a bad method if net power is negative.

	self.x0 and self.xb must be defined elsewhere"""
	
	time.clock()

        # dummy function that might be used with minimization 
        def fprime():
            return 1

        self.opt_iter = 0

        self.x0 = np.zeros(len(self.apar_list))

        for i in range(self.x0.size):
            self.x0[i] = (
            operator.attrgetter('.'.join(self.apar_list[i][1:]))(self)
            ) 

        self.xmin = fmin(self.get_minpar, self.x0,
                         xtol=self.xtol_fmin)  
	# self.xmin = fmin_l_bfgs_b(self.get_inv_power, self.x0, fprime=None,
	# approx_grad=True, bounds=self.xb)
	t1 = time.clock() 
        
        print '\n'
        for i in range(self.x0.size):
            varname = '.'.join(self.apar_list[i][1:])
            varval = (
                operator.attrgetter(varname)(self)
        ) 
            print varname + ":", varval

        print "\npower net:", self.power_net * 1000., 'W'
        print "power raw:", self.te_pair.power_total * 1000., 'W'
        print "pumping power:", self.Wdot_pumping * 1000., 'W'
        self.exh.volume = self.exh.height * self.exh.width * self.length
        print "exhaust volume:", self.exh.volume * 1000., 'L'
        print "exhaust power density:", self.power_net / self.exh.volume, 'kW/m^3'

	print """Elapsed time solving xmin1 =""", t1

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
    
