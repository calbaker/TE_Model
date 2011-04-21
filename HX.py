# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as mpl
import os

# User Defined Modules
# In this directory
import engine
import TEM
# In python directory
import properties as prop
reload(prop) # uncomment this when making changes in properties

# definitions of classes for mediums in which heat transfer can occur

def set_flow_geometry(self):
 self.perimeter = 2*(self.height+HX.width) # wetted perimeter (m) of
                                        # exhaust flow
 self.area = self.height * HX.width # cross-section area (m^2) of
                                    # exhaust flow
 self.D = 4*self.area / self.perimeter # coolant hydraulic diameter (m)

def set_Re_dependents(self):
 self.set_Re()
 if self.Re_D > 2300.: # Do these correlations hold for any tube geometry?
  self.f = 0.078*self.Re_D**(-1./4.) # friction factor for turbulent
  # flow from Bejan Eq. 8.13
  self.Nu_D = 0.023*self.Re_D**(4/5.)*self.Pr**(1/3.) # Adrian
  # Bejan, Convection Heat Transfer, 3rd ed., Equation 8.30
 else:
  self.Nu_D = 7.54 # Bejan, Convection Heat Transfer, Table 3.2
   # parallel plates with constant T
  self.f = 24./self.Re_D

class plate_wall():
 k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
 t = 0.01 # thickness (m) of HX plate
 def set_h(self):
  self.h = self.k/self.t

class TEdummy():
 I = 1
 V_Seebeck = 1
 Ate = 1
 qh = 1
 qc = 1
 def solve_TEM(self):
  self.h = 0.6 # guessed effective coefficient of convection (kW/m^2-K) for
         # TE device         

class exhaust(prop.ideal_gas):
 porous = 'no' # is there porous media?
 enhancement = 'none' # is there any means of enhancement? (i.e. fins,
                      # corrugate metal, etc.)

 T_ref = 300 # reference temperature (K) for availability calculation

 height = 1.25e-2 # height (m) of exhaust duct

 ducts = 1 # number of exhaust ducts
 porosity = 0.92 # volume of void per total volume
 k_matrix = 5.8e-3 # thermal conductivity(kW/m-K) of metal foam +
  # air
 PPI = 10 # pores per inch of porous media, used in Mancin model
 K = 2.e-7 # permeability (m^2) of porous metal foam, used in Bejan model

 set_flow_geometry = set_flow_geometry
 set_Re_dependents = set_Re_dependents

 def set_flow(self):
  self.T = 0.5 * (self.T_in + self.T_out) # Temperature (K) used to calculate fluid
                     # properties.  This is no good if T_out is much
                     # different from T_in
  self.set_TempPres_dependents()
  self.c_p = self.c_p_air

  self.C = self.mdot * self.c_p # heat capacity of
  # flow (kW/K)
  self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
  self.velocity = self.Vdot / (HX.width * self.height)

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
   self.deltaP = (self.f * self.perimeter * HX.length /
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
   self.deltaP = (HX.length * 2. * self.F * self.G**2 /
   (self.D_pore * self.rho)) # pressure drop from Mancin et al.

  elif self.enhancement == 'none':
   self.k = self.k_air
   self.set_Re_dependents()
   self.deltaP = (self.f * self.perimeter * HX.length /
    self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)

  elif self.enhancement == 'corrugated':
   self.k = self.k_air
   self.set_Re_dependents()
   self.deltaP = (self.f * self.perimeter * HX.length /
    self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)
   
  self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
  self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)
    
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

 def set_flow(self):
  self.T = 0.5 * (self.T_in + self.T_out) # Temperature (K) used to calculate fluid
                     # properties.  This is no good if T_out is much
                     # different from T_in
  self.C = self.mdot * self.c_p # heat capacity of flow (kW/K)
  self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
  self.velocity = self.Vdot / (HX.width * self.height * self.ducts)
  self.nu = self.mu/self.rho
  self.set_Re_dependents()
  self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)
  self.deltaP =  ( self.f * self.perimeter * HX.length / self.area *
  (0.5*self.rho * self.velocity**2)*1.e-3 ) # pressure drop (kPa) 
  self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)

class HX:
 # initilization of class instances
 cool = coolant()
 exh = exhaust()
 TEM = TEdummy()
 plate = plate_wall()
 Cummins = engine.engine()

 # More exhaust attributes
 Cummins.set_mdot_charge() # mass flow rate of exhaust
 exh.mdot = Cummins.mdot_charge

 # Geometry and constants 
 width = 15e-2 # width (cm*10**-2) of HX duct. This model treats
  # duct as parallel plates for simpler modeling.
 length = 1. # length (m) of HX duct
 nodes = 20 # number of nodes for numerical heat transfer model
 node_length = length / nodes # length (m) of each node
 x_dim = sp.arange(node_length/2, length + node_length/2, node_length)
 # x coordinate (m)

 def solve_node(self):
  self.exh.T_out = self.exh.T_in - 5 # Guess at exhaust node out temperature (K)
  self.cool.T_out = self.cool.T_in - 1 # Guess at exhaust node out temperature (K)
  
  # Exhaust stuff
  self.exh.set_flow()
  # Coolant stuff
  self.cool.set_flow()
  # Wall stuff
  self.plate.set_h()
  # TE stuff
  self.TEM.solve_TEM()

  self.exh.R_thermal = 1 / self.exh.h
  self.plate.R_thermal = 1 / self.plate.h
  self.TEM.R_thermal = 1 / self.TEM.h
  self.cool.R_thermal = 1 / self.cool.h

  self.leg_pairs = int(self.A / self.TEM.Ate) # Number of TEM leg pairs per node
  # Heat exchanger stuff
  if self.exh.C < self.cool.C:
   self.C_min = self.exh.C
   self.C_max = self.cool.C
  else:
   self.C_min = self.cool.C
   self.C_max = self.exh.C

  self.R_C = self.cool.C/self.exh.C

  self.U = ( (self.exh.R_thermal + self.plate.R_thermal + self.TEM.R_thermal +
  self.plate.R_thermal + self.cool.R_thermal )**-1 ) # overall heat transfer
                                        # coefficient (kW/m^2-K)
  self.NTU = self.U * self.A / self.C_min # number
                                        # of transfer units   
  self.effectiveness = ( (1 - sp.exp(-self.NTU * (1 + self.R_C))) / (1
  + self.R_C) )  # NTU method for parallel flow from Mills Heat
                 # Transfer Table 8.3a  
  self.Qdot = ( self.effectiveness * self.C_min * (self.exh.T_in -
  self.cool.T_in)  ) # NTU heat transfer (kW)
#  self.Qdot = ( self.U * self.A * (self.exh.T - self.cool.T) ) # linear heat transfer (kW) 
  self.exh.T_out = ( self.exh.T_in - self.Qdot / self.exh.C )
  # temperature (K) at exhaust outlet   
  self.cool.T_out = ( self.cool.T_in + self.Qdot / self.cool.C )
  # temperature (K) at coolant outlet

 def solve_HX(self):
  self.exh.set_flow_geometry()
  self.cool.set_flow_geometry()

  self.A = self.node_length*self.width*self.cool.ducts # area (m^2)
                                        # through which heat flux
                                        # occurs in each node
  self.exh.T_in = self.exh.T_inlet # T_in and T_out correspond to the
                                   # temperatures going into and out
                                   # of the node.  The suffix "let"
                                   # means the temperature is
                                   # referring to the entire HX.  
  self.cool.T_in = self.cool.T_inlet

  # initializing arrays for tracking variables at nodes
  self.Qdot_nodes = sp.zeros(self.nodes) # initialize array for storing
                                    # heat transfer (kW) in each node 
  self.effectiveness_nodes = sp.zeros(self.nodes) # initialize array for storing
                                    # heat transfer (kW) in each node 
  self.exh.T_nodes = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.exh.h_nodes = sp.zeros(self.nodes)
  self.cool.T_nodes = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.cool.h_nodes = sp.zeros(self.nodes) 
  self.U_nodes = sp.zeros(self.nodes) 
  self.TEM.T_cool = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.TEM.T_hot = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.TEM.I_nodes = sp.zeros(self.nodes)
  self.TEM.V_nodes = sp.zeros(self.nodes)
  self.TEM.power_nodes = sp.zeros(self.nodes)

  for i in sp.arange(self.nodes):
   self.TEM.Tc = self.cool.T_in # guess at cold side TEM temperature (K)
   self.TEM.Th = self.exh.T_in # guess at hot side TEM temperature (K)

   for j in range(20):
    self.solve_node()
    self.TEM.Th = ( self.exh.T - self.Qdot / ((self.exh.h**-1 +
   self.plate.h**-1)**-1 * self.A) ) # redefining TEM hot side 
     # temperature (K) based on
     # known heat flux
    self.TEM.Tc = ( self.Qdot * (1 / (self.plate.h * self.A) + 1 /
   (self.cool.h * self.A)) + self.cool.T) # redefining TEM cold side
     # temperature (K) based on
     # known heat flux
   
   self.Qdot_nodes[i] = self.Qdot # storing node heat transfer in array
   self.effectiveness_nodes[i] = self.effectiveness # storing node heat transfer in array

   self.exh.T_nodes[i] = (self.exh.T_in + self.exh.T_out)/2.
   self.exh.h_nodes[i] = self.exh.h

   self.cool.T_nodes[i] = (self.cool.T_in + self.cool.T_out)/2.
   self.cool.h_nodes[i] = self.cool.h

   self.TEM.T_hot[i] = self.TEM.Th # hot side
                                        # temperature (K) of TEM at
                                        # each node
   self.TEM.T_cool[i] = self.TEM.Tc # hot side temperature (K) of
                                       # TEM at each node.  Use
                                       # negative index because this
                                       # is counterflow.    
   self.U_nodes[i] = self.U
   self.TEM.I_nodes[i] = self.TEM.I
   self.TEM.V_nodes[i] = self.TEM.V_Seebeck * self.leg_pairs
   self.TEM.power_nodes[i] = sp.absolute(self.TEM.qh - self.TEM.qc) * self.A

   # redefining outlet temperature for next node
   self.exh.T_in = self.exh.T_out
   self.cool.T_in = self.cool.T_out
   
  self.exh.T_outlet = self.exh.T_out
  self.cool.T_outlet = self.cool.T_out

  self.Qdot = sp.sum(self.Qdot_nodes)
  self.available = self.exh.C * (self.exh.T_inlet - self.exh.T_ref)
#  self.TEM.power = self.TEM.I * sp.sum(self.TEM.V_nodes) * 1e-3 # total TE
                                        # power output (kW)
  self.TEM.power = sp.sum(self.TEM.power_nodes)
                                    
  # total TE power output (kW)
  self.Wdot_pumping = self.exh.Wdot_pumping + self.cool.Wdot_pumping
  # total pumping power requirement (kW) 
  self.power_net = self.TEM.power - self.Wdot_pumping 
  self.eta_1st = self.power_net / self.Qdot
  self.eta_2nd = self.power_net / self.available
  
