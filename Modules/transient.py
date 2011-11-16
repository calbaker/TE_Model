# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os
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
        self.t_max = 5. # total elapsed time (s)
        self.plate_hot = platewall.PlateWall()
        super(Transient_HX, self).__init__()

    def set_t_step(self):
        """Sets appropriate time step based on average residence time
        of flow in each node."""
        self.t_step = (self.node_length / self.exh.velocity_nodes).mean()

    def get_error_hot_trans(self,T_h):
        """Needs better doc string."""
        self.plate_hot.solve_transient(self.exh.T, T_h)
        # hot side heat flux coming from plate into TE devices
        self.tem.T_h_goal = T_h
        self.tem.solve_tem()
        self.error_hot = (self.plate_hot.q_c - self.tem.q_h) / self.tem.q_h
        return self.error_hot

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
        self.set_t_step()
        self.init_trans_zeros()
        self.init_trans_values()

        for t in range(1,int(self.t_max / self.t_step)):
	    if t%10==0:
		print "t_index =", t, "of", int(self.t_max / self.t_step)
	    self.exh.T = self.exh.T_inlet_trans[t]		
            for i in range(self.nodes):
                self.solve_node_transient(i,t)
                self.store_trans_values(i,t)

		# redefining temperatures (K) for next node
		self.exh.T = ( self.exh.T + self.tem.q_h * self.area /
			       self.exh.C )
		if self.type == 'parallel':
		    self.cool.T = ( self.cool.T - self.tem.q_c * self.area
				    / self.cool.C )  
		elif self.type == 'counter':
		    self.cool.T = ( self.cool.T + self.tem.q_c * self.area
				    / self.cool.C )

    def solve_node_transient(self,i,t):
        """needs a better doc string"""
        self.tem.Ntype.node = i # used within tem.py
        self.tem.Ptype.node = i
        self.node = i
        self.time = t
        
	self.tem.T_c = self.cool.T
	# guess at cold side tem temperature (K)
	self.tem.T_h_goal = self.exh.T
	# guess at hot side TEM temperature (K)
	self.tem.solve_tem()
	self.set_convection()
	self.q = self.U * (self.cool.T - self.exh.T)
	self.tem.T_h_goal = self.q / self.U_hot + self.exh.T
	self.tem.T_c = -self.q / self.U_cold + self.cool.T

	self.plate_hot.T_prev = self.plate_hot.T_trans[:,i,t-1]
        self.plate_hot.setup_transient(self.exh.h_trans[i,t-1])
        self.error_hot = 100. # really big number to start while loop

        self.loop_count = 0
        while ( np.absolute(self.error_hot) > self.xtol or
    np.absolute(self.error_cold) > self.xtol ): 

            self.tem.T_h_goal = spopt.fsolve(self.get_error_hot_trans,
    x0=self.tem.T_h_goal)
            # self.tem.solve_tem()

            self.tem.T_c = spopt.fsolve(self.get_error_cold,
    x0=self.tem.T_c)
	    self.loop_count = self.loop_count + 1
	    self.threshold = 10.
	    if self.loop_count > self.threshold:
		print ( "loop count is", self.loop_count,
			" which exceeds threshold of", self.threshold )

        self.Qdot_node = -self.tem.q_h * self.area

    def store_trans_values(self,i,t):
        """Storing solved values in array to keep track of what
        happens in every node."""
        self.Qdot_trans[i,t] = self.Qdot_node
        # storing node heat transfer in array

        self.plate_hot.q_c_trans[i,t] = self.plate_hot.q_c
        self.q_c_trans[i,t] = self.q_c
        self.tem.q_h_trans[i,t] = self.tem.q_h
        self.tem.q_c_trans[i,t] = self.tem.q_c
        self.error_hot_trans[i,t] = self.error_hot
        self.error_cold_trans[i,t] = self.error_cold

        self.exh.T_trans[i,t] = self.exh.T
        self.exh.h_trans[i,t] = self.exh.h
        self.exh.f_trans[i,t] = self.exh.f
        self.exh.Nu_trans[i,t] = self.exh.Nu_D

        self.cool.h_trans[i,t] = self.cool.h
        self.cool.T_trans[i,t] = self.cool.T
        self.cool.f_trans[i,t] = self.cool.f
        self.cool.Nu_trans[i,t] = self.cool.Nu_D

        self.tem.T_h_trans[i,t] = self.tem.T_h
        # hot side temperature (K) of TEM at each node 
        self.tem.T_c_trans[i,t] = self.tem.T_c
        # cold side temperature (K) of TEM at each node.  

        self.U_trans[i,t] = self.U
        self.U_hot_trans[i,t] = self.U_hot
        self.U_cold_trans[i,t] = self.U_cold

        self.tem.power_trans[i,t] = self.tem.P * self.leg_pairs
        self.tem.eta_trans[i,t] = self.tem.eta
        self.tem.h_trans[i,t] = self.tem.h

        self.plate_hot.T_trans[:,i,t] = self.plate_hot.T

	self.cool.Wdot_pump_trans[t] = self.cool.Wdot_pumping
	self.exh.Wdot_pump_trans[t] = self.exh.Wdot_pumping
	self.Wdot_pump_trans[t] = self.cool.Wdot_pumping + self.exh.Wdot_pumping

	self.power_net_trans[t] = self.tem.power_trans.sum(0)[t] - self.Wdot_pump_trans[t]
	
    def init_trans_zeros(self):
        """Initiating important values in arrays to keep track of what
        happens in every node.""" 
        self.Qdot_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        # storing node heat transfer in array

        self.plate_hot.q_c_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.q_c_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.tem.q_h_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.tem.q_c_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.error_hot_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.error_cold_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 

        self.exh.T_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.exh.h_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.exh.f_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.exh.Nu_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 

        self.cool.h_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.cool.T_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.cool.f_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.cool.Nu_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        
        self.tem.T_h_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        # hot side temperature (K) of TEM at each node 
        self.tem.T_c_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        # cold side temperature (K) of TEM at each node.  

        self.U_trans = np.zeros([self.nodes, self.t_max / self.t_step]) 
        self.U_hot_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.U_cold_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 

        self.tem.power_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.tem.eta_trans = np.zeros([self.nodes, self.t_max /
        self.t_step]) 
        self.tem.h_trans = np.zeros([self.nodes, self.t_max /
        self.t_step])

        self.plate_hot.T_trans = np.zeros([self.plate_hot.nodes,
        self.nodes, self.t_max / self.t_step]) 
        self.plate_hot.T_nodes = np.zeros([self.plate_hot.nodes,
        self.nodes])

	self.power_net_trans = np.zeros(self.t_max / self.t_step)
	self.Wdot_pump_trans = np.zeros(self.t_max / self.t_step)
	self.cool.Wdot_pump_trans = np.zeros(self.t_max / self.t_step)   
	self.exh.Wdot_pump_trans = np.zeros(self.t_max / self.t_step) 

    def init_trans_values(self):
        """Initiating t=0 values.""" 
        self.Qdot_trans[:,0] = self.Qdot_nodes
        # storing node heat transfer in array

        self.plate_hot.q_c_trans[:,0] = self.q_h_nodes
        self.q_c_trans[:,0] = self.q_c_nodes
        self.tem.q_h_trans[:,0] = self.tem.q_h_nodes
        self.tem.q_c_trans[:,0] = self.tem.q_c_nodes
        self.error_hot_trans[:,0] = self.error_hot_nodes
        self.error_cold_trans[:,0] = self.error_cold_nodes

        self.exh.T_trans[:,0] = self.exh.T_nodes
        self.exh.h_trans[:,0] = self.exh.h_nodes
        self.exh.f_trans[:,0] = self.exh.f_nodes
        self.exh.Nu_trans[:,0] = self.exh.Nu_nodes

        self.cool.h_trans[:,0] = self.cool.h_nodes
        self.cool.T_trans[:,0] = self.cool.T_nodes
        self.cool.f_trans[:,0] = self.cool.f_nodes
        self.cool.Nu_trans[:,0] = self.cool.Nu_nodes
        
        self.tem.T_h_trans[:,0] = self.tem.T_h_nodes
        # hot side temperature (K) of TEM at each node 
        self.tem.T_c_trans[:,0] = self.tem.T_c_nodes
        # cold side temperature (K) of TEM at each node.  

        self.U_trans[:,0] = self.U_nodes
        self.U_cold_trans[:,0] = self.U_cold_nodes

        self.tem.power_trans[:,0] = self.tem.power_nodes
        self.tem.eta_trans[:,0] = self.tem.eta_nodes
        self.tem.h_trans[:,0] = self.tem.h_nodes

        self.Qdot_trans[:,0] = self.Qdot_nodes
        # storing node heat transfer in array

	self.plate_hot.T_h_nodes = ( self.exh.T_nodes +
				     self.q_h_nodes / self.exh.h_nodes )
	self.plate_hot.T_c_nodes = self.tem.T_h_nodes

	for i in range(self.plate_hot.T_h_nodes.size):
	    self.plate_hot.T_nodes[:,i] = np.linspace(
		self.plate_hot.T_h_nodes[i], self.plate_hot.T_c_nodes[i],
		self.plate_hot.nodes) 
	    
        self.plate_hot.T_trans[:,:,0] = self.plate_hot.T_nodes

	self.cool.Wdot_pump_trans[0] = self.cool.Wdot_pumping
	self.exh.Wdot_pump_trans[0] = self.exh.Wdot_pumping
	self.Wdot_pump_trans[0] = self.cool.Wdot_pumping + self.exh.Wdot_pumping

	self.power_net_trans[0] = self.tem.power_trans.sum(0)[0] - self.Wdot_pump_trans[0]
