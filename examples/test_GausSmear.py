from vafmcircuits import Machine

machine = Machine(name='machine', dt=0.0001, pushed=True);
machine.AddCircuit(type='GausSmear',name='GS',pushed=True,Filename='host.LOCPOT',Sigma=0.1,OutputFilename='test.dat')