#!/usr/bin/env python
from vafmcircuits import Machine

def main():



	machine = Machine(machine=None, name='machine', dt=0.01)
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	
	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)
	inter.BiasStep=0.5
	inter.StartingV=2
	inter.ConfigureVASP(pbc=[True,True,False,False])
	inter.ReadVASPData("parchg.2.0")


	machine.AddCircuit(type='STM',name='STM', pushed=True)

	out1 = machine.AddCircuit(type='output',name='output',file='testSTM.dat', dump=1)
	out1.Register('scan.x', 'scan.y','scan.z','STM.Current','inter.F1')	


	imager = machine.AddCircuit(type='output',name='image',file='STM.dat', dump=0)
	imager.Register("scan.x","scan.y",'STM.Current','inter.F1')	

	machine.Connect("scan.x","inter.x")
	machine.Connect("scan.y","inter.y")
	machine.Connect("scan.z","inter.z")
	machine.Connect("inter.F1","STM.Density")
	machine.Connect("scan.record","image.record")


	machine.circuits['inter'].I['V'].Set(2)
	scanner.Place(x=0,y=0,z=5)

	
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [50,50]
	scanner.ImageArea(18,16)        
	#scan
	scanner.ScanArea()
	
if __name__ == '__main__':
        main()
