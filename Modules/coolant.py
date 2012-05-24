"""Contains class for coolant side of heat exchanger.""" 

# In python directory
import properties as prop
import types

# In local directory
import functions
reload(functions)
import enhancement
reload(enhancement)


class Coolant(object):
    """
    class for coolant flow
    """

    def __init__(self):
        """
        Sets contants and instantiates classes.

        """
        
        self.enh_lib = enhancement
        self.enh = None        

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
        self.set_flow = (
        types.MethodType(functions.set_flow, self) )

    def set_fluid_props(self):
        
        """Sets fluid properties needed """
        
        self.nu = self.mu / self.rho
