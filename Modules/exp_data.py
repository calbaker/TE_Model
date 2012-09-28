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
        self.fit_params = np.ones(6)

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
        self.exh.delta_T = self.exh.T_in - self.exh.T_out
        self.exh.eta = self.exh.delta_T / (self.exh.T_in - self.cool.T_in)

        self.exh.c_p = np.zeros(self.exh.T_in.size)

        for i in range(self.exh.T_in.size):
            self.exh.T = self.exh.T_mean[i]
            self.exh.set_TempPres_dependents()
            self.exh.c_p[i] = self.exh.c_p_air

        self.exh.Qdot = self.exh.mdot * self.exh.c_p * self.exh.delta_T

    def fit_Qdot_data(self):
        """Uses scipy.optimize leastsq to minimize the error of a 2nd
        order polynomial in fitting the experimental Qdot data.
        """
        self.leastsq_out = leastsq(
            self.get_Qdot_error, x0=self.fit_params
            )
        self.fit_params = self.leastsq_out[0]
        self.rep_Qdot_data(self.fit_params)

    def rep_Qdot_data(self, fit_params):
        """Represents experimental Qdot data using 2-dim 2nd order
        polynomial fit."""

        A = fit_params[0:3]
        B = fit_params[3:]

        self.exh.Qdot_fit = (
            A[0] + A[1] * self.exh.mdot + A[2] * self.exh.mdot ** 2. +
            B[0] + B[1] * self.exh.T_in + B[2] * self.exh.T_in ** 2.
            )

    def get_Qdot_error(self, fit_params):
        """Returns error between statistical fit and experimental Qdot
        data."""

        self.rep_Qdot_data(fit_params)
        self.exh.Qdot_fit_err = self.exh.Qdot - self.exh.Qdot_fit

        return self.exh.Qdot_fit_err
