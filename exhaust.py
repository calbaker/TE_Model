"""Module for modeling exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np

# In python directory
import properties as prop

# In this directory
import functions


class _Fin():
    """Class for modeling fin.  This class finds the necessary fin
    parameters such that the efficiency is near unity, and therefore
    the fin is isothermal."""

    def __init__(self):
        """Sets constants and things that need to be guessed to
        execute as a standalone model."""
        self.thickness = 1.e-3 # fin thickness (m)
        self.k = 0.2 # thermal conductivity (kW/m-K) of fin material
        self.h = 0.2
        # heat transfer coefficient (kW/m^2-K).  This can be updated
        # from Exhaust.

    def set_eta(self):
        """Determines fin efficiency"""
        self.m = np.sqrt(2. * self.h / (self.k * self.thickness))
        self.eta = ( np.tanh(self.m * self.height) / (self.m *
        self.height) )

    def set_h(self):
        """Determines effective heat transfer coefficient of fin."""
        self.set_eta()
        self.h_base = ( 2. * self.eta * self.h * self.height /
        self.thickness )


class Exhaust(prop.ideal_gas):
    """class for exhaust flow"""

    def __init__(self):
        """sets constants and initiates class instances"""
        prop.ideal_gas.__init__(self)
        self.porous = 'no' # is there porous media?
        self.enhancement = 'none' # is there any means of enhancement? (i.e. fins,
            # corrugate metal, etc.)
        self.T_ref = 300 # default reference temperature (K) for availability calculation
        self.height = 1.5e-2 # default height (m) of exhaust duct
        self.ducts = 1 # default number of exhaust ducts
        self.porosity = 0.92 # default volume of void per total volume
        self.k_matrix = 5.8e-3 # default thermal conductivity(kW/m-K) of metal foam +
            # air
        self.PPI = 10 # default pores per inch of porous media, used in Mancin model  
        self.K = 2.e-7 # default permeability (m^2) of porous metal foam, used in
            # Bejan model
        self.bypass = 0.80
        # fraction of exhaust flow bypassing heat exchanger
        self.fin = _Fin() # workaround to be able to change fin from
                          # instance

    set_flow_geometry = functions.set_flow_geometry
    set_Re_dependents = functions.set_Re_dependents

    def set_flow(self):
        """calculates flow parameters"""        
        self.T = 0.5 * (self.T_in + self.T_out)
        # Temperature (K) used to calculate fluid
            # properties.  This is no good if T_out is much
            # different from T_in
        self.set_alpha()
        self.c_p = self.c_p_air

        self.C = self.mdot * self.c_p # heat capacity of
        # flow (kW/K)
        self.Vdot = self.mdot / self.rho # volume flow rate (m^3/s) of exhaust
        self.velocity = self.Vdot / self.area # velocity (m/s) of exhaust

        if self.enhancement == 'Bejan porous':
            self.Nu_D = 6. # Nu for porous media parallel plates with const
                # heat flux.  Bejan Eq. 12.77 
            self.Re_K = self.velocity * self.K**0.5 / self.nu # Re
                # based on permeability from
                # Bejan Eq. 12.11    
            self.f = 1. / self.Re_K + 0.55 # Darcy Law, Bejan
                # Eq. 12.14.  It turns out
                # that f is pretty close to
                # 0.55
            self.k = self.k_matrix
            self.deltaP = (self.f * self.perimeter * self.length /
             self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)
            self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)

        elif self.enhancement == 'Mancin porous':
            self.k = self.k_matrix
            self.Nu_D = 4.93 # Nu for porous media parallel plates with
                # T_w = const.  Bejan Eq. 12.77
            self.G = self.rho * self.velocity # Mass velocity from
                # Mancin et al.
            self.D_pore = 0.0122 * self.PPI**(-0.849) # hydraulic
                # diameter (m?) of porous
                # media based on Mancin et
                # al.  
            self.Re_K = ( self.D_pore * self.G / (self.mu * self.porosity) )
            # Re of porous media from Mancin et al.
            self.F = ( (1.765 * self.Re_K**(-0.1014) * self.porosity**2 /
            self.PPI**(0.6)) ) # friction factor from Mancin et al. 
            self.deltaP = (self.length * 2. * self.F * self.G**2 /
            (self.D_pore * self.rho)) # pressure drop from Mancin et al.
            self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)

        elif self.enhancement == 'straight fins':
            # self.fins is the number of fins that fully extend across
            # the duct.  The flow area and flow perimeter calculations
            # depend on this.  For the heat transfer, this number also
            # work. The fins will be spaced in such a way as to make
            # an  array of square ducts. 
            self.fin.height = self.height / 2
            # height of fin pair such that their tips meet in the
            # middle and are adiabatic.  
            self.fin.length = self.length
            self.fin.spacing = ( self.width - self.fins *
        self.fin.thickness ) / (self.fins + 1)
            self.flow_perimeter = ( 2. * ((self.width - self.fins *
        self.fin.thickness) / (self.fins + 1.) + self.height) ) 
            # perimeter of new duct formed by fins with constant overal duct width
            self.flow_area = ( (self.width - self.fins *
        self.fin.thickness) / (self.fins + 1.) * self.height ) 
            # flow area (m^2) of new duct formed by fin    
            self.D = 4. * self.flow_area / self.flow_perimeter
            self.k = self.k_air
            self.set_Re_dependents()
            self.h = self.Nu_D * self.k / self.D
            # coefficient of convection (kW/m^2-K) 
            self.fin.h = self.h
            self.fin.set_h()
            self.h = ( (self.h * (self.width - self.fins *
        self.fin.thickness) + self.fin.h_base * self.fins *
        self.fin.thickness) / self.width ) 
            self.deltaP = (self.f * self.flow_perimeter * self.length /
        self.flow_area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)

        elif self.enhancement == 'none':            
            self.k = self.k_air
            self.set_Re_dependents()
            self.deltaP = (self.f * self.perimeter * self.length /
            self.area * (0.5*self.rho * self.velocity**2)*1.e-3) # pressure drop (kPa)
            self.h = self.Nu_D * self.k / self.D # coefficient of convection (kW/m^2-K)

        self.Wdot_pumping = self.Vdot * self.deltaP # pumping power (kW)

