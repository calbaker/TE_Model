"""This script replots a whole slew of the ICT paper plots."""

import matplotlib.pyplot as plt
import os

print "Running full_scale_instance.py"
execfile('full_scale_instance.py')
plt.close('all')

print "Running fin_inst.py"
execfile('fin_inst.py')
# execfile('varied_fins_inst.py')
plt.close('all')

print "Running parallel_duct_instance.py"
execfile('parallel_duct_inst.py')
# execfile('parallel_ducts_inst.py')
plt.close('all')

print "Preparing plots."
# Plot configuration

FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.figure()
plt.axes([0.15,0.15,0.8,0.8])
plt.plot(hx_inst.x_dim * 100., hx_inst.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.T_h_nodes, '-g', label='TEM Hot Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.T_c_nodes, '-k', label='TEM Cold Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.cool.T_nodes, '-b', label='Coolant')

plt.plot(hx_fins0.x_dim * 100., hx_fins0.exh.T_nodes, '--r')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.tem.T_h_nodes, '--g')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.tem.T_c_nodes, '--k')
plt.plot(hx_fins0.x_dim * 100., hx_fins0.cool.T_nodes, '--b')

plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.exh.T_nodes, ':r')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.tem.T_h_nodes, ':g')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.tem.T_c_nodes, ':k')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.cool.T_nodes, ':b')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
plt.grid()
plt.xlim(xmax = 100)
plt.legend(loc=(0.1,0.15))
# plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/temp.png')
plt.savefig('../Plots/temp.pdf')

plt.show()


