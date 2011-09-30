import matplotlib.pyplot as plt
import numpy as np
import xlrd
import scipy.interpolate as interp
import scipy.optimize as spopt

import exp_data
import properties as prop

FILENAME = 'trash can flow meter.xls'
worksheet = xlrd.open_workbook(filename=FILENAME).sheet_by_index(0)

START_ROW = 2
END_ROW = 17
H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
H2Oin = np.array(worksheet.col_values(1, start_rowx=START_ROW, end_rowx=END_ROW)) 
# manometer reading (inches of single column from datum)
pressure_drop = H2Oin * 2. * H2O_kPa
# pressure drop across heat exchanger (kPa)

trash_volume = 77.6
# volume (L) of trash can

time = np.array(worksheet.col_values(3, start_rowx=START_ROW,
                                     end_rowx=END_ROW)) 

T = np.array(worksheet.col_values(5, start_rowx=START_ROW,
                                  end_rowx=END_ROW))

flow = trash_volume / time 

pressure_drop.sort()
flow.sort()
f = pressure_drop / flow**2

ORDER = 2

pressure_fit = np.linspace(0,14.,100)

flow_poly = np.poly1d(np.polyfit(pressure_drop, flow, ORDER))
flow_poly_fit = flow_poly(pressure_fit)

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure()
plt.plot(pressure_drop, flow, 'sk',label='experimental')
plt.plot(pressure_fit, flow_poly_fit, '-r',
         label='order '+str(ORDER)+' polynomial')
plt.xlabel('Pressure Drop (kPa)')
plt.ylabel('Exhaust Flow Rate (L/s)')
plt.ylim(ymin=0)
plt.grid()
plt.legend(loc='upper left')
plt.savefig('Plots/flow_v_deltaP.pdf')
plt.savefig('Plots/flow_v_deltaP.png')

plt.figure()
plt.plot(pressure_drop, f, 'sk')
plt.grid()
plt.xlabel('Pressure Drop (kPa)')
plt.ylabel('Friction Factor Estimate')
plt.savefig('Plots/friction estimate.pdf')
plt.savefig('Plots/friction estimate.png')

plt.show()
