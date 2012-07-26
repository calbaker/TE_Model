"""Module containing set properties function."""

import numpy as np

def set_raw_property_data(self):

    """Sets temperature fit curves for thermoelectric properties.

    Methods:

    set_TEproperties
    set_raw_property_data

    """

    print "running set_raw_property_data"



    if self.material == "BiTe variable n-type":
        # properties trial 2 - need to add a comment
        poly_deg = 3
        
        alpha_raw = np.array([[112.301006188, -43.0457272427],
                              [137.129765223, -53.5256743351],
                              [156.431574472, -62.2549482734],
                              [179.857338561, -73.5981860267],
                              [210.184704048, -87.5634182059],
                              [239.165761255, -98.9227171808],
                              [272.270773301, -112.895979971],
                              [308.195946903, -124.275355473],
                              [339.954650668, -135.642685058],
                              [373.158864377, -143.544806084]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[100, 29.467689848],
                          [130, 27.8005198844],
                          [160, 26.4696917156],
                          [190, 24.9615826351],
                          [220, 23.1842086837],
                          [250, 21.0620306825],
                          [280, 18.4187680451],
                          [310, 14.8860234335],
                          [340, 9.7526188408],
                          [370, 1.6249327924]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)


        sigma_raw = np.array([[109.722222222, 64.802436126],
                              [125, 59.3315508021],
                              [138.888888889, 52.8995840761],
                              [158.333333333, 46.7825311943],
                              [179.166666667, 41.3057040998],
                              [201.388888889, 36.1482471777],
                              [229.166666667, 30.3431372549],
                              [259.722222222, 25.4976232917],
                              [284.722222222, 22.2623291741],
                              [309.722222222, 19.3478906714],
                              [336.111111111, 16.7528223411],
                              [359.722222222, 15.1232917409],
                              [376.388888889, 13.8220439691]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)


    if self.material == "BiTe variable p-type":
        # properties trial 2 - need to add a comment 
        poly_deg = 3
        
        alpha_raw = np.array([[112.301006188, 43.0457272427],
                              [137.129765223, 53.5256743351],
                              [156.431574472, 62.2549482734],
                              [179.857338561, 73.5981860267],
                              [210.184704048, 87.5634182059],
                              [239.165761255, 98.9227171808],
                              [272.270773301, 112.895979971],
                              [308.195946903, 124.275355473],
                              [339.954650668, 135.642685058],
                              [373.158864377, 143.544806084]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[100, 29.467689848],
                          [130, 27.8005198844],
                          [160, 26.4696917156],
                          [190, 24.9615826351],
                          [220, 23.1842086837],
                          [250, 21.0620306825],
                          [280, 18.4187680451],
                          [310, 14.8860234335],
                          [340, 9.7526188408],
                          [370, 1.6249327924]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)


        sigma_raw = np.array([[109.722222222, 64.802436126],
                              [125, 59.3315508021],
                              [138.888888889, 52.8995840761],
                              [158.333333333, 46.7825311943],
                              [179.166666667, 41.3057040998],
                              [201.388888889, 36.1482471777],
                              [229.166666667, 30.3431372549],
                              [259.722222222, 25.4976232917],
                              [284.722222222, 22.2623291741],
                              [309.722222222, 19.3478906714],
                              [336.111111111, 16.7528223411],
                              [359.722222222, 15.1232917409],
                              [376.388888889, 13.8220439691]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)
        


    if self.material == "typical BiTe n-type":
        # Extracted from Bed Poudel et al, Science 320, 634 (2008)
        # This was the properties used for first trial of validation
        # process. 
        poly_deg = 3
        
        alpha_raw = np.array([[297.3450032873, -213.717948718],
                              [321.1747205786, -223.974358974],
                              [343.6845825115, -227.820512821],
                              [367.6137409599, -231.025641026],
                              [391.61522025, -229.102564103],
                              [414.22452334, -225.897435897],
                              [439.726660092, -217.564102564],
                              [462.462524655, -205.384615385],
                              [472.47896121, -195.128205128],
                              [496.72452334, -175.897435897],
                              [522.425542406, -153.46153846]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[299.5228426396, 1.3873417722],
                          [321.8578680203, 1.3265822785],
                          [345.5888324873, 1.3164556962],
                          [369.3197969543, 1.3569620253],
                          [391.654822335, 1.3873417722],
                          [416.781725888, 1.4683544304],
                          [440.512690355, 1.6],
                          [462.847715736, 1.7620253165],
                          [474.015228426, 1.8329113924],
                          [497.746192893, 2.035443038],
                          [522.873096447, 2.2075949367]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)


        sigma_raw = np.array([[299.4305754926, 9.746835443],
                              [323.4029100874, 8.6835443038],
                              [344.5312214537, 7.5443037975],
                              [369.9479968681, 6.7088607595],
                              [392.5476641, 6.0253164557],
                              [416.58280047, 5.4936708861],
                              [440.626908521, 5.0379746835],
                              [463.271434164, 4.7341772152],
                              [473.158227848, 4.4303797468],
                              [497.229250946, 4.2025316456],
                              [522.744714864, 4.2025316456]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)


    if self.material == "typical BiTe p-type":
        
        poly_deg = 3
        # Extracted from Bed Poudel et al, Science 320, 634 (2008)
        # This was the properties used for first trial of validation
        # process.
        alpha_raw = np.array([[297.3450032873, 213.717948718],
                              [321.1747205786, 223.974358974],
                              [343.6845825115, 227.820512821],
                              [367.6137409599, 231.025641026],
                              [391.61522025, 229.102564103],
                              [414.22452334, 225.897435897],
                              [439.726660092, 217.564102564],
                              [462.462524655, 205.384615385],
                              [472.47896121, 195.128205128],
                              [496.72452334, 175.897435897],
                              [522.425542406, 153.46153846]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[299.5228426396, 1.3873417722],
                          [321.8578680203, 1.3265822785],
                          [345.5888324873, 1.3164556962],
                          [369.3197969543, 1.3569620253],
                          [391.654822335, 1.3873417722],
                          [416.781725888, 1.4683544304],
                          [440.512690355, 1.6],
                          [462.847715736, 1.7620253165],
                          [474.015228426, 1.8329113924],
                          [497.746192893, 2.035443038],
                          [522.873096447, 2.2075949367]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)


        sigma_raw = np.array([[299.4305754926, 9.746835443],
                              [323.4029100874, 8.6835443038],
                              [344.5312214537, 7.5443037975],
                              [369.9479968681, 6.7088607595],
                              [392.5476641, 6.0253164557],
                              [416.58280047, 5.4936708861],
                              [440.626908521, 5.0379746835],
                              [463.271434164, 4.7341772152],
                              [473.158227848, 4.4303797468],
                              [497.229250946, 4.2025316456],
                              [522.744714864, 4.2025316456]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)


    if self.material == "HMS":
        # Raw data taken from Luo et al. HMS is p-type
        poly_deg = 3
        # print "Curve fitting for HMS"

        alpha_raw = np.array([[296.89119171, 138.265544041], 
                              [380.829015544, 140.620466321],
                              [561.139896373, 176.845854922],
                              [701.03626943, 206.270725389],
                              [806.735751295, 217.652849741],
                              [900., 205.769430052]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[300, 2.40620446533],
                          [485.869565217, 2.20460634548],
                          [593.47826087, 2.1252173913],
                          [707.608695652, 2.07168037603],
                          [815.217391304, 2.09607520564],
                          [900.0, 2.12944770858]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)

        sigma_raw = np.array([[283.888641142, 6.55346563038],
                              [396.056571319, 6.22507485507],
                              [573.510861948, 4.86979996178],
                              [786.035548194, 3.5398961585],
                              [856.520354208, 3.34810791871],
                              [901.20405173, 3.34610116583]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1], poly_deg)

    if self.material == "MgSi":
        # Raw data comes from Gao et al. MgSi is n-type
        poly_deg = 2
        # print "Curve fitting for MgSi"
        
        alpha_raw = np.array([[311.289993567, -111.872146119],
                              [464.006967001, -141.552511416],
                              [644.121200709, -184.931506849],
                              [777.984904831, -207.762557078]])
        self.alpha_params = np.polyfit(alpha_raw[:,0], alpha_raw[:,1], poly_deg)

        k_raw = np.array([[291.236965464, 2.80871520138],
                          [472.020791479, 2.62097005644],
                          [725.982971396, 2.38897924041],
                          [576.615963519, 2.50282215632]])
        self.k_params = np.polyfit(k_raw[:,0], k_raw[:,1], poly_deg)

        sigma_raw = np.array([[307.385007162, 13.156135604],
                              [456.638548464, 9.79627566449],
                              [574.442145472, 8.21502466974],
                              [722.524271845, 7.17849753303]])
        self.sigma_params = np.polyfit(sigma_raw[:,0], sigma_raw[:,1],
                              poly_deg)

def set_properties_v_temp(self,T_props):
    
    """ Sets properties based on polynomial fit values.  

    Used by set_TEproperties to set the temperature-dependent
    properties of materials for which polynomial curve fits have been
    done.  

    This may need to changed to spline fitting at some point for a
    more accurate fit.

    Inputs:
    
    T_props : temperature (K) at which properties are to be evaluated
    
    """
    try: 
        self.alpha_params
    except AttributeError:
        self.set_prop_fit()
    self.alpha = ( np.polyval(self.alpha_params, T_props) * 1.e-6 )
    # Seebeck coefficient (V/K)        
    self.k = np.polyval(self.k_params, T_props)  
    # thermal conductivity (W/m-K) 
    self.sigma = np.polyval(self.sigma_params, T_props) * 1.e4 
    # electrical conductivity (S/m)
    self.rho = 1. / self.sigma
    # electrical resistivity (Ohm-m)        

def set_TEproperties(self,T_props):

    """Sets TE properties

    Inputs:

    T_props : temperature (K) at which properties are to be evaluated

    """
    
    
    # Materials with tabulated properties
    if self.material == 'BiTe variable n-type':
        self.set_TEprop_polyfit(T_props)

    if self.material == 'BiTe variable p-type':
        self.set_TEprop_polyfit(T_props)

    if self.material == 'typical BiTe n-type':
        self.set_TEprop_polyfit(T_props)

    if self.material == 'typical BiTe p-type':
        self.set_TEprop_polyfit(T_props)

    if self.material == 'HMS':
        self.set_TEprop_polyfit(T_props)

    if self.material == 'MgSi': 
        self.set_TEprop_polyfit(T_props)

    # Material properties for validation trial. These properties are
    # for typical BiTe materials at 423 K. The properties for a range
    # of temperature are given above as a poly curve. 
    if self.material == 'BiTe variable n-type':
        self.k = 1.54 # Thermal conductivity (W/m-K)
        self.alpha = -150.e-6 # Seebeck coefficient (V/K)
        # I made this negative even though it's for a p-type
        # material.  This is just for a hypothetical model.
        self.rho = 9.0909 * 1.e-6
        # electrical resistivity (Ohm-m)

    if self.material == 'BiTe variable p-type':
        self.k = 1.54 # Thermal conductivity (W/m-K)
        self.alpha = 150.e-6 # Seebeck coefficient (V/K)
        self.rho = 9.0909 * 1.e-6
        # electrical resistivity (Ohm-m)

    # Materials with properties that are either constant or dependent
    # on temperature by some convenient function.  
    # from CRC TE Handbook Table 12.1
    if self.material == 'ex1 n-type':
        self.k = 54. / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.268 * T_props - 329.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = (T_props - 310.) / 0.1746
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex1 p-type':
        self.k = 3.194 / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.150 * T_props + 211.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 25.
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex2 n-type':
        self.k = 3. / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (0.20 * T_props - 400.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1.e5 / T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex2 p-type':
        self.k = 10. / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = (200.) * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex3 n-type':
        self.k = 3. / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = 0.20 * T_props * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = 1000.
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # from CRC TE Handbook Table 12.1
    if self.material == 'ex3 p-type':
        self.k = 10. / T_props * 100.
        # thermal conductivity (W/m-K)
        self.alpha = 200. * 1.e-6
        # Seebeck coefficient (V/K)
        self.sigma = T_props
        # electrical conductivity (S/cm)
        self.rho = 1. / self.sigma / 100.
        # electrical resistivity (Ohm-m)

    # From CRC TE Handbook Table 27.7
    if self.material == 'constant BiTe n-type':
        self.k = 1.5 # Thermal conductivity (W/m-K)
        self.alpha = -206.e-6 # Seebeck coefficient (V/K)
        # I made this negative even though it's for a p-type
        # material.  This is just for a hypothetical model.
        self.rho = 8.89 * 1.e-6
        # electrical resistivity (Ohm-m)

    # From CRC TE Handbook Table 27.7
    if self.material == 'constant BiTe p-type':
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

