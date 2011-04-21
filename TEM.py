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
  self.Ate = self.Ap + self.An # area of TE leg pair (m^2)

  # init values for loop
  self.dx = self.L / self.n

 def solve_TEM(self):
  # The following block is to plug in a J value based on an
  # approximate load resistance 
  self.SUM1 = 0 #initialize integrals
  #self.SUM2 = 0 #   ""         ""
  for k in range(self.n):
   self.T0 = self.Tc + k*(self.Th-self.Tc)/self.n #updates temperature
   self.Ap0 = (0.15*self.T0 + 211.)*1.e-6 #seebeck coefficient (SI Units)
   self.Pp0 = 0.01*1/25 #resistivity (SI units)
   self.Kp0 = 100*3.194/self.T0 #Thermal conductivity (SI Units)
   self.An0 = (0.268*self.T0 - 329)*1.e-6 #ntype seebeck
   self.Pn0 = 0.01*0.1746/(self.T0 - 310) #ntype resistivity
   self.Kn0 = 100.*54./self.T0 #ntype thermal conductivity
   self.SUM1 = ( self.Ap0 * (self.Th - self.Tc) / self.n - self.An0 *
  (self.Th - self.Tc) / self.n + self.SUM1 ) #seebeck voltage (V)

    #self.SUM2 = ( 2. * (self.Pp0 * self.L / self.n / self.Ap + self.Pp0
  #* self.L/self.n) +self.SUM2 ) #Accounts for load resistance and
   #internal resistance (Ohms) 

  self.T0 = self.Tc
  #self.I = self.SUM1/self.SUM2 #Seebeck voltage/total resistance =
                               #current (Amps)
  self.Jn = self.I/self.An #ntype current density (si units)
  self.Jp = -self.I/self.Ap #pytpe current density (Si Units)
 
  self.Ti = self.Tc #(initialize Ti for the while loop condition )

  while sp.absolute(self.Ti - self.Th) > self.err: #while loop condition
   self.T0 = self.Tc #initialize T0 for the inside for loop
   self.q0 = self.qc #initialize cold side heat flux for the for loop
   self.sum1 = 0
   self.sum2 = 0

   for i in range(self.n):
    self.Ap0 = (0.15 * self.T0 + 211.)*1.e-6  # ptype seebeck
    self.Pp0 = 0.01 * 1. / 25. # ptype resisitivity
    self.Kp0 = 100. * 3.194 / self.T0 # ptype conducitivity
    self.Ti = ( self.T0 + (self.dx / self.Kp0) * (self.Jp * self.T0 *
   self.Ap0 - self.q0) ) #finite difference for temperature eq.
    self.qi = ( self.q0 + (self.Pp0 * self.Jp * self.Jp * (1 +
   self.Ap0 * self.Ap0 * self.T0 / (self.Pp0 * self.Kp0)) - self.Jp *
   self.Ap0 * self.q0 / self.Kp0) * self.dx ) #finite difference for heat flux eq
    self.dT = self.Ti - self.T0
    self.sum1 = self.sum1 + self.Ap0*self.dT #calculates numerator of efficiency
    self.sum2 = self.Pp0*self.dx + self.sum2 #denominator of efficiency
    self.T0 = self.Ti #updates T0 within for loop
    self.q0 = self.qi #updates q0 within for loop

   self.qc = self.qc*(1 + (self.Th-self.Ti)/self.Th) #updates guess value of qc

  self.qc = ( -100 * 3.194 * 2 / (self.Th + self.Tc) *
  (self.Th-self.Tc) / (self.L / 2) ) #resets qc to original guess value

  self.Ti = self.Tc #reinitializes Ti for the while loop condition
 
  while sp.absolute(self.Ti - self.Th) > self.err:
   self.T0 = self.Tc 
   self.q0 = self.qc
   self.sum1 = 0
   self.sum2 = 0
  
   for i in range(self.n):
    self.An0 = (0.268 * self.T0 - 329.)*1e-6 # ntype seebeck
    self.Pn0 = 0.01 * 0.1746 / (self.T0 - 310.) # ntype resistivity
    self.Kn0 = 100. * 54. / self.T0 # ntype thermal conductivity
    self.Ti = ( self.T0 + (self.dx / self.Kn0) * (self.Jn * self.T0 *
   self.An0 - self.q0) ) #same as previous for loop
    self.qi = ( self.q0 + (self.Pn0 * self.Jn * self.Jn * (1 +
   self.An0 * self.An0 * self.T0 / (self.Pn0 * self.Kn0)) - self.Jn *
   self.An0 * self.q0 /self.Kn0) * self.dx )#same as previous for loop
    self.dT = self.Ti - self.T0
    self.sum1 = self.sum1 + self.An0 * self.dT #same as previous for loop
    self.sum2 = self.Pn0 * self.dx + self.sum2# same as previous for loop
    self.T0 = self.Ti #updates T0 within for loop
    self.q0 = self.qi #updates q0 within for loop
   
   self.qc = self.qc * (1 + (self.Th - self.Ti) / self.Th) #updates T0 w/i while loop
  
  self.Rte = -1/(self.qi / (self.Th - self.Tc)) # Effective TE Resistance in m^2-K/W

  # variables that Chad will use
  self.h = 1. / self.Rte * 1e-3 # heat transfer coefficient (kW/m^2-K)
  self.V_Seebeck = self.SUM1 # seebeck voltage
