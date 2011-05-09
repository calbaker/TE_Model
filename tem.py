# Distribution modules

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

# User defined modules
# none yet


class Leg():
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """this method sets everything that is constant and
        initializes some arrays""" 
        self.segments = 10. # number of segments for finite difference model
        self.length = 1.e-3  # leg length (m)
        self.area = (1.e-3)**2. # leg area (m^2)
        self.T_h_goal = 550.
        # hot side temperature (K) that matches HX BC
        self.T_c = 350. # cold side temperature (K)
        self.I = -0.35 # electrical current (Amps)
        self.J = self.I / self.area # (Amps/m^2)
        self.T = sp.zeros(self.segments) # initial array for
                                        # temperature (K)
        self.q = sp.zeros(self.segments) # initial array for heat flux (W/m^2)
        self.error = 1. # allowable hot side temperature (K) error

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
            

    def solve_leg(self):
        """Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006. The model guesses a cold
        side heat flux and changes that heat flux until it results in
        the desired hot side temperature."""
        self.T[0] = self.T_c
        self.set_properties()
        self.q_c = ( sp.array([0.9,1.1]) * (-self.k / self.length * (self.T_h_goal -
        self.T_c)) )
        # array for storing guesses for q[0] (W/m^2) during while loop
        # iteration
        self.T_h = sp.zeros(2)
        # array for storing T_h (K) during while loop iteration.  
        # for loop for providing two arbitrary points to use for
        # linear interpolation 
        for i in sp.arange(sp.size(self.q_c)):
            self.q[0] = self.q_c[i]
            self.solve_leg_once()
            print self.T[-1]
            self.T_h[i] = self.T[-1]
        self.q_c_new = ( (self.q_c[1] - self.q_c[0]) / (self.T_h[1] - self.T_h[0]) * (self.T_h_goal - self.T_h[1]) + self.q_c[1] )
        # linear interpolation for q_c based on previous q_c's
        # and previous T_h's 
        self.q_c = sp.append(self.q_c, self.q_c_new)
        self.q[0] = self.q_c_new
        print "q_c_new =",self.q_c_new
        print "q_c[-1] =",self.q_c[-1]
        print "q[0] =",self.q[0]
        self.solve_leg_once()
        self.T_h = sp.append(self.T_h, self.T[-1])
            
    def solve_leg_once(self):
        """Solves leg once with no attempt to match hot side
        temperature BC. Used by solve_leg."""
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        # for loop for iterating over segments
        for i in sp.arange(1,self.segments):
            self.set_properties()
            # this method is here because properties will eventually
            # be temperature dependent
            self.T[i] = ( self.T[i-1] + self.segment_length / self.k *
        (self.J * self.T[i-1] * self.alpha - self.q[i-1]) ) 
            # determines temperature of current segment based on
            # properties evaluated at previous segment
            self.q[i] = ( self.q[i-1] + (self.rho * self.J**2. * (1. -
        self.alpha**2. * self.T[i-1] / (self.rho * self.k)) - self.J
        * self.alpha * self.q[i-1] / self.k) * self.segment_length
        )


class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.area = self.Ntype.area + self.Ptype.area

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
