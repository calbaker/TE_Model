# Distribution modules

import scipy as sp
import numpy as np

# User defined modules
# none yet


class Leg():
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """this method sets everything that is constant and
        initializes some arrays""" 
        self.segments = 100 # number of segments for finite difference model
        self.length = 1.e-3  # leg length (m)
        self.area = (1.e-3)**2. # leg area (m^2)
        self.T_h = 550 # hot side temperature (K)
        self.T_c = 350 # cold side temperature (K)
        self.I = -0.35 # electrical current (Amps)
        self.J = self.I / self.area # (Amps/m^2)
        self.T = sp.zeros(self.segments) # initial array for
                                        # temperature (K)
        self.q = sp.zeros(self.segments) # initial array for heat flux (W/m^2)

    def set_properties(self):
        """sets thermal and electrical properties"""
        if self.material == "HMS":
            # These properties came from Xi Chen's HMS properties.ppt
            self.k = 4.
            # thermal conductivity (W/m-K) 
            self.alpha = 150.e-6
            # Seebeck coefficient (V/K)
            self.sigma = 1000.
            # electrical conductivity (1/Ohm-cm)
            self.rho = 1./self.sigma / 100.
            # electrical resistivity (Ohm-m)
        self.R_thermal = self.length / self.k
        # thermal resistance (m^2-K/W)

    def solve_leg(self):
        """Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006"""
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        self.T[0] = self.T_c
        self.set_properties()
        self.q[0] = ( -self.k / self.length * (self.T_h -
        self.T_c) )
        # initial guess for q[0] (W/m^2)
        
        # for loop for iterating over segments
        for i in sp.arange(1,self.segments):
            self.set_properties()
            # this method is here because properties will eventually
            # be temperature dependent
            self.T[i] = ( self.T[i-1] + self.segment_length / self.k *
        (self.J * self.T[i-1] * self.alpha - self.q[i-1]) ) 
            # determines temperature of current segment based on
            # properties evaluated at previous segment
            self.q[i] = ( self.q[i-1] + (self.rho * self.J**2 * (1 -
        self.alpha**2 * self.T[i-1] / (self.rho * self.k)) - self.J
        * self.alpha * self.q[i-1] / self.k) * self.segment_length )

    def solve_dumb(self):
        """solves for the case of pure conduction"""
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        self.T[0] = self.T_c
        self.set_properties()
        self.q[0] = ( -self.k / self.segment_length * (self.T_h -
            self.T_c) )
        
        # for loop for iterating over segments
        for i in sp.arange(1,self.segments):
            self.q[i] = ( self.k / self.segment_length * (self.T_h -
        self.T_c) )
            self.set_properties()
                # this method is here because properties will eventually
                # be temperature dependent
            self.T[i] = ( self.T[i-1] + self.q[i-1] / self.k * self.segment_length )
                # determines temperature of current segment based on
                # properties evaluated at previous segment
                    

class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.Ptype = leg() # p-type instance of leg
        self.Ntype = leg() # n-type instance of leg
        self.area = self.Ntype.area + self.Ptype.area

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        
leg = Leg()
leg.material = 'HMS'
leg.solve_leg()
