# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import numpy as np
import xlrd

# User Defined Modules
# In this directory
import hx
reload(hx)

area = (0.002)**2
length = 2.e-3

hx = hx.HX()
hx.width = 9.e-2
hx.length = 0.195
hx.exh.bypass = 0.
hx.exh.height = 1.e-2
mdot_cool = 4. * hx.cool.rho # coolant flow rate (GPM) 
hx.cool.mdot = mdot_cool / 60. * 3.8
hx.cool.height = 0.5e-2
hx.tem.I = 4.5
hx.tem.length = length
hx.tem.Ntype.material = 'MgSi'
hx.tem.Ntype.area = area
hx.tem.Ptype.material = 'HMS'
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'counter'
hx.exh.P = 100.

# things that must be consistent with experimental independent
# variables 

FILENAME = 'alumina paper.xls'
worksheet = xlrd.open_workbook(filename=FILENAME).sheet_by_index(0)

H2Oin = np.array(worksheet.col_values(0, start_rowx=4, end_rowx=16))
H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
datum = -11.0 # manometer datum (in)
pressure_drop = (H2Oin - datum) * 2. * H2O_kPa
# pressure drop across heat exchanger (kPa)

p = np.poly1d([3.23, 19.0])
flow = p(pressure_drop) # exhaust flow rate (L/s)

T_exh_in = np.array(worksheet.col_values(2, start_rowx=4,
                                         end_rowx=16))
T_exh_out = np.array(worksheet.col_values(3, start_rowx=4,
                                         end_rowx=16))
T_cool_in = np.array(worksheet.col_values(5, start_rowx=4,
                                         end_rowx=16))
T_cool_out = np.array(worksheet.col_values(4, start_rowx=4,
                                         end_rowx=16))

hx.Qdot1d = np.empty(np.size(flow))

for i in range(np.size(flow)):
    hx.cool.T_outlet = T_cool_out[i] + 273.15
    hx.exh.T_inlet = T_exh_in[i] + 273.15
    hx.exh.T = hx.exh.T_inlet
    hx.exh.set_TempPres_dependents()
    hx.exh.mdot = flow[i] * 1.e-3 * hx.exh.rho 
    hx.solve_hx()
    hx.Qdot1d[i] = hx.Qdot

print "\nProgram finished."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

flow_shaped = flow.reshape([3,4])
T1_shaped = T_exh_in.reshape([3,4])
hx.Qdot2d = hx.Qdot1d.reshape([3,4])

fig1 = plt.figure()
TICKS = np.arange(0,1.1,0.1)
LEVELS = np.arange(0, .75, 0.05)
FCS = plt.contourf(flow_shaped, T1_shaped, hx.Qdot2d) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label(label='Heat Transfer (kW)')
plt.grid()
# plt.subplots_adjust(left=0.18)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(right=0.75)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/model heat v T1 and Vdot alumina.pdf')
plt.savefig('Plots/model heat v T1 and Vdot alumina.png')

plt.show()

