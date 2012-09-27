# Distribution modules

import types
import numpy as np
from scipy.integrate import odeint
from numpy.testing import assert_approx_equal
from scipy.optimize import fsolve

# User defined modules
import mat_prop
reload(mat_prop)


class Leg(object):

    """Class for individual TE leg.

    Methods:

    __init__
    get_dTq_dx
    set_ZT
    set_constants
    set_power_factor
    set_q_guess
    solve_leg_anal
    solve_leg_once
    solve_leg
    get_error

    """

    def __init__(self):

        """Sets constants and binds methods.

        Methods:

        self.set_constants

        Binds the following methods:

        mat_prop.import_raw_property_data
        mat_prop.set_properties_v_temp
        mat_prop.set_TEproperties"""

        self.I = 0.5  # current (A) in TE leg pair
        self.nodes = 10
        # number of nodes for which values are stored
        self.length = 1.e-3  # leg length (m)
        self.area = (3.e-3) ** 2.  # leg area (m^2)

        self.C = 1.e7
        # assumed value for heat capacity (kJ / K)
        self.t_array = np.linspace(0, 5, 10)
        # array of times for transient solution

        self.set_constants()

        self.import_raw_property_data = (
            types.MethodType(mat_prop.import_raw_property_data, self)
            )
        self.set_properties_v_temp = (
            types.MethodType(mat_prop.set_properties_v_temp, self)
            )
        self.set_TEproperties = (
            types.MethodType(mat_prop.set_TEproperties, self)
            )

    def set_constants(self):

        """Sets attributes that are typically held constant."""

        self.x = np.linspace(0., self.length, self.nodes)

        self.J = self.I / self.area  # (Amps/m^2)

    def get_dTq_dx(self, Tq, x):

        """Solves node. Returns array of derivatives.

        Function for evaluating the derivatives of temperature and
        heat flux w.r.t. x-dimension

        Inputs:

        Tq : initial conditions
        x : array of locations where results are desired

        Methods:

        self.set_TEproperties(T_props)

        If there were a function called solve_node, it would do the
        same thing as this.

        """

        T = Tq[0]
        q = Tq[1]

        self.set_TEproperties(T)

        dT_dx = (
            1. / self.k * (self.J * T * self.alpha - q)
            )

        self.set_ZT()

        dq_dx = (
            (self.rho * self.J ** 2. * (1. + self.ZT)) - self.J *
            self.alpha * q / self.k
            )

        dVs_dx = self.alpha * dT_dx
        # Seebeck voltage, aka open circuit voltage

        dV_dx = self.alpha * dT_dx + self.rho * self.J
        # Seebeck voltage minus resistance-dissipated voltage per unit
        # length

        dR_dx = self.rho / self.area
        # Internal resistance per unit length

        return dT_dx, dq_dx, dVs_dx, dV_dx, dR_dx

    def solve_leg(self):

        """Solves leg based on specified convection boundary
        conditions."""
        self.T_h = self.T_h_conv
        self.T_c = self.T_c_conv

        self.fsolve_output = fsolve(self.get_error, x0=self.T_h - 1.)

    def get_error(self, T_h):

        """Returns error in heat flux and temperature convection
        boundary conditions.

        Methods:
        self.solve_leg_once"""

        self.T_h = T_h[0]

        self.q_h_conv = self.U_hot * (self.T_h_conv - self.T_h)
        self.q_h = self.q_h_conv

        self.solve_leg_once(self.q_h)

        self.q_c_conv = self.U_cold * (self.T_c - self.T_c_conv)

        self.q_c_error = self.q_c - self.q_c_conv

        return self.q_c_error

    def solve_leg_once(self, q_h):

        """Solves leg once based on hot side heat flux.

        Solution procedure comes from Ch. 12 of Thermoelectrics
        Handbook, CRC/Taylor & Francis 2006. x-axis has been reversed
        relative to reference procedure.

        Inputs:
        q_h - hot side heat flux (W / m^2)

        """

        self.q_h = q_h
        self.y0 = np.array([self.T_h, self.q_h, 0, 0, 0])

        self.y = odeint(self.get_dTq_dx, y0=self.y0, t=self.x)

        self.T_x = self.y[:, 0]
        self.q_x = self.y[:, 1]
        self.Vs_x = self.y[:, 2]
        self.V_x = self.y[:, 3]
        self.R_int_x = self.y[:, 4]

        self.T_c = self.T_x[-1]
        self.q_c = self.q_x[-1]
        
        self.Vs = self.Vs_x[0] - self.Vs_x[-1]
        self.V = self.V_x[0] - self.V_x[-1]
        self.R_internal = self.R_int_x[-1]

        self.P_flux = self.J * self.V
        self.P = self.P_flux * self.area
        # Power for the entire leg (W)

        self.eta = self.P / (self.q_h * self.area)
        # Efficiency of leg
        self.R_load = self.V / self.I

        # Sanity check.  q_h - q_c should be nearly equal but not
        # exactly equal to P.  It is not exact because of spatial
        # asymmetry in electrical resistivity along the leg.  I
        # imported assert_approx_equal in the front matter to make
        # this print an error if there is too much disagreement.

        self.P_from_heat = (self.q_h - self.q_c) * self.area

        sig_figs = 3
        # tolerance in number of sig figs that agree.  Higher number
        # is stricter aka tighter tolerance.  This may need to be
        # reduced if you know the code is correct and it is still
        # printing the error statement.

        try:
            assert_approx_equal(self.P, self.P_from_heat, sig_figs)
        except AssertionError:
            print "\nPower from q_h - q_c and I  **  2 * R disagree."
            print "Consider reducing sig_figs under solve_leg_once"
            print "in leg.py if you think this is an error."

    def set_q_guess(self):

        """Sets guess for q_c to be used by iterative solutions.

        Methods:

        self.set_TEproperties(T_props)

        """

        self.T_props = 0.5 * (self.T_h + self.T_c)
        self.set_TEproperties(T_props=self.T_props)
        delta_T = self.T_h - self.T_c
        self.q_c = - (
            self.alpha * self.T_c * self.J - delta_T / self.length *
        self.k - self.J ** 2 * self.length * self.rho
            )
        # cold side heat flux (W / (m^2 * K))

        self.q_h = - (
            self.alpha * self.T_h * self.J - delta_T / self.length *
            self.k + self.J ** 2. * self.length * self.rho / 2.
            )

        self.q_c_guess = self.q_c
        # cold side heat flux (W / (m^2 * K))
        self.q_h_guess = self.q_h
        self.q_guess = self.q_h

    def solve_leg_anal(self):

        """Analytically solves the leg based on lumped properties.

        Methods:

        self.set_TEproperties

        No iteration is needed.

        """

        self.T_props = 0.5 * (self.T_h + self.T_c)

        self.set_TEproperties(T_props=self.T_props)

        delta_T = self.T_h - self.T_c
        self.q_h = (
            self.alpha * self.T_h * self.J - delta_T / self.length *
            self.k + self.J ** 2. * self.length * self.rho / 2.
            )
        self.q_c = (
            self.alpha * self.T_c * self.J - delta_T / self.length *
            self.k - self.J ** 2 * self.length * self.rho
            )

        self.P_flux = (
            (self.alpha * delta_T * self.J + self.rho * self.J ** 2 *
             self.length)
            )
        self.P = self.P_flux * self.area
        self.eta = self.P / (self.q_h * self.area)
        self.eta_check = (
            (self.J * self.alpha * delta_T + self.rho * self.J **
            2. * self.length) / (self.alpha * self.T_h * self.J -
            delta_T / self.length * self.k + self.J ** 2 * self.length
            * self.rho / 2.)
            )
        self.V = -self.P / np.abs(self.I)
        self.R_internal = self.rho * self.length / self.area
        self.R_load = - self.V / self.I

    def set_ZT(self):

        """Sets ZT based on formula.

        Formula:

        self.ZT = self.sigma * self.alpha ** 2. / self.k

        """

        self.ZT = self.alpha ** 2. * self.T_props / (self.k * self.rho)

    def set_power_factor(self):

        """Sets power factor and maximum theoretical power for leg."""

        self.power_factor = self.alpha ** 2 * self.sigma
        self.power_max = (
            self.power_factor * self.T_props ** 2 / self.length *
            self.area
            )

    def solve_leg_transient(self):

        """Solves leg based on array of transient BC's."""

        self.delta_x = self.x[1] - self.x[0]

        self.y0 = self.T_x

        try: 
            self.T_xt

        except AttributeError:
            self.odeint_output = odeint(
                self.get_dTx_dt, y0=self.y0, t=self.t_array,
                full_output=1 
                )
            self.T_xt = self.odeint_output[0]

        else:
            self.y0 = self.T_xt[-1,:]
            self.odeint_output = odeint(
                self.get_dTx_dt, y0=self.y0, t=self.t_array,
                full_output=1 
                )
            self.T_xt = np.concatenate((self.T_xt, self.odeint_output[0]))

    def get_dTx_dt(self, T, t):

        """Returns derivative of array of T wrt time.
        """

        self.dT_dt = np.zeros(T.size)
        self.q0 = np.zeros(T.size)
        self.dq_dx_ss = np.zeros(T.size)
        self.dq_dx = np.zeros(T.size)
        self.dT_dx = np.zeros(T.size)

        self.dT_dx[1:-1] = 0.5 * (T[2:] - T[:-2]) / self.delta_x  
        self.dT_dx[0] = (T[1] - T[0]) / self.delta_x
        self.dT_dx[-1] = (T[-1] - T[-2]) / self.delta_x

        for i in range(self.nodes):

            T_props = T[i]  # i for central differencing
            self.set_TEproperties(T_props)
            self.set_ZT()

            self.q0[i] = (
                self.J * T[i] * self.alpha - self.k * self.dT_dx[i]
                ) 

            self.dq_dx_ss[i] = (
                (self.rho * self.J ** 2. * (1. + self.ZT)) - self.J *
                self.alpha * self.q0[i] / self.k
                )

        # hot side BC, q_h
        self.q0[0] = self.U_hot * (self.T_h_conv - T[0]) 

        # cold side BC, q_c 
        self.q0[-1] = self.U_cold * (T[-1] - self.T_c_conv)

        self.dq_dx[1:-1] = (
            (self.q0[2:] - self.q0[:-2]) / (2. * self.delta_x)
            )
        self.dq_dx[0] = (
            (self.q0[1] - self.q0[0]) / self.delta_x
            )
        self.dq_dx[-1] = (
            (self.q0[-1] - self.q0[-2]) / self.delta_x
            )

        for i in range(self.nodes):

            T_props = T[i]  # i for central differencing
            self.set_TEproperties(T_props)
            self.set_ZT()

            self.dT_dt[i] = (
                1. / self.C * (-self.dq_dx[i] + self.dq_dx_ss[i])
                )

        return self.dT_dt
