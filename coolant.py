# In python directory
import properties as prop

from functions import *


class Coolant(prop.flow):
    """class for coolant flow"""

    def __init__(self):
        """sets constants and initiates class instances"""        
        self.height = 0.25e-2 # height (m) of coolant duct
        self.mdot = 0.5 # mass flow rate (kg/s) of coolant
        self.ducts = 2 # number of coolant ducts per hot duct
        self.geometry = 'parallel plates'
        self.c_p = 4.179 # Specific heat (kJ/kg*K) of water at 325K 
        self.mu = 5.3e-4 # viscosity of water at 325K (Pa*s), WolframAlpha
        self.k = 0.646e-3 # thermal conductivity of water at 325K (kW/m*K) 
        # through cooling duct
        self.Pr = (7.01 + 5.43)/2 # Prandtl # of water from Engineering
        # Toolbox
        self.rho = 1000. # density (kg/m**3) of water
        self.k = 0.646e-3 # thermal conductivity of water at 325K (kW/m*K)

    set_flow_geometry = set_flow_geometry
    set_Re_dependents = set_Re_dependents

    def set_flow(self,length):
        """calculates flow parameters"""
        # If T_out is not defined, set it equal to T_in since it really
        # doesn't matter for calculations. Also, vice versa.
        try:
            self.T_out
        except AttributeError:
            self.T_out = None
        try:
            self.T_in
        except AttributeError:
            self.T_in = None
        if self.T_out is None:
            self.T_out = self.T_in
        elif self.T_in is None:
            self.T_in = self.T_outlet

        # Resume with other calculations
        self.T = 0.5 * (self.T_in + self.T_out) # Temperature (K) used to calculate fluid
            # properties.  This is no good if T_out is much
            # different from T_in
        self.C = self.mdot * self.c_p # heat capacity of flow (kW/K)
        self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
        self.velocity = self.Vdot / (self.area * self.ducts) # velocity (m/s) of coolant
        self.nu = self.mu/self.rho
        self.set_Re_dependents()
        self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
        self.deltaP =  ( self.f * self.perimeter * length / self.area *
        (0.5*self.rho * self.velocity**2)*1.e-3 ) # pressure drop (kPa) 
        self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)
