"""Module for importing data from excel and getting into numpy arrays
for use with model."""

# Distribution Modules
import matplotlib.pyplot as plt
import xlrd
import numpy as np
import scipy.interpolate as spint 
import scipy.optimize as spopt

# User Defined Modules
# In this directory
import hx
reload(hx)
import properties as prop

def get_flow(pressure_drop, coeff):
    """Sets flow based on coefficient and pressure drop.""" 
    flow = coeff * pressure_drop**0.5
    return flow

class Dummy_TE(object):
    """Class for handling TE device without any TE properties."""

    def __init__(self):
        """Defaults"""
        self.k = 1.5e-3
        # thermal conductivity of alumina (kW/m-K)
        self.thickness = 1.e-3
        # thickness (m) of alumina paper
        self.h = self.k / self.thickness
        # effective heat transfer coefficient (kW/m^2-K)
        self.R_thermal = 1. / self.h
    

class FlowData():
    """Class for handling flow rate and pressure drop data.""" 
    def __init__(self):
        """Sets default file name, start row, and end row.""" 
        self.filename_flow = 'trash can flow meter.xls'
        self.start_rowx = 2
        self.end_rowx = 17
        self.poly_order = 2
        self.trash_volume = 77.6e-3 # trash can volume (m^3) 

    H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa        

    def import_flow_data(self):
        """Imports data and stores it in numpy arrays."""
        worksheet = (
        xlrd.open_workbook(filename=self.filename_flow).sheet_by_index(0) )
        self.corrected_reading = np.array(worksheet.col_values(1,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx))
        # corrected manometer reading (in) for downstream side only
        self.time = np.array(worksheet.col_values(3,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx))
        # time (s) for trash can to fill with exhaust
        self.T = ( np.array(worksheet.col_values(5,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx)) + 273.15
        ) # temperature (K) of gas in trash can flow meter

        self.flow_trash = self.trash_volume / self.time
        # exhaust flow (m^3/s) into trash can

        self.pressure_drop = self.corrected_reading * self.H2O_kPa
        # pressure drop (kPa) through HX


class HeatData(hx.HX):
    """Class for handling data from heat exchanger experiments."""

    def __init__(self):
        super(HeatData, self).__init__()
        self.alumina = Dummy_TE()
        self.filename_heat = 'alumina paper.xls'
        self.start_rowx = 4
        self.end_rowx = 16
        self.Nu_guess = 0.023
        # guess for Nu = Nu_guess * Re_D**(4/5) * Pr**(1/3)
        self.cool.flow = 4. * 3.8 * 1.e-3 / 60.
        # default coolant flow rate (m^3/s)
        
    H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
    flow_data = FlowData()

    def import_heat_data(self):
        """Function for importing data from heat exchanger experiment
        excel files and recasting it as numpy arrays."""
        worksheet = (
    xlrd.open_workbook(filename=self.filename_heat).sheet_by_index(0)
        )  
        self.exh.corrected_reading = np.array(worksheet.col_values(0,
    start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        self.exh.datum = worksheet.cell_value(2,4) # manometer datum (in) 
        self.exh.pressure_drop = ( (self.exh.corrected_reading -
        self.exh.datum) * 2. * self.H2O_kPa ) 
        # pressure drop across heat exchanger (kPa)
        self.cummins.torque = np.array(worksheet.col_values(1,
        start_rowx=self.start_rowx,  end_rowx=self.end_rowx))
        self.exh.T_inlet_array = np.array(worksheet.col_values(2,
            start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        self.exh.T_outlet_array = np.array(worksheet.col_values(3,
            start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        self.cool.T_inlet_array = np.array(worksheet.col_values(5,
            start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        self.cool.T_outlet_array = np.array(worksheet.col_values(4,
            start_rowx=self.start_rowx, end_rowx=self.end_rowx))  

    def manipulate_heat_data(self):
        """Gets heat exchanger data ready for doing stuff to it.""" 
        self.exh.T_array = ( 0.5 * (self.exh.T_inlet_array +
        self.exh.T_outlet_array) + 273.15)
        self.exh.delta_T_array = ( self.exh.T_inlet_array -
        self.exh.T_outlet_array )
                
        self.cool.delta_T_array = ( self.cool.T_inlet_array -
        self.cool.T_outlet_array )
        self.cool.C = self.cool.mdot * self.cool.c_p

    def set_flow_corrected(self):
        """Sets fit parameters for flow through the heat exchanger
        based on temperature correction."""
        self.exh.temp_v_press_fit = (
        np.polyfit(self.exh.pressure_drop[0:4],
        self.exh.T_array[0:4], 2) ) 
        self.flow_data.T_hx = np.polyval(self.exh.temp_v_press_fit,
        self.flow_data.pressure_drop) 
        self.flow_data.flow = ( self.flow_data.flow_trash *
        self.flow_data.T_hx / self.flow_data.T )

    def set_flow_array(self):
        """Sets experimental flow rate through heat exchanger"""
        flow = self.flow_data.flow
        pressure_drop = self.flow_data.pressure_drop
        popt, pcov = spopt.curve_fit(get_flow, pressure_drop,
        flow)
        self.exh.flow_coeff = popt
        self.exh.flow_array = ( self.exh.flow_coeff *
        self.exh.pressure_drop**0.5 )

    def set_Qdot_exp(self):
        """Sets heat transfer based on mdot c_p delta T."""
        self.manipulate_heat_data()
        self.exh.Qdot_exp = ( self.exh.C * self.exh.delta_T_array )
        self.cool.Qdot_exp = ( self.cool.C * self.cool.delta_T_array )        

    def set_T_lm(self):
        """Sets log mean temperature difference."""
        self.delta_T_lm_array = ( ((self.exh.T_outlet_array -
        self.cool.T_inlet_array) - (self.exh.T_inlet_array -
        self.cool.T_outlet_array)) / np.log((self.exh.T_outlet_array -
        self.cool.T_inlet_array) / (self.exh.T_inlet_array -
        self.cool.T_outlet_array)) )

    def set_U_exp(self):
        """Sets overall heat transfer coefficient based on
        something."""
        self.set_T_lm()
        self.set_Qdot_exp()
        self.exh.U_exp = ( self.exh.Qdot_exp / (self.width *
        self.length * self.delta_T_lm_array) )  
        self.cool.U_exp = ( self.cool.Qdot_exp / (self.width *
        self.length * self.delta_T_lm_array) )

    def set_Re_exp(self):
        """Sets experimental Reynolds number."""
        self.exh.set_flow_geometry(self.width)
        self.set_properties()
        self.exh.velocity_array = self.exh.flow_array / self.exh.area 
        self.exh.Re_exp = ( self.exh.rho_array * self.exh.velocity_array *
        self.exh.D / self.exh.mu_array )

    def set_f_exp(self):
        """Sets friction factor based on experimental data."""
        self.set_Re_exp()
        self.exh.f_exp = ( 0.25 * 2. * self.exh.pressure_drop * 1.e3 / (
        self.exh.length * self.exh.perimeter / self.exh.area * 
        self.exh.rho_array * self.exh.velocity_array**2) )         

    def set_properties(self):
        """Sets array of temperature and pressure dependent properties
        based on average temperature in HX."""
        self.exh.rho_array = np.empty(np.size(self.exh.T_array))
        self.exh.mu_array = np.empty(np.size(self.exh.T_array))
        for i in range(np.size(self.exh.T_array)):
            self.exh.T = self.exh.T_array[i]
            self.exh.set_TempPres_dependents()
            self.exh.rho_array[i] = self.exh.rho
            self.exh.mu_array[i] = self.exh.mu

    def set_mass_flow(self):
        """Sets mass flow based on other stuff"""
        self.exh.mdot_exp = self.exh.flow_array * self.exh.rho_array
        self.exh.C = self.exh.mdot_exp * self.exh.c_p_air
