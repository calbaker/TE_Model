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
    
    def solve_enh(self,exh):
        self.Re_K = self.velocity * self.K**0.5 / self.nu 
        # Re based on permeability from Bejan Eq. 12.11    
        self.f = 1. / self.Re_K + 0.55 
        # Darcy Law, Bejan Eq. 12.14.  It turns out that f is pretty
        # close to 0.55  
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
        # Nu for porous media parallel plates with T_w = const.  Bejan
        # Eq. 12.77 

    def solve_enh(self):
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
        self.k : thermal conductivity (kW/m-K) of fin material
        self.N : number of fins in duct in spanwise direction"""

        self.thickness = 1.e-3
        self.k = 0.2
        self.N = 45

    def set_geometry(self,exh):
        """Fixes appropriate geometrical parameters."""

        self.height = exh.height / 2
        # height of fin pair such that their tips meet in the
        # middle and are adiabatic.  
        self.spacing = ( (exh.width - self.N *  self.thickness) /
        (self.N + 1.) )  
        self.perimeter = ( 2. * (self.spacing + exh.height) * (self.N
        + 1.) )    
        # perimeter of new duct formed by fins with constant overal duct width
        self.flow_area = self.spacing * exh.height * (self.N + 1.)
        # flow area (m^2) of new duct formed by fin    
        self.D = 4. * self.flow_area / self.perimeter

    def set_h(self,exh):
        """Determines effective heat transfer coefficient of fin."""
        exh.h_unfinned = exh.h

        self.effectiveness = self.eta * 2. * self.height / self.thickness
        self.h_base = self.effectiveness * exh.h 
        exh.h = ( (exh.h_unfinned * (exh.width - self.N *
        self.thickness) + self.h_base * self.N * self.thickness) /
        exh.width )  

    def set_eta(self,exh):
        """Determines fin efficiency
        Sets
        ------------------
        self.beta : dimensionless fin parameter
        self.xi : beta times fin length (self.height)
        self.eta : fin efficiency"""
        self.beta = np.sqrt(2. * exh.h / (self.k * self.thickness)) 
        self.xi = self.beta * self.height
        self.eta = np.tanh(self.xi) / self.xi

        exh.deltaP = ( exh.f * self.perimeter * exh.node_length /
        self.flow_area * (0.5 * exh.rho * exh.velocity**2) * 0.001 )    
        # pressure drop (kPa)
 
    def solve_enh(self,exh):
        """Runs all the other methods that need to run."""
        self.set_geometry(exh)
        exh.velocity = exh.Vdot / self.flow_area
        exh.set_Re_dependents()
        exh.h = exh.Nu_D * exh.k / exh.D
        # coefficient of convection (kW/m^2-K) 
        self.h = exh.h
        self.set_eta(exh) 
        self.set_h(exh)
        self.h = ( (self.h * (exh.width - self.N *  self.thickness) +
        self.h_base * self.N * self.thickness) / exh.width )   
        

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
        
        self.D = 3.0e-3
        self.H = 1.0e-2
        self.K = 0.5
        self.spacing = 0.5e-2
        
    def set_number(self,exh):
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

        self.N_streamwise = exh.length / self.spacing
        self.N_transverse = exh.width / self.spacing
        self.N = self.N_streamwise * self.N_transverse 
        self.area = self.spacing**2 
        
    def set_annulus(self,exh):
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

        self.ann_area = exh.width * self.H
        self.ann_perimeter = 2. * (exh.width + self.H)
        self.ann_velocity = exh.Vdot / self.ann_area / 2. 

    def set_flow(self,exh):
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
        self.V = exh.Vdot / (self.flow_area * self.N) 
        self.h_loss = self.K * self.V**2 / 2.
        exh.deltaP = self.h_loss * exh.rho * 0.001

    def set_Nu_D(self,exh):
        """Sets Nusselt number and some other variables

        Sets the following variables
        -------------------------
        self.Nu_D : average Nusselt number based on jet diameter
        self.Re_D : Re based on jet diameter
        
        Variables that must be set to run this method
        ------------
        self.nu : viscosity (m^2 / s) of fluid
        self.Pr : Prandtl number of fluid"""

        self.Re_D = self.V * self.D / exh.nu
        exh.Nu_D = ( 0.285 * self.Re_D**0.710 * exh.Pr**0.33 *
        (self.H / self.D)**-0.123 * (self.spacing / self.D)**-0.725 )  
        
    def solve_enh(self,exh):
        self.set_number(exh)
        self.set_annulus(exh)
        self.set_flow(exh)
        self.set_Nu_D(exh)
        exh.h = exh.Nu_D * exh.k / self.D
        exh.f = 37.
        # this might need to be changed, or it might be a dummy
        # variable just to keep the code from complaining.  


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
        self.l : length (m) of fin
        self.s : pitch (m) of fin
        self.k : thermal conductivity (W/m/K) of osf material""" 

        self.t = 0.001
        self.l = 0.01
        self.s = 0.001
        self.k = 0.2

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
        self.area_frac : fraction of original area still available
        for flow 
        self.flow_area : actual flow area (m^2)
        self.velocity : actual velocity (m/s) based on flow area
        self.area_enh : heat transfer area enhancment factor
        self.rows : number of rows of offset strip fins in streamwise
        direction 

        more stuff that needs to be documented"""
        
        self.h = exh.height - self.t

        self.alpha = self.s / self.h
        self.delta = self.t / self.l
        self.gamma = self.t / self.s 

        self.rows = exh.length / self.l

        self.area_frac = ( (self.s * self.h) / ((self.h + self.t) *
        (self.s + self.t)) )  

        self.area_enh = ( (self.h * self.t +  self.h * self.l + self.s
        * self.l) / ((self.t + self.s) * self.l) )

        self.D = ( 4. * self.s * self.h * self.l / (2. * (self.s *
        self.l + self.h * self.l + self.t * self.h) + self.t * self.s)
        )

        self.flow_area = exh.flow_area * self.area_frac 
        self.velocity = exh.velocity / self.area_frac
        self.Re_D = self.velocity * self.D / exh.nu

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

    def solve_enh(self,exh):
        """Solves all the stuff for this class.
        self.h comes from Thermal Design by HoSung Lee, eq. 5.230
        self.eta_fin : fin efficiency"""
        self.set_params(exh)
        self.set_f()
        exh.f = self.f
        exh.deltaP = ( self.f * exh.perimeter * exh.node_length /
                    exh.flow_area * (0.5 * exh.rho * self.velocity**2) * 0.001 )  
        # pressure drop (kPa)
        self.set_j()
        self.h_conv = ( self.j * exh.mdot / self.flow_area * exh.c_p /
                   exh.Pr**0.667 )
        self.beta = np.sqrt(2. * self.h_conv / (self.k * self.t))   
        self.xi = self.beta * self.h / 2. 
        self.eta_fin = np.tanh(self.xi) / self.xi
        self.effectiveness = self.eta_fin * self.h / self.t
        self.h_base = self.h_conv * self.effectiveness
        exh.h = ( (self.h_base * self.t + self.h_conv * self.s) /
        (self.s + self.t) ) 

        exh.Nu_D = exh.h * exh.D / exh.k
    
