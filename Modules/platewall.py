"""Module for definining PlateWall class methods and parameters."""

# Created on 7 Nov 2011 by Chad Baker

import scipy.optimize as spopt

class PlateWall(object):
    """class for modeling metal walls of heat exchanger"""

    def __init__(self):
        """Initializes material properties and plate wall geometry defaults."""
        self.k = 0.2 # thermal conductivity (kW/m-K) of Aluminum HX plate
        self.thickness = 0.00635 # thickness (m) of HX plate
        self.R_contact = 0.
        # thermal contact resistance (m^2*K/kW) between plates
        self.nodes = 3.
        self.time = 1. # time (s) of something that I don't understand
                       # yet.  
        self.t_step = 0.01 # time step (s) in transient solution

    def set_h(self):
        """Sets the effective convection coefficient which is the
        inverse of thermal resistance."""
        self.h = self.k/self.thickness
        self.R_thermal = 1. / self.h

    def solve_ss(self):
        """sets up for solve_transient"""
        self.T0 = np.linspace(self.T_c, self.T_h, self.nodes)

    def setup_transient(self):
        """sets Fo and maybe other things."""
        self.x_step = self.thickness / (self.nodes - 1.)
        self.Fo = ( self.alpha * self.t_step / self.x_step**2)         
        self.t_crit = self.x_step**2 / (2. * self.alpha)
        self.margin = (t_crit - t_step) / t_crit * 100.
        if self.t_step > self.t_crit:
            print "time step is", margin, """percent lower than
        necessary."""
        self.T = np.zeros([self.x.size, self.t.size])

    def solve_transient(self):
        """Similar to tem.solve_leg but simpler."""
        self.T_old = self.T

        T[:,0] = np.array(np.linspace(T_hot[0], T_cold, x.size))
        T[-1,:] = T_cold

        # creating and populating the coefficient matrix
        coeff_mat = np.zeros([T.shape[0], T.shape[0]])
        coeff_mat[0,0] = 1.
        coeff_mat[-1,-1] = 1.
        for pop in range(coeff_mat.shape[0]-2):
            coeff_mat[pop+1, pop] = Fo
            coeff_mat[pop+1, pop+1] = 1. - 2. * Fo
            coeff_mat[pop+1, pop+2] = Fo

            # solving
        for i in range(1,t.size):
            T[:,i] = np.dot(coeff_mat, T[:,i-1])

