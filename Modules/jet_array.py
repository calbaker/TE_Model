"""Module for modeling fins in exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np

class JetArray(object):
    """Class for modeling impinging jet array."""

    def __init__(self):
        """Initializes variables that do not require calculation.  

        Variables that are set
        -------------------------
        self.D : jet diameter (m)
        self.H : distance (m) from jet exit to impingement surface
        self.l : thickness (m) of the orifice plate
        self.K : minor loss coefficient. Fox, McDonald, and Pritchard
        Table 8.2.
        self.spacing : distance (m) between adjacent jets"""
        
        self.D = 0.005
        self.H = 0.01 
        self.l = 0.005
        self.K = 0.5
        self.spacing = 0.01
        
    def set_number(self):
        """Sets number of jets based on jet spacing and overall size
        of jet array.

        Set variables
        ----------------
        self.N_streamwise : number of jets in streamwise direction
        self.N_transverse : number of jets in transverse direction
        self.N : total number of jets in array

        Arguments
        ---------
        width : width (m) of jet array in transverse direction
        length : length (m) of jet array in streamwise direction""" 

        self.N_streamwise = length / self.spacing
        self.N_transverse = width / self.spacing
        self.N = self.N_streamwise * self.N_transverse 
        
    def set_flow(self):
        """Determines pressure drop through jet array. 

        Sets the following variables
        -------------------------------
        self.area : flow area (m^2) for single jet 
        self.V : velocity through jet orifice (m/s)
        self.h_loss : head loss (m^2/s^2) through jet orifice
        self.deltaP : pressure drop (kPa) thorugh jet orifice

        Variables that must be set to run this method
        ------------
        self.rho : density (kg/m^3) of fluid passing through jet
        self.Vdot : volume flow rate (m^3/s) of fluid passing through jet
        array""" 

        self.area = np.pi * self.D**2 / 4. 
        self.V = self.Vdot / (self.area * self.N) 
        self.h_loss = self.K * self.V**2 / 2.
        self.deltaP = self.h_loss * self.rho * 0.001

    def set_Nu_Dbar(self):
        """Sets Nusselt number and some other variables

        Sets the following variables
        -------------------------
        self.Nu_Dbar : average Nusselt number based on jet diameter
        self.Re_D : Re based on jet diameter
        
        Variables that must be set to run this method
        ------------
        self.nu : viscosity (m^2 / s) of fluid
        self.Pr : Prandtl number of fluid"""

        self.Re_D = self.V * self.D / self.nu
        self.Nu_Dbar = ( 0.285 * self.Re_D**0.710 * self.Pr**0.33 *
        (self.H / self.D)**-0.123 * (self.spacing / self.D)**-0.725 )  
        
    def solve_jet(self):
        """Runs the following methods:
        self.set_number
        self.set_flow
        self.set_Nu_Dbar"""
        
        self.set_number()
        self.set_flow()
        self.set_Nu_Dbar()
        
        
        
    
