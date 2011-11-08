# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os

#
# User Defined Modules
# In this directory
import hx
reload(hx)

area = (0.002)**2
length = 1.e-3
current = 4.
area_ratio = 0.69
fill_fraction = 1. / 40.

hx1 = hx.HX()
hx1.tem.method = 'analytical'
hx1.width = 30.e-2
hx1.exh.bypass = 0.
hx1.exh.height = 3.5e-2
hx1.cool.mdot = 1.
hx1.length = 1.
hx1.tem.I = current
hx1.tem.length = length

hx1.tem.Ptype.material = 'HMS'
hx1.tem.Ntype.material = 'MgSi'

hx1.tem.Ptype.area = area                           
hx1.tem.Ntype.area = hx1.tem.Ptype.area * area_ratio
hx1.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx1.tem.Ptype.area +
                            hx1.tem.Ntype.area) )  

hx1.type = 'parallel'

hx1.exh.T_inlet = 800.
hx1.exh.P = 100.
hx1.cool.T_inlet = 300.

hx1.set_mdot_charge()

offset = 700.
amplitude = 100.

hx1.exh.T_inlet_array = ( offset + amplitude *
                          np.linspace(0, 2.*np.pi, 25) )

for i in range(np.size(hx1.exh.T_inlet_array)):
    hx1.exh.T_inlet = hx1.exh.T_inlet_array[i]
    hx1.solve_hx()

