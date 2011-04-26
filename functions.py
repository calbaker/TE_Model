# functions to be used in exhaust and coolant modules

def set_flow_geometry(self,width):
 self.perimeter = 2.*(self.height+width) # wetted perimeter (m) of
                                        # exhaust flow
 self.area = self.height * width # cross-section area (m^2) of
                                    # exhaust flow
 self.D = 4.*self.area / self.perimeter # coolant hydraulic diameter (m)

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
