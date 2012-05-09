# Chad Baker

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

leg_area = (0.002)**2

area_ratio = 0.745
fill_fraction = 3.10e-2
leg_length = 3.56e-4
current = 13.0

te1 = te_pair.TE_Pair()

te1.I = current
te1.length = leg_length

te1.Ntype.material = 'MgSi'
te1.Ptype.material = 'HMS'

te1.set_all_areas(leg_area, area_ratio, fill_fraction) 
te1.set_constants()

te1.T_h_conv = 800.
te1.T_c_conv = 300.
te1.U_hot = 0.5
te1.U_cold = 2.
te1.T_h_goal = 615.
te1.T_c = 315.

te1.set_q_c_guess()
