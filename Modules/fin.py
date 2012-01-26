"""Module for modeling fins in exhaust side of heat exhanger"""
# Distribution libraries
import numpy as np

class Fin(object):
    """Class for modeling fin.  This class finds the necessary fin
    parameters such that the efficiency is near unity, and therefore
    the fin is isothermal."""

    def __init__(self):
        """Sets constants and things that need to be guessed to
        execute as a standalone model.

        Sets
        ------------------
        self.thickness : thickness (m) of fin
        self.k : thermal conductivity (kW/m-K) of fin material"""

        self.thickness = 5.e-3
        self.k = 0.2

    def set_eta(self):
        """Determines fin efficiency"""
        self.m = np.sqrt(2. * self.h / (self.k * self.thickness))
        self.eta = ( np.tanh(self.m * self.height) / (self.m *
        self.height) )

    def set_h(self):
        """Determines effective heat transfer coefficient of fin."""
        self.set_eta()
        self.h_base = ( 2. * self.eta * self.h * self.height /
        self.thickness )
