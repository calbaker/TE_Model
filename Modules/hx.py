# coding=utf-8
"""
Script defining HX class.

Chad Baker
Created on 2011 Feb 10
"""

# Distribution Modules
import time
import numpy as np
import operator
from scipy.optimize import fmin  # _l_bfgs_b

# User Defined Modules
# In this directory
import engine
import te_pair
reload(te_pair)
import exhaust
reload(exhaust)
import coolant
reload(coolant)
import platewall
reload(platewall)


class Dimension(object):
    """Class for hx attribute containing physical dimensions.  This is
    used on an ad hoc basis."""
    pass


class HX(object):

    """Class definition for heat exchanger.

    Class instances:

    cool : coolant.Coolant instance
    cummins : engine.Engine instance
    exh : exhaust.Exhaust instance
    plate : platewall.PlateWall instance
    te_pair : te_pair.TE_pair instance

    Methods:

    fix_geometry
    get_T_inlet_error
    get_minpar
    init_arrays
    optimize
    set_availability
    set_constants
    set_convection
    set_mdot_charge
    setup
    solve_hx
    solve_node
    store_node_values
    """

    def __init__(self):

        """Sets several attributes, including instance attributes.

        Instance attributes

        self.cool = coolant.Coolant()
        self.exh = exhaust.Exhaust()
        self.te_pair = te_pair.TE_Pair()
        self.plate = platewall.PlateWall()
        self.cummins = engine.Engine()

        Methods:

        self.fix_geometry

        """

        self.R_extra = 0.
        # Dummy variable that can be used as a fit parameter or for
        # any other appropriate purpose to add thermal resistance to
        # the model

        self.R_interconnect = 0.00075  # (m^2*K/kW)
        # Resistance of copper interconnect assuming a thickness of
        # 0.3 mm (Ref: Hori, Y., D. Kusano, T. Ito, and
        # K. Izumi. “Analysis on Thermo-mechanical Stress of
        # Thermoelectric Module.” In Thermoelectrics 1999. Eighteenth
        # International Conference On, 328 –331, 1999), where
        # k_interconnect = 400 W/(m-K)

        self.R_substrate = 0.005  # (m^2*K/kW)
        # resistance of ceramic substrate(AlN) 1 mmm thick (Hori, Y.,
        # D. Kusano, T. Ito, and K. Izumi. “Analysis on
        # Thermo-mechanical Stress of Thermoelectric Module.” In
        # Thermoelectrics, 1999. Eighteenth International Conference
        # On, 328 –331, 1999.), based on k_ceramic = 200 W/(m-K)
        # obtained from Thermoelectrics Handbook.

        self.R_contact = 0.00003  # (m^2*K/kW)
        # Thermal contact resistance for all three contacts estimated
        # using alumina/copper contact resistance extracted from
        # Gundrum, Bryan C., David G. Cahill, and Robert
        # S. Averback. “Thermal Conductance of Metal-metal
        # Interfaces.” Physical Review B 72, no. 24 (December 30,
        # 2005): 245426.

        # self.R_contact = 0.8322 # (m^2*K/kW)
        # thermal contact resistance (m^2*K/kW) for plate/substrate,
        # substrate/interconnect, and interconnect/TE leg interfaces
        # all combined. All estimated (at 450 K) based on AlN/Cu
        # contact resistance extracted from Shi, Ling, Gang Wu,
        # Hui-ling Wang, and Xin-ming Yu. “Interfacial Thermal Contact
        # Resistance Between Aluminum Nitride and Copper at Cryogenic
        # Temperature.” Heat and Mass Transfer 48, no. 6 (2012):
        # 999–1004.

        self.dimension = Dimension()
        self.dimension.width = 0.55
        # width (cm*10**-2) of HX duct. This model treats duct as
        # parallel plates for simpler modeling.
        self.dimension.length = 0.55
        # length (m) of HX duct
        self.nodes = 25
        # number of nodes for numerical heat transfer model
        self.x0 = np.array([.7, 0.02, 0.001, 4.])
        self.xb = [(0.5, 2.), (0., 1.), (1.e-4, 20.e-3), (0.1, None)]
        # initial guess and bounds for x where entries are N/P area,
        # fill fraction, leg length (m), and current (A)
        self.xmin_file = 'xmin'
        self.T0 = 300.
        # temperature (K) at restricted dead state
        self.equal_width = True

        self.apar_list = [
            ['self', 'te_pair', 'leg_area_ratio'],
            ['self', 'te_pair', 'fill_fraction'],
            ['self', 'te_pair', 'length'],
            ['self', 'te_pair', 'I']
            ]
        # list of strings used to construct names of attributes to be
        # optimized

        # initialization of instance attributes
        self.cool = coolant.Coolant()
        self.exh = exhaust.Exhaust()
        self.te_pair = te_pair.TE_Pair()
        self.plate = platewall.PlateWall()
        self.cummins = engine.Engine()

        self.arrangement = 'single'
        self.fix_geometry()

    def init_arrays(self):

        """Initializes arrays for storing node values."""

        self.Qdot_nodes = np.zeros(self.nodes)

        self.exh.Vdot_nodes = np.zeros(self.nodes)

        self.exh.T_nodes = np.zeros(self.nodes)
        self.exh.h_nodes = np.zeros(self.nodes)
        self.exh.f_nodes = np.zeros(self.nodes)
        self.exh.deltaP_nodes = np.zeros(self.nodes)
        self.exh.Wdot_nodes = np.zeros(self.nodes)
        self.exh.Nu_nodes = np.zeros(self.nodes)
        self.exh.c_p_nodes = np.zeros(self.nodes)
        self.exh.entropy_nodes = np.zeros(self.nodes)
        self.exh.enthalpy_nodes = np.zeros(self.nodes)
        self.exh.velocity_nodes = np.zeros(self.nodes)
        self.exh.rho_nodes = np.zeros(self.nodes)
        self.exh.Re_nodes = np.zeros(self.nodes)

        self.cool.T_nodes = np.zeros(self.nodes)
        self.cool.entropy_nodes = np.zeros(self.nodes)
        self.cool.enthalpy_nodes = np.zeros(self.nodes)
        self.cool.deltaP_nodes = np.zeros(self.nodes)
        self.cool.Wdot_nodes = np.zeros(self.nodes)

        self.U_hot_nodes = np.zeros(self.nodes)
        self.U_cold_nodes = np.zeros(self.nodes)

        self.te_pair.q_h_conv_nodes = np.zeros(self.nodes)
        self.te_pair.q_c_conv_nodes = np.zeros(self.nodes)
        self.te_pair.q_h_nodes = np.zeros(self.nodes)
        self.te_pair.q_c_nodes = np.zeros(self.nodes)
        self.te_pair.error_nodes = np.zeros([3, self.nodes])
        self.te_pair.T_c_nodes = np.zeros(self.nodes)
        self.te_pair.T_h_nodes = np.zeros(self.nodes)
        self.te_pair.h_nodes = np.zeros(self.nodes)
        self.te_pair.power_nodes = np.zeros(self.nodes)
        self.te_pair.power_nodes_check = np.zeros(self.nodes)
        self.te_pair.eta_nodes = np.zeros(self.nodes)

    def setup(self):

        """Sets attributes that must be defined before running model.

        Methods:

        self.set_mdot_charge
        self.set_constants

        Useful for terminal.  Not necessary elsewhere.

        """

        self.exh.T = 800.
        self.cool.T = 300.
        self.set_mdot_charge()
        self.set_constants()

    def set_constants(self):

        """Sets constants used at the HX level.

        Methods:

        self.fix_geometry
        self.exh.set_flow_geometry
        self.cool.set_flow_geometry

        """

        self.x = np.linspace(0, self.dimension.length, self.nodes)
        self.node_length = self.dimension.length / self.nodes
        # length (m) of each node
        self.area = self.node_length * self.dimension.width * self.cool.ducts
        # area (m^2) through which heat flux occurs in each node
        self.te_pair.set_constants()
        self.leg_pairs = self.area / self.te_pair.area
        # Number of TEM leg pairs per node
        self.x_dim = np.arange(self.node_length / 2, self.dimension.length +
        self.node_length / 2, self.node_length)
        # x coordinate (m)
        self.fix_geometry()
        self.exh.set_flow_geometry(self.exh.width)
        self.cool.set_flow_geometry(self.cool.width)

    def fix_geometry(self):

        """Matches geometry of ducts.

        Makes sure that common geometry like width and length is the
        same between exh, cool, and the overal heat exchanger.

        """

        if self.equal_width == True:
            self.exh.width = self.dimension.width
            self.cool.width = self.dimension.width
        self.cool.length = self.dimension.length
        self.exh.length = self.dimension.length

    def set_mdot_charge(self):

        """Sets exhaust mass flow rate.

        Methods:

        self.cummins.set_mdot_charge

        Eventually, this should be a function of speed, load, and EGR
        fraction.  Also, it should come from experimental data.  Also,
        it should probably go within the exhaust module.

        """

        self.cummins.set_mdot_charge()
        # mass flow rate (kg/s) of exhaust
        self.exh.mdot = self.cummins.mdot_charge

    def set_convection(self):

        """Sets values for convection coefficients.

        Methods:

        self.exh.set_flow
        self.cool.set_flow

        """

        # Exhaust stuff
        self.exh.set_flow()
        # Coolant stuff
        self.cool.set_flow()
        # The previous three commands need only execute once per node.

        self.U_hot = ((self.exh.R_thermal + self.R_parasitic) ** -1)
        # heat transfer coefficient (kW/m^-K) between TE hot side and
        # exhaust
        self.U_cold = ((self.cool.R_thermal + self.R_parasitic) ** -1)
        # heat transfer coefficient (kW/m^-K) between TE cold side and
        # coolant

    def solve_node(self, i):

        """Solves for performance of streamwise slice of HX.

        Methods:

        self.set_convection
        self.te_pair.solve_te_pair

        """

        self.te_pair.T_h_conv = self.exh.T
        self.te_pair.T_c_conv = self.cool.T

        self.set_convection()

        if i == 0:
            self.te_pair.T_h = self.exh.T
            # guess at hot side TEM temperature (K)
            self.te_pair.T_c = self.cool.T
            # guess at cold side tem temperature (K)

        self.te_pair.U_hot = self.U_hot
        self.te_pair.U_cold = self.U_cold

        self.te_pair.solve_te_pair()
        self.q_h = self.te_pair.q_h
        self.q_c = self.te_pair.q_c

        self.Qdot_node = self.q_h * self.area
        # heat transfer on hot side of node, positive values indicates
        # heat transfer from hot to cold

    def solve_hx(self, ** kwargs):
        # solve parallel flow heat exchanger

        """Solves for performance of all stream-wise nodes.

        Methods:

        self.init_arrays
        self.set_constants
        self.solve_node
        self.store_node_values
        self.set_availability

        """

        self.init_arrays()
        self.set_constants()

        self.R_parasitic = (self.plate.R_thermal + self.R_interconnect +
        self.R_substrate + self.R_contact + self.R_extra)
        # R_parasitic (m^2-K/kW) includes plate resistance from module
        # platewall, resistance of interconnect and ceramic substrate
        # and all the contact resistances

        self.exh.node_length = self.node_length
        self.exh.T = self.exh.T_inlet
        # T_inlet and T_outlet correspond to the temperatures going
        # into and out of the heat exchanger.
        if self.type == 'parallel':
            self.cool.T = self.cool.T_inlet
        elif self.type == 'counter':
            self.cool.T = self.cool.T_outlet
        self.cool.node_length = self.node_length

        # for loop iterates of nodes of HX in streamwise direction
        for i in np.arange(self.nodes):
            self.solve_node(i)
            self.store_node_values(i)

            # redefining temperatures (K) for next node
            self.exh.T = (self.exh.T - self.te_pair.q_h * self.area /
                self.exh.C)
            if self.type == 'parallel':
                self.cool.T = (self.cool.T + self.te_pair.q_c * self.area
                    / self.cool.C)
            elif self.type == 'counter':
                self.cool.T = (self.cool.T - self.te_pair.q_c * self.area
                    / self.cool.C)

        # defining HX outlet/inlet temperatures (K)
        self.exh.T_outlet = self.exh.T
        if self.type == 'parallel':
            self.cool.T_outlet = self.cool.T
        elif self.type == 'counter':
            self.cool.T_inlet = self.cool.T

        self.Qdot_total = self.Qdot_nodes.sum()
        self.effectiveness = (self.Qdot_total / (self.exh.C *
        (self.exh.T_inlet - self.cool.T_inlet)))
        # heat exchanger effectiveness

        self.te_pair.power_total = self.te_pair.power_nodes.sum()
        # total TE power output (kW)

        self.exh.Wdot_total = self.exh.Wdot_nodes.sum()
        self.cool.Wdot_total = self.cool.Wdot_nodes.sum()
        self.Wdot_pumping = (self.exh.Wdot_total +
                              self.cool.Wdot_total)
        # total pumping power requirement (kW)

        self.exh.deltaP_total = self.exh.deltaP_nodes.sum()
        self.cool.deltaP_total = self.cool.deltaP_nodes.sum()

        try:
            self.exh.enh.type
        except AttributeError:
            pass
        else:
            if self.exh.enh.type == 'IdealFin':
                self.exh.G_minor = (
                    self.exh.rho_nodes[0] * self.exh.velocity_nodes[0]
                    )
                self.exh.K_c = 0.4
                self.exh.K_e = 0.2
                self.exh.deltaP_minor = (
                    self.exh.G_minor ** 2. *
            self.exh.velocity_nodes[0] / 2. * ((self.exh.K_c + 1. -
            self.exh.sigma ** 2.) - (1. - self.exh.sigma ** 2. -
            self.exh.K_e) * self.exh.velocity_nodes[-1] /
            self.exh.velocity_nodes[0])
                    )
                self.exh.deltaP_total += self.exh.deltaP_minor

        self.power_net = (
            self.te_pair.power_total - self.Wdot_pumping
            ) 

        self.set_availability()

    def set_availability(self):

        """Sets availability of exhaust and coolant along all nodes.
        """

        # Availability analysis
        self.exh.enthalpy0 = self.exh.get_enthalpy(self.T0)
        # enthalpy (kJ/kg) of exhaust at restricted dead state
        self.exh.entropy0 = self.exh.get_entropy(self.T0)
        # entropy (kJ/kg*K) of exhuast at restricted dead state

        self.exh.availability_flow_nodes = ((self.exh.enthalpy_nodes
        - self.exh.enthalpy0 - self.T0 * (self.exh.entropy_nodes -
        self.exh.entropy0)) * self.exh.mdot)
        # availability (kJ/kg) of exhaust

        self.cool.enthalpy_nodes = (self.cool.c_p *
        (self.cool.T_nodes - self.T0) + self.cool.enthalpy0)
        # enthalpy (kJ/kg*K) of coolant
        self.cool.entropy_nodes = (self.cool.c_p *
        np.log(self.cool.T_nodes / self.T0) + self.cool.entropy0)

        self.cool.availability_flow_nodes = (
        (self.cool.enthalpy_nodes - self.cool.enthalpy0 - self.T0 *
        (self.cool.entropy_nodes - self.cool.entropy0)) *
        self.cool.mdot)
        # availability (kJ/kg) of coolant

    def store_node_values(self, i):

        """Stores values of parameters of interest in node i.

        This should eventually also store the node valuves for T, q,
        and material properties in the te legs.
        """

        self.Qdot_nodes[i] = self.Qdot_node
        # storing node hot side heat transfer in array

        self.te_pair.q_h_conv_nodes[i] = self.q_h
        self.te_pair.q_c_conv_nodes[i] = self.q_c
        self.te_pair.q_h_nodes[i] = self.te_pair.q_h
        self.te_pair.q_c_nodes[i] = self.te_pair.q_c
        self.te_pair.error_nodes[:, i] = self.te_pair.error
        self.te_pair.T_h_nodes[i] = self.te_pair.T_h
        self.te_pair.T_c_nodes[i] = self.te_pair.T_c
        self.te_pair.power_nodes[i] = self.te_pair.P * self.leg_pairs
        self.te_pair.power_nodes_check[i] = (
            self.te_pair.P_flux * self.area
            )
        self.te_pair.eta_nodes[i] = self.te_pair.eta
        self.te_pair.h_nodes[i] = self.te_pair.h_eff

        self.exh.T_nodes[i] = self.exh.T
        self.exh.Vdot_nodes[i] = self.exh.Vdot
        self.exh.f_nodes[i] = self.exh.f
        self.exh.deltaP_nodes[i] = self.exh.deltaP
        self.exh.Wdot_nodes[i] = self.exh.Wdot_pumping
        self.exh.Nu_nodes[i] = self.exh.Nu_D
        self.exh.c_p_nodes[i] = self.exh.c_p
        self.exh.h_nodes[i] = self.exh.h_conv
        self.exh.velocity_nodes[i] = self.exh.velocity
        self.exh.entropy_nodes[i] = self.exh.entropy
        self.exh.enthalpy_nodes[i] = self.exh.enthalpy
        self.exh.rho_nodes[i] = self.exh.rho
        self.exh.Re_nodes[i] = self.exh.Re_D

        self.cool.T_nodes[i] = self.cool.T
        self.cool.deltaP_nodes[i] = self.cool.deltaP
        self.cool.Wdot_nodes[i] = self.cool.Wdot_pumping

        self.U_hot_nodes[i] = self.U_hot
        self.U_cold_nodes[i] = self.U_cold

    def get_minpar(self, apar):

        """Returns inverse of net power.

        Methods:

        self.solve_hx
        self.set_leg_areas

        Used by method self.optimize

        Uses self.apar_list to determine which paramters are to be
        varied in optimization.  Use with scipy.optimize.fmin to find
        optimal set of input parameters."""

        self.opt_iter = self.opt_iter + 1
        if self.opt_iter % 15 == 0:
            print "\n\noptimizaton iteration", self.opt_iter
            print "net power", self.power_net
            for i in range(self.x0.size):
                varname = '.'.join(self.apar_list[i][1:])
                varval = (
                    operator.attrgetter(varname)(self)
                    )
                print varname + ":", varval

            print "leg pairs =", self.leg_pairs

        apar = np.array(apar)

        # unpack guess vector
        for i in range(apar.size):
            setattr(operator.attrgetter(
                    '.'.join(self.apar_list[i][1:-1]))(self),
            self.apar_list[i][-1], apar[i])

        # reset surrogate variables
        self.te_pair.set_leg_areas()

        self.solve_hx()

        if (apar <= 0.).any():
            minpar = np.abs(self.power_net) ** 3 + 100.
            # penalizes negative parameters
            print "Encountered impossible value."

        else:
            minpar = - self.power_net

        return minpar

    def optimize(self):

        """Finds optimal set of paramters in self.apar_list

        Methods:

        self.get_minpar

        self.x0 and self.xb must be defined elsewhere."""

        time.clock()

        # dummy function that might be used with minimization
        def fprime():
            return 1

        self.opt_iter = 0

        self.x0 = np.zeros(len(self.apar_list))

        for i in range(self.x0.size):
            self.x0[i] = (
            operator.attrgetter('.'.join(self.apar_list[i][1:]))(self)
           )

        self.xmin = fmin(self.get_minpar, self.x0)

        t1 = time.clock()

        print '\n'
        for i in range(self.x0.size):
            varname = '.'.join(self.apar_list[i][1:])
            varval = (
                operator.attrgetter(varname)(self)
                )
            print varname + ":", varval

        print "\npower net:", self.power_net * 1000., 'W'
        print "power raw:", self.te_pair.power_total * 1000., 'W'
        print "pumping power:", self.Wdot_pumping * 1000., 'W'
        self.exh.volume = (
            self.exh.height * self.exh.width * self.dimension.length
            )
        print "exhaust volume:", self.exh.volume * 1000., 'L'
        VAR = self.power_net / self.exh.volume
        print "exhaust power density:", VAR, 'kW/m^3'

        print """Elapsed time solving xmin1 =""", t1

    def save_opt_par(self, opt_par_dir):
        """Saves parameters found by optimize."""

        if self.opt_iter == 0:
            print """\nError. Script must run the function optimize
            before running save_opt_par."""

        for i in range(self.x0.size):
            varname = '.'.join(self.apar_list[i][1:])
            varval = (
                operator.attrgetter(varname)(self)
                )
            np.save(opt_par_dir + varname, varval)

    def get_T_inlet_error(self, T_outlet):

        """Returns error for coolant inlet temperature.

        Error is determined relative to desired setpoint inlet
        temperature for the counter flow configuration in which the
        outlet coolant temperaure is specified.  Should be used with
        fsolve to determine the correct inlet temperature for the
        coolant.

        Inputs:

        self.cool.T_outlet

        Methods:

        self.solve_hx

        """

        self.cool.T_outlet = np.float(T_outlet)
        self.solve_hx()
        error = self.cool.T_inlet_set - self.cool.T_inlet
        return error
