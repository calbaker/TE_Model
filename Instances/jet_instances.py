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

spacing = np.load("../output/jet_opt/spacing")
D = np.load("../output/jet_opt/D")
H = np.load("../output/jet_opt/H") 

def set_values():
    hx_jets.exh.enh.spacing = spacing 
    hx_jets.exh.enh.D = D 
    hx_jets.exh.enh.H = H

set_values()

SIZE = 10

H_array = np.linspace(0.5, 2., SIZE) * H
# range of annular height to be used for getting results
D_array = np.linspace(0.5, 2., SIZE + 1) * D
# range of jet diameter
X_array = np.linspace(0.5, 2., SIZE + 1) * spacing
# range of jet spacing

power_net_H = np.zeros(H_array.size)
power_net_D = np.zeros(D_array.size)
power_net_X = np.zeros(X_array.size)

for i in range(H_array.size):
    hx_jets.exh.enh.H = H_array[i]
    # hx_jets.cool.T_outlet = fsolve(hx_jets.get_T_inlet_error, x0=hx_jets.cool.T_outlet)
    hx_jets.solve_hx()
    power_net_H[i] = hx_jets.power_net
    if i%5 == 0:
        print "loop 1 of 3, iteration", i, "of", H_array.size

set_values()
    
for i in range(D_array.size):
    hx_jets.exh.enh.D = D_array[i]
    # hx_jets.cool.T_outlet = fsolve(hx_jets.get_T_inlet_error, x0=hx_jets.cool.T_outlet)
    hx_jets.solve_hx()
    power_net_D[i] = hx_jets.power_net
    if i%5 == 0:
        print "loop 2 of 3, iteration", i, "of", D_array.size

set_values()
    
for i in range(X_array.size):
    hx_jets.exh.enh.spacing = X_array[i]
    # hx_jets.cool.T_outlet = fsolve(hx_jets.get_T_inlet_error, x0=hx_jets.cool.T_outlet)
    hx_jets.solve_hx()
    power_net_X[i] = hx_jets.power_net
    if i%5 == 0:
        print "loop 3 of 3, iteration", i, "of", X_array.size

print "\nSaving."

np.save("../output/jet_instances/power_net_H", power_net_H)
np.save("../output/jet_instances/power_net_D", power_net_D)
np.save("../output/jet_instances/power_net_X", power_net_X)

np.save("../output/jet_instances/H_array", H_array)
np.save("../output/jet_instances/D_array", D_array)
np.save("../output/jet_instances/X_array", X_array)

execfile('plot_jet_instances.py')
