# Distribution modules

import numpy as np
import time

# User defined modules
import mat_prop
reload(mat_prop)
import leg
reload(leg)


class TE_Pair(object):
    """Class definition for TE leg pair with convection BC

    Methods:

    __init__
    get_error
    set_A_opt
    set_TEproperties
    set_ZT
    set_all_areas
    set_area
    set_constants
    set_eta_max
    set_power_max
    set_q_c_guess
    solve_te_pair
    solve_te_pair_once

    """

    def __init__(self):

        """Sets attributes and instantiates classes.

        Class instances:

        self.Ptype = leg.Leg()
        self.Ntype = leg.Leg()

        Methods:

        self.set_constants

        """

        self.leg_area_ratio = 0.7
        # Ratio of cross-section area of N-type leg to cross-section
        # area of P-type leg
        self.fill_fraction = 0.02
        # Percentage of nominal area occupied by TE legs
        self.length = 1.e-3
        # Length (m) of TE legs
        self.I = 1.  # electrical current (Amps)
        self.Ptype = leg.Leg()
        self.Ntype = leg.Leg()
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3) ** 2
        # void area (m^2) associated with each leg pair
        self.length = 1.e-3
        self.nodes = 10
        #  number of nodes for which the temperature values are
        #  returned by odeint.  This does not affect the actual
        #  calculation, only the values for which results are stored.

        self.set_constants()

    def set_constants(self):

        """Sets a bunch of attributes that are usually held constant.

        Methods:

        self.Ntype.set_constants
        self.Ptype.set_constants

        """

        self.area = self.Ntype.area + self.Ptype.area + self.area_void
        self.Ntype.length = self.length
        self.Ptype.length = self.length
        self.Ptype.nodes = self.nodes
        self.Ntype.nodes = self.nodes
        self.Ptype.I = -self.I
        # Current must have same sign as heat flux for p-type
        # material. Heat flux is negative because temperature gradient
        # is positive.  
        self.Ntype.I = self.I
        self.Ntype.set_constants()
        self.Ptype.set_constants()

    def solve_te_pair_once(self):

        """Solves legs and combines results of leg pair. 
        
        Methods:

        self.Ntype.solve_leg_once
        self.Ptype.solve_leg_once

        """

        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c

        self.Ntype.solve_leg_once(self.Ntype.q_c)
        self.Ptype.solve_leg_once(self.Ptype.q_c)
        self.T_h = self.Ntype.T_h

        self.q_h = ((self.Ptype.q_h * self.Ptype.area + self.Ntype.q_h
        * self.Ntype.area) / (self.area)) * 0.001
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ((self.Ptype.q_c * self.Ptype.area + self.Ntype.q_c
        * self.Ntype.area) / (self.area)) * 0.001
        # area averaged hot side heat flux (kW/m^2)

        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1. / self.h

    def get_error(self, knob_arr):

        """Returns BC error.

        This function uses guesses at the cold side temperature and
        heat fluxes for both legs to solve the pair a single time.
        The resulting errors in boundary conditions are then
        determined. This is then used by fsolve in solve_te_pair.
        
        Methods:

        self.solve_te_pair_once

        """ 

        self.Ntype.q_c = knob_arr[0]
        self.Ptype.q_c = knob_arr[1]
        self.T_c = knob_arr[2]

        self.solve_te_pair_once()

        self.q_c_conv = self.U_cold * (self.T_c_conv - self.T_c)
        self.q_h_conv = - self.U_hot * (self.T_h_conv - self.T_h)

        T_error = self.Ntype.T_h - self.Ptype.T_h 
        q_c_error = self.q_c - self.q_c_conv
        q_h_error = self.q_h - self.q_h_conv

        self.error = np.array([T_error, q_c_error, q_h_error])
        self.error = self.error.reshape(self.error.size)  

        return self.error

    def set_q_c_guess(self):

        """Sets cold side guess for both Ntype and Ptype legs.

        Methods:

        self.Ntype.set_q_c_guess
        self.Ptype.set_q_c_guess 

        """

        self.Ntype.set_q_c_guess()
        self.Ptype.set_q_c_guess()

    def solve_te_pair(self):

        """Solves legs and combines results of leg pair.

        Methods:

        self.set_q_c_guess

        """
        
        self.set_q_c_guess()
        knob_arr0 = np.array([self.Ntype.q_c_guess,
        self.Ptype.q_c_guess, self.T_c_conv])  

        from scipy.optimize import fsolve

        self.fsolve_output = fsolve(self.get_error, x0=knob_arr0)

        self.P = -(self.Ntype.P + self.Ptype.P) * 0.001 
        # power for the entire leg pair(kW). Negative sign makes this
        # a positive number. Heat flux is negative so efficiency needs
        # a negative sign also.  
        self.P_flux = self.P / self.area
        # power flux (kW / m^2) through leg pair
        self.eta = -self.P / (self.q_h * self.area)
        self.V = self.Ntype.V + self.Ptype.V
        self.R_load = self.Ntype.R_load + self.Ptype.R_load
        self.R_internal = ( self.Ntype.R_internal +
        self.Ptype.R_internal )

    def set_TEproperties(self, T_props):

        """Sets properties for both legs based on temperature.

        Methods:

        self.Ntype.set_TEproperties(T_props)
        self.Ptype.set_TEproperties(T_props)

        """

        self.Ntype.set_TEproperties(T_props)
        self.Ptype.set_TEproperties(T_props)

    def set_ZT(self):

        """Sets ZT based on whatever properties were used last."""

        self.ZT = ( ((self.Ptype.alpha - self.Ntype.alpha) /
        ((self.Ptype.rho * self.Ptype.k) ** 0.5 + (self.Ntype.rho *
        self.Ntype.k) ** 0.5)) ** 2. * self.T_props )

    def set_eta_max(self):

        """Sets theoretical maximum efficiency.

        Methods:

        self.set_TEproperties(T_props)

        Uses material properties evaluated at the average temperature
        based on Sherman's analysis.

        """

        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        self.set_ZT()
        delta_T = self.T_h - self.T_c
        self.eta_max = ( delta_T / self.T_h * ((1. + self.ZT) ** 0.5 -
        1.) / ((1. + self.ZT) ** 0.5 + self.T_c / self.T_h) ) 
                
    def set_A_opt(self):

        """Sets Ntype / Ptype area that results in max efficiency.  

        Methods:
        
        self.set_TEproperties(T_props)

        Based on material properties evaluated at the average
        temperature.

        """ 

        self.set_TEproperties(T_props=self.T_props)
        self.A_opt = np.sqrt(self.Ntype.rho * self.Ptype.k /
        (self.Ptype.rho * self.Ntype.k))

    def set_power_max(self):

        """Sets power factor and maximum theoretical power.

        Methods:

        self.Ntype.set_power_factor
        self.Ptype.set_power_factor

        """

        self.Ntype.set_power_factor()
        self.Ptype.set_power_factor()
        self.power_max = self.Ntype.power_max + self.Ptype.power_max 
    
    def set_leg_areas(self):

        """Sets leg areas and void area.

        Based on leg area ratio and fill fraction.

        Methods:

        self.set_constants

        """

        leg_area_ratio = self.leg_area_ratio 
        fill_fraction = self.fill_fraction 

        self.Ntype.area = self.Ptype.area * leg_area_ratio
        self.area_void = ( (1. - fill_fraction) / fill_fraction *
        (self.Ptype.area + self.Ntype.area) )  

        self.set_constants()

    def get_minpar(self, apar):

	"""Returns inverse of power flux. 

        Methods:

        self.set_leg_areas

        Used by method self.optimize

        self.length = apar[0]
        self.fill_fraction = apar[1]
        self.I = apar[2]
        self.leg_area_ratio = apar[3]

        Use with scipy.optimize.fmin to find optimal set of input
        parameters.

        This method uses power flux rather than power because for
        optimal power, leg height approaches zero and void area
        approaches infinity.  This trivial result is not useful."""

        self.opt_iter = self.opt_iter + 1
        if self.opt_iter % 15 == 0:
            print "optimizaton iteration", self.opt_iter
            print "power", self.P
	apar = np.array(apar)

        self.length = apar[0]
        self.fill_fraction = apar[1]
        self.I = apar[2]
        self.leg_area_ratio = apar[3]

        # reset surrogate variables
        self.set_leg_areas()

	self.solve_te_pair()

        if (apar <= 0.).any(): 
            minpar = np.abs(self.P_flux) ** 3. + 100

        else:
            minpar = - self.P_flux 

	return minpar

    def optimize(self):

	"""Minimizes self.get_minpar 

        Methods:

        self.get_minpar
        
        self.x0 and self.xb must be defined elsewhere."""
	
	time.clock()

        # dummy function that might be used with minimization 
        def fprime():
            return 1

        self.opt_iter = 0

        self.x0 = np.array([self.length, self.fill_fraction,
        self.I, self.leg_area_ratio]) 

        from scipy.optimize import fmin

        self.xmin = fmin(self.get_minpar, self.x0)

	t1 = time.clock() 
        
        print '\n'
        
        print "Optimized parameters:"
        print "leg length =", self.length, "m"
        print "fill fraction =", self.fill_fraction * 100., "%"
        print "current =", self.I, "A"
        print "area ratio =", self.leg_area_ratio
        
        print "\npower:", self.P * 1000., 'W'

	print """Elapsed time solving xmin1 =""", t1
