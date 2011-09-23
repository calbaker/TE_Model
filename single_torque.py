# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import xlrd
import numpy as np

# User Defined Modules
# In this directory
import hx
reload(hx)
import properties as prop
import exp_data
reload(exp_data)

hx = exp_data.HeatData()
hx.type = 'counter'
hx.thermoelectrics_on = False
hx.filename_heat = 'alumina paper.xls'
hx.start_rowx = 5
hx.end_rowx = 8
hx.import_heat_data()
hx.poly_eval()
hx.set_U_exp()

hx.Qdot1d = np.empty(np.size(hx.exh.flow_array))

for i in range(np.size(hx.Qdot1d)):
    hx.cool.T_outlet = hx.cool.T_outlet_array[i] + 273.15
    hx.exh.T_inlet = hx.exh.T_inlet_array[i] + 273.15
    hx.exh.T = hx.exh.T_inlet
    hx.exh.set_TempPres_dependents()
    hx.exh.mdot = hx.exh.flow_array[i] * hx.exh.rho 
    hx.solve_hx()
    hx.Qdot1d[i] = hx.Qdot

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.scatter(hx.exh.flow_array * 1.e3, hx.exh.U_exp, label="experimental")
plt.legend(loc='best')
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Heat Transfer Coefficient (kW/m^2-K)')
plt.ylim(0,0.5)

plt.show()
