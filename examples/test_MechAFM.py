#!/usr/bin/env python

from vafmcircuits import Machine

machine = Machine(name='machine', dt=0.0001, pushed=True);

machine.AddCircuit(type="MechAFM",name="mechAFM",xyzfile="graphene.xyz",paramfile="parameters.dat",
					TipAtom="O", DummyAtom="X",PlaneAtom="C", MinTerm="f",etol=0.1,ftol=0.1, cfac=0.001,
					MaxSteps=50000, coulomb="on",zhigh=10.0,zlow=6.0,dx=0.5,dy=0.5,dz=0.1,bufsize=1000,InputFileName="test.in",MPICommand="/path/to/mpirun -np 1")
