# Chad Baker
# Created on 2011 Feb 10
1
# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
import te_pair

area = (0.002)**2
length = 5.e-3

hx_pores = hx.HX()
hx_pores.width = 30.e-2
hx_pores.exh.bypass = 0.
hx_pores.exh.height = 3.5e-2
hx_pores.length = 1.
hx_pores.te_pair.I = 2.
hx_pores.te_pair.length = length
hx_pores.te_pair.Ntype.material = 'MgSi'
hx_pores.te_pair.Ntype.area = area
hx_pores.te_pair.Ptype.material = 'HMS'
hx_pores.te_pair.Ptype.area = area * 2. 
hx_pores.te_pair.area_void = 25. * area
hx_pores.te_pair.method = 'analytical'
hx_pores.type = 'parallel'
hx_pores.exh.enhancement = "Mancin porous"

hx_pores.exh.T_inlet = 800.
hx_pores.exh.P = 100.
hx_pores.cool.T_inlet = 300.

hx_pores.set_mdot_charge()
hx_pores.solve_hx()

hx_pores.exh.porosity = .99
hx_pores.exh.PPI = 10.
hx_pores.solve_hx()
    
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

