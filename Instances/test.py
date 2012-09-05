"""This script is used to run several other scripts that may fail due
to changes in Modules.  This script will help troubleshoot failures
caused by these changes."""

execfile('te_inst.py')
execfile('fin_inst.py')
execfile('osf_inst.py')
execfile('leg_inst.py')
execfile('hx_validation.py')
execfile('hx_validation_noTE.py')
