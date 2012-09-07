# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import real_hx
reload(real_hx)

hx_val = real_hx.get_hx()

hx_val.exh.T_inlet = 700.
hx_val.cool.T_outlet = 300.

hx_val.exh.mdot = 0.0833

# hx_val.cool.T_outlet = fsolve(hx_val.get_T_inlet_error,
#                                 x0=hx_val.cool.T_outlet, xtol=0.01)
hx_val.solve_hx()

print "\nPlotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()

plt.figure()
plt.plot(hx_val.x * 100., hx_val.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_val.x * 100., hx_val.te_pair.T_h_nodes, '-g', label='TE Hot Side')
plt.plot(hx_val.x * 100., hx_val.te_pair.T_c_nodes, '-k', label='TE Cold Side')
plt.plot(hx_val.x * 100., hx_val.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_val.type)
plt.grid()
# plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
plt.ylim(ymax=950)
plt.legend(loc="upper right")
plt.savefig('../Plots/fin_inst/temp.png')
plt.savefig('../Plots/fin_inst/temp.pdf')

print "\ndeltaP:", hx_val.exh.deltaP_total

print "\nhot side heat transfer:", hx_val.Qdot_total, 'W'
print "power net:", hx_val.power_net * 1000., 'W'
print "power raw:", hx_val.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_val.Wdot_pumping * 1000., 'W'
hx_val.exh.volume = hx_val.exh.height * hx_val.exh.width * hx_val.length
print "exhaust volume:", hx_val.exh.volume * 1000., 'L'
print "exhaust power density:", hx_val.power_net / hx_val.exh.volume, 'kW/m^3'

plt.show()
