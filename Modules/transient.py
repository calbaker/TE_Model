# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules

# User Defined Modules
# In this directory
import hx
reload(hx)
import platewall
reload(platewall)


class Transient_HX(hx.HX):
    """Transient HX class.

    Special class for modeling waste heat recovery heat exchanger
    with transient inlet temperature and flow conditions."""

    def solve_transient(self):
        """Solves transient hx performance given varying inlet BCs

        """

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
