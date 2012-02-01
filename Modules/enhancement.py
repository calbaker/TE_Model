"""Module for modeling fins in exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np

class BejanPorous(object):
    """Class for modeling porous media according to Bejan."""

    def __init__(self):
        """Initializes the following: 
        --------------------------
        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.Nu_D : Nu for porous media parallel plates with const
        heat flux.  Bejan Eq. 12.77"""

        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.Nu_D = 6. 
    
    def solve_enhancement(self,exh):
        self.Re_K = self.velocity * self.K**0.5 / self.nu 
        # Re based on permeability from Bejan Eq. 12.11    
        self.f = 1. / self.Re_K + 0.55 # Darcy Law, Bejan
        # Eq. 12.14.  It turns out that f is pretty close to 0.55 
        self.k = self.k_matrix
        self.deltaP = ( self.f * self.perimeter * self.length /
                    self.flow_area * (0.5 * self.rho * self.velocity**2) * 0.001 )   
        # pressure drop (kPa) 
        self.h = self.Nu_D * self.k / self.D 
        # coefficient of convection (kW/m^2-K)
        
class MancinPorous(object):            
    """Class for modeling porous media according to Mancin."""

    def __init__(self):
        """Doc string"""

        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.k = self.k_matrix
        self.Nu_D = 4.93
        # Nu for porous media parallel plates with T_w = const.  Bejan Eq. 12.77

    def solve_enhancement(self):
        self.G = self.rho * self.velocity 
        # Mass velocity from Mancin et al.
        self.D_pore = 0.0122 * self.PPI**(-0.849) 
        # hydraulic diameter (m?) of porous media based on Mancin
        # et al.  
        self.Re_K = ( self.D_pore * self.G / (self.mu * self.porosity) )
        # Re of porous media from Mancin et al.
        self.F = ( (1.765 * self.Re_K**(-0.1014) * self.porosity**2 /
                    self.PPI**(0.6)) ) 
        # friction factor from Mancin et al. 
        self.f = self.F 
        # possibly wrong assignment but gets code to shut up and run 
        self.deltaP = ( self.length * 2. * self.F * self.G**2 /
                        (self.D_pore * self.rho) * 0.001 )  
        # pressure drop from Mancin et al.
        self.h = self.Nu_D * self.k_matrix / self.D 
        # coefficient of convection (kW/m^2-K)

class IdealFin(object):
    """Class for modeling fin."""

    def __init__(self):
        """Sets constants and things that need to be guessed to
        execute as a standalone model.

        Sets
        ------------------
        self.thickness : thickness (m) of fin
        self.k : thermal conductivity (kW/m-K) of fin material"""

        self.thickness = 5.e-3
        self.k = 0.2

    def set_eta(self,exh):
        """Determines fin efficiency"""
        exh.set_Re_dependents()
        exh.deltaP = ( exh.f * exh.perimeter * exh.length /
                        exh.flow_area * (0.5*exh.rho * exh.velocity**2) * 0.001 ) 
        # pressure drop (kPa)
        exh.h = exh.Nu_D * exh.k / exh.D 
        # coefficient of convection (kW/m^2-K)
        
        self.m = np.sqrt(2. * exh.h / (self.k * self.thickness))
        self.eta = ( np.tanh(self.m * exh.height) / (self.m *
        exh.height) )

    def set_h(self,exh):
        """Determines effective heat transfer coefficient of fin."""
        self.set_eta(exh)
        self.h_base = ( 2. * self.eta * exh.h * exh.height /
        self.thickness )
        exh.h_unfinned = exh.h
        exh.h = self.h_base

    def solve_enhancement(self,exh):
        """Runs all the other methods that need to run."""
        self.set_h(exh)
        
class JetArray(object):
    """Class for modeling impinging jet array."""

    def __init__(self):
        """Initializes variables that do not require calculation.  

        Variables that are set
        -------------------------
        self.D : jet diameter (m)
        self.H : distance (m) from jet exit to impingement surface
        self.K : minor loss coefficient. Fox, McDonald, and Pritchard
        Table 8.2.
        self.spacing : distance (m) between adjacent jets"""
        
        self.D = 2.4e-3
        self.H = 5.5e-2
        self.K = 0.5
        self.spacing = 1.3e-2
        
    def set_number(self):
        """Sets number of jets based on jet spacing and overall size
        of jet array.

        Set variables
        ----------------
        self.N_streamwise : number of jets in streamwise direction
        self.N_transverse : number of jets in transverse direction
        self.N : total number of jets in array
        self.area : area (m^2) of a jet unit cell

        Variables that must be set to run this method
        ---------
        self.width : width (m) of jet array in transverse direction
        self.length : length (m) of jet array in streamwise direction""" 

        self.N_streamwise = self.length / self.spacing
        self.N_transverse = self.width / self.spacing
        self.N = self.N_streamwise * self.N_transverse 
        self.area = self.spacing**2 
        
    def set_annulus(self):
        """Sets variables related to annulus geometry.

        Requires
        ---------------
        self.width
        self.Vdot

        Sets
        ---------------
        self.ann_area
        self.ann_perimeter
        self.ann_velocity"""

        self.ann_area = self.width * self.H
        self.ann_perimeter = 2. * (self.width + self.H)
        self.ann_velocity = self.Vdot / self.ann_area / 2. 

    def set_flow(self):
        """Determines pressure drop through jet array. 

        Sets the following variables
        -------------------------------
        self.flow_area : flow area (m^2) for single jet 
        self.V : velocity through jet orifice (m/s)
        self.h_loss : head loss (m^2/s^2) through jet orifice
        self.deltaP : pressure drop (kPa) thorugh jet orifice

        Variables that must be set to run this method
        ------------
        self.rho : density (kg/m^3) of fluid passing through jet
        self.Vdot : volume flow rate (m^3/s) of fluid passing through jet
        array""" 

        self.flow_area = np.pi * self.D**2 / 4. 
        self.V = self.Vdot / (self.flow_area * self.N) 
        self.h_loss = self.K * self.V**2 / 2.
        self.deltaP = self.h_loss * self.rho * 0.001

    def set_Nu_D(self):
        """Sets Nusselt number and some other variables

        Sets the following variables
        -------------------------
        self.Nu_D : average Nusselt number based on jet diameter
        self.Re_D : Re based on jet diameter
        
        Variables that must be set to run this method
        ------------
        self.nu : viscosity (m^2 / s) of fluid
        self.Pr : Prandtl number of fluid"""

        self.Re_D = self.V * self.D / self.nu
        self.Nu_D = ( 0.285 * self.Re_D**0.710 * self.Pr**0.33 *
        (self.H / self.D)**-0.123 * (self.spacing / self.D)**-0.725 )  
        
    def solve_enhancement(self,exh):
        self.set_number()
        self.set_annulus()
        self.set_flow()
        self.set_Nu_D()

class OffsetStripFin(object):
    """Class for modeling offset strip fins. Uses correlations from:
 
    Manglik, Raj M., and Arthur E. Bergles, 'Heat Transfer and
    Pressure Drop Correlations for the Rectangular Offset Strip Fin
    Compact Heat Exchanger', Experimental Thermal and Fluid Science,
    10 (1995), 171-180 <doi:10.1016/0894-1777(94)00096-Q>."""

    def __init__(self):
        """Sets constants and things that need to be guessed to
        execute as a standalone model.

        Sets
        ------------------
        self.t : thickness (m) of fin strip
        self.l : length (m) of fin"""

        self.t = 0.001
        self.l = 0.01
        self.s = 0.001

    def set_params(self,exh):
        """Sets parameters used to calculate friction factor and
        Colburn factor.  See Manglik and Bergles Fig. 1.

        Requires
        -------------------
        self.height
        self.t : thickness (m) of fin strip
        self.l : length (m) of fin

        Sets
        --------------------
        self.h : vertical gap (m) between fins and hx walls
        self.s : horizontal gap (m) between fins  
        self.alpha = self.s / self.h
        self.delta = self.t / self.l
        self.gamma = self.t / self.s

        more stuff that needs to be documented"""
        
        self.h = exh.height - self.t

        self.alpha = self.s / self.h
        self.delta = self.t / self.l
        self.gamma = self.t / self.s 

        self.D = ( 4. * self.s * self.h * self.l / (2. * (self.s *
        self.l + self.h * self.l + self.t * self.h) + self.t * self.s)
        )
        self.Re_D = exh.velocity * self.D / exh.nu

    def set_f(self):
        """Sets friction factor, f."""
        self.f = ( 9.6243 * self.Re_D**-0.7422 * self.alpha**-0.1856 *
        self.delta**0.3053 * self.gamma**-0.2659 ) 

    def set_j(self):
        """Sets Colburn factor, j."""
        self.j = ( 0.6522 * self.Re_D**-0.5403 * self.alpha**-0.1541 *
        self.delta**0.1499 * self.gamma**-0.0678 * (1. + 5.269e-5 *
        self.Re_D**1.340 * self.alpha**0.504 * self.delta**0.456 *
        self.gamma**-1.055)**0.1 ) 

    def solve_enhancement(self,exh):
        self.set_params(exh)
        self.set_f()
        exh.f = self.f
        exh.deltaP = ( self.f * exh.perimeter * exh.length /
                    exh.flow_area * (0.5 * exh.rho * exh.velocity**2) * 0.001 )  
        # pressure drop (kPa)
        self.set_j()
        exh.h = ( self.j * exh.mdot / exh.flow_area * exh.c_p /
                   exh.Pr**0.667 )
        exh.Nu_D = self.h * self.D / exh.k
    
