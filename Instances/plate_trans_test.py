# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('../Modules/')

# User Defined Modules
# In this directory
import platewall 
reload(platewall)

os.chdir('..')

plate = platewall.PlateWall()

plate.T_h = 500.
plate.T_c = 300.

plate.set_h()
plate.solve_ss()
plate.time = np.arange(0, 30., plate.t_step) # total run time (s)

h_exh = 100.
plate.setup_transient(h_exh)

plate.solve_transient(900., 300.)

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

fig1 = plt.figure()
for i in range(plate.time.size):
    if i%250 == 0:
        plt.plot(plate.x*100., plate.T[:,i])

plt.xlabel('X coordinate (cm)')
plt.ylabel('Temperature (K)')
plt.grid()

plt.show()

os.chdir('Instances')
