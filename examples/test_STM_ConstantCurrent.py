#!/usr/bin/env python
from vafmcircuits import Machine

def main():
	I = 5e-5

	machine = Machine(machine=None, name='machine', dt=1e-3)


	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )

	machine.AddCircuit(type='PI', name='pi',Kp=-1e1,Ki=-1e1, set = I, pushed=True)
	machine.AddCircuit(type='opAdd', name='Add', pushed=True)

	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)
	inter.BiasStep=0.5
	inter.StartingV=1.5
	inter.ConfigureVASP(pbc=[True,True,False,False])
	inter.ReadVASPData("parchg.1.5")


	machine.AddCircuit(type='STM',name='STM', pushed=True)
	

	out1 = machine.AddCircuit(type='output',name='output',file='testSTM.dat', dump=100)
	out1.Register('global.time','scan.x', 'scan.y','Add.out','STM.Current','inter.F1','pi.out')	


	imager = machine.AddCircuit(type='output',name='image',file='STM.dat', dump=0)
	imager.Register("scan.x","scan.y",'STM.Current','inter.F1','pi.out',"inter.z")	

	machine.Connect("scan.x","inter.x")
	machine.Connect("scan.y","inter.y")
#	machine.Connect("scan.z","inter.z")

	machine.Connect("Add.out","inter.z")



	machine.Connect("inter.F1","STM.Density")
	machine.Connect("scan.record","image.record")
	machine.Connect("STM.Current","pi.signal")

	machine.Connect("scan.z","Add.in1")
	machine.Connect("pi.out","Add.in2")







	
	machine.circuits['inter'].I['V'].Set(1.5)
	scanner.Place(x=0,y=0,z=17)
	machine.Wait(1)


	'''
	machine.circuits['pi'].I['signal'].Set(1)
	machine.Wait(0.1)
	machine.circuits['pi'].I['signal'].Set(2)
	machine.Wait(0.1)
	machine.circuits['pi'].I['signal'].Set(0.1)
	machine.Wait(0.1)
	'''	

	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [200,200]
	scanner.ImageArea(18,16)        
	#scan
	scanner.ScanArea()
	
		
	
if __name__ == '__main__':
        main()
