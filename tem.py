# Distribution modules

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import time
import scipy.optimize as spopt

# User defined modules
import te_prop
reload(te_prop)

def set_ZT(self):
    """Sets ZT based on formula
    self.ZT = self.sigma * self.alpha**2. / self.k""" 
    self.ZT = self.alpha**2. * self.T_props / (self.k * self.rho)


class Leg():
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """this method sets everything that is constant and
        initializes some arrays""" 
        self.I = 0.5 # current (A)
        self.segments = 25
        # number of segments for finite difference model
        self.length = 1.e-2  # leg length (m)
        self.area = (3.e-3)**2. # leg area (m^2)
        self.T_h_goal = 550.
        # hot side temperature (K) that matches HX BC
        self.T_c = 350. # cold side temperature (K)
        self.T = sp.zeros(self.segments) # initial array for
                                        # temperature (K)
        self.q = sp.zeros(self.segments)
        # initial array for heat flux (W/m^2)
        self.V_segment = sp.zeros(self.segments)
        # initial array for Seebeck voltage (V)
        self.P_flux_segment = sp.zeros(self.segments)
        # initial array for power flux in segment (W/m^2)
        self.xtol = 0.01 # tolerable fractional error in hot side
                         # temperature  

    set_ZT = set_ZT
    set_prop_fit = te_prop.set_prop_fit
    set_TEproperties = te_prop.set_TEproperties
    
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
        self.T[0] = self.T_c
        self.T_props = self.T[0]
        self.set_TEproperties()
        self.q_c_guess = ( -self.k / self.length * (self.T_h_goal -
        self.T_c) )
        # (W/m^2) guess for q[0] (W/m^2)
        self.q_c = spopt.fsolve(self.solve_leg_once,
        x0=self.q_c_guess, xtol=self.xtol)
        self.solve_leg_once(self.q_c)
        self.P = sp.sum(self.P_flux_segment) * self.area
        # Power for the entire leg (W)
        self.eta = self.P / (self.q[-1] * self.area)
        # Efficiency of leg
            
    def solve_leg_once(self,q_c):
        """Solves leg once with no attempt to match hot side
        temperature BC. Used by solve_leg."""
        self.q[0] = q_c
        # for loop for iterating over segments
        for j in range(1,self.segments):
            self.T_props = self.T[j-1]
            self.set_TEproperties()
            self.T[j] = ( self.T[j-1] + self.segment_length / self.k *
            (self.J * self.T[j-1] * self.alpha - self.q[j-1]) )
            # determines temperature of current segment based on
            # properties evaluated at previous segment
            self.dq = ( (self.rho * self.J**2 * (1 + self.alpha**2 *
            self.T[j-1] / (self.rho * self.k)) - self.J * self.alpha *
            self.q[j-1] / self.k) )
            self.q[j] = ( self.q[j-1] + self.dq * self.segment_length )
            self.V_segment[j] = ( self.alpha * (self.T[j] -
            self.T[j-1]) )
            self.P_flux_segment[j] = ( self.J * (self.V_segment[j] +
            self.J * self.rho * self.segment_length) )
            self.T_h = self.T[-1]
            error = (self.T_h - self.T_h_goal) / self.T_h_goal
        return error


class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.I = 1. # electrical current (Amps)
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3)**2 # void area (m^2)
        self.length = 2.e-3 # default leg height (m)
        self.segments = 25

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

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        exponential = 1.e-3
        self.Ptype.T_h_goal = self.T_h_goal
        self.Ntype.T_h_goal = self.T_h_goal
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c
        self.Ntype.solve_leg()
        self.Ptype.solve_leg()
        self.T_h = self.Ntype.T[-1]
        # Everything from here on out is in kW instead of W
        self.q_h = ( (self.Ptype.q[-1] * self.Ptype.area + self.Ntype.q[-1]
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void) ) * exponential
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ( (self.Ptype.q[0] * self.Ptype.area + self.Ntype.q[0]
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void) * exponential )
        # area averaged hot side heat flux (kW/m^2)
        self.P = -( self.Ntype.P + self.Ptype.P ) * exponential
        # power for the entire leg pair(kW). Negative sign makes this
        # a positive number. Heat flux is negative so efficiency needs
        # a negative sign also.  
        self.eta = -self.P / (self.q_h * self.area)
        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1 / self.h
                

        
