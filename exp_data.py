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

p = np.poly1d([3.23, 19.0])
air = prop.ideal_gas()

FILENAME = 'empty heat exchanger.xls'
worksheet = xlrd.open_workbook(filename=FILENAME).sheet_by_index(0)

H2Oin = np.array(worksheet.col_values(0, start_rowx=4, end_rowx=16))
H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
datum = -11.0 # manometer datum (in)
pressure_drop = (H2Oin - datum) * 2. * H2O_kPa
# pressure drop across heat exchanger (kPa)

flow = p(pressure_drop) # exhaust flow rate (L/s)

T_exh_in = np.array(worksheet.col_values(2, start_rowx=4,
                                         end_rowx=16))
T_exh_out = np.array(worksheet.col_values(3, start_rowx=4,
                                         end_rowx=16))
T_cool_in = np.array(worksheet.col_values(5, start_rowx=4,
                                         end_rowx=16))
T_cool_out = np.array(worksheet.col_values(4, start_rowx=4,
                                         end_rowx=16))

air.P = 100.

air.T = 0.5 * (T_exh_in + T_exh_out)
air.set_TempPres_dependents()

deltaT_exh = T_exh_in - T_exh_out
deltaT_cool = T_cool_in - T_cool_out
heat_exh = flow * 1.e-3 * air.rho * air.c_p_air * deltaT_exh

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

flow_shaped = flow.reshape([3,4])
T1_shaped = T_exh_in.reshape([3,4])
heat_exh_shaped = heat_exh.reshape([3,4])

fig1 = plt.figure()
TICKS = np.arange(0,1.1,0.1)
LEVELS = np.arange(0, .75, 0.05)
FCS = plt.contourf(flow_shaped, T1_shaped, heat_exh_shaped) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label(label='Heat Transfer (kW)')
plt.grid()
# plt.subplots_adjust(left=0.18)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(right=0.75)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Exhaust Inlet Temp (K)')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/heat v T1 and Vdot.pdf')

plt.show()
