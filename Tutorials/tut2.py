from vafmbase import ChannelType
from vafmcircuits import Machine
import vafmcircuits


machine = Machine(machine=None, name='machine', dt=0.01)
scan = machine.AddCircuit(type='Scanner',name='scann')
inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3)

inter.Configure(steps=[0.805,0.805,0.1], npoints=[8,8,171])
inter.Configure(pbc=[True,True,False])
inter.ReadData('NaClforces.dat')

machine.Connect("scann.x" , "inter.x")
machine.Connect("scann.y" , "inter.y")
machine.Connect("scann.z" , "inter.z")


#image output
imager = machine.AddCircuit(type='output',name='image',file='tut2.dat', dump=0)
imager.Register("scann.x", "scann.y", 'inter.F3')

machine.Connect("scann.record", "image.record")

scan.Place(x=0.805, y=0.805, z=4)
#this will print an empty line after each scanline
scan.Recorder = imager
scan.BlankLines = True 
#not necessary, but it makes it easier for gnuplot
	
#resolution of the image [# points per line, # lines]
scan.Resolution = [64,64]
scan.ImageArea(11.68,11.68) 
	
#scan
scan.ScanArea()