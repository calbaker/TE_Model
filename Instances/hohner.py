# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import harmonica
reload(harmonica)

hohner = harmonica.Harmonica()
hohner.hx1.te_pair.method = 'analytical'
hohner.hx2.te_pair.method = 'analytical'

hohner.length = 0.5

hohner.hx1.length = hohner.length

hohner.hx1.exh.height = 4.e-2
hohner.hx1.width = 10.e-2

hohner.hx2.width = hohner.hx1.length

hohner.hx2.cool.width = hohner.hx1.cool.width
hohner.hx2.cool.length = hohner.hx1.cool.length

hohner.hx2.length = 35.e-2
hohner.hx2.exh.height = 4.e-2

hohner.hx2.exh.enhancement = 'straight fins'
hohner.hx2.exh.fin.thickness = 0.001
hohner.hx2.exh.fins = 200.

hohner.solve_harmonica()

print "\n"
print "harmonica net power:", hohner.power_net * 1.e3
print "hx1 net power:", hohner.hx1.power_net * 1.e3
print "hx2 net power:", hohner.hx2.power_net * 1.e3
print "------"
print "harmonica Wdot:", hohner.Wdot_pumping * 1.e3
print "hx1 Wdot:", hohner.hx1.Wdot_pumping * 1.e3
print "hx2 Wdot:", hohner.hx2.Wdot_pumping * 1.e3
print "------"
print "harmonica power:", hohner.power_total * 1.e3 
print "hx1 power:", hohner.hx1.te_pair.power_total * 1.e3
print "hx2 power:", hohner.hx2.te_pair.power_total * 1.e3

print "outlet temperature:", hohner.hx2.exh.T_outlet

