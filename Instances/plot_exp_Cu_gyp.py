"""Plots results from heat exchanger experiments."""

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
# pychecker will flag this statement, but it is necessary
import numpy as np
import matplotlib.pyplot as plt

f = open('../output/model_validation/file',"r")
FILE = f.read()
f.close()

FILE = 'copper'

npzfile = np.load(
    '../output/model_validation/' + FILE + '.npz'
    ) 
Cu_deltaP = npzfile['deltaP']
Cu_mdot = npzfile['mdot']
Cu_T_in = npzfile['T_in']
Cu_Qdot = npzfile['Qdot']
Cu_Re_D = npzfile['Re_D']

FILE = 'gypsum'

npzfile = np.load(
    '../output/model_validation/' + FILE + '.npz'
    ) 
gyp_deltaP = npzfile['deltaP']
gyp_mdot = npzfile['mdot']
gyp_T_in = npzfile['T_in']
gyp_Qdot = npzfile['Qdot']
gyp_Re_D = npzfile['Re_D']

# Plot configuration
FONTSIZE = 24
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.show()
plt.close()
    
plt.figure('Qdot v mdot')
plt.plot(gyp_mdot, gyp_Qdot, 'md', label='gypsum')
plt.plot(Cu_mdot, Cu_Qdot, 'c>', label='Cu mesh')
plt.xticks(rotation=45)
plt.xlabel('Exhaust Mass Flow Rate (kg/s)')
plt.ylabel('Heat Transfer Rate (kW)')
plt.legend(loc="lower right")
plt.grid()
plt.subplots_adjust(bottom=0.21)
plt.savefig('../Plots/plot_exp/exp_Qdot_v_mdot.pdf')

plt.figure('Qdot v T_in')
plt.plot(gyp_T_in, gyp_Qdot, 'md', label='gypsum')
plt.plot(Cu_T_in, Cu_Qdot, 'c>', label='Cu mesh')
plt.xticks(rotation=45)
plt.xlabel("HX Inlet Temperature (K)")
plt.ylabel('Heat Transfer Rate (kW)')
plt.grid()
plt.legend(loc="upper left")
plt.subplots_adjust(bottom=0.21)
plt.savefig('../Plots/plot_exp/exp_Qdot_v_T_in.pdf')

plt.show()
