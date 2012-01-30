# In python directory
import properties as prop
import types
from scimath.units import * 
from scimath.units.api import *

# In local directory
import functions
reload(functions)


class Coolant(object):
    """class for coolant flow"""

    def __init__(self):
        """sets constants and initiates class instances"""
        super(Coolant, self).__init__()
        self.height = 1.e-2
        # height (m) of coolant duct
        self.mdot = 1.0
        # mass flow rate (kg/s) of coolant
        self.ducts = 2 # number of coolant ducts per hot duct
        self.geometry = 'parallel plates'
        self.c_p = 4.179
        # Specific heat (kJ/kg*K) of water at 325K 
        self.mu = 5.3e-4
        # viscosity of water at 325K (Pa*s), WolframAlpha
        self.k = 0.646e-3
        # thermal conductivity of water at 325K (kW/m*K) through
        # cooling duct 
        self.Pr = (7.01 + 5.43)/2 # Prandtl # of water from Engineering
        # Toolbox
        self.rho = 1000.
        # density (kg/m**3) of water
        self.Nu_coeff = 0.023
        self.enthalpy0 = 113.25
        # enthalpy (kJ/kg) of coolant at restricted dead state
        self.entropy0 = 0.437
        # entropy (kJ/kg*K) of coolant at restricted dead state
            
        self.set_flow_geometry = (
        types.MethodType(functions.set_flow_geometry, self) )
        self.set_Re = (
        types.MethodType(functions.set_Re, self) )
        self.set_Re_dependents = (
        types.MethodType(functions.set_Re_dependents, self) )

    def set_flow(self):
        """calculates flow parameters"""
        self.C = self.mdot * self.c_p # heat capacity of flow (kW/K)
        self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
        self.velocity = self.Vdot / (self.flow_area * self.ducts) # velocity (m/s) of coolant
        self.nu = self.mu/self.rho
        self.set_Re_dependents()
        self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
        self.deltaP =  ( self.f * self.perimeter * self.length / self.flow_area *
        (0.5 * self.rho * self.velocity**2) * 1.e-3 ) # pressure drop (kPa) 
        self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)
        self.R_thermal = 1 / self.h
        # thermal resistance of coolant (m^2-K/W)
