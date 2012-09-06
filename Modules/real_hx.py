"""Sets up and returns an hx instance that has the geometry of the
experimental hx downstairs."""

# Distribution Modules
import os, sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

def get_hx():

    hx_exp = hx.HX()

    # These values must be checked
    hx_exp.width = 20. * 2.54e-2
    hx_exp.exh.height = 2.5 * 2.54e-2
    hx_exp.cool.height = 1. * 2.54e-2
    hx_exp.length = 20. * 2.54e-2
    
    hx_exp.te_pair.Ptype.area = (2.e-3) ** 2
    
    hx_exp.te_pair.leg_area_ratio = 0.662
    hx_exp.te_pair.I = 0.001  # turns off TE effect
    hx_exp.te_pair.length = 1.e-5
    hx_exp.te_pair.fill_fraction = 1.
    
    hx_exp.te_pair.set_leg_areas()
    
    hx_exp.te_pair.Ntype.material = 'MgSi'
    hx_exp.te_pair.Ptype.material = 'HMS'
    
    hx_exp.type = 'counter'

    hx_exp.exh.enh = hx_exp.exh.enh_lib.IdealFin2()
    hx_exp.exh.enh.thickness = 0.1 * 2.54e-2
    hx_exp.exh.enh.spacing = 0.298 * 2.54e-2
    # spacing = 0.400 - 0.124 / 2. - 0.040 = 0.298
    
    hx_exp.cool.enh = hx_exp.cool.enh_lib.IdealFin()
    hx_exp.cool.enh.thickness = 0.08 * 2.54e-2
    hx_exp.cool.enh.spacing = 0.320 * 2.54e-2
    # spacing = 0.400 - 0.100 / 2. - 0.030 = 0.320
    
    hx_exp.cool.T_inlet_set = 300.

    return hx_exp
