# Distribution modules

import types
import numpy as np
import matplotlib.pyplot as mpl
import time
from scipy.optimize import fsolve
from scipy.integrate import odeint

# User defined modules
import te_prop
reload(te_prop)

class Leg(object):
    """class for individual p-type or n-type TE leg"""

    def __init__(self):
        """Sets the following: 
        self.I : current (A) in TE leg pair
        self.nodes : number of nodes for finite difference model
        self.length : leg length (m)
        self.area = : leg area (m^2)
        self.T_h_goal : hot side temperature (K) that matches HX BC
        self.T_c : cold side temperature (K)
        self.T : initial array for temperature (K) for finite
        difference model
        self.q : initial array for heat flux (W/m^2)
        self.V_nodes : initial array for Seebeck voltage (V)
        self.P_flux_nodes : initial array for power flux in node (W/m^2)

        Binds the following methods:
        te_prop.set_prop_fit
        te_prop.set_TEproperties"""
    
        self.I = 0.5 
        self.nodes = 10 
        self.length = 1.e-3
        self.area = (3.e-3)**2. 
        self.T_h_goal = 550. 
        self.T_c = 350. 

        self.alpha_nodes = np.zeros(self.nodes)
        self.rho_nodes = np.zeros(self.nodes)
        self.k_nodes = np.zeros(self.nodes)
        self.V_nodes = np.zeros(self.nodes) 
        self.P_flux_nodes = np.zeros(self.nodes) 

        self.set_constants()

        self.set_prop_fit = types.MethodType(te_prop.set_prop_fit,
        self) 
        self.set_TEproperties = (
        types.MethodType(te_prop.set_TEproperties, self) )
    
    def set_constants(self):
        """sets a few parameters"""
        self.node_length = self.length / self.nodes
        # length of each node (m)
        self.x = np.linspace(0., self.length, self.nodes) 

        self.J = self.I / self.area # (Amps/m^2)

    def set_q_c_guess(self):
        """Sets guess for q_c to be used by iterative solutions.""" 
        self.T_h = self.T_h_goal
        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        delta_T = self.T_h - self.T_c
        self.q_c = ( self.alpha * self.T_c * self.J - delta_T /
                     self.length * self.k - self.J**2 * self.length * self.rho )

        self.q_c_guess = self.q_c

    def get_Yprime(self, y, x):
        """Function for evaluating the derivatives of
        temperature and heat flux w.r.t. x."""
        
        T = y[0]
        q = y[1]
        V = y[2]
        R_int = y[3]
        
        self.T_props = T
        self.set_TEproperties(self.T_props)

        dT_dx = ( 1. / self.k * (self.J * T * self.alpha - q) )   

        dq_dx = ( (self.rho * self.J**2. * (1. + self.alpha**2. * T /
        (self.rho * self.k)) - self.J * self.alpha * q / self.k) )      

        dV_dx = ( self.alpha * dT_dx + self.J * self.rho ) 
        
        dR_dx = ( self.rho / self.area )  

        return dT_dx, dq_dx, dV_dx, dR_dx
            
    def solve_leg_once(self, q_c):
        """Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006. The model guesses a cold
        side heat flux and changes that heat flux until it results in
        the desired hot side temperature.  Hot side and cold side
        temperature as well as hot side heat flux must be
        specified.""" 

        print "running solve_leg_once"""
        self.q_c = q_c
        self.y0 = np.array([self.T_c, self.q_c, 0, 0])

        self.y = odeint(self.get_Yprime, y0=self.y0, t=self.x) 

        self.T_nodes = self.y[:,0]
        self.q_nodes = self.y[:,1]
        self.V_nodes = self.y[:,2]
        self.R_int_nodes = self.y[:,3]

        self.T_h = self.T_nodes[-1]
        self.q_h = self.q_nodes[-1]

        self.V = self.V_nodes[-1] 
        self.R_internal = self.R_int_nodes[-1]

        self.P_flux = self.J * self.V
        self.P = self.P_flux * self.area
        # Power for the entire leg (W)

        self.eta = self.P / (self.q_h * self.area)
        # Efficiency of leg
        self.R_load = - self.V / self.I

        self.T_h_error = self.T_h - self.T_h_goal
        
        return self.T_h_error
            
    def solve_leg(self):
        """Solves leg until specified hot side temperature is met.""" 

        self.set_q_c_guess()
        fsolve(self.solve_leg_once, x0=self.q_c_guess) 

    def solve_leg_anal(self):
        """Analytically solves the leg based on lumped properties.  No
        iteration is needed."""

        self.T_h = self.T_h_goal
        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        delta_T = self.T_h - self.T_c
        self.q_h = ( self.alpha * self.T_h * self.J - delta_T /
                     self.length * self.k + self.J**2. * self.length * self.rho
                     / 2. ) 
        self.q_c = ( self.alpha * self.T_c * self.J - delta_T /
                     self.length * self.k - self.J**2 * self.length * self.rho )

        self.P_flux = ( (self.alpha * delta_T * self.J + self.rho *
                         self.J**2 * self.length) ) 
        self.P = self.P_flux  * self.area
        self.eta = self.P / (self.q_h * self.area)
        self.eta_check = ( (self.J * self.alpha * delta_T + self.rho *
                            self.J**2. * self.length) / (self.alpha *
                            self.T_h * self.J - delta_T / self.length
                            * self.k + self.J**2 * self.length *
                            self.rho / 2.) ) 
        self.V = -self.P / np.abs(self.I)
        self.R_internal = self.rho * self.length / self.area
        self.R_load = - self.V / self.I

    def set_ZT(self):
        """Sets ZT based on formula
        self.ZT = self.sigma * self.alpha**2. / self.k""" 
        self.ZT = self.alpha**2. * self.T_props / (self.k * self.rho)

    def set_power_factor(self):
        """Sets power factor and maximum theoretical power for leg."""
        self.power_factor = self.alpha**2 * self.sigma
        self.power_max = ( self.power_factor * self.T_props**2 /
        self.length * self.area ) 


class TE_Pair(object):
    """class for TEModule that includes a pair of legs"""

    def __init__(self):
        """sets constants and defines leg instances"""
        self.leg_area_ratio = 0.7
        self.fill_fraction = 0.02
        self.length = 1.e-3
        self.I = 1. # electrical current (Amps)
        self.Ptype = Leg() # p-type instance of leg
        self.Ntype = Leg() # n-type instance of leg
        self.Ptype.material = 'HMS'
        self.Ntype.material = 'MgSi'
        self.area_void = (1.e-3)**2 # void area (m^2)
        self.length = 1.e-3 # default leg height (m)
        self.nodes = 10
        self.method = "numerical"

    def set_constants(self):
        """Sets constants that are calculated."""

        self.area = self.Ntype.area + self.Ptype.area + self.area_void 
        self.Ntype.length = self.length
        self.Ptype.length = self.length
        self.Ptype.nodes = self.nodes
        self.Ntype.nodes = self.nodes
        self.Ptype.I = -self.I
        # Current must have same sign as heat flux for p-type
        # material. Heat flux is negative because temperature gradient
        # is positive.  
        self.Ntype.I = self.I
        self.Ntype.set_constants()
        self.Ptype.set_constants()
        self.Ntype.method = self.method
        self.Ptype.method = self.method

    def solve_te_pair_once(self):
        """solves legs and combines results of leg pair"""
        self.Ptype.T_c = self.T_c
        self.Ntype.T_c = self.T_c

        self.Ntype.solve_leg_once(self.Ntype.q_c)
        self.Ptype.solve_leg_once(self.Ptype.q_c)
        self.T_h = self.Ntype.T_h

        self.q_h = ((self.Ptype.q_h * self.Ptype.area + self.Ntype.q_h
        * self.Ntype.area) / (self.area)) * 0.001
        # area averaged hot side heat flux (kW/m^2)
        self.q_c = ((self.Ptype.q_c * self.Ptype.area + self.Ntype.q_c
        * self.Ntype.area) / (self.area)) * 0.001
        # area averaged hot side heat flux (kW/m^2)

        self.h = self.q_h / (self.T_c - self.T_h) 
        # effective coeffient of convection (kW/m^2-K)
        self.R_thermal = 1. / self.h

    def get_error(self,knob_arr):
        """Returns hot and cold side error.  This doc string needs
        work.""" 

        self.Ntype.q_c = knob_arr[0]
        self.Ptype.q_c = knob_arr[1]
        self.T_c = knob_arr[2]

        self.solve_te_pair_once()

        self.q_c_conv = self.U_cold * (self.T_c_conv - self.T_c)
        self.q_h_conv = - self.U_hot * (self.T_h_conv - self.T_h)

        T_error = self.Ntype.T_h - self.Ptype.T_h 
        q_c_error = self.q_c - self.q_c_conv
        q_h_error = self.q_h - self.q_h_conv

        self.error = np.array([T_error, q_c_error, q_h_error])
        self.error = self.error.reshape(self.error.size)  

        return self.error

    def set_q_c_guess(self):
        """Sets cold side guess for both Ntype and Ptype legs."""
        self.Ntype.set_q_c_guess()
        self.Ptype.set_q_c_guess()

    def solve_te_pair(self):
        """solves legs and combines results of leg pair"""

        self.set_q_c_guess()
        knob_arr0 = np.array([self.Ntype.q_c_guess,
        self.Ptype.q_c_guess, self.T_c_conv])  

        self.fsolve_output = fsolve(self.get_error, x0=knob_arr0)

        self.P = -(self.Ntype.P + self.Ptype.P) * 0.001 
        # power for the entire leg pair(kW). Negative sign makes this
        # a positive number. Heat flux is negative so efficiency needs
        # a negative sign also.  
        self.P_flux = self.P / self.area
        # power flux (kW / m^2) through leg pair
        self.eta = -self.P / (self.q_h * self.area)
        self.V = self.Ntype.V + self.Ptype.V
        self.R_load = self.Ntype.R_load + self.Ptype.R_load
        self.R_internal = ( self.Ntype.R_internal +
        self.Ptype.R_internal )

    def set_TEproperties(self, T_props):
        """Sets properties for both legs based on temperature of
        module."""
        self.Ntype.set_TEproperties(T_props)
        self.Ptype.set_TEproperties(T_props)

    def set_ZT(self):
        """Sets ZT based on whatever properties were used last."""
        self.ZT = ( ((self.Ptype.alpha - self.Ntype.alpha) /
        ((self.Ptype.rho * self.Ptype.k)**0.5 + (self.Ntype.rho *
        self.Ntype.k)**0.5))**2. * self.T_props )

    def set_eta_max(self):
        """Sets theoretical maximum efficiency with material
        properties evaluated at the average temperature based on
        Sherman's analysis."""
        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        self.set_ZT()
        delta_T = self.T_h - self.T_c
        self.eta_max = ( delta_T / self.T_h * ((1. + self.ZT)**0.5 -
        1.) / ((1. + self.ZT)**0.5 + self.T_c / self.T_h) ) 
                
    def set_area(self):
        """Sets new N-type and P-type area based on desired area
        ratio. Ensures that sum of N-type and P-type area is
        constant.""" 
        area = self.Ntype.area + self.Ptype.area
        self.Ptype.area = area / (1. + self.leg_area_ratio)
        self.Ntype.area = area - self.Ptype.area

    def set_A_opt(self):
        """Sets Ntype / Ptype area that results in maximum efficiency
        based on material properties evaluated at the average
        temperature."""
        self.set_TEproperties(T_props=self.T_props)
        self.A_opt = np.sqrt(self.Ntype.rho * self.Ptype.k /
        (self.Ptype.rho * self.Ntype.k))

    def set_power_max(self):
        """Sets power factor and maximum theoretical power."""
        self.Ntype.set_power_factor()
        self.Ptype.set_power_factor()
        self.power_max = self.Ntype.power_max + self.Ptype.power_max 
    
    def set_all_areas(self, leg_area, leg_area_ratio, fill_fraction):
        """Sets leg areas and void area based on leg area ratio and
        fill fraction. 

        Arguments
        ----------------
        leg_area : base area of P-type leg
        leg_area_ratio : N/P area ratio
        fill_fraction : fraction of area taken up by legs"""

        self.leg_area_ratio = leg_area_ratio
        self.fill_fraction = fill_fraction

        self.Ptype.area = leg_area                           
        self.Ntype.area = self.Ptype.area * leg_area_ratio
        self.area_void = ( (1. - fill_fraction) / fill_fraction *
        (self.Ptype.area + self.Ntype.area) )  
        
