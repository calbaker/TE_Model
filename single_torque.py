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
hx.start_rowx = 5
hx.end_rowx = 8
hx.import_heat_data()
hx.poly_eval()
hx.set_U_exp()

area = (0.002)**2
length = 2.e-3
hx.Qdot1d = np.empty(np.size(hx.exh.flow_array))
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

plt.figure()
plt.plot(hx.x_dim * 100., hx.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/temp '+hx.type+'.png')
plt.savefig('Plots/temp '+hx.type+'.pdf')

plt.show()

