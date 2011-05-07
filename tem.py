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
        self.segments = 10 # number of segments for finite difference model
        self.length = 1.e-3  # leg length (m)
        self.area = (1.e-3)**2. # leg area (m^2)
        self.T_hot = 550 # hot side temperature (K)
        self.T_cool = 350 # cold side temperature (K)

    def set_properties(self):
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
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        self.set_properties(self)
        for i in sp.arange(self.segments
        
        

class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.Ptype = leg() # p-type instance of leg
        self.Ntype = leg() # n-type instance of leg
        self.area = self.Ntype.area + self.Ptype.area

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        
