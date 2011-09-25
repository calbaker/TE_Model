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
hx.import_heat_data()
hx.poly_eval()
hx.set_Qdot_exp()
hx.set_U_exp()

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

flow_shaped = hx.exh.flow_array.reshape([3,4]) * 1.e3
# exponent converts back to L/s
T1_shaped = hx.exh.T_inlet_array.reshape([3,4]) 
heat_exh_shaped = hx.exh.Qdot_exp.reshape([3,4])
torque_shaped = hx.cummins.torque.reshape([3,4])
delta_T_shaped = hx.exh.delta_T_array.reshape([3,4])
U_exh_shaped = hx.exh.U_exp.reshape([3,4])

fig1 = plt.figure()
TICKS = np.arange(0,1.1,0.1)
LEVELS = np.arange(0, .75, 0.05)
FCS = plt.contourf(flow_shaped, T1_shaped, heat_exh_shaped) 
CB = plt.colorbar(FCS, orientation='vertical')
CB.set_label(label='Heat Transfer (kW)')
plt.scatter(hx.exh.flow_array * 1.e3, hx.exh.T_inlet_array) 
plt.grid()
# plt.subplots_adjust(left=0.18)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(right=0.75)
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Exhaust Inlet Temp ($^\circ$C)')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/heat v T1 and Vdot.pdf')
plt.savefig('Plots/heat v T1 and Vdot.png')

######## Plots of stuff v flow rate

fig2 = plt.figure()
plt.plot(flow_shaped[0,:], heat_exh_shaped[0,:], '-x',
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(flow_shaped[1,:], heat_exh_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(flow_shaped[2,:], heat_exh_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Flow Rate (L/s)')
plt.ylabel('Heat Transfer (kW)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/heat v Vdot.pdf')
plt.savefig('Plots/heat v Vdot.png')

fig3 = plt.figure()
plt.plot(flow_shaped[0,:], delta_T_shaped[0,:], '-x',
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(flow_shaped[1,:], delta_T_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(flow_shaped[2,:], delta_T_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'$\Delta T$ (K)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/delta_T v Vdot.pdf')
plt.savefig('Plots/delta_T v Vdot.png')

fig4 = plt.figure()
plt.plot(flow_shaped[0,:], U_exh_shaped[0,:], '-x',
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(flow_shaped[1,:], U_exh_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(flow_shaped[2,:], U_exh_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Flow Rate (L/s)')
plt.ylabel(r'Overall Heat Transfer Coefficient ($kW/m^2K$)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/U v Vdot.pdf')
plt.savefig('Plots/U v Vdot.png')

### Plots of stuff v. inlet temperature

fig5 = plt.figure()
plt.plot(T1_shaped[0,:], heat_exh_shaped[0,:], '-x', 
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(T1_shaped[1,:], heat_exh_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(T1_shaped[2,:], heat_exh_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Exhaust Inlet Temperature (C)')
plt.ylabel('Heat Transfer (kW)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/heat v temp.pdf')
plt.savefig('Plots/heat v temp.png')

fig6 = plt.figure()
plt.plot(T1_shaped[0,:], delta_T_shaped[0,:], '-x',
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(T1_shaped[1,:], delta_T_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(T1_shaped[2,:], delta_T_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Exhaust Inlet Temperature (C)')
plt.ylabel(r'$\Delta T$ (K)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/delta_T v temp.pdf')
plt.savefig('Plots/delta_T v temp.png')

fig7 = plt.figure()
plt.plot(T1_shaped[0,:], U_exh_shaped[0,:], '-x',
            label=str(torque_shaped[0,0])+'ft-lbs') 
plt.plot(T1_shaped[1,:], U_exh_shaped[1,:], '-.s',
            label=str(torque_shaped[1,0])+'ft-lbs') 
plt.plot(T1_shaped[2,:], U_exh_shaped[2,:], '--d',
            label=str(torque_shaped[2,0])+'ft-lbs') 
plt.xlabel('Exhaust Inlet Temperature (C)')
plt.ylabel(r'Overall Heat Transfer Coefficient ($kW/m^2K$)')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/U v temp.pdf')
plt.savefig('Plots/U v temp.png')

plt.show()
