# distribution modules
import scipy as sp
import matplotlib.pyplot as mpl
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import leg
reload(leg)

leg = leg.Leg()
leg.length = 3.56e-4
leg.I = 1.
leg.material = 'HMS'

leg.T_h_conv = 570.
leg.U_hot = 54e3
leg.T_c_conv = 300.
leg.U_cold = 253e3

leg.set_constants()

leg.solve_leg()

print "\n" * 3
print "T_nodes:\n", leg.T_nodes
print "q_nodes:\n", leg.q_nodes

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

