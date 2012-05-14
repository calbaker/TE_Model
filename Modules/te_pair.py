# Distribution modules

import types
import numpy as np
import matplotlib.pyplot as mpl
import time
from scipy.optimize import fsolve
from scipy.integrate import odeint

# User defined modules
import te_prop
reload(te_prop)
import leg
reload(leg) 


class TE_Pair(object):
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.leg_area_ratio = 0.7
        self.fill_fraction = 0.02
        self.length = 1.e-3
        self.I = 1. # electrical current (Amps)
        self.Ptype = leg.Leg() # p-type instance of leg
        self.Ntype = leg.Leg() # n-type instance of leg
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3)**2 # void area (m^2)
        self.length = 1.e-3 # default leg height (m)
        self.nodes = 10
        self.method = "numerical"

    def set_constants(self):
        """Sets constants that are calculated."""

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
        self.Ntype.method = self.method
        self.Ptype.method = self.method

    def solve_te_pair_once(self):
        """solves legs and combines results of leg pair"""
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

    def get_error(self,knob_arr):
        """Returns hot and cold side error.  This doc string needs
        work.""" 

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
        """Sets cold side guess for both Ntype and Ptype legs."""
        self.Ntype.set_q_c_guess()
        self.Ptype.set_q_c_guess()

    def solve_te_pair(self):
        """solves legs and combines results of leg pair"""

        self.set_q_c_guess()
        knob_arr0 = np.array([self.Ntype.q_c_guess,
        self.Ptype.q_c_guess, self.T_c_conv])  

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
        """Sets properties for both legs based on temperature of
        module."""
        self.Ntype.set_TEproperties(T_props)
        self.Ptype.set_TEproperties(T_props)

    def set_ZT(self):
        """Sets ZT based on whatever properties were used last."""
        self.ZT = ( ((self.Ptype.alpha - self.Ntype.alpha) /
        ((self.Ptype.rho * self.Ptype.k)**0.5 + (self.Ntype.rho *
        self.Ntype.k)**0.5))**2. * self.T_props )

    def set_eta_max(self):
        """Sets theoretical maximum efficiency with material
        properties evaluated at the average temperature based on
        Sherman's analysis."""
        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        self.set_ZT()
        delta_T = self.T_h - self.T_c
        self.eta_max = ( delta_T / self.T_h * ((1. + self.ZT)**0.5 -
        1.) / ((1. + self.ZT)**0.5 + self.T_c / self.T_h) ) 
                
    def set_area(self):
        """Sets new N-type and P-type area based on desired area
        ratio. Ensures that sum of N-type and P-type area is
        constant.""" 
        area = self.Ntype.area + self.Ptype.area
        self.Ptype.area = area / (1. + self.leg_area_ratio)
        self.Ntype.area = area - self.Ptype.area

    def set_A_opt(self):
        """Sets Ntype / Ptype area that results in maximum efficiency
        based on material properties evaluated at the average
        temperature."""
        self.set_TEproperties(T_props=self.T_props)
        self.A_opt = np.sqrt(self.Ntype.rho * self.Ptype.k /
        (self.Ptype.rho * self.Ntype.k))

    def set_power_max(self):
        """Sets power factor and maximum theoretical power."""
        self.Ntype.set_power_factor()
        self.Ptype.set_power_factor()
        self.power_max = self.Ntype.power_max + self.Ptype.power_max 
    
    def set_all_areas(self, leg_area, leg_area_ratio, fill_fraction):
        """Sets leg areas and void area based on leg area ratio and
        fill fraction. 

        Arguments
        ----------------
        leg_area : base area of P-type leg
        leg_area_ratio : N/P area ratio
        fill_fraction : fraction of area taken up by legs"""

        self.leg_area_ratio = leg_area_ratio
        self.fill_fraction = fill_fraction

        self.Ptype.area = leg_area                           
        self.Ntype.area = self.Ptype.area * leg_area_ratio
        self.area_void = ( (1. - fill_fraction) / fill_fraction *
        (self.Ptype.area + self.Ntype.area) )  
        
