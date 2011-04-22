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
reload(TEM)
from functions import *
import exhaust
import coolant

# definitions of classes for mediums in which heat transfer can occur

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

class HX:
 def __init__(self):
  # Geometry and constants 
  self.width = 15e-2 # width (cm*10**-2) of HX duct. This model treats
   # duct as parallel plates for simpler modeling.
  self.length = 1. # length (m) of HX duct
  self.nodes = 20 # number of nodes for numerical heat transfer model
  self.node_length = self.length / self.nodes # length (m) of each node
  self.x_dim = sp.arange(self.node_length/2, self.length +
  self.node_length/2, self.node_length)  
  # x coordinate (m)

 # initilization of class instances
 cool = coolant.coolant()
 exh = exhaust.exhaust()
 TEM = TEM.TEModule()
 plate = plate_wall()
 Cummins = engine.engine()

 # More exhaust attributes
 Cummins.set_mdot_charge() # mass flow rate of exhaust
 exh.mdot = Cummins.mdot_charge


 def solve_node(self):
  self.exh.T_out = self.exh.T_in - 5 # Guess at exhaust node out temperature (K)
  self.cool.T_out = self.cool.T_in - 1 # Guess at exhaust node out temperature (K)
  
  # Exhaust stuff
  self.exh.set_flow(self.length)
  # Coolant stuff
  self.cool.set_flow(self.length)
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
  self.exh.T_out = ( self.exh.T_in - self.Qdot / self.exh.C )
  # temperature (K) at exhaust outlet   
  self.cool.T_out = ( self.cool.T_in + self.Qdot / self.cool.C )
  # temperature (K) at coolant outlet

 def solve_HX(self):
  self.exh.set_flow_geometry(self.width) # this should be moved to the
                               # corresponding module
  self.cool.set_flow_geometry(self.width)

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
   print "\nSolving node", i
   self.TEM.Tc = self.cool.T_in # guess at cold side TEM temperature (K)
   self.TEM.Th = self.exh.T_in # guess at hot side TEM temperature (K)

   for j in range(3):
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
   self.TEM.I_nodes[i] = self.TEM.I # current (A)
   self.TEM.V_nodes[i] = self.TEM.V_Seebeck * self.leg_pairs
   self.TEM.V = sp.sum(self.TEM.V_nodes) # total voltage (V) across
                                        # all nodes
   self.TEM.power_nodes[i] = self.TEM.I * self.TEM.V * 1.e-3
   # electrical power (kW)  
   # change this formula if
   # current is ever varied along
   # the nodes.   

   # redefining outlet temperature for next node
   self.exh.T_in = self.exh.T_out
   self.cool.T_in = self.cool.T_out
   
  self.exh.T_outlet = self.exh.T_out
  self.cool.T_outlet = self.cool.T_out

  self.Qdot = sp.sum(self.Qdot_nodes)
  self.available = self.exh.C * (self.exh.T_inlet - self.exh.T_ref)
#  self.TEM.power = self.TEM.I * sp.sum(self.TEM.V_nodes) * 1e-3 # total TE
                                        # power output (kW)
  self.effectiveness = self.Qdot / self.available # global HX effectiveness                                        
  self.TEM.power = sp.sum(self.TEM.power_nodes)
                                    
  # total TE power output (kW)
  self.Wdot_pumping = self.exh.Wdot_pumping + self.cool.Wdot_pumping
  # total pumping power requirement (kW) 
  self.power_net = self.TEM.power - self.Wdot_pumping 
  self.eta_1st = self.power_net / self.Qdot
  self.eta_2nd = self.power_net / self.available
  
