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
hx.filename_heat = 'alumina paper truncated.xls'
hx.start_rowx = 4
hx.end_rowx = 13
hx.import_heat_data()
hx.poly_eval()
hx.set_U_exp()

area = (0.002)**2
length = 2.e-3
hx.Qdot2d = np.empty(np.size(hx.exh.flow_array))
hx.tem.Ntype.material = 'alumina'
hx.tem.Ptype.material = 'alumina'
hx.thermoelectrics_on = False
hx.width = 9.e-2
hx.length = 0.195
hx.exh.bypass = 0.
hx.exh.height = 1.e-2
Vdot_cool = 4. # coolant flow rate (GPM) 
mdot_cool = 4. / 60. * 3.8 / 1000. * hx.cool.rho  
hx.cool.mdot = mdot_cool / 60. * 3.8
hx.cool.height = 0.5e-2
hx.tem.I = 1.5
hx.tem.length = length
hx.tem.Ntype.area = area
hx.tem.Ptype.area = area * 2. 
hx.tem.area_void = 25. * area
hx.type = 'counter'
hx.exh.P = 100.


for i in range(np.size(hx.Qdot2d)):
    hx.cool.T_outlet = hx.cool.T_outlet_array[i] + 273.15
    hx.exh.T_inlet = hx.exh.T_inlet_array[i] + 273.15
    hx.exh.T = hx.exh.T_inlet
    hx.exh.set_TempPres_dependents()
    hx.exh.mdot = hx.exh.flow_array[i] * hx.exh.rho 
    hx.solve_hx()
    hx.Qdot2d[i] = hx.Qdot

hx.exh.Qdot_exp.reshape([3,3])
hx.exh.flow_array = hx.exh.flow_array.reshape([3,3])
hx.Qdot2d = hx.Qdot2d.reshape([3,3])
hx.exh.Qdot_exp = hx.exh.Qdot_exp.reshape([3,3])
hx.exh.T_inlet_array = hx.exh.T_inlet_array.reshape([3,3]) 

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

fig1 = plt.figure()
fig1.canvas.set_window_title('Parameterized')
plt.plot(hx.exh.flow_array[0,:] * 1.e3, hx.exh.Qdot_exp[0,:], 'xr', label='exp 32 ft-lbs') 
plt.plot(hx.exh.flow_array[1,:] * 1.e3, hx.exh.Qdot_exp[1,:], 'sg', label='exp 90 ft-lbs') 
plt.plot(hx.exh.flow_array[2,:] * 1.e3, hx.exh.Qdot_exp[2,:], 'ob', label='exp 214 ft-lbs') 
plt.plot(hx.exh.flow_array[0,:] * 1.e3, hx.Qdot2d[0,:], '-r', label='model 32 ft-lbs') 
plt.plot(hx.exh.flow_array[1,:] * 1.e3, hx.Qdot2d[1,:], '--g', label='model 90 ft-lbs') 
plt.plot(hx.exh.flow_array[2,:] * 1.e3, hx.Qdot2d[2,:], '-.b', label='model 214 ft-lbs') 

plt.legend(loc='upper left')
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Heat Transfer (kW)')
fig1.savefig('Plots/heat v Vdot parameterized.pdf')
fig1.savefig('Plots/heat v Vdot parameterized.png')

fig2 = plt.figure()
fig2.canvas.set_window_title('Experimental') 
TICKS = np.arange(0.2,1.6,0.2)
LEVELS = np.arange(0.2, 1.6, 0.1)
FCS = plt.contourf(hx.exh.flow_array * 1.e3, hx.exh.T_inlet_array,
                   hx.exh.Qdot_exp, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer (kW)')
plt.scatter(hx.exh.flow_array * 1.e3, hx.exh.T_inlet_array)
plt.grid()
# plt.subplots_adjust(left=0.18)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(right=0.75)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/heat v T1 and Vdot exp.pdf')
plt.savefig('Plots/heat v T1 and Vdot exp.png')

fig3 = plt.figure()
fig3.canvas.set_window_title('Model') 
FCS = plt.contourf(hx.exh.flow_array * 1.e3, hx.exh.T_inlet_array,
                   hx.Qdot2d, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer (kW)')
plt.scatter(hx.exh.flow_array * 1.e3, hx.exh.T_inlet_array) 
plt.grid()
# plt.subplots_adjust(left=0.18)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(right=0.75)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/heat v T1 and Vdot mod.pdf')
plt.savefig('Plots/heat v T1 and Vdot mod.png')

# plt.show()

