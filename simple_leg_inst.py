# Distribution modules

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl

T_c = 400.
T_h = 750.
length = 0.001
segments = 100.
currents = sp.arange(0., -2.5, -0.1) * 1e4
segment_length = length / segments
error = 1.

T = sp.zeros(segments)
q = sp.zeros(segments)
V_segment = sp.zeros(segments)

eta_currents = sp.zeros(sp.size(currents))

T[0] = T_c
k = 100. * 3.194 / T_c
q[0] = - k * (T_h - T_c) / segment_length

for i2 in sp.arange(sp.size(currents)):
    for i in sp.arange(1, segments, 1):
        alpha = (0.15 * T[i-1] + 211.) * 1e-6
        rho = 0.01 * 1. / 25.
        k = 100. * 3.194 / T[i-1]
        T[i] = T[i-1] + (segment_length / k) * (currents[i2] * T[i-1] * alpha - q[i-1])
        q[i] = ( q[i-1] + (rho * currents[i2]**2 * (1. + alpha**2 * T[i-1] / (rho
    * k)) - currents[i2] * alpha * q[i-1] / k) * segment_length ) 
        dT = T[i] - T[i-1]
        V_segment = alpha * dT
    V = sp.sum(V_segment)
    P = V * currents[i2]
    eta = -P / q[-1]
    eta_currents[i2] = eta

fig1 = mpl.figure()
mpl.plot(currents, eta_currents)
mpl.xlabel(r'Current Density (A/$m^2$)')
mpl.ylabel('Efficiency (%)')
mpl.title('Efficiency v. Current Density')
mpl.grid()

mpl.show()
