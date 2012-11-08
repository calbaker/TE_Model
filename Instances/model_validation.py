"""Plots results from heat exchanger experiments."""

import numpy as np
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import exp_data
reload(exp_data)
import real_hx
reload(real_hx)

hx_exp = exp_data.ExpData()
hx_exp.folder = '../ExpData/'

hx_exp.file = 'gypsum'
# fit_status = ''

# hx_exp.file = 'copper'

fit_status = '_fit'
# fit_status = '_exp'

hx_exp.import_data()
hx_exp.get_Qdot_fit()

SIZE = 10
mdot_surf = np.linspace(
    hx_exp.exh.mdot.min(), hx_exp.exh.mdot.max(), SIZE
    )
T_in_surf = np.linspace(
    hx_exp.exh.T_in.min(), hx_exp.exh.T_in.max(), SIZE
    )
mdot2d, T_in2d = np.meshgrid(mdot_surf, T_in_surf)
hx_exp.rep_Qdot_surf(mdot_surf, T_in_surf)

hx_mod = real_hx.get_hx()

if hx_exp.file == 'gypsum':
    k_gypsum = 0.17e-3
    # # thermal conductivity (kW / (m * K)) of gypsum board from Incropera
    # # and DeWitt Intro. to Heat Transfer 5th ed., Table A.3
    thickness_gypsum = 0.25 * 2.54e-2
    # thickness (m) of gypsum board
    hx_mod.R_extra = thickness_gypsum / k_gypsum


elif hx_exp.file == 'copper':
    # the following expressions for k come from Li and Peterson, 2006. The
    # effective thermal conductivity of wire screen
    k_copper = 400.e-3  # thermal conductivity of copper (kW / (m * K))
    # from Wolfram Alpha
    thickness_copper = 508.e-6  # effective thickness (m) of copper mesh 
    phi_copper = 0.95  # effective porosity of copper based on density
    # calculated by weiging a sample and estimating its volume then
    # comparing this result to the solid material density.  
    k_air = 3.24e-5  
    # thermal conductivity (kW / (m * K)) of air at 405 K, which is mean
    # temperature between coolant and exhaust over all nodes.
    k_alexander = (
        k_air / (k_copper / k_air) ** ((1. - phi_copper) ** 0.59)
        )
    k_koh = (
        (1. - phi_copper) / (1. + 11. * phi_copper) * k_copper
        )
    k_upper = phi_copper * k_air + (1. - phi_copper) * k_copper
    k_lower = (
        (phi_copper / k_air + (1. - phi_copper) / k_copper) ** -1.
        )

    k_effective = 0.5 * (k_alexander + k_koh)
    # thermal conductivity of mesh screen according to average of
    # Alexander's and Koh and Fortini's model taken from Li and Peterson
    # 2006 - The effective thermal conductivity of wire screen.
    # hx_mod.R_extra = thickness_copper / k_effective
    hx_mod.R_extra = 6.54
    k_effective = thickness_copper / hx_mod.R_extra

hx_mod.R_interconnect = 0.
hx_mod.R_substrate = 0.
hx_mod.R_contact = 0.

if fit_status == '_fit':
    if hx_exp.file == "gypsum":
        hx_exp.R_extra = 17.1
    elif hx_exp.file == "copper":
        hx_exp.R_extra = 8.21
    hx_mod = real_hx.solve_hx(hx_exp, hx_mod)
    # print "running fit_hx"
    # print hx_mod.R_extra
    # hx_mod = real_hx.fit_hx(hx_exp, hx_mod)
    # print hx_mod.R_extra
    f2 = open("../output/model_validation/fit", "w")
    f2.write(fit_status)
    f2.close()
if fit_status == '_exp':
    hx_mod.R_extra = 4.2
    hx_mod = real_hx.solve_hx(hx_exp, hx_mod)
    f2 = open("../output/model_validation/fit", "w")
    f2.write(fit_status)
    f2.close()
else:
    hx_mod = real_hx.solve_hx(hx_exp, hx_mod)

hx_exp.epsilon = (
    hx_exp.exh.deltaT / (hx_exp.exh.T_in - hx_exp.cool.T_in)
    )
hx_exp.capacity = hx_exp.Qdot_max

np.savez(
    '../output/model_validation/' + hx_exp.file + fit_status,
    mdot=hx_exp.exh.mdot, T_in=hx_exp.exh.T_in, deltaP=hx_exp.exh.deltaP,
    deltaP_arr=hx_mod.exh.deltaP_arr, Qdot=hx_exp.exh.Qdot,
    Qdot_arr=hx_mod.Qdot_arr, Qdot_surf=hx_exp.exh.Qdot_surf,
    mdot2d=mdot2d, T_in2d=T_in2d, velocity=hx_mod.exh.velocity_arr,
    rho=hx_mod.exh.rho_arr, Re_D=hx_mod.exh.Re_arr,
    Re_omega=hx_mod.exh.Re_omega_arr,
    epsilon_exp=hx_exp.epsilon,
    epsilon_mod=hx_mod.epsilon_arr, capacity=hx_exp.capacity,
    R_extra=hx_mod.R_extra, 
    Qdot_omega=hx_exp.Qdot_omega,
    Qdot_max_omega=hx_exp.Qdot_max_omega
    )

f = open('../output/model_validation/file',"w")
f.write(hx_exp.file + fit_status)
f.close()

f_R_extra = open(
    "../output/model_validation/" + hx_exp.file + "_R_extra","w"
    )
f_R_extra.write(str(hx_mod.R_extra))
f_R_extra.close()

execfile('plot_exp.py')
