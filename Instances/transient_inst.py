# Chad Baker
# Created on 2011 Nov 14

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import transient
reload(transient)

area = (0.002)**2
length = 1.e-3
current = 4.
area_ratio = 0.69
fill_fraction = 1. / 40.

hx_trans = transient.Transient_HX()
hx_trans.tem.method = 'analytical'
hx_trans.width = 30.e-2
hx_trans.exh.bypass = 0.
hx_trans.exh.height = 3.5e-2
hx_trans.cool.mdot = 1.
hx_trans.length = 1.
hx_trans.tem.I = current
hx_trans.tem.length = length

hx_trans.t_max = .1

hx_trans.tem.Ptype.material = 'HMS'
hx_trans.tem.Ntype.material = 'MgSi'

hx_trans.tem.Ptype.area = area                           
hx_trans.tem.Ntype.area = hx_trans.tem.Ptype.area * area_ratio
hx_trans.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_trans.tem.Ptype.area +
                            hx_trans.tem.Ntype.area) )  

hx_trans.type = 'parallel'

hx_trans.exh.T_inlet = 700.
hx_trans.exh.P = 100.
hx_trans.cool.T_inlet = 300.

hx_trans.set_mdot_charge()
hx_trans.init_arrays()
hx_trans.solve_hx()
hx_trans.set_t_step()

hx_trans.init_trans_zeros()
hx_trans.exh.T_inlet_trans = np.zeros(hx_trans.power_net_trans.size)

hx_trans.exh.T_inlet_trans = np.linspace(500., 900., hx_trans.power_net_trans.size)

hx_trans.solve_hx_transient()

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

plt.close('all')

fig1 = plt.figure()
# plt.plot(np.arange(1,hx_trans.t_max,hx_trans.t_step),
# 	 hx_trans.exh.T_inlet_trans, label='Exhaust Temperature (K)')
plt.plot(np.linspace(0,hx_trans.t_max,hx_trans.power_net_trans.size),
	 hx_trans.Qdot_trans.sum(0))
plt.grid()
plt.xlabel('Time (s)')

fig2 = plt.figure()

for i in range(hx_trans.plate_hot.T_trans.shape[0]):
    plt.plot(hx_trans.plate_hot.T_trans[i,5,:])
plt.plot(hx_trans.exh.T_trans[5,:])
plt.plot(hx_trans.cool.T_trans[5,:])
plt.plot(hx_trans.tem.T_h_trans[5,:])
plt.plot(hx_trans.tem.T_c_trans[5,:])

plt.grid()
plt.legend()

plt.show()


