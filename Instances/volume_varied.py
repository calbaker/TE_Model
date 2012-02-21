# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve, fmin

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.721
fill_fraction = 3.13e-2
leg_length = 3.45e-4
current = 13.5

hx2 = hx.HX()
hx2.width = 0.3
hx2.exh.height = 3.5e-2
hx2.length = 1.
hx2.te_pair.I = current
hx2.te_pair.length = leg_length

hx2.te_pair.Ntype.material = 'MgSi'
hx2.te_pair.Ptype.material = 'HMS'

hx2.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx2.te_pair.method = 'analytical'
hx2.type = 'counter'

hx2.exh.enh = hx2.exh.enh_lib.OffsetStripFin()
hx2.exh.enh.thickness = 2.e-3
hx2.exh.enh.spacing = 3.19e-3
hx2.exh.enh.k = 0.02

hx2.plate.k = 0.02 # for Ti
hx2.plate.thickness = .125 * 2.54e-2

hx2.exh.T_inlet = 800.
hx2.cool.T_inlet_set = 300.
hx2.cool.T_outlet = 310.

hx2.set_mdot_charge()
hx2.cool.T_outlet = fsolve(hx2.get_T_inlet_error,
                                x0=hx2.cool.T_outlet)

hx2.footprint = hx2.width * hx2.length
hx2.exh.volume_spec = 10.e-3

def get_minpar(spacing):
    """Returns parameter to be minimized as a function of apar.
    apar : fin spacing"""
    
    hx2.exh.enh.spacing = spacing
    hx2.solve_hx()

    if hx2.power_net < 0:
        minpar = np.abs(hx2.power_net)
    else:
        minpar = 1. / hx2.power_net
    
    return minpar

length_array = np.linspace(0.2, 0.9, 26)
width_array = np.linspace(0.3, 0.9, 25)

power_net_array = np.zeros([length_array.size, width_array.size])
spacing_array = np.zeros([length_array.size, width_array.size])
x0 = 3.e-3

for i in range(length_array.size):
    for j in range(width_array.size):
        iter = i * width_array.size + j
        itermax = length_array.size * width_array.size
        print "iteration", iter, "of", itermax

        hx2.length = length_array[i]
        hx2.width = width_array[j]

        hx2.exh.height = hx2.exh.volume_spec / (hx2.width * hx2.length)  
    
        hx2.exh.enh.spacing = fmin(get_minpar, x0)
        
        power_net_array[i,j] = hx2.power_net
        spacing_array[i,j] = hx2.exh.enh.spacing

dirpath = '../data/volume_varied/'
np.save(dirpath + 'length_array', length_array)
np.save(dirpath + 'width_array', width_array)
np.save(dirpath + 'spacing_array', spacing_array)
np.save(dirpath + 'power_net_array', power_net_array)

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

plt.figure()
x_2d, y_2d = np.meshgrid(length_array * 100., width_array * 100.)
TICKS = np.linspace(800, power_net_array.max() * 1.e3, 12)
LEVELS = np.linspace(800, power_net_array.max() * 1.e3, 12)
FCS = plt.contourf(x_2d, y_2d, power_net_array.T * 1.e3, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.0f', ticks=TICKS)
CB.set_label(r'Power')
plt.grid()
plt.xlabel('Length (cm)')
plt.ylabel('Width (cm)')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/volume_varied/power_net.pdf')

plt.figure()
# TICKS = np.linspace(800, power_net_array.max() * 1.e3, 12)
# LEVELS = np.linspace(800, power_net_array.max() * 1.e3, 12)
FCS = plt.contourf(x_2d, y_2d, spacing_array.T * 1.e3)#, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.0f', ticks=TICKS)
CB.set_label(r'Fin Spacing (mm)')
plt.grid()
plt.xlabel('Length (cm)')
plt.ylabel('Width (cm)')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/volume_varied/fin spacing.pdf')

# plt.show()
