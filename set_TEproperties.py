"""Module containing set properties function.  It got too big to be in
the tem module."""

import scipy as sp

def set_TEproperties(self):
    """Sets thermal and electrical properties, as a function of
    temperature if self.T_props is used.
    Material choices for n-type are HMS, ex1 n-type, ex2 n-type,
    and ex3 n-type
    Material choices for p-type are MgSI, ex1 p-type, ex2 p-type,
    and ex3 p-type"""
    if self.material == "HMS":
        # These properties came from Xi Chen's HMS properties.ppt
        self.k = 4.
        # thermal conductivity (W/m-K) 
        self.alpha = 150.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1000.
        # electrical conductivity (1/Ohm-cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    if self.material == "MgSi":
        # These properties came from Gao et al.  
        self.k = 3. 
        # thermal conductivity (W/m-K) 
        self.alpha = -150.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1.5e3 # (S/cm) (S/cm = 1/Ohm-cm)
        # electrical conductivity (1/Ohm-cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)
        self.I

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex1 n-type':
        self.k = 54. / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.268 * self.T_props - 329.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = (self.T_props - 310.) / 0.1746
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex1 p-type':
        self.k = 3.194 / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.150 * self.T_props + 211.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 25.
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex2 n-type':
        self.k = 3. / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.20 * self.T_props - 400.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1.e5 / self.T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex2 p-type':
        self.k = 10. / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (200.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = self.T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex3 n-type':
        self.k = 3. / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = 0.20 * self.T_props * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1000.
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex3 p-type':
        self.k = 10. / self.T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = 200. * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = self.T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # From CRC TE Handbook Table 27.7
    if self.material == 'ideal BiTe n-type':
        self.k = 1.5 # Thermal conductivity (W/m-K)
        self.alpha = -206.e-6 # Seebeck coefficient (V/K)
        # I made this negative even though it's for a p-type
        # material.  This is just for a hypothetical model.
        self.rho = 8.89 * 1.e-6
        # electrical resistivity (Ohm-m)

    # From CRC TE Handbook Table 27.7
    if self.material == 'ideal BiTe p-type':
        self.k = 1.5 # Thermal conductivity (W/m-K)
        self.alpha = 206.e-6 # Seebeck coefficient (V/K)
        self.rho = 8.89 * 1.e-6
        # electrical resistivity (Ohm-m)

