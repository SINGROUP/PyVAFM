from vafmbase import ChannelType
from vafmcircuits import Machine
import vafmcircuits

# Assign the machine with a time step of 0.01
machine = Machine(name='machine', dt=0.01)

# Add waver and add circuit
machine.AddCircuit(type='waver', name='wave', amp=1, freq=2)
machine.AddCircuit(type='opAdd', name='Add')

# connect a sin wave to both inputs
machine.Connect("wave.sin", "Add.in1")
machine.Connect("wave.sin", "Add.in2")

# Add the output circuit and register channels
out1 = machine.AddCircuit(
    type='output', name='output', file='tut1.dat', dump=1)
out1.Register('global.time', 'wave.sin', 'Add.out')

# ask the machine to wait for 5 seconds
machine.Wait(5)
