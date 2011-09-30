import matplotlib.pyplot as plt
import numpy as np

import exp_data
reload(exp_data)

hx = exp_data.HeatData()
hx.flow_data.import_flow_data()
hx.import_heat_data()
hx.manipulate_heat_data()
hx.set_flow_corrected()
hx.set_flow_exp()

pressure_drop = np.linspace(0, 14, 100)
flow = hx.exh.flow_coeff * pressure_drop**0.5

plt.plot(hx.flow_data.pressure_drop, hx.flow_data.flow * 1e3, 'sk',
         label="Flow Experiment")
plt.plot(hx.exh.pressure_drop, hx.exh.flow_exp * 1e3, 'xk', label="HX Experiment")
plt.plot(pressure_drop, flow * 1e3, '--k', label="Correlation")
plt.grid()
plt.xlim(xmin=0)
plt.xlabel("Pressure Drop (kPa)")
plt.ylabel("Flow Rate (L/s)")
plt.legend(loc='best')

plt.show()
