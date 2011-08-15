

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

FIGDIM1 = ([0.12, 0.12, 0.75, 0.75])

XTICKS = list()

for i in sp.arange(sp.size(hx.exh.height_array)):
    XTICKS.append('{:01.1f}'.format(hx.exh.height_array[i] * 1.e2))

fig = plt.figure()
ax1 = fig.add_axes(FIGDIM1)
ax1.plot(ducts, hx.Qdot_array / 10., label=r'$\dot{Q}/10$') 
ax1.plot(ducts, hx.tem.power_array, label='TEM')
ax1.plot(ducts, hx.power_net_array, label='$P_{net}$')  
ax1.plot(ducts, hx.Wdot_pumping_array, label='Pumping')
ax1.legend(loc='best')
ax1.grid()
ax1.set_xlabel('Ducts')
ax1.set_ylabel('Power (kW)')
ax1.set_ylim(0,5)
ax1.set_ylim(ymin=0)
ax2 = plt.twiny(ax1)
plt.xticks(sp.arange(sp.size(hx.exh.height_array)), XTICKS)
ax2.set_xlabel('Exhaust Duct Height (cm)')

#ax1.set_title('\n\nPower v. Number of Ducts')

fig.savefig('Plots/power v ducts.pdf')
fig.savefig('Plots/power v ducts.png')

plt.show()

