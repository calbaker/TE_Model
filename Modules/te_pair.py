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

class Leg(object):
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """Sets the following: 
        self.I : current (A) in TE leg pair
        self.segments : number of segments for finite difference model
        self.length : leg length (m)
        self.area = : leg area (m^2)
        self.T_h_goal : hot side temperature (K) that matches HX BC
        self.T_c : cold side temperature (K)
        self.T : initial array for temperature (K) for finite
        difference model
        self.q : initial array for heat flux (W/m^2)
        self.V_segment : initial array for Seebeck voltage (V)
        self.P_flux_segment : initial array for power flux in segment (W/m^2)
        self.xtol : tolerable fractional error in hot side temperature

        Binds the following methods:
        te_prop.set_prop_fit
        te_prop.set_TEproperties"""
    
        self.I = 0.5 
        self.segments = 25 
        self.length = 1.e-3
        self.area = (3.e-3)**2. 
        self.T_h_goal = 550. 
        self.T_c = 350. 
        self.T = np.zeros(self.segments) 
        self.q = np.zeros(self.segments) 
        self.V_segment = np.zeros(self.segments) 
        self.P_flux_segment = np.zeros(self.segments) 
        self.xtol = 1.

        self.set_prop_fit = types.MethodType(te_prop.set_prop_fit,
        self) 
        self.set_TEproperties = (
        types.MethodType(te_prop.set_TEproperties, self) )
    
    def set_q_c_guess(self):
        self.solve_leg_anal()
        self.q_c_guess = self.q_c

    def solve_leg(self):
        """Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006. The model guesses a cold
        side heat flux and changes that heat flux until it results in
        the desired hot side temperature.  Hot side and cold side
        temperature as well as hot side heat flux must be
        specified.""" 
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        self.x = np.linspace(0., self.segment_length, self.segments) 

        self.J = self.I / self.area # (Amps/m^2)

        if self.method == "numerical":
            self.T[0] = self.T_c

            self.T_props = self.T[0]
            self.set_TEproperties(T_props=self.T_props)

            # Do some stuff with integrate.odeint here
            
            def get_Yprime(y, x):
                """Function for evaluating the derivatives of
                temperature and heat flux w.r.t. x."""

                self.T = y[0]
                self.q = y[1]

                self.dTdx = ( 1. / self.k * (self.J * self.T * self.alpha -
                self.q) )  

                self.dqdx = ( (self.rho * self.J**2. * (1. +
                self.alpha**2. * self.T / (self.rho * self.k)) -
                self.J * self.alpha * self.q / self.k) )     
            
                
            y0 = np.array([self.T_c, self.q_c])
            y = odeint(get_Yprime, y0=y0, t=self.x) 

        #         self.V_segment[j] = ( self.alpha * (self.T[j] -
        # self.T[j-1]) + self.J * self.rho * self.segment_length )
        #     self.R_int_seg = ( self.rho * self.segment_length /
        # self.area )
        #     self.P_flux_segment[j] = self.J * self.V_segment[j]
            
            self.V = self.V_segment.sum() 
            self.P = self.P_flux_segment.sum() * self.area
            # Power for the entire leg (W)
            self.eta = self.P / (self.q_h * self.area)
            # Efficiency of leg
            self.R_internal = self.R_int_seg.sum()

        if self.method == "analytical":
            self.solve_leg_anal()

        self.R_load = - self.V / self.I
            
    def solve_leg_anal(self):
        """Analytically solves the leg based on lumped properties.  No
        iteration is needed."""
        self.T_h = self.T_h_goal
        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        delta_T = self.T_h - self.T_c
        self.q_h = ( self.alpha * self.T_h * self.J - delta_T /
                     self.length * self.k + self.J**2. * self.length * self.rho
                     / 2. ) 
        self.q_c = ( self.alpha * self.T_c * self.J - delta_T /
                     self.length * self.k - self.J**2 * self.length * self.rho )
        self.P_flux = ( (self.alpha * delta_T * self.J + self.rho *
                         self.J**2 * self.length) ) 
        self.P = self.P_flux  * self.area
        self.eta = self.P / (self.q_h * self.area)
        self.eta_check = ( (self.J * self.alpha * delta_T + self.rho *
                            self.J**2. * self.length) / (self.alpha *
                            self.T_h * self.J - delta_T / self.length
                            * self.k + self.J**2 * self.length *
                            self.rho / 2.) ) 
        self.V = -self.P / np.abs(self.I)
        self.R_internal = self.rho * self.length / self.area

    def set_ZT(self):
        """Sets ZT based on formula
        self.ZT = self.sigma * self.alpha**2. / self.k""" 
        self.ZT = self.alpha**2. * self.T_props / (self.k * self.rho)

    def set_power_factor(self):
        """Sets power factor and maximum theoretical power for leg."""
        self.power_factor = self.alpha**2 * self.sigma
        self.power_max = ( self.power_factor * self.T_props**2 /
        self.length * self.area ) 


class TE_Pair(object):
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.leg_area_ratio = 0.7
        self.fill_fraction = 0.02
        self.length = 1.e-3
        self.I = 1. # electrical current (Amps)
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3)**2 # void area (m^2)
        self.length = 1.e-3 # default leg height (m)
        self.segments = 25
        self.xtol_fsolve = 0.01
        self.method = "numerical"

    def set_constants(self):
        """Sets constants that are calculated."""
        self.area = self.Ntype.area + self.Ptype.area + self.area_void 
        self.Ntype.length = self.length
        self.Ptype.length = self.length
        self.Ptype.segments = self.segments
        self.Ntype.segments = self.segments
        self.Ptype.I = -self.I
        # Current must have same sign as heat flux for p-type
        # material. Heat flux is negative because temperature gradient
        # is positive.  
        self.Ntype.I = self.I
        self.Ntype.method = self.method
        self.Ptype.method = self.method

    def solve_te_pair_once(self):
        """solves legs and combines results of leg pair"""
        self.Ptype.T_h_goal = self.T_h_goal
        self.Ntype.T_h_goal = self.T_h_goal
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c
        self.Ntype.solve_leg()
        self.Ptype.solve_leg()
        self.T_h = self.Ntype.T_h

        self.q_h = ((self.Ptype.q_h * self.Ptype.area + self.Ntype.q_h
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void)) * 0.001
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ((self.Ptype.q_c * self.Ptype.area + self.Ntype.q_c
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void)) * 0.001
        # area averaged hot side heat flux (kW/m^2)

        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1. / self.h

    def get_error(self,T_arr):
        """Returns hot and cold side error.  This doc string needs
        work.""" 
        T_h = T_arr[0]
        T_c = T_arr[1]

        self.q_h_conv = self.U_hot * (T_h - self.T_h_conv)
        self.T_h_goal = T_h

        self.q_c_conv = self.U_cold * (self.T_c_conv - T_c)
        self.T_c = T_c

        self.solve_te_pair_once()

        self.error_hot = ( (self.q_h_conv - self.q_h) /
        self.q_h )

        self.error_cold = ( (self.q_c_conv - self.q_c) /
        self.q_c )
 
        self.error = np.array([self.error_hot,
        self.error_cold])
        self.error = self.error.reshape(self.error.size)  

        return self.error

    def solve_te_pair(self):
        """solves legs and combines results of leg pair"""
        self.fsolve_output = fsolve(self.get_error, x0=self.T_guess,
        xtol=self.xtol_fsolve)

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
        self.T_props = 0.5 * (self.T_h_goal + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        self.set_ZT()
        delta_T = self.T_h_goal - self.T_c
        self.eta_max = ( delta_T / self.T_h_goal * ((1. +
        self.ZT)**0.5 - 1.) / ((1. + self.ZT)**0.5 + self.T_c /
        self.T_h_goal) )
                
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
        
