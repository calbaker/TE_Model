# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

hx_exp = hx.HX()

# These values must be checked
hx_exp.width = 20. * 2.54e-2
hx_exp.exh.height = 2.5 * 2.54e-2
hx_exp.cool.height = 1. * 2.54e-2
hx_exp.length = 20. * 2.54e-2

hx_exp.te_pair.Ptype.area = (2.e-3) ** 2

hx_exp.te_pair.leg_area_ratio = 0.662
hx_exp.te_pair.I = 0.001  # turns off TE effect
hx_exp.te_pair.length = 1.e-5
hx_exp.te_pair.fill_fraction = 1.

hx_exp.te_pair.set_leg_areas()

hx_exp.te_pair.Ntype.material = 'MgSi'
hx_exp.te_pair.Ptype.material = 'HMS'

hx_exp.type = 'counter'

hx_exp.exh.enh = hx_exp.exh.enh_lib.OffsetStripFin()
hx_exp.exh.enh.thickness = 0.1 * 2.54e-2
hx_exp.exh.enh.spacing = 0.298 * 2.54e-2
# spacing = 0.400 - 0.124 / 2. - 0.040 = 0.298
hx_exp.exh.enh.l = hx_exp.length

hx_exp.cool.enh = hx_exp.cool.enh_lib.IdealFin()
hx_exp.cool.enh.thickness = 0.08 * 2.54e-2
hx_exp.cool.enh.spacing = 0.320 * 2.54e-2
# spacing = 0.400 - 0.100 / 2. - 0.030 = 0.320

hx_exp.exh.T_inlet = 406.1 + 273.15
hx_exp.cool.T_inlet_set = 300.
hx_exp.cool.T_outlet = 310.

hx_exp.cummins.RPM = 1940.
hx_exp.set_mdot_charge()
hx_exp.exh.mdot = hx_exp.exh.mdot * 10.

# hx_exp.cool.T_outlet = fsolve(hx_exp.get_T_inlet_error,
#                                 x0=hx_exp.cool.T_outlet, xtol=0.01)
hx_exp.solve_hx()

print "\nProgram finished."
print "\nPlotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.figure()
plt.plot(hx_exp.x * 100., hx_exp.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_exp.x * 100., hx_exp.te_pair.T_h_nodes, '-g', label='TE Hot Side')
plt.plot(hx_exp.x * 100., hx_exp.te_pair.T_c_nodes, '-k', label='TE Cold Side')
plt.plot(hx_exp.x * 100., hx_exp.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_exp.type)
plt.grid()
# plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
plt.ylim(ymax=950)
plt.legend(loc="upper right")
plt.savefig('../Plots/fin_inst/temp.png')
plt.savefig('../Plots/fin_inst/temp.pdf')

# plt.show()

print "hot side heat transfer:", hx_exp.Qdot_total, 'W'
print "power net:", hx_exp.power_net * 1000., 'W'
print "power raw:", hx_exp.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_exp.Wdot_pumping * 1000., 'W'
hx_exp.exh.volume = hx_exp.exh.height * hx_exp.exh.width * hx_exp.length
print "exhaust volume:", hx_exp.exh.volume * 1000., 'L'
print "exhaust power density:", hx_exp.power_net / hx_exp.exh.volume, 'kW/m^3'


