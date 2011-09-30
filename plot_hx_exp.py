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
hx_exp.flow_data.import_flow_data()
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

# model stuff
area = (0.002)**2
length = 2.e-3

hx_mod = hx.HX()
hx_mod.Qdot2d = np.empty(np.size(hx_mod.exh.T_array))
hx_mod.tem.Ntype.material = 'alumina'
hx_mod.tem.Ptype.material = 'alumina'
hx_mod.thermoelectrics_on = False
hx_mod.tem.I = 1.5
hx_mod.tem.length = length
hx_mod.tem.Ntype.area = area
hx_mod.tem.Ptype.area = area * 2. 
hx_mod.tem.area_void = 25. * area
hx_mod.type = 'counter'
hx_mod.exh.P = 100.

hx_mod.exh.f_model = np.empty(np.size(hx_mod.Qdot2d))
hx_mod.exh.Nu_model = np.empty(np.size(hx_mod.Qdot2d))

for i in range(np.size(hx_mod.Qdot2d)):
    hx_mod.cool.T_outlet = hx_mod.cool.T_outlet_array[i] + 273.15
    hx_mod.exh.T_inlet = hx_mod.exh.T_inlet_array[i] + 273.15
    hx_mod.exh.T = hx_mod.exh.T_inlet
    hx_mod.exh.set_TempPres_dependents()
    hx_mod.exh.mdot = hx_mod.exh.flow_array[i] * hx_mod.exh.rho 
    hx_mod.solve_hx()
    hx_mod.exh.f_model[i] = hx_mod.exh.f_nodes.mean()
    hx_mod.exh.Nu_model[i] = hx_mod.exh.Nu_nodes.mean()
    hx_mod.Qdot2d[i] = hx_mod.Qdot

hx_mod.exh.delta_T_array = hx_mod.exh.delta_T_array.reshape([3,4])
hx_mod.exh.flow_shaped = hx_mod.exh.flow_array.reshape([3,4])
hx_mod.Qdot2d = hx_mod.Qdot2d.reshape([3,4])
hx_mod.exh.Qdot_exp = hx_mod.exh.Qdot_exp.reshape([3,4])
hx_mod.exh.T_inlet_array = hx_mod.exh.T_inlet_array.reshape([3,4]) 
Re_exh_shaped = hx_mod.exh.Re_exp.reshape([3,4])
f_model_shaped = hx_mod.exh.f_model.reshape([3,4])

############ Plots!

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE 
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8
plt.rcParams['axes.formatter.limits'] = -3,3

fig01 = plt.figure()
fig01.canvas.set_window_title('Parameterized Delta T')
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_exp.exh.delta_T_array[0,:], '--xr', label='exp 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_exp.exh.delta_T_array[1,:], '--sg', label='exp 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_exp.exh.delta_T_array[2,:], '--ob', label='exp 290 Nm') 
plt.legend(loc='upper right')
plt.grid()
plt.ylim(0,60)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'$\Delta$ T (K)')
fig01.savefig('Plots/SAE Paper/delta T v Vdot parameterized.pdf')
fig01.savefig('Plots/SAE Paper/delta T v Vdot parameterized.png')

fig02 = plt.figure()
fig02.canvas.set_window_title('Parameterized Qdot')
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_exp.exh.Qdot_exp[0,:], 'xr', label='exp 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_exp.exh.Qdot_exp[1,:], 'sg', label='exp 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_exp.exh.Qdot_exp[2,:], 'ob', label='exp 290 Nm') 
plt.plot(hx_mod.exh.flow_shaped[0,:] * 1.e3, hx_mod.Qdot2d[0,:], '-r', label='model 43.4 Nm') 
plt.plot(hx_mod.exh.flow_shaped[1,:] * 1.e3, hx_mod.Qdot2d[1,:], '--g', label='model 122 Nm') 
plt.plot(hx_mod.exh.flow_shaped[2,:] * 1.e3, hx_mod.Qdot2d[2,:], '-.b', label='model 290 Nm') 
plt.legend(loc='upper left')
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Heat Transfer Rate (kW)')
fig02.savefig('Plots/SAE Paper/heat v Vdot parameterized.pdf')
fig02.savefig('Plots/SAE Paper/heat v Vdot parameterized.png')

fig03 = plt.figure()
fig03.canvas.set_window_title('Friction Factor')
plt.plot(hx_exp.flow_data.Re_D, hx_exp.flow_data.f_exp, 'kx',
            label='43.4 Nm exp') 
plt.plot(Re_exh_shaped[0,:], f_model_shaped[0,:], '-r',
            label='43.4 Nm model') 
plt.plot(Re_exh_shaped[1,:], f_model_shaped[1,:], '-g',
            label='122 Nm model') 
plt.plot(Re_exh_shaped[2,:], f_model_shaped[2,:], '-b',
            label='290 Nm model') 
plt.xlabel('Exhaust Reynolds Number')
plt.ylabel('Exhaust Friction Factor')
plt.ylim(ymin=0)
plt.grid()
plt.legend(loc='lower left')
plt.savefig('Plots/SAE Paper/f v Re.pdf')
plt.savefig('Plots/SAE Paper/f v Re.png')

fig04 = plt.figure()
fig04.canvas.set_window_title('Experimental Qdot2d') 
TICKS = np.linspace(0.2, 2, 10)
LEVELS = np.linspace(0.2, 2, 10)
FCS = plt.contourf(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array,
                   hx_exp.exh.Qdot_exp, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer Rate (kW)')
plt.scatter(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array)
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/heat v T1 and Vdot exp.pdf')
plt.savefig('Plots/SAE Paper/heat v T1 and Vdot exp.png')

fig05 = plt.figure()
fig05.canvas.set_window_title('Model Qdot2d') 
FCS = plt.contourf(hx_mod.exh.flow_shaped * 1.e3, hx_mod.exh.T_inlet_array,
                   hx_mod.Qdot2d, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer Rate (kW)')
plt.scatter(hx_mod.exh.flow_shaped * 1.e3, hx_mod.exh.T_inlet_array) 
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/heat v T1 and Vdot mod.pdf')
plt.savefig('Plots/SAE Paper/heat v T1 and Vdot mod.png')

pressure_drop = hx_mod.exh.pressure_drop.copy()
flow = hx_mod.exh.flow_array.copy()
pressure_drop.sort()
flow.sort()
fig06 = plt.figure()
fig06.canvas.set_window_title('Flow v Pressure')
plt.plot(hx_exp.flow_data.pressure_drop, hx_exp.flow_data.flow *1e3, 'or',
         label='experiment')
plt.plot(pressure_drop, flow * 1e3, '--sk', 
         label='model')
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Pressure Drop (kPa)')
plt.grid()
plt.legend(loc='lower right')
plt.savefig('Plots/SAE Paper/press v flow.pdf')
plt.savefig('Plots/SAE Paper/press v flow.png')
