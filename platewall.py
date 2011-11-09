"""Module for definining PlateWall class methods and parameters."""

# Created on 7 Nov 2011 by Chad Baker

import scipy.optimize as spopt

class PlateWall(object):
    """class for modeling metal walls of heat exchanger"""

    def __init__(self):
        """Initializes material properties and plate wall geometry defaults."""
        self.k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
        self.t = 0.00635 # thickness (m) of HX plate
        self.c_p = 900.e-3 # specific heat of aluminum (J/kg-K)
        self.R_contact = 0.
        # thermal contact resistance (m^2*K/kW) between plates
        self.t_step = 1. # time step (s) for transient model 

    def set_h(self):
        """Sets the effective convection coefficient which is the
        inverse of thermal resistance."""
        self.h = self.k/self.t
        self.R_thermal = 1. / self.h

    def get_error_hot(self, delta_T):
        """needs a better doc string"""
        self.delta_T = delta_T
        self.q_h = ( self.h * (self.T_c - self.T_h) + 0.5 * self.m *
        self.c_p * self.delta_T / self.t_step )
        
    def get_error_cold(self, delta_T):
        """needs a better doc string"""
        self.delta_T = delta_T
        self.q_c = ( self.h * (self.T_c - self.T_h) - 0.5 * self.m *
        self.c_p * self.delta_T / self.t_step )         

    def solve(self):
        """Similar to tem.solve_leg but simpler."""
        self.delta_T = 3.
        # change in temperature with respect to time.  
