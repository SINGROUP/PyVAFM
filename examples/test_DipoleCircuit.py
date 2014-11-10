#!/usr/bin/env python
from vafmcircuits import Machine
import math
import numpy as np
####################################


machine = Machine(machine=None, name='machine', dt=0.01)

#machine.AddCircuit(type='LOCPOTShaping',name='LOCPOTShaping', OutputFilename="Ceria.dat",PotentialFilename="host.LOCPOT",ForcefieldSize=[15.562592,13.4776,25.413607]
#					,ForcefieldStepSize=[0.072049037037,0.0748755555556,0.075635735119]
#					, LatticeVectora=[15.562592,0.0,0.0], LatticeVectorb=[-7.781296,13.4776,0.0], LatticeVectorc=[15.562592,-8.985067,25.413607] ,pushed=True)

machine.AddCircuit(type='Dipole',name='Dipole',InputFile="Ceria.dat", OutputFile="FF.dat", stepsize= [0.072049037037,0.0748755555556,0.075635735119])