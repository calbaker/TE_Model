# In python directory
import properties as prop

# In this directory
from functions import *

class exhaust(prop.ideal_gas):
 def __init__(self):
  self.porous = 'no' # is there porous media?
  self.enhancement = 'none' # is there any means of enhancement? (i.e. fins,
   # corrugate metal, etc.)

  self.T_ref = 300 # default reference temperature (K) for availability calculation

  self.height = 1.25e-2 # default height (m) of exhaust duct

  self.ducts = 1 # default number of exhaust ducts
  self.porosity = 0.92 # default volume of void per total volume
  self.k_matrix = 5.8e-3 # default thermal conductivity(kW/m-K) of metal foam +
   # air
  self.PPI = 10 # default pores per inch of porous media, used in Mancin model  
  self.K = 2.e-7 # default permeability (m^2) of porous metal foam, used in
   # Bejan model   

 set_flow_geometry = set_flow_geometry
 set_Re_dependents = set_Re_dependents

 def set_flow(self,length):

  self.T = 0.5 * (self.T_in + self.T_out) # Temperature (K) used to calculate fluid
                     # properties.  This is no good if T_out is much
                     # different from T_in
  self.set_TempPres_dependents()
  self.c_p = self.c_p_air

  self.C = self.mdot * self.c_p # heat capacity of
  # flow (kW/K)
  self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
  self.velocity = self.Vdot / self.area # velocity (m/s) of exhaust

  if self.porous == 'Bejan':
   self.Nu_D = 6. # Nu for porous media parallel plates with const
                  # heat flux.  Bejan Eq. 12.77 
   self.Re_K = self.velocity * self.K**0.5 / self.nu # Re
    # based on permeability from
    # Bejan Eq. 12.11    
   self.f = 1. / self.Re_K + 0.55 # Darcy Law, Bejan
    # Eq. 12.14.  It turns out
    # that f is pretty close to
    # 0.55
   self.k = self.k_matrix
   self.deltaP = (self.f * self.perimeter * length /
    self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)


  elif self.porous == 'Mancin':
   self.k = self.k_matrix
   self.Nu_D = 6. # Nu for porous media parallel plates with
                          # q''= const.  Bejan Eq. 12.77
   self.G = self.rho * self.velocity # Mass velocity from
                                        # Mancin et al.
   self.D_pore = 0.0122 * self.PPI**(-0.849) # hydraulic
                                        # diameter (m?) of porous
                                        # media based on Mancin et
                                        # al.  
   self.Re_K = ( self.D_pore * self.G / (self.mu * self.porosity) )
   # Re of porous media from Mancin et al.
   self.F = ( (1.765 * self.Re_K**(-0.1014) * self.porosity**2 /
   self.PPI**(0.6)) ) # friction factorb from Mancin et al. 
   self.deltaP = (length * 2. * self.F * self.G**2 /
   (self.D_pore * self.rho)) # pressure drop from Mancin et al.

  elif self.enhancement == 'none':
   self.k = self.k_air
   self.set_Re_dependents()
   self.deltaP = (self.f * self.perimeter * length /
    self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)

  elif self.enhancement == 'corrugated':
   self.k = self.k_air
   self.set_Re_dependents()
   self.deltaP = (self.f * self.perimeter * length /
    self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)
   
  self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
  self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)
    
