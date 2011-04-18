# Distribution modules

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

# User defined modules
# none yet

class TEModule():
 def __init__(self):
  # init values
  self.Tc = 400. #Cold side temp (K)
  self.Th = 750. #Hot side temp (K)
  self.n = 50 #Number of segments in p and n legs
  self.L = 0.01 #length in meters of each leg
  self.i = 1.
  self.err = 0.1 #Tolerance
  self.qc = ( -100. * 3.194 * 2 / (self.Th + self.Tc) * (self.Th -
 self.Tc) / (self.L / 2) ) #initial guess value for qc (based on pure
                           #conduction) 
  self.I = 2.0 # (Amps)
  self.q0 = self.qc
  self.Ap = 20.e-4 #Area of p-type (m^2)
  self.An = 1.e-4 # Area of n-type (m^2)
  self.Ate = self.Ap + self.An

  # init values for loop
  self.dx = self.L / self.n

 def solve_TEM(self):
  # The following block is to plug in a J value based on an
  # approximate load resistance 
  self.SUM1 = 0 #initialize integrals
  #self.SUM2 = 0 #   ""         ""
  for k in range(self.n):
   self.T0 = self.Tc + k*(self.Th-self.Tc)/self.n
   self.Ap0 = (0.15*self.T0 + 211.)*1.e-6
   self.Pp0 = 0.01*1/25 
   self.Kp0 = 100*3.194/self.T0
   self.An0 = (0.268*self.T0 - 329)*1.e-6
   self.Pn0 = 0.01*0.1746/(self.T0 - 310) 
   self.Kn0 = 100.*54./self.T0
   self.SUM1 = ( self.Ap0 * (self.Th - self.Tc) / self.n - self.An0 *
  (self.Th - self.Tc) / self.n + self.SUM1 ) #seebeck voltage (V)

   # self.SUM2 = ( 2. * (self.Pp0 * self.L / self.n / self.Ap + self.Pp0
  #* self.L/self.n) +self.SUM2 ) #Accounts for load resistance and
   #internal resistance (Ohms) 

  self.T0 = self.Tc
  #self.I = self.SUM1/self.SUM2 #Seebeck voltage/total resistance =
                               #current (Amps)
  self.Jn = self.I/self.An
  self.Jp = -self.I/self.Ap
 
  self.Ti = self.Tc

  while sp.absolute(self.Ti - self.Th) > self.err:
   self.T0 = self.Tc
   self.q0 = self.qc
   self.sum1 = 0
   self.sum2 = 0

   for i in range(self.n):
    self.Ap0 = (0.15 * self.T0 + 211.)*1.e-6  # Uncommented by Chad on 14 Apr at 1 pm
    self.Pp0 = 0.01 * 1. / 25. # Uncommented by Chad on 14 Apr at 1 pm
    self.Kp0 = 100. * 3.194 / self.T0 # Uncommented by Chad on 14 Apr at 1 pm
    self.Ti = ( self.T0 + (self.dx / self.Kp0) * (self.Jp * self.T0 *
   self.Ap0 - self.q0) ) 
    self.qi = ( self.q0 + (self.Pp0 * self.Jp * self.Jp * (1 +
   self.Ap0 * self.Ap0 * self.T0 / (self.Pp0 * self.Kp0)) - self.Jp *
   self.Ap0 * self.q0 / self.Kp0) * self.dx ) 
    self.dT = self.Ti - self.T0
    self.sum1 = self.sum1 + self.Ap0*self.dT
    self.sum2 = self.Pp0*self.dx + self.sum2
    self.T0 = self.Ti
    self.q0 = self.qi

   self.qc = self.qc*(1 + (self.Th-self.Ti)/self.Th)
  

  self.qc = ( -100 * 3.194 * 2 / (self.Th + self.Tc) *
  (self.Th-self.Tc) / (self.L / 2) ) 

  self.qh = self.qi

  self.Ti = self.Tc
 
  while sp.absolute(self.Ti - self.Th) > self.err:
   self.T0 = self.Tc
   self.q0 = self.qc
   self.sum1 = 0
   self.sum2 = 0
  
   for i in range(self.n):
    self.An0 = (0.268 * self.T0 - 329.)*1e-6 # Uncommented by Chad on 14 Apr at 1 pm
    self.Pn0 = 0.01 * 0.1746 / (self.T0 - 310.) # Uncommented by Chad on 14 Apr at 1 pm
    self.Kn0 = 100. * 54. / self.T0 # Uncommented by Chad on 14 Apr at 1 pm
    self.Ti = ( self.T0 + (self.dx / self.Kn0) * (self.Jn * self.T0 *
   self.An0 - self.q0) )
    self.qi = ( self.q0 + (self.Pn0 * self.Jn * self.Jn * (1 +
   self.An0 * self.An0 * self.T0 / (self.Pn0 * self.Kn0)) - self.Jn *
   self.An0 * self.q0 /self.Kn0) * self.dx )
    self.dT = self.Ti - self.T0
    self.sum1 = self.sum1 + self.An0 * self.dT
    self.sum2 = self.Pn0 * self.dx + self.sum2
    self.T0 = self.Ti
    self.q0 = self.qi
   
   self.qc = self.qc * (1 + (self.Th - self.Ti) / self.Th)
  
  self.Rte = -1/(self.qi / (self.Th - self.Tc)) # Effective TE Resistance in m2K/W

  # variables that Chad will use
  self.h = 1. / self.Rte
  self.V_Seebeck = self.SUM1 
