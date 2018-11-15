from vafmcircuits import Machine

machine = Machine(name='machine', dt=0.01)

machine.AddCircuit(type='waver', name='osc', freq=1, amp=1)

machine.AddCircuit(type='TutCircuit', name='TutCircuit', gain=2)

# machine.Connect('osc.sin','TutCircuit.in')

logger = machine.AddCircuit(
    type='output', name='logger', file='tutorial_AddCircuits.out', dump=1)
logger.Register('global.time', 'osc.sin', 'TutCircuit.out')

machine.Wait(1)
