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
import enhancement
reload(enhancement)

class Exhaust(prop.ideal_gas):
    """Class for modeling convection and flow of engine exhaust
    through heat exchanger."""

    def __init__(self):
        """Sets the following constants:
        self.porous : determines whether porous metal foam is used as
        heat transfer enhancement.  Default is 'no'.  
        self.enh : determines what method of heat transfer
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
        
        self.enh_lib : class attribute copy of enhancement library

        Binds the following methods from functions.py:
        set_flow_geometry
        set_Re
        set_Re_dependents
        
        Also initializes super class"""

        super(Exhaust, self).__init__()

        self.enh_lib = enhancement
        self.T_ref = 300.
        self.P = 101.
        self.height = 1.5e-2
        self.ducts = 1

        self.Nu_coeff = 0.023

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
        self.velocity = self.Vdot / self.flow_area # velocity (m/s) of exhaust

        self.k = self.k_air
        
        try:
            self.enh
        except AttributeError:
            self.enh = None
        
        if self.enh == None:
            self.set_Re_dependents()
            self.deltaP = ( self.f * self.perimeter * self.node_length /
            self.flow_area * (0.5 * self.rho * self.velocity**2) * 0.001 ) 
            # pressure drop (kPa)
            self.h = self.Nu_D * self.k / self.D 
            # coefficient of convection (kW/m^2-K)

        else:
            self.enh.solve_enh(self)

        self.Wdot_pumping = self.Vdot * self.deltaP 
        # pumping power (kW)

        self.R_thermal = 1. / self.h
        # thermal resistance (m^2-K/kW) of exhaust

