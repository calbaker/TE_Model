# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np

# User Defined Modules
# In this directory
import hx
reload(hx)

class hx_series(object):
    """Class for modeling several heat exchanger in series that have
    different properties or parameters."""

    def __init__(self):
        """Initializes the following variables:
        ----------------------
        self.N : number of heat exchangers in series
        self."""
        self.N = 
