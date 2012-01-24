# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

# parameters for TE legs
area_ratio =    6.414362693368951263e-01
fill_fraction = 2.571583488993029604e-02
length =        9.635165319449931357e-04
current =       4.773474042990549115e+00

hx_ducts0 = hx.HX()
hx_ducts0.width = 30.e-2
# hx_ducts0.exh.bypass = 0.
hx_ducts0.exh.height = 3.5e-2
hx_ducts0.length = 1.
hx_ducts0.te_pair.I = current
hx_ducts0.te_pair.length = length

hx_ducts0.te_pair.Ntype.material = 'MgSi'
hx_ducts0.te_pair.Ptype.material = 'HMS'

hx_ducts0.te_pair.Ptype.area = area                           
hx_ducts0.te_pair.Ntype.area = hx_ducts0.te_pair.Ptype.area * area_ratio
hx_ducts0.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_ducts0.te_pair.Ptype.area +
                            hx_ducts0.te_pair.Ntype.area) )  

# hx_ducts0.te_pair.method = 'analytical'
hx_ducts0.type = 'counter'

hx_ducts0.exh.T_inlet = 800.
hx_ducts0.exh.P = 100.
hx_ducts0.cool.T_inlet_set = 300.
hx_ducts0.cool.T_outlet = 310.

ducts = 3

hx_ducts0.exh.height = 7.24e-3 # from *const.py
hx_ducts0.cool.height = 4.14e-3

hx_ducts0.set_mdot_charge()
hx_ducts0.exh.mdot0 = hx_ducts0.exh.mdot 

hx_ducts0.exh.mdot = hx_ducts0.exh.mdot0 / ducts
hx_ducts0.cool.mdot = hx_ducts0.cool.mdot * 2. / (ducts + 1.) 

hx_ducts0.height = ( ducts * hx_ducts0.exh.height + (ducts + 1) *
                     hx_ducts0.cool.height )  

hx_ducts0.cool.T_outlet = fsolve(hx_ducts0.get_T_inlet_error, x0=hx_ducts0.cool.T_outlet) 
    
hx_ducts0.Qdot = hx_ducts0.Qdot * ducts
hx_ducts0.te_pair.power = hx_ducts0.te_pair.power_total * ducts
hx_ducts0.power_net = hx_ducts0.power_net * ducts
hx_ducts0.Wdot_pumping = hx_ducts0.Wdot_pumping * ducts

print "\nProgram finished."
print "Plotting..."

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

plt.figure()
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.te_pair.T_h_nodes, '-g', label='TE_PAIR Hot Side')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.te_pair.T_c_nodes, '-k', label='TE_PAIR Cold Side')
plt.plot(hx_ducts0.x_dim * 100., hx_ducts0.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_ducts0.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/temp '+hx_ducts0.type+str(ducts)+'.png')
plt.savefig('../Plots/temp '+hx_ducts0.type+str(ducts)+'.pdf')

# plt.show()

print hx_ducts0.power_net

# hx_ducts0.optimize()
