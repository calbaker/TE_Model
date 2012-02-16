# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fminbound, fmin

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.717
fill_fraction = 2.98e-2
leg_length = 3.50e-4
current = 13.6

hx1 = hx.HX()

length = 1.
width = 0.3

hx1.length = length
hx1.width = width
hx1.exh.height = 3.5e-2

hx1.footprint = hx1.length * hx1.width

hx1.te_pair.I = current
hx1.te_pair.length = leg_length

hx1.te_pair.Ntype.material = 'MgSi'
hx1.te_pair.Ptype.material = 'HMS'

hx1.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx1.te_pair.method = 'analytical'
hx1.type = 'counter'
hx1.exh.enh = hx1.exh.enh_lib.IdealFin()
hx1.exh.enh.thickness = 1.e-3

hx1.exh.T_inlet = 800.
hx1.cool.T_inlet_set = 300.
hx1.cool.T_outlet = 310.

hx1.set_mdot_charge()

def get_minpar(spacing):
    """Returns parameter to be minimized as a function of apar.
    apar[0] : number of fins"""
    hx1.exh.enh.spacing = spacing
    hx1.solve_hx()

    if hx1.power_net < 0:
        minpar = np.abs(hx1.power_net)
    else:
        minpar = 1. / hx1.power_net
    
    return minpar

# hx1.exh.enh.spacing = fminbound(get_minpar, 1.e-3, 10.e-3,
# xtol=0.01)
x0 = np.array([3.e-3])
hx1.exh.enh.spacing = fmin(get_minpar, x0)

N_fins = hx1.exh.enh.N
print "Default number of fins:", N_fins

length_array = np.linspace(0.2, 2, 10)
width_array = hx1.footprint / length_array 
aspect_array = length_array / width_array
P_net = np.zeros(aspect_array.size)
P_raw = np.zeros(aspect_array.size)
P_pumping = np.zeros(aspect_array.size)
Q_hot = np.zeros(aspect_array.size)
fin_array = np.zeros(aspect_array.size)
spacing_array = np.zeros(aspect_array.size)

for i in range(aspect_array.size):
    print "\niteration", i+1, "of", aspect_array.size
    hx1.width = width_array[i]
    hx1.length = length_array[i]

    if i > 0:
        x0 = np.abs(fin_array[i-1])
    else:
        x0 = N_fins

        # hx1.exh.enh.spacing = fminbound(get_minpar, 1.e-3, 15.e-3,
        # xtol=0.01)
        hx1.exh.enh.spacing = fmin(get_minpar, x0=3.e-3, xtol=0.01)

    fin_array[i] = hx1.exh.enh.N
    spacing_array[i] = hx1.exh.enh.spacing
    P_net[i] = hx1.power_net
    P_raw[i] = hx1.te_pair.power_total
    P_pumping[i] = hx1.Wdot_pumping
    Q_hot[i] = hx1.Qdot_total

    print "net power", P_net[i]
    print "raw power", P_raw[i]
    print "pumping power", P_pumping[i]
    print "Q_hot", Q_hot[i]
    print "flow:", hx1.exh.flow
    print "fin spacing:", spacing_array[i]
    print "number of fins:", fin_array[i]
    
# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 3.

plt.close('all')

plt.figure()
plt.plot(aspect_array, P_net * 1000., '-sg', label=r"P$_{net}$")
plt.plot(aspect_array, P_raw * 1000., '--xk', label=r"P$_{raw}$")
plt.plot(aspect_array, P_pumping * 1000., '-.ob', label=r"P$_{pump}$")
plt.plot(aspect_array, Q_hot * 100., ':or', label=r"$\dot{Q}_{hot}$/10")
plt.plot(np.ones(100) * 1. / 0.3, np.linspace(0,1800,100), '--k')
plt.xlabel("Aspect Ratio")
plt.ylabel("Net Power (W)")
plt.ylim(0,4000)
plt.grid()
plt.legend()
plt.subplots_adjust(bottom=0.12, left=0.15)

ax = plt.axes()
ax.annotate("default",
            xy=(3.33, 0), xycoords='data',
            xytext=(5, 750), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

plt.savefig("../Plots/power v. aspect ratio.pdf")
plt.savefig("../Plots/power v. aspect ratio.png")
