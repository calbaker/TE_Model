# In python directory
import properties as prop

from functions import *

class coolant(prop.flow):
 height = 0.25e-2 # height (m) of coolant duct
 mdot = 0.5 # mass flow rate (kg/s) of coolant
 ducts = 2 # number of coolant ducts per hot duct
 geometry = 'parallel plates'
 c_p = 4.179 # Specific heat (kJ/kg*K) of water at 325K 
 mu = 5.3e-4 # viscosity of water at 325K (Pa*s), WolframAlpha
 k = 0.646e-3 # thermal conductivity of water at 325K (kW/m*K) 
 # through cooling duct
 Pr = (7.01 + 5.43)/2 # Prandtl # of water from Engineering
  # Toolbox
 rho = 1000. # density (kg/m**3) of water
 k = 0.646e-3 # thermal conductivity of water at 325K (kW/m*K)

 set_flow_geometry = set_flow_geometry
 set_Re_dependents = set_Re_dependents

 def set_flow(self,length):
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
