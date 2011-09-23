"""Module for importing data from excel and getting into numpy arrays
for use with model."""

# Distribution Modules
import matplotlib.pyplot as plt
import xlrd
import numpy as np
import scipy.interpolate as interp
import scipy.optimize as spopt

# User Defined Modules
# In this directory
import hx
reload(hx)
import properties as prop

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
        self.filename_flow = 'manometer calibration.xls'
        self.start_rowx = 2
        self.end_rowx = 11
        self.poly_order = 1

    H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa        

    def import_flow_data(self):
        """Imports data and stores it in numpy arrays."""
        worksheet = (
        xlrd.open_workbook(filename=self.filename_flow).sheet_by_index(0) )
        self.datum = worksheet.cell_value(0,1)
        self.reading = np.array(worksheet.col_values(0,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx))
        # manometer reading (in) for downstream side only 
        self.steel = np.array(worksheet.col_values(1,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx))
        # position of steel ball in rotameter controlling propane flow 
        self.pressure_C3H8 = np.array(worksheet.col_values(2,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        # pressure guage reading (psi)
        self.C3H8 = np.array(worksheet.col_values(3,
        start_rowx=self.start_rowx, end_rowx=self.end_rowx))
        # propane concentration (ppm) with propane flow

    def manipulate_flow_data(self):
        """Converts imported data into convenient units and such."""
        self.C3H8flow0psi = 11.276 * self.steel + 62.102
        # propane flow (mL/min) with no back pressure
        self.C3H8flow2psi = 12.303 * self.steel + 46.823
        # propane flow (mL/min) with 2 psi back pressure
        self.C3H8flow = ( self.C3H8flow0psi - (self.C3H8flow0psi -
        self.C3H8flow2psi) / 2. * self.pressure_C3H8 ) 
        # propane flow (mL/min) based on linear interpolation for pressure
        self.flow = ( self.C3H8flow / (self.C3H8 * 1.e-6) / 1000. /
        60. )  
        # exhaust flow (L/s)
        self.pressure_drop = ( (self.reading - self.datum) * 2. *
        self.H2O_kPa )
        # pressure drop (kPa) in heat exchanger

    def spline_rep(self):
        """Determines spline parameters to fit flow to pressure drop."""
        self.import_flow_data()
        self.manipulate_flow_data()
        self.flow.sort()
        self.pressure_drop.sort()
        self.spline = interp.splrep(self.pressure_drop, self.flow)

    def poly_rep(self):
        """Determines polynomial coefficients to produce fit for flow
        v. pressure drop data."""
        self.import_flow_data()
        self.manipulate_flow_data()
        self.poly1d = np.poly1d(np.polyfit(self.pressure_drop,
        self.flow, self.poly_order))

class HeatData(hx.HX):
    """Class for handling data from heat exchanger experiments."""

    def __init__(self):
        super(HeatData, self).__init__()
        self.alumina = Dummy_TE()
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
        self.exh.reading = np.array(worksheet.col_values(0,
    start_rowx=self.start_rowx, end_rowx=self.end_rowx)) 
        self.exh.datum = worksheet.cell_value(2,4) # manometer datum (in) 
        self.exh.pressure_drop = ( (self.exh.reading - self.exh.datum) * 2. *
        self.H2O_kPa )
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
        self.exh.T = ( 0.5 * (self.exh.T_inlet_array +
        self.exh.T_outlet_array) + 273.15)
        self.exh.set_TempPres_dependents()
        self.exh.delta_T = ( self.exh.T_inlet_array -
        self.exh.T_outlet_array )
        self.exh.mdot = self.exh.rho * self.exh.flow
        self.exh.C = self.exh.mdot * self.exh.c_p_air
        
        self.cool.delta_T = ( self.cool.T_inlet_array -
        self.cool.T_outlet_array )
        self.cool.mdot = self.cool.rho * self.cool.flow
        self.cool.C = self.cool.mdot * self.cool.c_p        

    def spline_eval(self):
        """Evaluates spline fit parameters to fit flow to pressure
        drop. """
        self.flow_data.spline_rep()
        self.exh.flow = interp.splev(self.exh.pressure_drop,
        self.flow_data.spline)  

    def poly_eval(self):
        """Evaluates polynomial fit of flow to pressure."""
        self.flow_data.poly_rep()
        self.exh.flow = ( self.flow_data.poly1d(self.exh.pressure_drop)
        * 1.e-3 )

    def set_Qdot_exp(self):
        """Sets heat transfer based on mdot c_p delta T."""
        self.manipulate_heat_data()
        self.exh.Qdot_exp = ( self.exh.C * self.exh.delta_T )
        self.cool.Qdot_exp = ( self.cool.C * self.cool.delta_T )        

    def set_T_lm(self):
        """Sets log mean temperature difference."""
        self.delta_T_lm = ( ((self.exh.T_outlet_array -
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
        self.length * self.delta_T_lm) )  
        self.cool.U_exp = ( self.cool.Qdot_exp / (self.width *
        self.length * self.delta_T_lm) )  

