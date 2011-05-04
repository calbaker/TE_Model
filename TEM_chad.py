# Distribution modules

import scipy as sp

# User defined modules
# none yet

class leg():
 """class for individual p-type or n-type TE leg"""
 def __init__(self):
  self.I = 5.0e-1   # (Amps)
  self.Tc = 400. # Cold side temp (K)
  self.Th = 750. # Hot side temp (K)
  self.segments = 100 # Number of segments in p and n legs
  self.err = 0.1 # error tolerance (K) for while loop 
  self.A = 2.25e-6 # cross-section area (m^2) of leg
  self.A_void = 1.e-6 # cross-section area (m^2) of void per leg
  self.L = 0.002 #length (m) of leg
  self.rho = 0.01 * 1. / 25. # n-type resisitivity UNITS ???
                                     # what are all of these different
                                     # numbers??? 
  self.dx = self.L / self.segments # length of each segment

  # initial arrays for storing data in each segment                           
  self.q = sp.zeros(self.segments) # Segment heat flux (W/m^2)
  self.T = sp.zeros(self.segments) # Segment Temperature (K)
  self.S = sp.zeros(self.segments) # Segment Seebeck coefficient (???)
  self.k = sp.zeros(self.segments) # Segment Thermal conductivity (W/m-K)
  self.V_Seebeck = sp.zeros(self.segments) # Segment Seebeck voltage (V)
  self.R_segment = sp.zeros(self.segments) # Segment resistance (ohms) ???

 def solve_leg(self):
  self.J = self.I / self.A # current density in leg (A/m^2)
  # The following block is to plug in a J value based on an
  # approximate load resistance 
  self.q_c = ( -100. * 3.194 * 2 / (self.Th + self.Tc) * (self.Th -
   self.Tc) / (self.L / 2) ) #initial guess for cold side heat flux (W/m^2) based on pure
                           #conduction UNITS??? Also, what is 3.194???

  while sp.absolute(self.T[-1] - self.Th) > self.err: # condition such
                                        # that calculated hot side
                                        # temperature matches actual
                                        # hot side temperature
   self.T[0] = self.Tc # initialize T[0] for the inside for loop
   self.q[0] = self.q_c # initialize cold side heat flux for the for loop

   for i in sp.arange(1,self.segments):
    self.S[i-1] = (0.15 * self.T[i-1] + 211.)*1.e-6  # p-type seebeck
                                        # UNITS ??? what is 0.15 and
                                        # 211???
    self.k[i-1] = 100. * 3.194 / self.T[i-1] # p-type conducitivity
                                        # UNITS ???
    self.T[i] = ( self.T[i-1] + (self.dx / self.k[i-1]) * (self.J * self.T[i-1] *
     self.S[i-1] - self.q[i-1]) ) # finite difference for temperature
                                  # eq.
    self.q[i] = ( self.q[i-1] + (self.rho * self.J**2 * (1 +
    self.S[i-1]**2 * self.T[i-1] / (self.rho * self.k[i-1])) - self.J
    * self.S[i-1] * self.q[i-1] / self.k[i-1]) * self.dx ) #finite
                                        #difference  
                                        #for heat flux eq.  Chad
                                        #changed J * J to J**2
    self.dT = self.T[i] - self.T[i-1] # temperature (K) difference
                                      # between current and previous
                                      # segment
    self.V_Seebeck[i] = self.S[i] * self.dT # voltage (V) in segment
    self.R_segment[i] = self.rho * self.dx  # resistance (ohms ???)
                                        # of segment
   self.q_c = self.q_c * (1 + (self.Th - self.T[-1]) / self.Th)
    #updates guess value of q_c
#    self.R = self. 
  

# class TEModule():
#  """class for TEModule that includes a pair of legs"""
#  def __init__(self):
#   self.N = leg() # n-type instance of leg
#   self.P = leg() # p-type instance of leg

#   self. = -1/(self.qi / (self.Th - self.Tc)) # Effective TE Resistance (m^2-K/W)

#   # variables that Chad will use
#   self.h = 1. / self.Rte * 1e-3 # heat transfer coefficient (kW/m^2-K)
#   self.V_Seebeck = self.SUM1 # seebeck voltage
