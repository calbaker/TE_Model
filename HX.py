# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import os

# User Defined Modules
# In this directory
import engine
import TEM
# In python directory
import properties as prop 

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
  self.set_flow_geometry()
  self.T = 0.5*(self.T_in + self.T_out)
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
  self.T = 0.5 * (self.T_in + self.T_out)
  self.set_flow_geometry()
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
 TEM = TEM.TEModule()
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
  # Exhaust stuff
  self.exh.set_flow()
  # Coolant stuff
  self.cool.set_flow()
  # Wall stuff
  self.plate.set_h()
  # TE stuff
  self.TEM.solve_TEM()
  self.leg_pairs = int(self.A / self.TEM.Ate) # Number of TEM leg pairs per node
  # Heat exchanger stuff
  self.U = ( (self.exh.h**-1 + self.plate.h**-1 + self.TEM.h**-1 +
  self.plate.h**-1 + self.cool.h**-1)**-1 ) # overall heat transfer
                                        # coefficient (kW/m^2-K)  

  self.Qdot = ( self.U * self.A * (self.exh.T - self.cool.T) ) # heat transfer (kW)

  self.exh.T_out = ( self.exh.T_in - self.Qdot / self.exh.C )
  # temperature (K) at exhaust outlet   
  self.cool.T_out = ( self.cool.T_in + self.Qdot / self.cool.C )
  # temperature (K) at coolant outlet

 def solve_HX(self):
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
  self.exh.T_nodes = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.exh.h_nodes = sp.zeros(self.nodes)
  self.cool.T_nodes = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.cool.h_nodes = sp.zeros(self.nodes) 
  self.TEM.T_cool = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.TEM.T_hot = sp.zeros(self.nodes) # initializing array for storing
                                     # temperature (K) in each node 
  self.TEM.I_nodes = sp.zeros(self.nodes)
  self.TEM.V_nodes = sp.zeros(self.nodes)
  self.TEM.power_nodes = sp.zeros(self.nodes)

  for i in sp.arange(self.nodes):
   self.exh.T_out = self.exh.T_in - 1. # guess at temperature (K) drop in each node
   self.cool.T_out = self.cool.T_in + 1. # guess at temperature (K) increase in each node
   self.TEM.Tc = self.cool.T_in # guess at cold side TEM temperature (K)
   self.TEM.Th = self.exh.T_in # guess at hot side TEM temperature (K)

   for j in range(4):
    #print self.TEM.Th # troubleshooting convergence
    self.solve_node()
    self.TEM.Th = ( -self.Qdot * (1 / (self.plate.h * self.A) + 1 /
   (self.exh.h * self.A)) + self.exh.T) # redefining TEM hot side
     # temperature (K) based on
     # known heat flux
    self.TEM.Tc = ( self.Qdot * (1 / (self.plate.h * self.A) + 1 /
   (self.cool.h * self.A)) + self.cool.T) # redefining TEM cold side
     # temperature (K) based on
     # known heat flux

   #print '\n' # troubleshooting
   
   self.Qdot_nodes[i] = self.Qdot # storing node heat transfer in array
   self.exh.T_nodes[i] = (self.exh.T_in + self.exh.T_out)/2.
   self.exh.h_nodes[i] = self.exh.h
   self.cool.T_nodes[-i-1] = (self.cool.T_in + self.cool.T_out)/2. # nodes are reversed to reflect counterflow
   self.cool.h_nodes[-i-1] = self.cool.h

   self.TEM.T_hot[i] = self.TEM.Th # hot side
                                        # temperature (K) of TEM at
                                        # each node
   self.TEM.T_cool[-i-1] = self.TEM.Tc # hot side temperature (K) of
                                       # TEM at each node.  Use
                                       # negative index because this
                                       # is counterflow.    
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
  self.effectiveness = self.Qdot / (self.exh.C * (self.exh.T_inlet - self.cool.T_inlet))
#  self.TEM.power = self.TEM.I * sp.sum(self.TEM.V_nodes) * 1e-3 # total TE
                                        # power output (kW)
  self.TEM.power = sp.sum(self.TEM.power_nodes)
                                    
  # total TE power output (kW)
  self.Wdot_pumping = self.exh.Wdot_pumping + self.cool.Wdot_pumping
  # total pumping power requirement (kW) 
  self.power_net = self.TEM.power - self.Wdot_pumping 
  self.eta_1st = self.power_net / self.Qdot
  self.eta_2nd = self.power_net / self.available
  
##############################################
# # Instantiation
# HX1 = HX()
# HX1.exh.porous = 'no' 
# HX1.exh.T_inlet = 600.
# HX1.exh.P = 100.
# HX1.cool.T_inlet = 300.
# HX1.solve_HX()

# # Plotting
# # Plot configuration
# FONTSIZE = 16
# mpl.rcParams['axes.labelsize'] = FONTSIZE
# mpl.rcParams['axes.titlesize'] = FONTSIZE
# mpl.rcParams['legend.fontsize'] = FONTSIZE
# mpl.rcParams['xtick.labelsize'] = FONTSIZE
# mpl.rcParams['ytick.labelsize'] = FONTSIZE
# mpl.rcParams['lines.linewidth'] = 1.5

# fig3 = mpl.figure()

# mpl.plot(HX1.x_dim*100, HX1.exh.T_nodes, label='Exhaust (K)')
# mpl.plot(HX1.x_dim*100, HX1.cool.T_nodes, label='Coolant (K)')
# mpl.plot(HX1.x_dim*100, HX1.TEM.T_hot, label='TE Hot (K)')
# mpl.plot(HX1.x_dim*100, HX1.TEM.T_cool, label='TE Cold (K)')

# mpl.xlabel('Distance Along HX (cm)')
# mpl.ylabel('Temperature (K)')
# mpl.title('Temperature v. Distance in HX')
# mpl.legend(loc='best')
# mpl.grid()
# mpl.savefig('Plots/temperature distribution.pdf')
# mpl.savefig('Plots/temperature distribution.png')

# fig4 = mpl.figure()

# mpl.plot(HX1.x_dim*100, HX1.TEM.I_nodes)

# mpl.xlabel('Distance Along HX (cm)')
# mpl.ylabel('Current (A)')
# mpl.title('Current v. Distance in HX')
# mpl.legend(loc='best')
# mpl.grid()
# mpl.savefig('Plots/current distribution.pdf')
# mpl.savefig('Plots/current distribution.png')

# height = sp.arange(0.5,2.,0.25)*1.e-2
# power_net = sp.empty(0)
# Wdot_pumping_cool = sp.empty(0)
# Wdot_pumping_exh = sp.empty(0)
# Qdot = sp.empty(0)
# effectiveness = sp.empty(0)
# eta_1st = sp.empty(0)
# eta_2nd = sp.empty(0)

# for i in sp.arange(sp.size(height)):
#     HX0.exh.height = height[i]
#     HX0.solve_HX()
#     HX0.solve_HX()
#     power_net = sp.append(power_net,HX0.power_net)
#     Wdot_pumping_exh = sp.append(Wdot_pumping_exh,HX0.exh.Wdot_pumping)
#     Wdot_pumping_cool = sp.append(Wdot_pumping_cool,HX0.cool.Wdot_pumping)
#     Qdot = sp.append(Qdot,HX0.Qdot)
#     effectiveness = sp.append(effectiveness,HX0.effectiveness)
#     eta_2nd = sp.append(eta_2nd,HX0.eta_2nd)
#     eta_1st = sp.append(eta_1st,HX0.eta_1st)

# fig1 = mpl.figure()

# mpl.plot(height*1e2,power_net,label='Net Power')
# mpl.plot(height*1e2,Wdot_pumping_exh,label='Exhaust Pumping Power')
# mpl.plot(height*1e2,Wdot_pumping_cool,label='Coolant Pumping Power')
# mpl.plot(height*1e2,Qdot,label='Heat Transfer')

# mpl.title('Power v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
# mpl.xlabel('Duct Height (cm)')
# mpl.ylabel('(kW)')
# mpl.legend()
# mpl.grid()
# mpl.savefig('Plots/power.pdf')
# mpl.savefig('Plots/power.png')

# fig2 = mpl.figure()

# mpl.plot(height*1e2,effectiveness,label='Effectiveness')
# mpl.plot(height*1e2,eta_1st,label='1st Law Efficiency')
# mpl.plot(height*1e2,eta_2nd,label='modified 2nd Law Efficiency')

# mpl.title('Effectiveness v. Exhaust Duct Height, '+str(HX0.width*100)+'cm duct width')
# mpl.xlabel('Duct Height (cm)')
# mpl.ylabel('HX Effectiveness')
# mpl.legend()
# mpl.grid()
# mpl.savefig('Plots/effectiveness.pdf')
# mpl.savefig('Plots/effectiveness.png')

# mpl.show()

