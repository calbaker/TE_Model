# Distribution modules

import scipy as sp
import numpy as np

# User defined modules
# none yet


class Leg():
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """this method sets everything that is constant and initializes some arrays"""

    def solve_leg(self):
        """solves for temperatures, heat fluxes, and power output"""


class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.Ptype = leg() # p-type instance of leg
        self.Ntype = leg() # n-type instance of leg
        self.A = self.Ntype.A + self.Ptype.A

    def solve_tem(self):
        """solves legs and combines results of leg pair"""

    def solve_dumb(self):
        """solves for pure conduction"""
        self.Ntype.q = self.Ntype.k / self.L * (self.Th - self.Tc)
        self.Ptype.q = self.Ptype.k / self.L * (self.Th - self.Tc)
        self.q = self.Ntype.
        
