# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import xlrd
import numpy as np

# User Defined Modules
import hx
reload(hx)
import properties as prop
import exp_data
reload(exp_data)

width = 9.e-2
length = 0.195
height_exh = 1.e-2
height_cool = 0.005
Vdot_cool = 4. # coolant flow rate (GPM) 

# experimental stuff
hx_exp = exp_data.HeatData()
hx_exp.type = 'counter'
hx_exp.flow_data.import_flow_data()
hx_exp.start_rowx = 8
hx_exp.end_rowx = 12
hx_exp.import_heat_data()
hx_exp.manipulate_heat_data()
hx_exp.set_flow_corrected()
hx_exp.set_flow_array()
hx_exp.P = 100.
hx_exp.set_properties()
hx_exp.width = width
hx_exp.length = length
hx_exp.exh.bypass = 0.
hx_exp.exh.height = height_exh 
hx_exp.cool.height = height_cool
mdot_cool = Vdot_cool / 60. * 3.8 / 1000. * hx_exp.cool.rho   
hx_exp.cool.mdot = mdot_cool 
hx_exp.set_mass_flow()
hx_exp.set_U_exp()
hx_exp.exh.set_flow_geometry(hx_exp.width)
hx_exp.set_f_exp()
hx_exp.set_Re_exp()
hx_exp.set_params()

############ Plots!
plt.close('all')

FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE 
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8
plt.rcParams['axes.formatter.limits'] = -3,3

