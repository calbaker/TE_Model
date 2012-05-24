"""Contains class for exhaust side of heat exhanger"""

# Distribution libraries
import numpy as np
import types

# In python directory
import properties as prop
reload(prop)

# In this directory
import functions
reload(functions)
import enhancement
reload(enhancement)


class Exhaust(prop.ideal_gas):
    """
    Class for modeling convection and flow of engine exhaust
    through heat exchanger.

    Methods:

    """

    def __init__(self):

        """
        Sets a bunch of constants, binds methods, inits parent class 

        Binds these methods:

        set_flow_geometry
        set_Re
        set_Re_dependents
        set_flow

        self.enh_lib = enhancement - Used in hx.py 

        Also initializes super class

        """

        super(Exhaust, self).__init__()

        self.enh_lib = enhancement
        self.enh = None
        self.T_ref = 300.
        self.P = 101.
        self.height = 1.5e-2
        self.ducts = 1

        self.Nu_coeff = 0.023

        self.set_flow_geometry = (
        types.MethodType(functions.set_flow_geometry, self) )
        self.set_Re = (
        types.MethodType(functions.set_Re, self) )
        self.set_Re_dependents = (
        types.MethodType(functions.set_Re_dependents, self) )
        self.set_flow = (
        types.MethodType(functions.set_flow, self) )

    def set_fluid_props(self):
         
        """
        Sets properties needed for set_flow.

        Methods:

        self.set_thermal_props

        """
        
        self.set_thermal_props()
        self.c_p = self.c_p_air
        self.k = self.k_air

