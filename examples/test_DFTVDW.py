from vafmcircuits import Machine

machine = Machine(name='machine', dt=0.0001, pushed=True)
machine.AddCircuit(type='DFTD3', name='DFTD3', pushed=True,)
