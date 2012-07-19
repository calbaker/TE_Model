"""Contains PlateWall class."""

# Created on 7 Nov 2011 by Chad Baker

class PlateWall(object):

    """Class for metal walls of heat exchanger.

    Methods:

    __init__
    set_h

    """ 

    def __init__(self):

        """Initializes material properties and geometry defaults.""" 

        self.k = 200.e-3
        # thermal conductivity (kW/m-K) of Aluminum HX plate
        # (Incropera and DeWitt)  
        self.alpha = 73.0e-6
        # thermal diffusivity (m^2/s) of Al HX plate  
        self.thickness = 0.00635
        # thickness (m) of HX plate        
        self.set_h()

    def set_h(self):

        """Sets the effective convection coefficient."""

        self.h = self.k/self.thickness
        self.R_thermal = 1. / self.h
