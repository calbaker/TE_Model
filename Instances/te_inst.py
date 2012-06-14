# distribution modules
import time
import os
import sys

# local user modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

t0 = time.clock()

leg_area = (0.002) ** 2
area_ratio = 0.849
fill_fraction = 3.85e-2
length = 4.00e-4
current = 13.2

te_pair = te_pair.TE_Pair()
# instantiate a te_pair object

te_pair.Ntype.material = 'MgSi'
te_pair.Ptype.material = 'HMS'
# declare materials to be used for property calculations

te_pair.I = current
# set current to be used in both legs

te_pair.length = length
te_pair.leg_area_ratio = area_ratio
te_pair.fill_fraction = fill_fraction
#set leg length and such
te_pair.set_leg_areas()

te_pair.T_c_conv = 300.  # cold side convection temperature (K)
te_pair.T_h_conv = 800.  # hot side convection temperature (K)

te_pair.U_cold = 2.
# cold side overall heat transfer coeffcient (kW / (m ** 2 * K))
te_pair.U_hot = 0.5
# hot side overall heat transfer coeffcient (kW / (m ** 2 * K))

te_pair.solve_te_pair()
# solves for temperature profile, hot side heat flux, cold side heat
# flux, power, and some other stuff.
