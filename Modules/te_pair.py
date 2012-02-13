# Distribution modules

import types
import numpy as np
import matplotlib.pyplot as mpl
import time
from scipy.optimize import fsolve

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
        if self.node == 0:
            self.q_c_guess = ( -self.k / self.length * (self.T_h_goal
        - self.T_c) )   
            # (W/m^2) guess for q[0] (W/m^2)
        else:
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
        self.J = self.I / self.area # (Amps/m^2)

        if self.method == "numerical":
            self.T[0] = self.T_c
            self.T_props = self.T[0]
            self.set_TEproperties(T_props=self.T_props)
            self.set_q_c_guess()
            self.q_c = fsolve(self.get_T_h_error_numerical,
            x0=self.q_c_guess, xtol=self.xtol)  
            # the previous line runs get_T_h_error_numerical with the
            # correct value of q_c so there is no need to run it
            # again.  In addition, get_T_h_error_numerical runs the
            # finite difference method that solves for the
            # temperature, heat flux, and power flux profile in the
            # leg.  
            self.V = self.V_segment.sum()
            self.P = self.P_flux_segment.sum() * self.area
            # Power for the entire leg (W)
            self.eta = self.P / (self.q_h * self.area)
            # Efficiency of leg
            self.R_internal = self.R_int_seg.sum()

        if self.method == "analytical":
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
            self.J**2. * self.length) / (self.alpha * self.T_h * self.J -
            delta_T / self.length * self.k + self.J**2 * self.length *
            self.rho / 2.) )
            self.V = -self.P / np.abs(self.I)
            self.R_internal = self.rho * self.length / self.area

        self.R_load = - self.V / self.I
            
    def get_T_h_error_numerical(self,q_c):
        """Solves leg once with no attempt to match hot side
        temperature BC. Used by solve_leg."""
        self.q[0] = q_c
        # for loop for iterating over segments
        for j in range(1,self.segments):
            self.T_props = self.T[j-1]
            self.set_TEproperties(T_props=self.T_props)
            self.T[j] = ( self.T[j-1] + self.segment_length / self.k *
            (self.J * self.T[j-1] * self.alpha - self.q[j-1]) )
            # determines temperature of current segment based on
            # properties evaluated at previous segment
            self.dq = ( (self.rho * self.J**2. * (1. +
        self.alpha**2. * self.T[j-1] / (self.rho * self.k)) - self.J *
        self.alpha * self.q[j-1] / self.k) )   
            self.q[j] = ( self.q[j-1] + self.dq * self.segment_length )
            self.V_segment[j] = ( self.alpha * (self.T[j] -
        self.T[j-1]) + self.J * self.rho * self.segment_length )
            self.R_int_seg = ( self.rho * self.segment_length /
        self.area )
            self.P_flux_segment[j] = self.J * self.V_segment[j]
            self.T_h = self.T[-1]
            self.q_h = self.q[-1]
            self.error = (self.T_h - self.T_h_goal) / self.T_h_goal
        return self.error

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
        self.I = 1. # electrical current (Amps)
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3)**2 # void area (m^2)
        self.length = 1.e-3 # default leg height (m)
        self.segments = 25
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

    def solve_te_pair(self):
        """solves legs and combines results of leg pair"""
        self.Ptype.T_h_goal = self.T_h_goal
        self.Ntype.T_h_goal = self.T_h_goal
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c
        self.Ntype.solve_leg()
        self.Ptype.solve_leg()
        self.T_h = self.Ntype.T_h

        # Renaming stuff for use elsewhere
        self.q_h = ((self.Ptype.q_h * self.Ptype.area + self.Ntype.q_h
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void)) * 0.001
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ((self.Ptype.q_c * self.Ptype.area + self.Ntype.q_c
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void)) * 0.001
        # area averaged hot side heat flux (kW/m^2)
        self.P = -(self.Ntype.P + self.Ptype.P) * 0.001 
        # power for the entire leg pair(kW). Negative sign makes this
        # a positive number. Heat flux is negative so efficiency needs
        # a negative sign also.  
        self.P_flux = self.P / self.area
        # power flux (kW / m^2) through leg pair
        self.eta = -self.P / (self.q_h * self.area)
        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1. / self.h
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
        self.Ptype.area = area / (1. + self.area_ratio)
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
