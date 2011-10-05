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
flow_sim = exp_data.HeatData()
flow_sim.flow_data.import_flow_data()
flow_sim.flow_data.flow = flow_sim.flow_data.flow_trash
flow_sim.exh.pressure_drop = np.linspace(0.,14,100)
flow_sim.set_flow_array()

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

pressure_drop = flow_sim.exh.pressure_drop.copy()
flow = flow_sim.exh.flow_array.copy()
pressure_drop.sort()
flow.sort()
fig06 = plt.figure()
fig06.canvas.set_window_title('Flow v Pressure')
plt.plot(flow_sim.flow_data.pressure_drop, flow_sim.flow_data.flow *1e3, 'or',
         label='experiment')
plt.plot(pressure_drop, flow * 1e3, '-k', 
         label='model')
plt.ylabel('Flow Rate (L/s)')
plt.xlabel('Pressure Drop (kPa)')
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.legend(loc='lower right')
plt.savefig('Plots/SAE Paper/Flow v Pressure.pdf')
plt.savefig('Plots/SAE Paper/Flow v Pressure.png')

plt.show()
