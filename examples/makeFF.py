#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
		
	machine.AddCircuit(type='Dipole',name='Dipole', OutputFilename="Cerium.dat",PotentialFilename ="host.LOCPOT" ,pushed=True)

#	machine.AddCircuit(type='PlotAtoms',name='PlotAtoms', Filename ="ceo2_111_host_ortho.LOCPOT" ,pushed=True)


if __name__ == '__main__':
        main()
