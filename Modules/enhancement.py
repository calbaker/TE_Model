# coding=utf-8
"""Contains classes for modeling convection heat transfer
enhancement."""

# Distribution libraries
import numpy as np


class BejanPorous(object):

    """Class for porous media according to the book of Bejan.

    Bejan, A. “Designed Porous Media: Maximal Heat Transfer Density at
    Decreasing Length Scales.” International Journal of Heat and Mass
    Transfer 47, no. 14 (2004): 3073–3083.

    Methods:

    __init__
    solve_enh

    """

    def __init__(self):

        """Initializes a bunch of constants."""

        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.Nu_D
        # Nu for porous media parallel plates with const heat flux.
        # Bejan Eq. 12.77

    def solve_enh(self):

        """Solves for convection parameters with enhancement."""

        self.Re_K = self.velocity * self.K ** 0.5 / self.nu
        # Re based on permeability from Bejan Eq. 12.11
        self.f = 1. / self.Re_K + 0.55
        # Darcy Law, Bejan Eq. 12.14.  It turns out that f is pretty
        # close to 0.55
        self.k = self.k_matrix
        self.deltaP = (self.f * self.perimeter * self.node_length /
        self.flow_area * (0.5 * self.rho * self.velocity ** 2) *
        0.001)
        # pressure drop (kPa)
        self.h_conv = self.Nu_D * self.k / self.D
        # coefficient of convection (kW/m^2-K)


class MancinPorous(object):

    """Class for modeling porous media according to Mancin.

    Mancin, S., C. Zilio, A. Cavallini, and L. Rossetto. “Pressure
    Drop During Air Flow in Aluminum Foams.” International Journal of
    Heat and Mass Transfer 53, no. 15–16 (2010): 3121–3130.

    Methods:

    __init__
    solve_enh

    """

    def __init__(self):

        """Sets constants."""

        self.porosity = 0.92
        self.k_matrix = 5.8e-3
        self.PPI = 10.
        self.K = 2.e-7
        self.k = self.k_matrix
        self.Nu_D = 4.93
        # Nu for porous media parallel plates with T_w = const.  Bejan
        # Eq. 12.77

    def solve_enh(self):

        """Solves for convection parameters with enhancement."""

        self.G = self.rho * self.velocity
        # Mass velocity from Mancin et al.
        self.D_pore = 0.0122 * self.PPI ** (-0.849)
        # hydraulic diameter (m?) of porous media based on Mancin
        # et al.
        self.Re_K = (self.D_pore * self.G / (self.mu * self.porosity))
        # Re of porous media from Mancin et al.
        self.F = ((1.765 * self.Re_K ** (-0.1014) * self.porosity ** 2
        / self.PPI ** (0.6)))
        # friction factor from Mancin et al.
        self.f = self.F
        # possibly wrong assignment but gets code to shut up and run
        self.deltaP = (self.length * 2. * self.F * self.G ** 2 /
        (self.D_pore * self.rho) * 0.001)
        # pressure drop from Mancin et al.
        self.h_conv = self.Nu_D * self.k_matrix / self.D
        # coefficient of convection (kW/m^2-K)


class IdealFin(object):

    """Class for modeling straight fin.

    Mills, A. F. Heat Transfer. 2nd ed. Prentice Hall, 1998.

    Methods:

    __init__
    set_eta
    set_enh_geometry
    set_h_and_P
    solve_enh

    """

    def __init__(self, flow):

        """Sets constants and things are needed at runtime.  Runs
        set_fin_height and set_area_convection."""

        self.thickness = 1.e-3
        # fin thickness (m)
        self.k = 0.2
        # thermal conductivity (kW / (m * K)) of fin material
        self.spacing = 0.003
        # distance (m) between adjacent fin edges

        self.flow = flow
        self.set_fin_height()

    def set_fin_height(self):

        """Sets fin height based on half of duct height."""

        if self.flow.sides == 2:
            self.height = self.flow.height / 2
            # height of fin pair such that their tips meet in the
            # middle and are adiabatic.
        else:
            self.height = self.flow.height
            # height of fin that crosses the channel

    def set_area_convection(self):

        """Sets finned and unfinned area for convection."""
        
        if self.flow.sides == 2:
            self.flow.area_unfinned = (
                2. * (self.flow.width - self.N * self.thickness)
                )
            # unfinned base area on both sides of duct
            self.flow.area_finned = 2. * self.N * self.thickness
            # finned base area on both sides of duct
        else:
            self.flow.area_unfinned = (
                self.flow.width - self.N * self.thickness
                )
            # unfinned base area on both sides of duct
            self.flow.area_finned = self.N * self.thickness
            # finned base area on both sides of duct

    def set_enh_geometry(self):

        """Fixes appropriate geometrical parameters.

        """

        self.set_fin_height()

        self.N = ((self.flow.width / self.spacing - 1.) / (1. +
        self.thickness / self.spacing))

        self.flow.perimeter = (
            2. * (self.spacing + self.flow.height) * (self.N + 1.)
            )
        # perimeter of new duct formed by fins with constant overall duct width
        self.flow.flow_area = self.spacing * self.flow.height * (self.N + 1.)
        # flow area (m^2) of new duct formed by fin

        self.flow.D = 4. * self.flow.flow_area / self.flow.perimeter
        # hydraulic diameter (m)

        self.set_area_convection()

    def set_eta(self):

        """Sets fin efficiency and related parameters.

        """

        self.beta = np.sqrt(
            2. * self.flow.h_conv / (self.k * self.thickness)
            )
        # dimensionless fin parameter
        self.xi = self.beta * self.height
        # beta times fin length (self.height)
        self.eta = np.tanh(self.xi) / self.xi
        # fin efficiency

    def set_h_and_P(self):

        """Sets effective heat transfer coefficient and deltaP.

        """

        self.flow.h_unfinned = self.flow.h_conv

        self.effectiveness = (
            self.eta * 2. * self.height / self.thickness 
            )
        self.h_base = self.effectiveness * self.flow.h_conv

        self.flow.h_conv = (
            (self.flow.h_unfinned * self.flow.area_unfinned +
            self.h_base * self.flow.area_finned) / self.flow.width
            )

        self.flow.deltaP = (
            self.flow.f * self.flow.perimeter * self.flow.node_length
            / self.flow.flow_area * (0.5 * self.flow.rho *
            self.flow.velocity ** 2) * 0.001
            )
        # pressure drop (kPa)

    def solve_enh(self):

        """Runs all the other methods that need to run.

        Methods:

        self.set_enh_geometry
        self.set_eta
        self.set_h_and_P

        """

        self.flow.set_Re_dependents()
        self.flow.h_conv = self.flow.Nu_D * self.flow.k / self.flow.D
        # coefficient of convection (kW/m^2-K)

        self.set_eta()
        self.set_h_and_P()


class OffsetStripFin(object):

    """Class for modeling offset strip fins.

    Uses correlations from:

    Manglik, Raj M., and Arthur E. Bergles, 'Heat Transfer and
    Pressure Drop Correlations for the Rectangular Offset Strip Fin
    Compact Heat Exchanger', Experimental Thermal and Fluid Science,
    10 (1995), 171-180 <doi:10.1016/0894-1777(94)00096-Q>.

    Methods:

    __init__
    set_params
    set_f
    set_j
    solve_enh

    """

    def __init__(self, flow):

        """Sets constants and things that need to be guessed to
        execute as a standalone model.

        Sets
        ------------------
        self.thickness : thickness (m) of fin strip
        self.l : length (m) of fin
        self.spacing : pitch (m) of fin
        self.k : thermal conductivity (W/m/K) of osf material"""

        self.thickness = 0.001
        self.l = 0.01
        self.spacing = 0.001
        self.k = 0.2
        self.flow = flow

    def set_params(self):

        """Sets flow parameters.

        See Manglik and Bergles Fig. 1.

        """

        self.height = self.flow.height - self.thickness
        # vertical gap (m) between fins and hx walls

        # self.spacing : horizontal gap (m) between fins

        self.alpha = self.spacing / self.height
        self.delta = self.thickness / self.l
        self.gamma = self.thickness / self.spacing

        self.rows = self.flow.length / self.l
        # number of rows of offset strip fins in streamwise direction

        self.area_frac = ((self.spacing * self.height) /
        ((self.height + self.thickness) * (self.spacing +
        self.thickness)))
        # fraction of original area still available for flow

        self.area_enh = ((self.height * self.thickness + self.height
                           * self.l + self.spacing * self.l) /
                          ((self.thickness + self.spacing) * self.l))
        # heat transfer area enhancement factor

        self.D = (4. * self.spacing * self.height * self.l / (2. *
        (self.spacing * self.l + self.height * self.l + self.thickness
        * self.height) + self.thickness * self.spacing))

        self.flow_area = self.flow.flow_area * self.area_frac
        # actual flow area (m^2)
        self.perimeter = 4. * self.flow_area / self.D
        # check this calculation at some point ???
        self.velocity = self.flow.velocity / self.area_frac
        # actual velocity (m/s) based on flow area
        self.Re_D = self.velocity * self.D / self.flow.nu

    def set_f(self):

        """Sets friction factor, f."""

        self.f = (9.6243 * self.Re_D ** -0.7422 * self.alpha ** -0.1856 *
                   self.delta ** 0.3053 * self.gamma ** -0.2659)

    def set_j(self):

        """Sets Colburn factor, j."""

        self.j = (0.6522 * self.Re_D ** -0.5403 * self.alpha ** -0.1541 *
        self.delta ** 0.1499 * self.gamma ** -0.0678 * (1. + 5.269e-5 *
        self.Re_D ** 1.340 * self.alpha ** 0.504 * self.delta ** 0.456 *
        self.gamma ** -1.055) ** 0.1)

    def solve_enh(self):
        """Runs all the methods for this class.

        self.h_convcomes from Thermal Design by HoSung Lee, eq. 5.230
        self.eta_fin : fin efficiency


        Methods:

        self.set_params
        self.set_f
        self.set_j

        """

        self.set_params()
        self.set_f()
        self.flow.f = self.f
        self.flow.deltaP = (self.f * self.perimeter * self.flow.node_length /
                    self.flow.flow_area * (0.5 * self.flow.rho * self.velocity
        ** 2) * 0.001)
        # pressure drop (kPa)
        self.set_j()
        self.h_conv = (
            self.j * self.flow.mdot / self.flow_area * self.flow.c_p /
        self.flow.Pr ** 0.667
            )
        self.beta = np.sqrt(2. * self.h_conv / (self.k * self.thickness))
        self.xi = self.beta * self.height / 2.
        self.eta_fin = np.tanh(self.xi) / self.xi
        self.effectiveness = self.eta_fin * self.height / self.thickness
        self.h_base = self.h_conv * self.effectiveness
        self.flow.h_conv = (
            (self.h_base * self.thickness + self.h_conv *
             self.spacing) / (self.spacing + self.thickness)
            )

        self.flow.Nu_D = self.flow.h_conv * self.flow.D / self.flow.k


class JetArray(object):
    """Class for impinging jet array.

    Huber, Aaron M., and Raymond Viskanta. “Effect of Jet-jet Spacing
    on Convective Heat Transfer to Confined, Impinging Arrays of
    Axisymmetric Air Jets.” International Journal of Heat and Mass
    Transfer 37, no. 18 (December 1994): 2859–2869.
    """

    def __init__(self):
        """Initializes variables that do not require calculation.

        Variables that are set
        -------------------------
        self.D : jet diameter (m)
        self.H : distance (m) from jet exit to impingement surface
        self.K : minor loss coefficient. Fox, McDonald, and Pritchard
        Table 8.2.
        self.spacing : distance (m) between adjacent jets"""

        self.D = 3.0e-3
        self.H = 1.0e-2
        self.K = 0.5
        self.spacing = 0.5e-2

    def set_number(self, flow):
        """Sets number of jets based on jet spacing and overall size
        of jet array.

        Set variables
        ----------------
        self.N_streamwise : number of jets in streamwise direction
        self.N_transverse : number of jets in transverse direction
        self.N : total number of jets in array
        self.area : area (m^2) of a jet unit cell

        Variables that must be set to run this method
        ---------
        self.width : width (m) of jet array in transverse direction
        self.length : length (m) of jet array in streamwise direction"""

        self.N_streamwise = flow.length / self.spacing
        self.N_transverse = flow.width / self.spacing
        self.N = self.N_streamwise * self.N_transverse
        self.area = self.spacing ** 2

    def set_annulus(self, flow):
        """Sets variables related to annulus geometry.

        Requires
        ---------------
        self.width
        self.Vdot

        Sets
        ---------------
        self.ann_area
        self.ann_perimeter
        self.ann_velocity"""

        self.ann_area = flow.width * self.H
        self.ann_perimeter = 2. * (flow.width + self.H)
        self.ann_velocity = flow.Vdot / self.ann_area / 2.

    def set_enh_flow(self, flow):
        """Determines pressure drop through jet array.

        Sets the following variables
        -------------------------------
        self.flow_area : flow area (m^2) for single jet
        self.V : velocity through jet orifice (m/s)
        self.h_loss : head loss (m^2/s^2) through jet orifice
        self.deltaP : pressure drop (kPa) thorugh jet orifice

        Variables that must be set to run this method
        ------------
        self.rho : density (kg/m^3) of fluid passing through jet
        self.Vdot : volume flow rate (m^3/s) of fluid passing through jet
        array"""

        self.flow_area = np.pi * self.D ** 2 / 4.
        self.V = flow.Vdot / (self.flow_area * self.N)
        self.h_loss = self.K * self.V ** 2 / 2.
        flow.deltaP = self.h_loss * flow.rho * 0.001

    def set_Nu_D(self, flow):
        """Sets Nusselt number and some other variables

        Sets the following variables
        -------------------------
        self.Nu_D : average Nusselt number based on jet diameter
        self.Re_D : Re based on jet diameter

        Variables that must be set to run this method
        ------------
        self.nu : viscosity (m^2 / s) of fluid
        self.Pr : Prandtl number of fluid"""

        self.Re_D = self.V * self.D / flow.nu
        flow.Nu_D = (
            0.285 * self.Re_D ** 0.710 * flow.Pr ** 0.33 * (self.H /
        self.D) ** -0.123 * (self.spacing / self.D) ** -0.725
            )

    def solve_enh(self, flow):
        """This method is probably not useful so this doc string is
        not good."""

        self.set_number(flow)
        self.set_annulus(flow)
        self.set_enh_flow(flow)
        self.set_Nu_D(flow)
        flow.h_conv = flow.Nu_D * flow.k / self.D
        flow.f = 37.
        # this might need to be changed, or it might be a dummy
        # variable just to keep the code from complaining.
