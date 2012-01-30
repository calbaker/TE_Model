"""Module for modeling fins in exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np

class OffsetStripFin(object):
    """Class for modeling offset strip fins. Uses correlations from:
 
    Manglik, Raj M., and Arthur E. Bergles, ‘Heat Transfer and
    Pressure Drop Correlations for the Rectangular Offset Strip Fin
    Compact Heat Exchanger’, Experimental Thermal and Fluid Science,
    10 (1995), 171-180 <doi:10.1016/0894-1777(94)00096-Q>."""

    def __init__(self):
        """Sets constants and things that need to be guessed to
        execute as a standalone model.

        Sets
        ------------------
        self.s : horizontal gap (m) between fins  
        self.h : vertical gap (m) between fins and hx walls
        self.t : thickness (m) of fin strip
        self.l : length (m) of fin"""

    def set_params(self):
        """Sets parameters used to calculate friction factor and
        Colburn factor.  See Manglik and Bergles Fig. 1.

        Requires
        -------------------
        self.s : horizontal gap (m) between fins  
        self.h : vertical gap (m) between fins and hx walls
        self.t : thickness (m) of fin strip
        self.l : length (m) of fin

        Sets
        --------------------
        self.alpha = self.s / self.h
        self.delta = self.t / self.l
        self.gamma = self.t / self.s"""
        
        self.alpha = self.s / self.h
        self.delta = self.t / self.l
        self.gamma = self.t / self.s 

    def set_f(self):
        """Sets friction factor, f."""
        self.f = ( 9.6243 * self.Re**-0.7422 * self.alpha**-0.1856 *
        self.delta**0.3053 * self.gamma**-0.2659 ) 

    def set_j(self):
        """Sets Colburn factor, j."""
        self.j = ( 0.6522 * self.Re**-0.5403 * self.alpha**-0.1541 *
        self.delta**0.1499 * self.gamma**-0.0678 * (1. + 5.269e-5 *
        self.Re**1.340 * self.alpha**0.504 * self.delta**0.456 *
        self.gamma**-1.055)**0.1 ) 

    def solve(self):
        """Runs self.set_f and self.set_j"""
        self.set_params()
        self.set_f()
        self.set_j()
