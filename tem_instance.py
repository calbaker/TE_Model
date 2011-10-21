# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time

# local user modules
import tem
reload(tem)

t0 = time.clock()

length = 1. / 1000.
current = 5.
area = (0.002)**2
area_ratio = 1.25 # p-type area per n-type area

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


