# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os


# User Defined Modules
# In this directory
import tem
reload(tem)

tem = tem.TEModule()
tem.I = 10.
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 650.
tem.T_c = 400.

segments = sp.arange(150, 200, 1)
q_h = sp.empty(sp.size(segments))

tem.set_constants()
tem.Ntype.set_prop_fit()
tem.Ptype.set_prop_fit()

for i in range(sp.size(segments)):
    tem.segments = segments[i]
    tem.solve_tem()
    q_h[i] = tem.q_h
    print q_h[i]

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.figure()
plt.plot(segments, q_h)
plt.xlabel('Number of Segments')
plt.ylabel('Hot Side Heat Flux')
plt.grid()

plt.show()
