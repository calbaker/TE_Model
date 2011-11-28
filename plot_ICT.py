"""This script replots a whole slew of the ICT paper plots."""

import matplotlib.pyplot as plt
import os

os.chdir('Instances')

print "Running full_scale_instance.py"
execfile('full_scale_instance.py')
plt.close('all')

print "Running fin_inst.py"
execfile('fin_inst.py')
execfile('varied_fins_inst.py')
plt.close('all')

print "Running parallel_duct_instance.py"
execfile('parallel_duct_inst.py')
execfile('parallel_ducts_inst.py')
plt.close('all')

print "Preparing plots."

os.chdir('..')

plt.figure()
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
plt.xlim(xmax = 200)
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/temp.png')
plt.savefig('../Plots/temp.pdf')

plt.show()


