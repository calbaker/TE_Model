
class Pump(object):

    '''A simple pump model'''

    def __init__(self, flow=10., p_drop=330, eff=0.52):

        self.flow = flow
        self.p_drop = p_drop
        self.eff= eff

    def pump_pwr(self,check=0):

        '''Calculates the shaft work required to pump the working fluid.'''

        self.power = self.flow * self.p_drop / self.eff
        
        if check:
            return self.power #returns power in Watts if check == 1

    def set_vals(self, flow, p_drop):

        '''Set values for flow and pressure drop in liters per second and kPa'''

        self.flow = flow
        self.p_drop = p_drop
        


if __name__ == "__main__":
    a = Pump()
    a.pump_pwr(1)
    print "Pump requires %0.2f Watts" %a.power
