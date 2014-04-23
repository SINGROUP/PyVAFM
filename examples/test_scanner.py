#!/usr/bin/env python
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')


from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	machine.AddCircuit(type='Perlin', name='nx', octaves=3, persist=0.3, amp=0.05, period=1.23, pushed=True)
	machine.AddCircuit(type='Perlin', name='ny', octaves=3, persist=0.3, amp=0.05, period=1.23, pushed=True)
 	
  	#create a scalar field
  	machine.AddCircuit(type='opMul',name='mx', in2=19, pushed=True )
  	machine.AddCircuit(type='opMul',name='my', in2=19, pushed=True )
  	machine.AddCircuit(type='opSin',name='sinx', pushed=True )
  	machine.AddCircuit(type='opSin',name='siny', pushed=True )
  	machine.AddCircuit(type='opAdd',name='add', pushed=True )
	
	
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_scanner.log', dump=1)
	out1.Register('global.time', "scan.x", "scan.y", "scan.z", 'add.out')
	
	#image output
	imager = machine.AddCircuit(type='output',name='image',file='test_scanner_image.log', dump=0)
	imager.Register("scan.x", "scan.y", 'add.out')
	
	machine.Connect("scan.record","image.record")
	machine.Connect("scan.x","nx.signal")
	machine.Connect("scan.y","ny.signal")
	machine.Connect("nx.out","mx.in1")
	machine.Connect("ny.out","my.in1")
	machine.Connect("mx.out","sinx.signal")
	machine.Connect("my.out","siny.signal")
	machine.Connect("sinx.out", "add.in1")
	machine.Connect("siny.out", "add.in2")
	
	#this will print an empty line after each scanline
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#not necessary, but it makes it easier for gnuplot
	
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [30,60]
	
	#scan
	scanner.ScanArea()
	
	#visualise the image with gnuplot as follows:
	#set pm3d map
	#set palette rgbformula 34,35,36
	#sp'test_scanner_image.log' u 1:2:3
	

if __name__ == '__main__':
	main()

