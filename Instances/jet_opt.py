# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fsolve
import numpy as np

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
hx_jet_opt = hx.HX()
hx_jet_opt.exh.enh = hx_jet_opt.exh.set_enhancement('JetArray')

hx_jet_opt.width = 30.e-2
hx_jet_opt.exh.height = 3.5e-2
hx_jet_opt.cool.mdot = 1.
hx_jet_opt.length = 1.

hx_jet_opt.te_pair.Ptype.material = 'HMS'
hx_jet_opt.te_pair.Ntype.material = 'MgSi'

hx_jet_opt.type = 'counter'

hx_jet_opt.exh.T_inlet = 800.
hx_jet_opt.cool.T_inlet_set = 300.
hx_jet_opt.cool.T_outlet = 310.

hx_jet_opt.set_mdot_charge()

hx_jet_opt.apar_list.append(['hx_fins_opt', 'exh', 'enh', 'spacing'])
hx_jet_opt.apar_list.append(['hx_fins_opt', 'exh', 'enh', 'D'])
# hx_jet_opt.apar_list.append(['hx_fins_opt', 'exh', 'enh', 'H'])
hx_jet_opt.exh.enh.H = 0.01

hx_jet_opt.optimize()

spacing = hx_jet_opt.exh.enh.spacing
D = hx_jet_opt.exh.enh.D
H = hx_jet_opt.exh.enh.H

np.save('../output/jet_opt/spacing', spacing)
np.save('../output/jet_opt/D', D)
np.save('../output/jet_opt/H', H)

execfile('jet_instances.py')
