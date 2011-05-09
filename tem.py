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
        self.T_h = 550. # hot side temperature (K)
        self.T_c = 350. # cold side temperature (K)
        self.I = -0.35 # electrical current (Amps)
        self.J = self.I / self.area # (Amps/m^2)
        self.T = sp.zeros(self.segments) # initial array for
                                        # temperature (K)
        self.q = sp.zeros(self.segments) # initial array for heat flux (W/m^2)
        self.error = 5. # allowable hot side temperature (K) error

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
        Handbook, CRC/Taylor & Francis 2006"""
        self.T[0] = self.T_c
        self.set_properties()
        self.q_c = ( sp.array([-self.k / self.length * (self.T_h -
        self.T_c)]) )  
        # array for storing guesses for q[0] (W/m^2) during while loop
        # iteration
        self.T_h_guess = sp.zeros(1)
        # array for storing estimates of T_h (K) during while loop
        # iteration. Needs an element to match up with 

        self.cond_iter = 1 # counter for indexing q_c within while loop
        # while loop for iterating until last node temperature is
        # equal to hot side temperature
        while sp.absolute(self.T_h - self.T_h_guess[-1]) > self.error:
        #for gi in range(12):
            self.solve_leg_once()
            if self.cond_iter < 4: # attempt to guess in the right direction
                if self.T_h > self.T[-1]:
                    q_c_new = self.q_c[self.cond_iter - 1] * 1.01 # placeholder for
                                        # new value of
                                        # q_c[self.cond_iter]
                    print "\nStill just guessing"
                else:
                    q_c_new = self.q_c[self.cond_iter - 1] * 0.91
            else: # switches to linear interpolation when enough
                       # data points exist
                print "\nSwitching to linear interpolation",self.cond_iter
                q_c_new = ( (self.q_c[self.cond_iter - 1] - self.q_c[self.cond_iter - 2]) /
        (self.T_h_guess[self.cond_iter - 1] - self.T_h_guess[self.cond_iter - 2]) * (self.T_h
        - self.T_h_guess[self.cond_iter - 1]) +
            self.q_c[self.cond_iter - 1] )
                # linear interpolation for q_c based on previous q_c's
                # and previous T_h's 
            self.q_c = sp.append(self.q_c, q_c_new)
            self.q[0] = self.q_c[self.cond_iter-1]
            self.T_h_guess = sp.append(self.T_h_guess, self.T[-1])
            self.cond_iter = self.cond_iter + 1
            
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
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.area = self.Ntype.area + self.Ptype.area

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        
