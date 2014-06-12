from vafmcircuits import Machine
 
machine = Machine(name='machine', dt=0.01)

machine.AddCircuit(type='waver', name='osc', freq=1.2, amp=1)

machine.AddCircuit(type='opAdd', name='adder', factors=2)

machine.Connect('osc.sin','adder.in1')
machine.Connect('osc.cos','adder.in2')

logger = machine.AddCircuit(type='output', name='logger', file='tutorial_basic.out', dump=1)
logger.Register('global.time','osc.sin','osc.cos','adder.out')

machine.Wait(3)
