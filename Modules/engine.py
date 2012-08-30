"""Contains Engine class used to determine attributes of engine.  This will be
fleshed out with experimental data later."""

# User defined modules
import properties as prop

class Engine(object):

    """Class definition for engine object.

    Methods:
    
    self.set_mdot_charge

    """

    def __init__(self,**kwargs):
        
        """Sets constants

        Methods:
        
        self.air.set_TempPress_dependents()

        Instantiated in hx.py in HX class

        """

        if 'RPM' in kwargs:
            self.RPM = kwargs['kwargs']
        else:
            self.RPM = 2000. # engine speed (RPM)
        if 'torque' in kwargs:
            self.torque = kwargs['torque']
        else:
            self.torque = 300. # brake torque (lb-ft)
        self.displacement = 6.7e-3 # engine swept displacement (m**3)
        self.cylinders = 6. # number of cylinders
        self.eta_V = 1. # volumetric efficiency of engine. Can exceed unity for
        # turbo-charged unthrottled engine. Accounts for error
        # in intake manifold pressure estimate.
        self.T_intake = 300. # engine intake temperature (K)
        self.P_intake = 101.325 # pressure (kPa) at intake manifold
        self.air = prop.ideal_gas() # engine working fluid is ideal gas with
        # the properties of air
        self.air.T = self.T_intake
        self.air.P = self.P_intake
        self.air.set_TempPres_dependents()

    def set_mdot_charge(self):
        
        """Sets charge mass flow rate.""" 

        self.mdot_charge =( 
            (self.RPM / 2. * self.displacement * self.eta_V *
            self.air.rho) / 60.
            )  
        # charge flow (kg/s) in engine


