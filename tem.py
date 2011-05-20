# Distribution modules

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

# User defined modules
# none

def set_ZT(self):
    """Sets ZT based on formula
    self.ZT = self.sigma * self.alpha**2. / self.k""" 
    self.ZT = self.sigma * self.alpha**2. / self.k


class Leg():
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """this method sets everything that is constant and
        initializes some arrays""" 
        self.segments = 100. # number of segments for finite difference model
        self.length = 1.e-3  # leg length (m)
        self.area = (3.e-3)**2. # leg area (m^2)
        self.T_h_goal = 550.
        # hot side temperature (K) that matches HX BC
        self.T_c = 350. # cold side temperature (K)
        self.T = sp.zeros(self.segments) # initial array for
                                        # temperature (K)
        self.q = sp.zeros(self.segments) # initial array for heat flux (W/m^2)
        self.V_segment = sp.zeros(self.segments)
        # initial array for Seebeck voltage (V)
        self.error = 1. # allowable hot side temperature (K) error

    def set_properties(self):
        """sets thermal and electrical properties"""
        if self.material == "HMS":
            # These properties came from Xi Chen's HMS properties.ppt
            self.k = 4.
            # thermal conductivity (W/m-K) 
            self.alpha = 150.e-6
            # Seebeck coefficient (V/K)
            self.sigma = 1000.
            # electrical conductivity (1/Ohm-cm)
            self.rho = 1./self.sigma / 100.
            # electrical resistivity (Ohm-m)
            
        if self.material == "MgSi":
            # These properties came from Gao et al.  
            self.k = 3. 
            # thermal conductivity (W/m-K) 
            self.alpha = -150.e-6
            # Seebeck coefficient (V/K)
            self.sigma = 1.5e3 # (S/cm) (S/cm = 1/Ohm-cm)
            # electrical conductivity (1/Ohm-cm)
            self.rho = 1./self.sigma / 100.
            # electrical resistivity (Ohm-m)
            self.I
            
    def solve_leg(self):
        """Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006. The model guesses a cold
        side heat flux and changes that heat flux until it results in
        the desired hot side temperature."""
        self.segment_length = self.length / self.segments
        # length of each segment (m)
        self.T[0] = self.T_c
        self.set_properties()
        self.q_c = ( sp.array([0.9,1.1]) * (-self.k / self.length * (self.T_h_goal -
        self.T_c)) )
        # array for storing guesses for q[0] (W/m^2) during while loop
        # iteration
        self.T_h = sp.zeros(2)
        # array for storing T_h (K) during while loop iteration.  
        # for loop for providing two arbitrary points to use for
        # linear interpolation 
        for i in sp.arange(sp.size(self.q_c)):
            self.q[0] = self.q_c[i]
            self.solve_leg_once()
            self.T_h[i] = self.T[-1]
        self.q_c_new = ( (self.q_c[1] - self.q_c[0]) / (self.T_h[1] - self.T_h[0]) * (self.T_h_goal - self.T_h[1]) + self.q_c[1] )
        # linear interpolation for q_c based on previous q_c's
        # and previous T_h's 
        self.q_c = sp.append(self.q_c, self.q_c_new)
        self.q[0] = self.q_c_new
        self.solve_leg_once()
        self.T_h = sp.append(self.T_h, self.T[-1])
            
    def solve_leg_once(self):
        """Solves leg once with no attempt to match hot side
        temperature BC. Used by solve_leg."""
        self.J = self.I / self.area # (Amps/m^2)
        # for loop for iterating over segments
        for i in sp.arange(1,self.segments):
            self.set_properties()
            # this method is here because properties will eventually
            # be temperature dependent
            self.T[i] = ( self.T[i-1] + self.segment_length / self.k *
        (self.J * self.T[i-1] * self.alpha - self.q[i-1]) ) 
            # determines temperature of current segment based on
            # properties evaluated at previous segment
            self.q[i] = ( self.q[i-1] + (self.rho * self.J**2. * (1. -
        self.alpha**2. * self.T[i-1] / (self.rho * self.k)) - self.J
        * self.alpha * self.q[i-1] / self.k) * self.segment_length
        )
            self.V_segment[i] = self.alpha * (self.T[i] - self.T[i-1]) 
        self.V = sp.sum(self.V_segment)
        self.P_electrical = self.V * self.I
        self.P_heat = (self.q[-1] - self.q[0]) * self.area 

class TEModule():
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.I = 0.35 # electrical current (Amps)
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.Ptype.material = 'MgSi'
        self.Ntype.material = 'HMS'
        self.area_void = (1.e-3)**2 # void area (m^2)

    def solve_tem(self):
        """solves legs and combines results of leg pair"""
        self.area = self.Ntype.area + self.Ptype.area + self.area_void 
        self.Ptype.I = -self.I
        # Current must have same sign as heat flux for p-type
        # material. Heat flux is negative because temperature gradient
        # is positive.  
        self.Ntype.I = self.I
        self.Ptype.T_h_goal = self.T_h_goal
        self.Ntype.T_h_goal = self.T_h_goal
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c
        self.Ntype.solve_leg()
        self.Ptype.solve_leg()
        self.T_h = self.Ntype.T[-1]
        self.V = sp.sum(self.Ptype.V) + sp.sum(self.Ntype.V)
        # Everything from here on out is in kW instead of W
        self.q = ( (self.Ptype.q[-1] * self.Ptype.area + self.Ntype.q[-1]
        * self.Ntype.area) / (self.Ptype.area + self.Ntype.area +
        self.area_void) ) * 1.e-3 # area averaged heat flux (kW/m^2)
        self.P_electrical = ( self.Ntype.P_electrical +
        self.Ptype.P_electrical ) * 1.e-3 # power based on V*I (kW)
        self.P_heat = ( self.Ntype.P_heat +
        self.Ptype.P_heat ) * 1.e-3
        # power based on heat flux difference (kW)
        self.eta = -self.P_heat / (self.q * self.area)
        self.h = self.q / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)


class TECarnot():
    """Class for TE device with performance calculated using carnot
    efficiency evaluated over the entire leg"""
    def __init__(self):
        """Sets a bunch of constants and whatnot"""
        self.k = 4.
        # thermal conductivity (W/m-K) 
        self.alpha = 150.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1000.
        # electrical conductivity (1/Ohm-cm)
        self.rho = 1./self.sigma / 100.
        # electrical resistivity (Ohm-m)
        self.length = 1.e-3  # leg length (m)
        self.area = (3.e-3)**2. # leg area (m^2) 
        self.area_void = (3.e-3)**2. # void area (m^2)
        self.T_h_goal = 500. # dummy variable
        self.T_c = 350. # cold side temperature (K)
        self.ZT = 1. # arbitrary ZT guess

    set_ZT = set_ZT

    def set_h(self):
        """Sets TE effective heat transfer coefficient based on pure
        conduction""" 
        self.h = ( self.k * (self.area / (self.area_void + self.area)) 
        / self.length * 1.e-3)
        # effective heat transfer coefficient (kW/m^2-K)

    def solve_tem(self):
        """Solves for performance metrics of TE device"""
        self.set_h()
        self.T_h = self.T_h_goal
        self.eta = ( (self.T_h - self.T_c) * (sp.sqrt(1. + self.ZT) -
        1.) / (self.T_h * (sp.sqrt(1. + self.ZT) + self.T_c / self.T_h)) )
        # Carnot efficiency in segment
        self.q = self.h * (self.T_h - self.T_c)
        self.area_total = self.area + self.area_void
        self.P_heat = self.eta * self.q * self.area_total
        # TE power for leg pair (kW)
