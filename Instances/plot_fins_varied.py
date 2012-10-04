# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt

output_dir = "../output/fins_varied/"

power_net = np.load(output_dir + "power_net.npy")[1:]
Wdot_pumping = np.load(output_dir + "Wdot_pumping.npy")[1:]
Qdot = np.load(output_dir + "Qdot.npy")[1:]
power_total = np.load(output_dir + "power_total.npy")[1:]
spacing = np.load(output_dir + "spacing.npy")[1:]

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 3.

plt.close('all')

PLOT_DIR = "../Plots/fins_varied/"

plt.figure()
plt.plot(
    spacing * 100., Qdot / 10., '-.b',
    label=r'$\dot{Q}_{h}$ / 10'
    ) 
plt.plot(
    spacing * 100., power_total,':g',
    label=r'$P_{raw}$'
    )
plt.plot(
    spacing * 100., power_net, '-r',
    label='$P_{net}$'
    )  
plt.plot(
    spacing * 100., Wdot_pumping, '--k',
    label='Pumping'
    )

plt.grid()
plt.xticks(rotation=40)
plt.xlabel('Fin Spacing (cm)')
plt.ylabel('Power (kW)')
# plt.ylim(0,3)
plt.ylim(ymin=0)
plt.subplots_adjust(bottom=0.15)
plt.legend(loc='best')
plt.savefig(PLOT_DIR + 'p_v_fin_spacing.pdf')

plt.show()
