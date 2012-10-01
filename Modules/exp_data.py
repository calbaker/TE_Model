"""This script imports experimental data and does other stuff with
it."""

import numpy as np
from scipy.optimize import leastsq

import properties as prop


class DataPoint(object):
    pass


class ExpData(object):
    """Class for containing the experimental results."""

    def __init__(self):
        """nothing to do here yet"""

        self.folder = '../../../Heat Exchanger Experiments/gen2/'
        self.file = '2012-09-04'
        self.exh = prop.ideal_gas()
        self.exh.P = 101.325
        self.cool = DataPoint()
        self.fit_order = 1
        self.fit_params = np.ones(3. * self.fit_order + 1)

    def import_data(self):
        """Imports data from csv file as a numpy record array (aka
        structured array)"""

        self.data = np.recfromcsv(self.folder + self.file + '.csv')

        self.exh.T_in = self.data['hx_exh_in_t'] + 273.15  # K
        self.exh.T_out = self.data['hx_exh_out_t'] + 273.15  # K
        self.exh.mdot = self.data['exh_mdot_kgmin'] / 60.  # kg/s
        self.exh.deltaP = (
            self.data['hx_exh_delta_p_2_in_wc'] * 0.249 * 2.  # kPa
            )

        self.cool.T_in = (
            0.5 * (self.data['hx_cool_1_in_t'] +
            self.data['hx_cool_2_in_t']) + 273.15  # K
            )
        self.cool.T_out = (
            0.5 * (self.data['hx_cool_1_out_t'] +
            self.data['hx_cool_2_out_t']) + 273.15  # K
            )
        self.cool.Vdot = self.data['cool_vdot_gpm']

        self.exh.T_mean = 0.5 * (self.exh.T_in + self.exh.T_out)
        self.exh.deltaT = self.exh.T_in - self.exh.T_out
        self.exh.eta = self.exh.deltaT / (self.exh.T_in - self.cool.T_in)

        self.exh.c_p = np.zeros(self.exh.T_in.size)

        for i in range(self.exh.T_in.size):
            self.exh.T = self.exh.T_mean[i]
            self.exh.set_TempPres_dependents()
            self.exh.c_p[i] = self.exh.c_p_air

        self.exh.Qdot = self.exh.mdot * self.exh.c_p * self.exh.deltaT

    def get_Qdot_fit(self):
        """Uses scipy.optimize leastsq to minimize the error of a
        polynomial in fitting the experimental Qdot data.
        """
        self.leastsq_out = leastsq(
            self.get_Qdot_fit_error, x0=self.fit_params
            )
        self.fit_params = self.leastsq_out[0]

    def eval_Qdot_fit(self, fit_params, mdot, T_in):
        """Evaluates qdot at specific mdot and T_in."""

        ORDER = self.fit_order

        A = fit_params[0:ORDER]
        A = np.append(A, 0)
        self.A_coeff = A

        B = fit_params[ORDER:ORDER * 2]
        B = np.append(B, 0)
        self.B_coeff = B

        C = fit_params[ORDER * 2:ORDER * 3]
        C = np.append(C, 0)
        self.C_coeff = C

        self.offset = fit_params[-1]

        self.exh.Qdot_fit = (
            np.polyval(A, mdot) + np.polyval(B, T_in) + 
            np.polyval(C, mdot * T_in) + self.offset
            )

        return self.exh.Qdot_fit
        
    def rep_Qdot_surf(self, mdot, T_in):
        """Creates 2d surface of Qdot as function of mdot and T_in."""
 
        self.exh.Qdot_surf = np.zeros([mdot.size, T_in.size])

        for index in np.ndindex(mdot.size, T_in.size):
            i = index[0]
            j = index[1]
            self.exh.Qdot_surf[i, j] = (
                self.eval_Qdot_fit(self.fit_params, mdot[i], T_in[j])
                )

    def get_Qdot_fit_error(self, fit_params):
        """Returns error between statistical fit and experimental Qdot
        data."""

        self.eval_Qdot_fit(fit_params, self.exh.mdot, self.exh.T_in)
        self.exh.Qdot_fit_err = self.exh.Qdot - self.exh.Qdot_fit

        return self.exh.Qdot_fit_err
