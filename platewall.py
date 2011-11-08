"""Module for definining PlateWall class methods and parameters."""

# Created on 7 Nov 2011 by Chad Baker

class PlateWall(object):
    """class for modeling metal walls of heat exchanger"""
    k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
    t = 0.00635 # thickness (m) of HX plate
    def set_h(self):
        self.h = self.k/self.t
        self.R_thermal = 1 / self.h

