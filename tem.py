# Distribution modules

import types
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

        self.set_ZT = types.MethodType(set_ZT, self)
        self.set_prop_fit = types.MethodType(te_prop.set_prop_fit,
        self) 
        self.set_TEproperties = (
        types.MethodType(te_prop.set_TEproperties, self) )
    
    def set_q_c_guess(self):
        if self.node == 0:
            self.q_c_guess = ( -self.k / self.length * (self.T_h_goal -
                                                        self.T_c) )
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
        self.T[0] = self.T_c
        self.T_props = self.T[0]
        self.set_TEproperties()
        self.set_q_c_guess()

        if self.method == "numerical":
            self.q_c = spopt.fsolve(self.get_T_h_error_numerical,
        x0=self.q_c_guess, xtol=self.xtol)  
            self.error = self.get_T_h_error_numerical(self.q_c) 
            self.P = sp.sum(self.P_flux_segment) * self.area
            # Power for the entire leg (W)
            self.eta = self.P / (self.q_h * self.area)
            # Efficiency of leg
            

        if self.method == "analytical":
            q_h_guess = self.q_c_guess * 1.1
            q_guess = np.array[q_c_guess, q_h_guess]
            q_solved = spopt.fsolve(self.get_T_h_error_analytical,
            x0=q_guess, xtol=self.xtol)
            self.q_h = q_solved[0]
            self.q_c = q_solved[1]
            delta_T = self.T_h - self.T_c 
            q = np.array(self.q_h, self.q_c)
            self.error = self.get_T_h_error_analytical(q)
            self.eta = ( self.J**2. * (self.alpha * delta_T / self.J -
            self.rho * self.length) / (self.alpha * self.T_h * self.J +
            delta_T / self.length * self.k - self.J**2 * self.length *
            self.rho / 2.) )
            self.P = self.eta * self.q_h
            
    def get_T_h_error_numerical(self,q_c):
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
            self.dq = ( (self.rho * self.J * self.J * (1 + self.alpha
        * self.alpha * self.T[j-1] / (self.rho * self.k)) - self.J *
        self.alpha * self.q[j-1] / self.k) ) 
            self.q[j] = ( self.q[j-1] + self.dq * self.segment_length )
            self.V_segment[j] = ( self.alpha * (self.T[j] -
            self.T[j-1]) )
            self.P_flux_segment[j] = ( self.J * (self.V_segment[j] +
            self.J * self.rho * self.segment_length) )
            self.T_h = self.T[-1]
            self.q_h = self.q[-1]
            error = (self.T_h - self.T_h_goal) / self.T_h_goal
        return error

    def get_T_h_error_analytical(self,q):
        """Given a guess at cold side heat flux and hot side heat
        flux, this function finds the correct hot side and cold side
        heat flux to match up with the temperature boundary
        conditions."""
        self.T_props = 0.5 * (self.T_c + self.T_h_goal)
        q_h = q[0]
        q_c = q[1]

        def get_T_h_self_error(q_h):
            """Given a presumably guess at cold side heat flux, this
            function finds a hot side heat flux to get the two
            equations for temperature to agree."""
            T_h1 = ( (q_h + self.T_c / self.length * self.k +
            self.J**2. * self.length * self.rho / 2.) / (self.alpha *
            self.J + self.k / self.length) )
            T_h2 = ( (self.alpha * self.T_c * self.J + self.T_c /
            self.length * self.k + self.J**2 * self.length * self.rho
            / 2. + q_h - q_c) / (self.alpha * self.J + self.k /
            self.length) )
            error = (T_h2 - T_h1) / T_h1
            return error
        self.q_h = q_h
        self.q_c = q_c
        self.T_h = spopt.fsolve(get_T_h_self_error)
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

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        exponential = 1.e-3
        self.Ptype.T_h_goal = self.T_h_goal
        self.Ntype.T_h_goal = self.T_h_goal
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c
        self.Ntype.solve_leg()
        self.Ptype.solve_leg()
        self.T_h = self.Ntype.T_h

        # Renaming stuff for use elsewhere
        # Everything from here on out is in kW instead of W
        self.q_h = ( (self.Ptype.q_h * self.Ptype.area +
                      self.Ntype.q_h * self.Ntype.area) /
                     (self.Ptype.area + self.Ntype.area +
                      self.area_void) ) * exponential 
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ( (self.Ptype.q_c * self.Ptype.area +
                      self.Ntype.q_c * self.Ntype.area) /
                     (self.Ptype.area + self.Ntype.area +
                      self.area_void) * exponential ) 
        # area averaged hot side heat flux (kW/m^2)
        self.P = -( self.Ntype.P + self.Ptype.P ) * exponential
        # power for the entire leg pair(kW). Negative sign makes this
        # a positive number. Heat flux is negative so efficiency needs
        # a negative sign also.  
        self.eta = -self.P / (self.q_h * self.area)
        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1. / self.h
                

        
