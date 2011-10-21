# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import tem
reload(tem)

t0 = time.clock()

length = 1. * 0.001
current = 3.
area = (0.002)**2
area_ratio = 0.69 # n-type area per p-type area, consistent with
                  # Sherman.  

tem = tem.TEModule()
tem.I = current
tem.Ntype.material = 'MgSi'
tem.Ptype.material = 'HMS'
tem.T_h_goal = 500.
tem.T_c = 300.
tem.Ptype.node = 0
tem.Ntype.node = 0
tem.Ntype.area = area
tem.Ptype.area = tem.Ntype.area * area_ratio
tem.length = length
tem.area_void = 0.
tem.method = 'analytical'
tem.set_constants()
tem.Ptype.set_prop_fit()
tem.Ntype.set_prop_fit()
tem.solve_tem()
tem.set_eta_max()
tem.set_A_opt()

