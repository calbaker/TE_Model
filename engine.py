# Engine class used to determine attributes of engine.  This will be
# fleshed out with experimental data later. 

# Distribution modules
import scipy as sp

# User defined modules
import properties as prop

class engine: # Operating condintions for Cummins Engine
 # This module eventually needs to provide charge flow rate, EGR
 # flow rate, exhaust port temperature, post turbo temperature.  
 def __init__(self,**kwargs):
  if 'RPM' in kwargs:
   self.RPM = kwargs['kwargs']
  else:
   self.RPM = 2000. # engine speed (RPM)
  if 'torque' in kwargs:
   self.torque = kwargs['torque']
  else:
   self.torque = 300. # brake torque (lb-ft)

 displacement = 6.6e-3 # engine swept displacement (m**3)
 cylinders = 6. # number of cylinders
 eta_V = 1. # volumetric efficiency of engine. Can exceed unity for
  # turbo-charged unthrottled engine. Accounts for error
  # in intake manifold pressure estimate.
 T_intake = 300. # engine intake temperature (K)
 P_intake = 101.325 # pressure (kPa) at intake manifold
 air = prop.ideal_gas() # engine working fluid is ideal gas with
  # the properties of air
 air.T = T_intake
 air.P = P_intake
 air.set_TempPres_dependents()

 def set_mdot_charge(self):
  self.mdot_charge =(
  self.RPM / 2. * self.displacement * self.eta_V * self.air.rho) / 60.
  # charge flow (kg/s) in engine


