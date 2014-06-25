#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
	
	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)

	machine.Wait(1)

if __name__ == '__main__':
        main()
