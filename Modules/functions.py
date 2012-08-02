"""Contains functions to be used in both exhaust and coolant
modules."""

import numpy as np

def set_flow_geometry(self, width):

    """Sets perimeter, flow area, and hydraulic diameter.
    
    Inputs:

    width (m)

    """

    self.perimeter = 2.*(self.height + width) 
    # wetted perimeter (m) of flow
    self.flow_area = self.height * width 
    # cross-section area (m^2) of exhaust flow
    self.D = 4. * self.flow_area / self.perimeter
    # coolant hydraulic diameter (m)

    if self.enh != None:
        try:
            self.enh.set_geometry(self)
        except AttributeError:
            pass
        else:
            self.enh.set_geometry(self)

def set_Re_dependents(self):

    """Sets Nu and f based on Re.

    Methods:

    self.set_Re

    """

    self.set_Re()
    if np.size(self.Re_D) > 1:
        if (self.Re_D > 2300.).any(): 
            # Do these correlations hold for any tube geometry?
            self.f = 0.078 * self.Re_D**(-1. / 4.) 
            # friction factor for turbulent flow from Bejan Convection
            # Heat Transfer
            self.Nu_D = ( self.Nu_coeff * self.Re_D**(4. / 5.) *
                          self.Pr**(1. / 3.) ) 
            # Adrian Bejan, Convection Heat Transfer, 3rd ed.,
            # Equation 8.30 
            self.flow = 'turbulent'
        else:
            self.Nu_D = 7.54 # Bejan, Convection Heat Transfer, Table 3.2
                # parallel plates with constant T
            self.f = 24. / self.Re_D
            self.flow = 'laminar'
    else:
        if (self.Re_D > 2300.): # Do these correlations hold for any tube geometry?
            self.f = 0.078 * self.Re_D**(-1. / 4.) # friction factor for turbulent
            # flow from Bejan
            self.Nu_D = self.Nu_coeff * self.Re_D**(4. / 5.)*self.Pr**(1. / 3.) # Adrian
            # Bejan, Convection Heat Transfer, 3rd ed., Equation 8.30
            self.flow = 'turbulent'
        else:
            self.Nu_D = 7.54 # Bejan, Convection Heat Transfer, Table 3.2
                # parallel plates with constant T
            self.f = 24. / self.Re_D
            self.flow = 'laminar'

def set_Re(self):

    """Sets Reynolds number based on hydraulic diameter. 

    Requiures:

    self.velocity
    self.D
    self.nu
    self.Re_D = self.velocity * self.D / self.nu

    """ 

    self.Re_D = self.velocity * self.D / self.nu
    # Reynolds number

def set_flow(self):
    
    """
    Sets flow parameters for exhaust or coolant instance. 

    See exhaust.py and coolant.py

    Methods
    -------
    self.set_fluid_props
    self.set_Re_dependents
    self.enh.solve_enh
    self.set_thermal_props()
    
    Used in hx.py by hx.HX.set_convection and possibly
    elsewhere."""         

    self.set_fluid_props()

    self.C = self.mdot * self.c_p 
    # heat capacity of flow (kW/K)
    self.Vdot = self.mdot / self.rho 
    # volume flow rate (m^3/s) of exhaust
    self.velocity = self.Vdot / self.flow_area 
    # velocity (m/s) of exhaust

    self.set_Re_dependents()
    self.h = self.Nu_D * self.k / self.D 
    # coefficient of convection (kW/m^2-K)
        
    if self.enh == None:
        self.deltaP = ( self.f * self.perimeter * self.node_length /
        self.flow_area * (0.5 * self.rho * self.velocity**2) * 0.001 )       
        # pressure drop (kPa)
    else:
        self.enh.solve_enh(self)

    self.Wdot_pumping = self.Vdot * self.deltaP 
    # pumping power (kW)

    self.R_thermal = 1. / self.h
    # thermal resistance (m^2-K/kW) of exhaust

