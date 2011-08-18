"""Module for plotting temperature profile data from terminal or
another script."""  

import matplotlib.pyplot as plt

def Plot_temp(hx):
    """Function for plotting temperature profile data from terminal or
    another script."""
    # Plot configuration
    FONTSIZE = 20
    plt.rcParams['axes.labelsize'] = FONTSIZE
    plt.rcParams['axes.titlesize'] = FONTSIZE
    plt.rcParams['legend.fontsize'] = FONTSIZE
    plt.rcParams['xtick.labelsize'] = FONTSIZE
    plt.rcParams['ytick.labelsize'] = FONTSIZE
    plt.rcParams['lines.linewidth'] = 1.5

    plt.figure()
    plt.plot(hx.x_dim * 100., hx.exh.T_nodes, '-r', label='Exhaust')
    plt.plot(hx.x_dim * 100., hx.tem.T_h_nodes, '-g', label='TEM Hot Side')
    plt.plot(hx.x_dim * 100., hx.tem.T_c_nodes, '-k', label='TEM Cold Side')
    plt.plot(hx.x_dim * 100., hx.cool.T_nodes, '-b', label='Coolant')

    plt.xlabel('Distance Along HX (cm)')
    plt.ylabel('Temperature (K)')
    # plt.title('Temperature v. Distance, '+hx.type)
    plt.grid()
    plt.legend(loc='best')
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('Plots/temp '+hx.type+str(hx.exh.fins)+'.png')
    plt.savefig('Plots/temp '+hx.type+str(hx.exh.fins)+'.pdf')

    plt.show()
