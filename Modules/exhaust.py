"""Module for modeling exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np
import types

# In python directory
import properties as prop
reload(prop)

# In this directory
import functions
reload(functions)
import fin
reload(fin)
import jet_array
reload(jet_array)

class Exhaust(prop.ideal_gas):
    """Class for modeling convection and flow of engine exhaust
    through heat exchanger."""

    def __init__(self):
        """Sets the following constants:
        self.porous : determines whether porous metal foam is used as
        heat transfer enhancement.  Default is 'no'.  
        self.enhancement : determines what method of heat transfer
        enhancement, if any, is used.  Default is 'none'.
        self.T_ref : reference restricted dead state temperature (K)
        for availability calculations.
        self.P : pressure (kPa) at which calculations are done.
        self.height : exhaust duct height (m). Default is 1.5e-2 m.  
        self.ducts : number of exhaust ducts in parallel. 
        self.porosity : porosity (void volume per total volume) of
        porous metal foam enhancement 
        self.k_matrix : thermal conductivity (kW/m/K) of the metal
        foam matrix
        self.PPI : pores per inch for porous media in Mancin model
        self.K : default permeability (m^2) of porous metal foam, used
        in Bejan model  
        self.Nu_coeff : coefficient used in Nusselt number calculation

        self.fin : instance of fin.Fin class
        self.jets : instance of jet_array.JetArray class 

        
        Binds the following methods from functions.py:
        set_flow_geometry
        set_Re
        set_Re_dependents
        
        Also initializes super class"""

        super(Exhaust, self).__init__()
        self.porous = 'no' # is there porous media?
        self.enhancement = 'none' # is there any means of enhancement? (i.e. fins,
            # corrugate metal, etc.)
        self.T_ref = 300.
        self.P = 101.
        self.height = 1.5e-2
        self.ducts = 1
        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.Nu_coeff = 0.023

        self.fin = fin.Fin() 
        self.jets = jet_array.JetArray()

        self.set_flow_geometry = (
        types.MethodType(functions.set_flow_geometry, self) )
        self.set_Re = (
        types.MethodType(functions.set_Re, self) )
        self.set_Re_dependents = (
        types.MethodType(functions.set_Re_dependents, self) )

    def set_flow(self):
        """calculates flow parameters"""        
        self.set_thermal_props()
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
            self.deltaP = ( self.f * self.perimeter * self.length /
            self.area * (0.5 * self.rho * self.velocity**2) * 0.001 ) 
            # pressure drop (kPa) 
            self.h = self.Nu_D * self.k / self.D 
            # coefficient of convection (kW/m^2-K)

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
            self.f = self.F 
            # possibly wrong assignment but gets code to shut up and run 
            self.deltaP = ( self.length * 2. * self.F * self.G**2 /
            (self.D_pore * self.rho) * 0.001 ) 
            # pressure drop from Mancin et al.
            self.h = self.Nu_D * self.k / self.D 
            # coefficient of convection (kW/m^2-K)

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
            self.deltaP = ( self.f * self.flow_perimeter * self.length
        / self.flow_area * (0.5*self.rho * self.velocity**2) * 0.001 )  
        # pressure drop (kPa)

        elif self.enhancement == 'jet array':            
            self.k = self.k_air
            self.set_Re_dependents()
            self.deltaP_duct = ( self.f * self.perimeter * self.length
            / self.area * (0.5 * self.rho * self.velocity**2) * 0.001 )  
            # pressure drop (kPa)
            self.total_height = self.jets.H * 2. + self.height
            self.jets.width = self.width
            self.jets.length = self.length
            self.jets.rho = self.rho
            self.jets.Vdot = self.Vdot 
            self.jets.nu = self.nu 
            self.jets.Pr = self.Pr
            self.jets.solve_jet()


            self.deltaP_annulus = ( self.f * 2. *
            self.jets.ann_perimeter * self.length / self.jets.ann_area
            * (0.5 * self.rho * self.jets.ann_velocity**2) * 0.001 ) 

            self.deltaP = ( self.deltaP_duct + self.jets.deltaP +
            self.deltaP_annulus ) 
            self.h = self.jets.Nu_D * self.k / self.jets.D 
            # coefficient of convection (kW/m^2-K)

        elif self.enhancement == 'none':            
            self.k = self.k_air
            self.set_Re_dependents()
            self.deltaP = ( self.f * self.perimeter * self.length /
            self.area * (0.5*self.rho * self.velocity**2) * 0.001 ) 
            # pressure drop (kPa)
            self.h = self.Nu_D * self.k / self.D 
            # coefficient of convection (kW/m^2-K)

        self.Wdot_pumping = self.Vdot * self.deltaP 
        # pumping power (kW)
        if self.enhancement == 'straight fins':
            self.fin.h = self.h

        self.R_thermal = 1. / self.h
        # thermal resistance (m^2-K/kW) of exhaust

