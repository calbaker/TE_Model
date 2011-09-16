"""Module for importing data from excel and getting into numpy arrays
for use with model."""

# Distribution Modules
import matplotlib.pyplot as plt
import xlrd
import numpy as np
from scipy import interpolate 

# User Defined Modules
# In this directory
import hx
reload(hx)
import properties as prop

class FlowData():
    """Class for handling flow rate and pressure drop data.""" 
    def __init__(self):
        """Sets default file name, start row, and end row.""" 
        self.filename_flow = 'manometer calibration.xls'
        self.start_rowx = 1
        self.end_rowx = 10

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
        self.pressure_guage = np.array(worksheet.col_values(2,
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
        self.C3H8flow2psi) / 2. * self.C3H8pressure ) 
        # propane flow (mL/min) based on linear interpolation for pressure
        self.flow = ( self.C3H8flow / (self.C3H8conc * 1.e-6) /
        1000. / 60. ) 
        # exhaust flow (L/s)
        self.pressure_drop = ( (self.reading - self.datum) * 2. *
        self.H2O_kPa )
        # pressure drop (kPa) in heat exchanger

class HeatData(hx.HX):
    """Class for handling data from heat exchanger experiments."""
    H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
    flow_data = FlowData()

    def import_heat_data(self):
        """Function for importing data from heat exchanger experiment
        excel files and recasting it as numpy arrays."""
        worksheet = (
    xlrd.open_workbook(filename=self.filename_heat).sheet_by_index(0)
        )  
        self.reading = np.array(worksheet.col_values(0,
    start_rowx=self.start_rowx, end_rowx=16)) 
        self.datum = worksheet.cell_value(2,4) # manometer datum (in) 
        self.pressure_drop = ( (self.reading - self.datum) * 2. *
        self.H2O_kPa )
        # pressure drop across heat exchanger (kPa)

        self.exh.T_inlet_array = np.array(worksheet.col_values(2,
            start_rowx=self.start_rowx, end_rowx=16)) 
        self.exh.T_outlet_array = np.array(worksheet.col_values(3,
            start_rowx=self.start_rowx, end_rowx=16)) 
        self.cool.T_inlet = np.array(worksheet.col_values(5,
            start_rowx=self.start_rowx, end_rowx=16)) 
        self.cool.T_outlet = np.array(worksheet.col_values(4,
            start_rowx=self.start_rowx, end_rowx=16))  

    def manipulate_heat_data(self):
        """Gets heat exchanger data ready for doing stuff to it.""" 
        self.import_heat_data()
        self.exh.T = ( 0.5 * (self.exh.T_inlet_array +
        self.exh.T_outlet_array) )
        self.exh.set_TempPres_dependents()

    def spline_fit(self):
        """Spline fits flow to pressure drop."""
        self.flow_data.import_flow_data()
        self.flow_data.manipulate_flow_data()
        self.spline = splrep(self.flow_data.pressure_drop,
        self.flow_data.flow) 
        self.flow = splev(self.pressure_drop, self.spline)

    def set_Qdot(self):
        """Sets heat transfer based on mdot c_p delta T."""
        self.manipulate_heat_data()
        self.exh.Qdot_exp = ( self.flow * 1.e-3 * exh.rho *
        exh.c_p_air * (self.exh.T_inlet_array -
        self.exh.T_outlet_array) ) 

