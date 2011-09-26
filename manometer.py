import matplotlib.pyplot as plt
import numpy as np
import xlrd
import scipy.interpolate as interp
import scipy.optimize as spopt

FILENAME = 'manometer calibration2.xls'
worksheet = xlrd.open_workbook(filename=FILENAME).sheet_by_index(0)

H2O_kPa = 0.249 # 1 in H2O = 0.249 kPa
H2Oin = np.array(worksheet.col_values(0, start_rowx=2, end_rowx=16)) 
# manometer reading (inches of single column from datum)
datum = -10.1 # manometer datum (in)
pressure_drop = (H2Oin - datum) * 2. * H2O_kPa
# pressure drop across heat exchanger (kPa)

steel = np.array(worksheet.col_values(1, start_rowx=2, end_rowx=16))
# rotameter steel ball setting for propane flow rate

C3H8pressure = ( np.array(worksheet.col_values(2, start_rowx=2,
    end_rowx=16)) )
# pressure (kPa) measured by dial gauge in flow manifold

C3H8conc = np.array(worksheet.col_values(3, start_rowx=2,
    end_rowx=16)) 
# propane concentration (ppm) downstream of heat exchanger

T1 = np.array(worksheet.col_values(5, start_rowx=2, end_rowx=16))

# Section for doing stuff to the raw data
def get_flow(steel,C3H8_pressure,C3H8conc):
    """Function for determing flow rate through the heat exchanger.""" 
    C3H8flow0psi = 11.276 * steel + 62.102
    # propane flow (mL/min) with no back pressure
    C3H8flow2psi = 12.303 * steel + 46.823
    # propane flow (mL/min) with 2 psi back pressure
    C3H8flow = ( C3H8flow0psi - (C3H8flow0psi - C3H8flow2psi) / 2. *
    C3H8pressure )
    # propane flow (mL/min) based on linear interpolation for pressure
    flow = C3H8flow / (C3H8conc * 1.e-6) / 1000. / 60. 
    # exhaust flow (L/s)
    return flow, C3H8flow, C3H8flow0psi, C3H8flow2psi

flow, C3H8flow, C3H8flow0psi, C3H8flow2psi = (
get_flow(steel,C3H8pressure,C3H8conc) )

pressure_drop.sort()
flow.sort()

ORDER = 3

pressure_fit = np.linspace(0,14.,100)
flow_spline = interp.splrep(pressure_drop, flow)
flow_spline_fit = interp.splev(pressure_fit, flow_spline)

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
plt.plot(pressure_fit, flow_spline_fit, '-.r',label='spline fit')
plt.plot(pressure_fit, flow_poly_fit, '-k',
         label='order '+str(ORDER)+' polynomial')
plt.xlabel('Pressure Drop (kPa)')
plt.ylabel('Exhaust Flow Rate (L/s)')
plt.grid()
plt.legend(loc='upper left')
plt.savefig('Plots/flow_v_deltaP.pdf')
plt.savefig('Plots/flow_v_deltaP.png')

plt.show()
