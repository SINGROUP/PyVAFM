#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
		
#	machine.AddCircuit(type='Dipole',name='Dipole',Dx=0,Dy=0,Dz=3,ZOffsetLower=134,ZOffsetUpper=134 ,Divisons=1, OutputFilename="Dipole.dat",PotentialFilename ="surf_f_elec_NN.LOCPOT" ,pushed=True)
#	machine.AddCircuit(type='PlotAtoms',name='PlotAtoms', Filename ="surf_f_elec_NN.LOCPOT" ,pushed=True)



	scan = machine.AddCircuit(type='Scanner',name='scann')
	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1)

	inter.Configure(steps=[0.072049037037,0.0720490369539,0.0741075825003], npoints=[215,215,285])
	inter.Configure(pbc=[True,True,False])
	inter.ReadData('Dipole.dat')

	machine.Connect("scann.x" , "inter.x")
	machine.Connect("scann.y" , "inter.y")
	machine.Connect("scann.z" , "inter.z")


	#image output
	imager = machine.AddCircuit(type='output',name='image',file='DipoleTest.dat', dump=0)
	imager.Register("scann.x", "scann.y", 'inter.F1')

	machine.Connect("scann.record", "image.record")

	scan.Place(x=16, y=16, z=16)
	#this will print an empty line after each scanline
	scan.Recorder = imager
	scan.BlankLines = True 
	#not necessary, but it makes it easier for gnuplot
		
	#resolution of the image [# points per line, # lines]
	scan.Resolution = [256,256]
	scan.ImageArea(15,15) 
		
	#scan
	scan.ScanArea()

if __name__ == '__main__':
        main()
