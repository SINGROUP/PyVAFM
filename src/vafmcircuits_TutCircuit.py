from vafmbase import Circuit
from ctypes import *


class TutCircuit(Circuit):
    # MY VERSION
    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        gain = 1

        if 'gain' in list(keys.keys()):
            gain = float(keys['gain'])

        self.AddInput("in")
        self.AddOutput("out")

        self.cCoreID = Circuit.cCore.Add_TutCirc(
            self.machine.cCoreID, c_double(gain))
        print(self.cCoreID)
        self.SetInputs(**keys)
