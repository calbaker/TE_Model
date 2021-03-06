"""Contains class for exhaust side of heat exchanger"""

# In python directory
import properties as prop
reload(prop)

# In this directory
import functions
reload(functions)
import enhancement
reload(enhancement)


class Exhaust(prop.ideal_gas):

    """Class for engine exhaust in heat exchanger.

    Methods:

    __init__
    set_fluid_props

    """

    def __init__(self):

        """
        Sets a bunch of constants, binds methods, inits parent class

        self.enh_lib = enhancement - Used in hx.py 

        Also initializes super class, which is ideal_gas from the
        properties script.  I keep this script in ~/Documents/Python,
        which is part of my python path.

        """

        super(Exhaust, self).__init__()

        self.enh_lib = enhancement
        self.enh = None
        self.T_ref = 300.
        self.P = 101.
        self.height = 1.5e-2
        self.ducts = 1
        self.sides = 2
        self.mdot_omega = 0.2 / 60.

        self.Nu_coeff = 0.023

        functions.bind_functions(self)

    def set_fluid_props(self):
         
        """
        Sets properties needed for set_flow.

        Methods:

        self.set_thermal_props

        """
        
        self.set_thermal_props()
        self.c_p = self.c_p_air
        self.k = self.k_air

