"""Module containing set properties function.  It got too big to be in
the tem module."""

import scipy as sp

def set_prop_fit(self):
    """Sets temperature fit curves for thermoelectric properties."""

    if self.material == "HMS":
        # Raw data taken from Luo et al.
        poly_deg = 3
        print "Curve fitting for HMS"

        alpha_raw = sp.array([[296.89119171, 138.265544041], 
                              [380.829015544, 140.620466321],
                              [561.139896373, 176.845854922],
                              [701.03626943, 206.270725389],
                              [806.735751295, 217.652849741],
                              [900., 205.769430052]])
        self.alpha_params = sp.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = sp.array([[300, 2.40620446533],
                          [485.869565217, 2.20460634548],
                          [593.47826087, 2.1252173913],
                          [707.608695652, 2.07168037603],
                          [815.217391304, 2.09607520564],
                          [900.0, 2.12944770858]])
        self.k_params = sp.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)

        sigma_raw = sp.array([[283.888641142, 6.55346563038],
                              [396.056571319, 6.22507485507],
                              [573.510861948, 4.86979996178],
                              [786.035548194, 3.5398961585],
                              [856.520354208, 3.34810791871],
                              [901.20405173, 3.34610116583]])
        self.sigma_params = sp.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)

    if self.material == "MgSi":
        # Raw data comes from Gao et al.  
        poly_deg = 2
        print "Curve fitting for MgSi"
        
        alpha_raw = sp.array([[311.289993567, -111.872146119],
                              [464.006967001, -141.552511416],
                              [644.121200709, -184.931506849],
                              [777.984904831, -207.762557078]])
        self.alpha_params = sp.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = sp.array([[291.236965464, 2.80871520138],
                          [472.020791479, 2.62097005644],
                          [725.982971396, 2.38897924041],
                          [576.615963519, 2.50282215632]])
        self.k_params = sp.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)

        sigma_raw = sp.array([[307.385007162, 13.156135604],
                              [456.638548464, 9.79627566449],
                              [574.442145472, 8.21502466974],
                              [722.524271845, 7.17849753303]])
        self.sigma_params = sp.polyfit(sigma_raw[:,0], sigma_raw[:,1],
                              poly_deg)

def set_TEproperties(self):
    """Sets thermal and electrical properties, as a function of
    temperature if self.T_props is used."""

    if self.material == 'HMS':
        self.alpha = sp.polyval(self.alpha_params, self.T_props) * 1.e-6
        # Seebeck coefficient (V/K)        
        self.k = sp.polyval(self.k_params, self.T_props)      
        # thermal conductivity (W/m-K) 
        self.sigma = sp.polyval(self.sigma_params, self.T_props) * 1.e4 
        # electrical conductivity (S/m)
        self.rho = 1. / self.sigma
        # electrical resistivity (Ohm-m)        

    if self.material == 'MgSi': 
        self.alpha = sp.polyval(self.alpha_params, self.T_props) * 1.e-6
        # Seebeck coefficient (V/K)        
        self.k = sp.polyval(self.k_params, self.T_props)      
        # thermal conductivity (W/m-K) 
        self.sigma = sp.polyval(self.sigma_params, self.T_props) * 1.e4
        # electrical conductivity (S/m)
        self.rho = 1. / self.sigma
        # electrical resistivity (Ohm-m)        

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

    # Alumina with pure conduction
    if self.material == 'alumina':
        self.k = 1.5 # Thermal conductivity (W/m-K) this needs to be
                     # updated to what it actually is
        self.alpha = 1.e-9 # Seebeck coefficient (V/K)
        # I made this negative even though it's for a p-type
        # material.  This is just for a hypothetical model.
        self.rho = 1. # dummy value since I don't know what it
                      # actually is and it doesn't matter.  
        # electrical resistivity (Ohm-m)

    # Direct contact between hot and cold side
    if self.material == 'none':
        self.k = 1.e9 # really high thermal condutivity (W/m-K) so
                      # that resistance is zero
        self.alpha = 1.e-9 # dummy value
        self.rho = 1. # dummy value
