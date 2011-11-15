"""Module for definining PlateWall class methods and parameters."""

# Created on 7 Nov 2011 by Chad Baker

import scipy.optimize as spopt
import numpy as np

class PlateWall(object):
    """class for modeling metal walls of heat exchanger"""

    def __init__(self):
        """Initializes material properties and plate wall geometry defaults."""
        self.k = 200.e-3
        # thermal conductivity (kW/m-K) of Aluminum HX plate
        # (Incropera and DeWitt) 
        self.alpha = 73.0e-6 # thermal diffusivity (m^2/s) of Al HX
                             # plate  
        self.thickness = 0.00635 # thickness (m) of HX plate
        self.R_contact = 0.
        # thermal contact resistance (m^2*K/W) between plates
        self.nodes = 3. # default number of nodes in transient
                        # solution.  
        self.t_step = 0.005 # time step (s) in transient solution
        self.set_h()

    def set_h(self):
        """Sets the effective convection coefficient which is the
        inverse of thermal resistance."""
        self.h = self.k/self.thickness
        self.R_thermal = 1. / self.h

    def solve_ss(self):
        """sets up for solve_transient"""
        self.T_prev = np.linspace(self.T_c, self.T_h, self.nodes)

    def init_standalone(self):
        """initializes array for storying temperature"""
        self.T = np.zeros([self.nodes, np.size(self.time)])
        self.T[:,0] = np.array(np.linspace(self.T_h, self.T_c,
        self.nodes)) 

    def setup_transient(self, h_exh):
        """sets Fo and maybe other things.  See Mills Table 3.8""" 
        self.x_step = self.thickness / (self.nodes - 1.)
        self.x = np.linspace(0, 2. * self.x_step, self.nodes) 
        self.Fo = ( self.alpha * self.t_step / self.x_step**2) # Fourier number 
        self.Bi = ( h_exh * self.thickness / self.k ) # Biot number 
        self.Fo_crit = 1. / (2. * (1. + self.Bi))
        self.margin = (self.Fo_crit - self.Fo) / self.Fo_crit * 100. 
        if self.Fo > self.Fo_crit:
            print "time step is", self.margin, """percent lower than
        necessary."""

        # creating and populating the coefficient matrix
        self.coeff_mat = np.zeros([self.T_prev.shape[0], self.T_prev.shape[0]]) 
        self.coeff_mat[0,0] = 1. - 2. * self.Fo * (1. + self.Bi) 
        self.coeff_mat[0,1] = 2. * self.Fo
        self.coeff_mat[-1,-1] = 0
        for pop in range(self.coeff_mat.shape[0]-2):
            self.coeff_mat[pop+1, pop] = self.Fo
            self.coeff_mat[pop+1, pop+1] = 1. - 2. * self.Fo 
            self.coeff_mat[pop+1, pop+2] = self.Fo
        self.coeff_mat2 = np.zeros([self.T_prev.shape[0], self.T_prev.shape[0]])
        self.coeff_mat2[0,0] = 2. * self.Fo * self.Bi
        self.coeff_mat2[-1, -1] = 1.
            
    def solve_standalone(self, T_exh, T_te_hot):
        """Use this for standalone plate model."""
        self.T_bc = np.zeros(self.T.shape[0])
        self.T_bc[0] = T_exh
        self.T_bc[-1] = T_te_hot
        # forcing matrix

        for i in range(1, np.size(self.time)):
            self.T[:,i] = ( np.dot(self.coeff_mat, self.T[:,i-1]) +
        np.dot(self.coeff_mat2, self.T_bc) ) 

    def solve_transient(self, T_exh, T_te_hot):
        """Similar to tem.solve_leg but simpler and maybe not
        simpler. Time step should be the same as the residence time of
        exhaust gas in a particular node in the heat exchanger.""" 
        self.T_bc = np.zeros(self.T_prev.shape[0])
        self.T_bc[0] = T_exh
        self.T_bc[-1] = T_te_hot
        # forcing matrix

        self.T = ( np.dot(self.coeff_mat, self.T_prev) +
        np.dot(self.coeff_mat2, self.T_bc) )

        self.q_c = -self.k * (self.T[1] - self.T[2]) / self.x_step 
