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
hx.filename_heat = 'alumina paper.xls'
hx.start_rowx = 4
hx.end_rowx = 8
hx.import_heat_data()
hx.poly_eval()
hx.set_Qdot()
hx.set_Nu()

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.plot(hx.exh.Re_D, hx.U_ana, label="empirical")
plt.plot(hx.exh.Re_D, hx.exh.U_exp, label="experimental")
plt.legend(loc='best')
plt.grid()
plt.xlabel('Reynolds Number')
plt.ylabel('Heat Transfer Coefficient (kW/m^2-K)')

plt.show()
