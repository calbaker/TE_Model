"""
Script defining transient HX class.

Chad Baker
Created on 2011 Feb 10
"""

# Distribution Modules
import numpy as np
import scipy.optimize as spopt

# User Defined Modules
# In this directory
import hx
reload(hx)
import platewall
reload(platewall)


class Transient_HX(hx.HX):
    """Special class for modeling waste heat recovery heat exchanger
    with transient inlet temperature and flow conditions."""

    def __init__(self):
        """initializes variables."""
        self.t_max = 5.  # total elapsed time (s)
        self.plate_hot = platewall.PlateWall()
        self.t_step = 0.001  # time step (s)
        super(Transient_HX, self).__init__()

    # def get_error_hot_trans(self, T_h):
    #     """Needs better doc string."""
    #     self.plate_hot.solve_transient(self.exh.T, T_h)
    #     # hot side heat flux coming from plate into TE devices
    #     self.tem.T_h_goal = T_h
    #     self.tem.solve_te_pair()
    #     self.error_hot = (self.plate_hot.q_c - self.tem.q_h) / self.tem.q_h
    #     return self.error_hot

    def solve_hx_transient(self):
        """This doc string explains what this method should do.  The
        method should specify an inlet boundary condition after having
        initially run the steady state solution.  With the inlet
        boundary condition establish and temperature profiles in all
        of the nodes known (must store temp data in 2d for tem's), the
        inlet boundary condition can then be changed.  For the first
        streamwise hx node, the plate model and te model can be
        iterated until their boundary conditions match up.  When this
        happens the temperature values and performance parameters of
        interest must be stored.  Then the next node is iterated and
        so forth.

        After all the nodes have been iterated in this fashion, the
        time is incremented by the residence time of the exhaust in a
        single node (or perhaps less???)."""

        self.init_arrays()
        self.solve_hx()
        self.init_trans_zeros()
        self.init_trans_values()

        for t in range(1, int(self.t_max / self.t_step)):
                # initiate temperatures here

            for i in range(self.nodes):
                self.solve_node_transient(i, t)
                self.Qdot_node = -self.tem.q_h * self.area
                self.store_trans_values(i, t)

                # redefining temperatures (K) for next node
                self.exh.T = (self.exh.T_trans[i - 1, t - 1]
                               + self.plate_hot.q_h_trans[i - 1, t - 1]
                               * self.area / self.exh.C)

                if self.type == 'parallel':
                    self.cool.T = (self.cool.T_trans[i - 1, t - 1]
                                    - self.tem.q_c_trans[i - 1, t - 1]
                                    * self.area / self.cool.C)

                elif self.type == 'counter':
                    self.cool.T = (self.cool.T_trans[i - 1, t - 1]
                                    + self.tem.q_c_trans[i - 1, t - 1]
                                    * self.area / self.cool.C)

    def solve_node_transient(self, i, t):
        """needs a better doc string"""

        # Determines current temperature in node i at time t based on
        # previous temperature in node i at time t-1, previous
        # temperature in node i-1 at time t-1, and what amount of
        # exchange has happened between node i-1 and node i during the
        # previous time step.

        self.exh.exchange = (self.t_step / (self.exh.velocity_nodes[i,
        t - 1] / self.node_length))
        # percent of exhaust that is purged from node i during one
        # time step, must be less than one for model to work properly
        self.exh.T_node[i, t] = ((1. - self.exchange) * self.exh.T_node[i, t
        - 1] + self.exchange * self.exh.T_node[i - 1, t - 1])

        self.cool.exchange = (self.t_step / (self.cool.velocity_nodes[i,
        t - 1] / self.node_length))
        # percent of exhaust that is purged from node i during one
        # time step, must be less than one for model to work properly
        self.cool.T_node[i, t] = ((1. - self.exchange) * self.cool.T_node[i, t
        - 1] + self.exchange * self.cool.T_node[i - 1, t - 1])

        self.tem.T_c = self.cool.T
        # guess at cold side tem temperature (K)
        self.tem.T_h_goal = self.exh.T
        # guess at hot side TEM temperature (K)
        self.tem.solve_te_pair()
        self.set_convection()
        self.q = self.U * (self.cool.T - self.exh.T)
        self.tem.T_h_goal = self.q / self.U_hot + self.exh.T
        self.tem.T_c = -self.q / self.U_cold + self.cool.T

        self.plate_hot.T_prev = self.plate_hot.T_trans[:, i, t - 1]
        self.plate_hot.setup_transient(self.exh.h_trans[i, t - 1])

        # needs to have something that solves the plate transient
        # model 
        

        # This next block needs to be replaced with something that
        # does not suck, but what???

    #     self.error_hot = 100.  # really big number to start while loop
    #     self.loop_count = 0

    #     while (np.absolute(self.error_hot) > self.xtol or
    # np.absolute(self.error_cold) > self.xtol):

    #         self.tem.T_h_goal = spopt.fsolve(self.get_error_hot_trans,
    # x0=self.tem.T_h_goal)
    #         # self.tem.solve_te_pair()

    #         self.tem.T_c = spopt.fsolve(self.get_error_cold,
    # x0=self.tem.T_c)

    #         self.tem.T_h_goal = spopt.fsolve(self.get_error_hot_trans,
    # x0=self.tem.T_h_goal)
    #         self.loop_count = self.loop_count + 1
    #         self.threshold = 10.

    #         if self.loop_count > self.threshold:
    #             print ("loop count is", self.loop_count,
    #                     " which exceeds threshold of", self.threshold)

    def store_trans_values(self, i, t):
        """Storing solved values in array to keep track of what
        happens in every node."""
        self.Qdot_trans[i, t] = self.Qdot_node
        # storing node heat transfer in array

        self.plate_hot.q_h_trans[i, t] = self.plate_hot.q_h
        self.plate_hot.q_c_trans[i, t] = self.plate_hot.q_c
        self.q_c_trans[i, t] = self.q_c
        self.tem.q_h_trans[i, t] = self.tem.q_h
        self.tem.q_c_trans[i, t] = self.tem.q_c
        self.error_hot_trans[i, t] = self.error_hot
        self.error_cold_trans[i, t] = self.error_cold

        self.exh.T_trans[i, t] = self.exh.T
        self.exh.h_trans[i, t] = self.exh.h
        self.exh.f_trans[i, t] = self.exh.f
        self.exh.Nu_trans[i, t] = self.exh.Nu_D

        self.cool.h_trans[i, t] = self.cool.h
        self.cool.T_trans[i, t] = self.cool.T
        self.cool.f_trans[i, t] = self.cool.f
        self.cool.Nu_trans[i, t] = self.cool.Nu_D

        self.tem.T_h_trans[i, t] = self.tem.T_h_goal
        # hot side temperature (K) of TEM at each node
        self.tem.T_c_trans[i, t] = self.tem.T_c
        # cold side temperature (K) of TEM at each node.
