"""Module for definining PlateWall class methods and parameters."""

# Created on 7 Nov 2011 by Chad Baker

class PlateWall(object):
    """class for modeling metal walls of heat exchanger"""

    def __init__(self):
        """Initializes material properties and plate wall geometry defaults."""
        self.k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
        self.t = 0.00635 # thickness (m) of HX plate
        self.c_p = 900. # specific heat of aluminum (J/kg-K)
        self.R_contact = 0.
        # thermal contact resistance (m^2*K/kW) between plates

    def set_h(self):
        """Sets the effective convection coefficient which is the
        inverse of thermal resistance."""
        self.h = self.k/self.t
        self.R_thermal = 1. / self.h

