#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
	
	inter = machine.AddCircuit(type='LOCPOTInter',name='inter', components=1, pushed=True)
	inter.ConfigureLOCPOT(pbc=[True,True,False])
	inter.ReadLOCPOTData("parchg.1.0")

	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )

	out1 = machine.AddCircuit(type='output',name='output',file='testLOCPOT.dat', dump=1)
	out1.Register('scan.x', 'scan.y','scan.z','inter.U')	

	#Imaging output
	imager = machine.AddCircuit(type='output',name='image',file='LOCPOT.dat', dump=0)
	imager.Register("scan.x","scan.y",'inter.U')	

	machine.Connect("scan.x","inter.x")
	machine.Connect("scan.y","inter.y")
	machine.Connect("scan.z","inter.z")
	machine.Connect("scan.record","image.record")

	#machine.circuits['inter'].I['V'].Set(1.0)
	scanner.Place(x=0,y=0,z=15)
	#scanner.Move(x=16, v=1)
	
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [50,50]
	scanner.ImageArea(18,16)        
	#scan
	scanner.ScanArea()
	
if __name__ == '__main__':
        main()
