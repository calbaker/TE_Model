# In python directory
import properties as prop
import types
from scimath.units import * 
from scimath.units.api import *

# In local directory
import functions
reload(functions)


class Coolant(prop.flow):
    """class for coolant flow"""

    def __init__(self):
        """sets constants and initiates class instances"""
        super(Coolant, self).__init__()
        self.height = UnitScalar(1.e-2, units=length.m)
        # height (m) of coolant duct
        self.mdot = UnitScalar(1.0, units=length.m)
        # mass flow rate (kg/s) of coolant
        self.ducts = 2 # number of coolant ducts per hot duct
        self.geometry = 'parallel plates'
        self.c_p = UnitScalar(4.179, units=energy.kJ / mass.kg /
        temperature.K)
        # Specific heat (kJ/kg*K) of water at 325K 
        self.mu = UnitScalar(5.3e-4, units=pressure.Pa * time.sec)
        # viscosity of water at 325K (Pa*s), WolframAlpha
        self.k = UnitScalar(0.646e-3, units=power.kw / length.m /
        temperature.K) 
        # thermal conductivity of water at 325K (kW/m*K) through
        # cooling duct 
        self.Pr = (7.01 + 5.43)/2 # Prandtl # of water from Engineering
        # Toolbox
        self.rho = UnitScalar(1000., units=density.kg_per_m3) 
        # density (kg/m**3) of water
        self.Nu_coeff = 0.023
            
        self.set_flow_geometry = (
        types.MethodType(functions.set_flow_geometry, self) )
        self.set_Re_dependents = (
        types.MethodType(functions.set_Re_dependents, self) )

    def set_flow(self):
        """calculates flow parameters"""
        self.C = self.mdot * self.c_p # heat capacity of flow (kW/K)
        self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
        self.velocity = self.Vdot / (self.area * self.ducts) # velocity (m/s) of coolant
        self.nu = self.mu/self.rho
        self.set_Re_dependents()
        self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
        self.deltaP =  ( self.f * self.perimeter * self.length / self.area *
        (0.5 * self.rho * self.velocity**2)*1.e-3 ) # pressure drop (kPa) 
        self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)
        self.R_thermal = 1 / self.h
        # thermal resistance of coolant (m^2-K/W)
