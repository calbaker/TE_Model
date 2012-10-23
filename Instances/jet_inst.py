# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import os, sys
import numpy as np

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
hx_jets = hx.HX()
hx_jets.exh.enh = hx_jets.exh.set_enhancement('JetArray')

hx_jets.width = 30.e-2
hx_jets.exh.height = 3.5e-2
hx_jets.cool.mdot = 1.
hx_jets.length = 1.

hx_jets.te_pair.Ptype.material = 'HMS'
hx_jets.te_pair.Ntype.material = 'MgSi'

hx_jets.type = 'counter'

hx_jets.exh.T_inlet = 800.
hx_jets.cool.T_inlet_set = 300.
hx_jets.cool.T_outlet = 310.

hx_jets.set_mdot_charge()

hx_jets.exh.enh.H = 0.01
hx_jets.exh.enh.D = 0.005
hx_jets.exh.enh.spacing = 0.01

hx_jets.solve_hx()

