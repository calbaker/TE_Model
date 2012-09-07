"""This script sets up and solves an hx instance for comparison to
experimental data."""

# Distribution Modules
import os
import sys
import numpy as np

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

def get_hx():
    """Sets up and returns an hx instance that has the geometry of the
    experimental hx downstairs."""

    hx_mod = hx.HX()

    hx_mod.plate.thickness = (
        (0.300 +  # thickness (in) of coolant plate
         0.375)  # thickness (in) of exhaust plate
        * 2.54e-3
        )  # total thickness (m)
    hx_mod.plate.set_h()

    # These values must be checked
    hx_mod.width = 20. * 2.54e-2
    hx_mod.exh.height = 2.5 * 2.54e-2
    hx_mod.cool.height = 1. * 2.54e-2
    hx_mod.length = 20. * 2.54e-2
    
    hx_mod.te_pair.Ptype.area = (2.e-3) ** 2
    
    hx_mod.te_pair.leg_area_ratio = 0.662
    hx_mod.te_pair.I = 0.001  # turns off TE effect
    hx_mod.te_pair.length = 1.e-5
    hx_mod.te_pair.fill_fraction = 1.
    
    hx_mod.te_pair.set_leg_areas()
    
    hx_mod.te_pair.Ntype.material = 'MgSi'
    hx_mod.te_pair.Ptype.material = 'HMS'
    
    hx_mod.type = 'counter'

    hx_mod.exh.set_enhancement('IdealFin2')
    hx_mod.exh.enh.thickness = 0.1 * 2.54e-2
    hx_mod.exh.enh.spacing = 0.298 * 2.54e-2
    # spacing = 0.400 - 0.124 / 2. - 0.040 = 0.298
    
    hx_mod.cool.set_enhancement('IdealFin')
    hx_mod.cool.enh.thickness = 0.08 * 2.54e-2
    hx_mod.cool.enh.spacing = 0.320 * 2.54e-2
    # spacing = 0.400 - 0.100 / 2. - 0.030 = 0.320
    
    hx_mod.cool.T_inlet_set = 300.

    return hx_mod

def solve_hx(hx_exp, hx_mod):

    """Solves heat exchanger for all the conditions in the
    experimental data set."""
    
    hx_mod.Qdot_arr = np.zeros(hx_exp.exh.T_in.size)
    hx_mod.exh.delta_P_arr = np.zeros(hx_exp.exh.T_in.size)

    for i in range(hx_exp.exh.T_in.size):
        hx_mod.exh.T_inlet = hx_exp.exh.T_in[i]
        hx_mod.exh.mdot = hx_exp.exh.mdot[i]
        hx_mod.cool.mdot = hx_exp.cool.Vdot[i] * hx_mod.cool.rho
        hx_mod.cool.T_outlet = hx_exp.cool.T_out[i]

        hx_mod.solve_hx()

        hx_mod.Qdot_arr[i] = hx_mod.Qdot_total
        hx_mod.exh.delta_P_arr[i] = hx_mod.exh.deltaP_total

    return hx_mod
