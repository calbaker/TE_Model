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
height_cool = 0.01
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
hx_exp.exh.print_on = True

# model stuff
area = (0.002)**2
length = 1.e-3

hx_mod = hx.HX()
hx_mod.exh.bypass = 0.
hx_mod.cool.height = height_cool 
hx_mod.exh.height = height_exh
hx_mod.cool.mdot = mdot_cool
hx_mod.Qdot2d = np.empty(np.size(hx_exp.exh.T_array))
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
hx_mod.U_model = np.empty(np.size(hx_mod.Qdot2d))
hx_mod.exh.h_model = np.empty(np.size(hx_mod.Qdot2d))
hx_mod.effectiveness2d = np.empty(np.size(hx_mod.Qdot2d))
hx_exp.exh.Nu_exp = np.empty(np.size(hx_mod.Qdot2d))
hx_exp.exh.k = np.empty(np.size(hx_mod.Qdot2d))

for i in range(np.size(hx_mod.Qdot2d)):
    hx_mod.cool.T_outlet = hx_exp.cool.T_outlet_array[i] + 273.15
    hx_mod.exh.T_inlet = hx_exp.exh.T_inlet_array[i] + 273.15
    hx_mod.exh.T = hx_mod.exh.T_inlet
    hx_mod.exh.set_TempPres_dependents()
    hx_mod.exh.mdot = hx_exp.exh.flow_array[i] * hx_mod.exh.rho 
    hx_mod.solve_hx()
    hx_mod.exh.f_model[i] = hx_mod.exh.f_nodes.mean()
    hx_mod.exh.Nu_model[i] = hx_mod.exh.Nu_nodes.mean()
    hx_mod.U_model[i] = hx_mod.U_nodes.mean()
    hx_mod.exh.h_model[i] = hx_mod.exh.h_nodes.mean()
    hx_mod.Qdot2d[i] = hx_mod.Qdot
    hx_mod.effectiveness2d[i] = hx_mod.effectiveness
    hx_exp.exh.k[i] = hx_mod.exh.k

hx_exp.exh.delta_T_array = hx_exp.exh.delta_T_array.reshape([3,4])
hx_exp.exh.flow_shaped = hx_exp.exh.flow_array.reshape([3,4])
hx_mod.Qdot2d = hx_mod.Qdot2d.reshape([3,4])
hx_exp.exh.Qdot_exp2d = hx_exp.exh.Qdot_exp.reshape([3,4])
hx_exp.exh.T_inlet_array2d = hx_exp.exh.T_inlet_array.reshape([3,4]) 
Re_exh_shaped = hx_exp.exh.Re_exp.reshape([3,4])
f_model_shaped = hx_mod.exh.f_model.reshape([3,4])

# getting the experimental exhaust Nu
hx_exp.exh.R_thermal = ( hx_exp.exh.U_exp**-1 - ( 2. *
    hx_mod.plate.R_thermal + 2. * hx_mod.R_contact +
    hx_mod.cool.R_thermal) )
hx_exp.exh.h = 1. / hx_exp.exh.R_thermal
hx_exp.exh.Nu_exp = hx_exp.exh.h * hx_mod.exh.D / hx_exp.exh.k 


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

fig01 = plt.figure()
fig01.canvas.set_window_title('Parameterized Delta T')
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_exp.exh.delta_T_array[0,:], '--xr', label='exp 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_exp.exh.delta_T_array[1,:], '--sg', label='exp 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_exp.exh.delta_T_array[2,:], '--ob', label='exp 290 Nm') 
plt.legend(loc='upper right')
plt.grid()
plt.ylim(0,60)
plt.xlim(xmin=0)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'$\Delta$ T (K)')
fig01.savefig('Plots/SAE Paper/parameterized Delta T.pdf')
fig01.savefig('Plots/SAE Paper/parameterized Delta T.png')

fig02 = plt.figure()
fig02.canvas.set_window_title('Parameterized Qdot')
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_exp.exh.Qdot_exp2d[0,:], 'dr', label='exp 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_exp.exh.Qdot_exp2d[1,:], 'sg', label='exp 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_exp.exh.Qdot_exp2d[2,:], 'ob', label='exp 290 Nm') 
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_mod.Qdot2d[0,:], '-r', label='model 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_mod.Qdot2d[1,:], '--g', label='model 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_mod.Qdot2d[2,:], '-.b', label='model 290 Nm') 
plt.legend(loc='upper left')
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Heat Transfer Rate (kW)')
plt.xlim(xmin=0)
plt.ylim(ymax=3)
fig02.savefig('Plots/SAE Paper/Parameterized Qdot.pdf')
fig02.savefig('Plots/SAE Paper/Parameterized Qdot.png')

fig03 = plt.figure()
fig03.canvas.set_window_title('Friction Factor')
plt.plot(hx_exp.flow_data.Re_D, hx_exp.flow_data.f_exp, 'dk',
            label='43.4 Nm exp') 
plt.plot(Re_exh_shaped[0,:], f_model_shaped[0,:], '-r',
            label='43.4 Nm model') 
plt.plot(Re_exh_shaped[1,:], f_model_shaped[1,:], '-g',
            label='122 Nm model') 
plt.plot(Re_exh_shaped[2,:], f_model_shaped[2,:], '-b',
            label='290 Nm model') 
plt.xlabel('Exhaust Reynolds Number')
plt.ylabel('Exhaust Friction Factor')
plt.ylim(0, .15)
plt.xlim(xmin=0)
plt.subplots_adjust(left=0.14)
plt.grid()
plt.legend(loc='center left')
plt.savefig('Plots/SAE Paper/Friction Factor.pdf')
plt.savefig('Plots/SAE Paper/Friction Factor.png')

fig04 = plt.figure()
fig04.canvas.set_window_title('Experimental Qdot2d') 
TICKS = np.arange(0.1, 2.2, 0.2)
LEVELS = np.arange(0.1, 2.2, 0.2)
FCS = plt.contourf(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array2d,
                   hx_exp.exh.Qdot_exp2d, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer Rate (kW)')
plt.scatter(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array2d)
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/Experimental Qdot2d.pdf')
plt.savefig('Plots/SAE Paper/Experimental Qdot2d.png')

fig05 = plt.figure()
fig05.canvas.set_window_title('Model Qdot2d') 
FCS = plt.contourf(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array2d,
                   hx_mod.Qdot2d, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
CB.set_label(label='Heat Transfer Rate (kW)')
plt.scatter(hx_exp.exh.flow_shaped * 1.e3, hx_exp.exh.T_inlet_array2d) 
plt.grid()
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/Model Qdot2d.pdf')
plt.savefig('Plots/SAE Paper/Model Qdot2d.png')

# pressure_drop = hx_exp.exh.pressure_drop.copy()
# flow = hx_exp.exh.flow_array.copy()
# pressure_drop.sort()
# flow.sort()
# fig06 = plt.figure()
# fig06.canvas.set_window_title('Flow v Pressure')
# plt.plot(hx_exp.flow_data.pressure_drop, hx_exp.flow_data.flow *1e3, 'or',
#          label='experiment')
# plt.plot(pressure_drop, flow * 1e3, '--sk', 
#          label='model')
# plt.ylabel('Flow Rate (L/s)')
# plt.xlabel('Pressure Drop (kPa)')
# plt.ylim(ymin=0)
# plt.xlim(xmin=0)
# plt.grid()
# plt.legend(loc='lower right')
# plt.savefig('Plots/SAE Paper/Flow v Pressure.pdf')
# plt.savefig('Plots/SAE Paper/Flow v Pressure.png')

exchange_rate = ( hx_exp.exh.flow_shaped / (hx_mod.exh.height *
    hx_mod.exh.width * hx_mod.length) ) 
hx_mod.effectiveness2d = hx_mod.effectiveness2d.reshape([3,4])
hx_exp.effectiveness = ( hx_exp.exh.Qdot_exp / (hx_exp.exh.C
    * (hx_exp.exh.T_inlet_array - hx_exp.cool.T_inlet_array)) )
hx_exp.effectiveness2d = hx_exp.effectiveness.reshape([3,4])

eta_exp = hx_exp.effectiveness2d
eta_mod = hx_mod.effectiveness2d

fig07 = plt.figure()
fig07.canvas.set_window_title('Non-dim Parameterized Heat')
plt.plot(exchange_rate[0,:], eta_exp[0,:], 'dr', label='exp 43.4 Nm') 
plt.plot(exchange_rate[1,:], eta_exp[1,:], 'sg', label='exp 122 Nm') 
plt.plot(exchange_rate[2,:], eta_exp[2,:], 'ob', label='exp 290 Nm') 
plt.plot(exchange_rate[0,:], eta_mod[0,:], '-r', label='model 43.4 Nm') 
plt.plot(exchange_rate[1,:], eta_mod[1,:], '--g', label='model 122 Nm') 
plt.plot(exchange_rate[2,:], eta_mod[2,:], '-.b', label='model 290 Nm') 
plt.legend(loc='lower left')
plt.grid()
plt.xlabel('Gas Exchange Rate')
plt.ylabel('Heat Exchanger Effectiveness')
plt.ylim(0, 0.25)
plt.xlim(xmin=0)
plt.savefig('Plots/SAE Paper/Non-dim Parameterized Heat.pdf')
plt.savefig('Plots/SAE Paper/Non-dim Parameterized Heat.png')

fig08 = plt.figure()
fig08.canvas.set_window_title('Experimental eta_mod non-dim') 
TICKS = np.arange(0., 1.8, 0.2)
LEVELS = np.arange(0., 1.7, 0.1)
FCS = plt.contourf(exchange_rate, hx_exp.exh.T_inlet_array2d,
                   eta_exp)  
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label(label='Heat Exchanger Effectiveness')
plt.scatter(exchange_rate, hx_exp.exh.T_inlet_array2d)
plt.grid()
plt.xlabel('Gas Exchange Rate')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/Experimental eta_mod non-dim.pdf')
plt.savefig('Plots/SAE Paper/Experimental eta_mod non-dim.png')

fig09 = plt.figure()
fig09.canvas.set_window_title('Model eta_mod non-dim') 
FCS = plt.contourf(exchange_rate, hx_exp.exh.T_inlet_array2d,
                   eta_mod)  
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label(label='Heat Exchanger Effectiveness')
plt.scatter(exchange_rate, hx_exp.exh.T_inlet_array2d) 
plt.grid()
plt.xlabel('Gas Exchange Rate')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
plt.savefig('Plots/SAE Paper/Model eta_mod non-dim.pdf')
plt.savefig('Plots/SAE Paper/Model eta_mod non-dim.png')

fig10 = plt.figure()
fig10.canvas.set_window_title('Nu v Re')
plt.plot(hx_exp.exh.Re_exp[0:4] , hx_exp.exh.Nu_exp[0:4], '--sr',
         label='43.4 Nm exp')
plt.plot(hx_exp.exh.Re_exp[4:8] , hx_exp.exh.Nu_exp[4:8], '--sg',
         label='122 Nm exp')
plt.plot(hx_exp.exh.Re_exp[8:12], hx_exp.exh.Nu_exp[8:12], '--sb',
         label='290 Nm exp')
plt.plot(hx_exp.exh.Re_exp[0:4] , hx_mod.exh.Nu_model[0:4], '-dr',
         label='43.4 Nm model')
plt.plot(hx_exp.exh.Re_exp[4:8] , hx_mod.exh.Nu_model[4:8], '-dg',
         label='122 Nm model')
plt.plot(hx_exp.exh.Re_exp[8:12], hx_mod.exh.Nu_model[8:12], '-db',
         label='290 Nm model')
plt.xlabel('Reynolds Number')
plt.ylabel('Nusselt Number')
plt.xlim(0,6e4)
plt.ylim(ymin=0)
plt.grid()
plt.legend(loc='lower right')
fig10.savefig('Plots/SAE Paper/Nu v Re.pdf')
fig10.savefig('Plots/SAE Paper/Nu v Re.png')

fig11 = plt.figure()
fig11.canvas.set_window_title('Parameterized T_inlet')
plt.plot(hx_exp.exh.flow_shaped[0,:] * 1.e3, hx_exp.exh.T_inlet_array2d[0,:], '--xr', label='exp 43.4 Nm') 
plt.plot(hx_exp.exh.flow_shaped[1,:] * 1.e3, hx_exp.exh.T_inlet_array2d[1,:], '--sg', label='exp 122 Nm') 
plt.plot(hx_exp.exh.flow_shaped[2,:] * 1.e3, hx_exp.exh.T_inlet_array2d[2,:], '--ob', label='exp 290 Nm') 
plt.legend(loc='upper left')
plt.grid()
plt.xlim(xmin=0)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Hot Side $T_{inlet}$ ($^\circ$C)')
fig11.savefig('Plots/SAE Paper/parameterized T_inlet.pdf')
fig11.savefig('Plots/SAE Paper/parameterized T_inlet.png')
