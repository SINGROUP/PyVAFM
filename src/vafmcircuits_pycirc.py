from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
import ctypes as c

import math

## \package vafmcircuits_pycirc.py
# This file contains the controller circuits.
#


class PYCircuit(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		#print "PY: initing PYCircuit!"
		
		super(PYCircuit, self).__init__( machine, name )
		

	def Create(self, **keys):
		
		#create the callback function
		CBFunc = c.CFUNCTYPE(None)
		self.callback = CBFunc(self.Update)
		
		self.cCoreID = Circuit.cCore.Add_PYCircuit(self.machine.cCoreID, (c.py_object(self)),
			self.callback, len(self.I),len(self.O))
		
		self.SetInputs(**keys)
		
	def Initialize (self):

		pass
	


class myCirc(PYCircuit):

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		self.AddInput("in1")
		self.AddInput("in2")
		self.AddOutput("out")
		
		
		self.Create(**keys)
		
	
	def Update(self):
		
		self.O["out"].value = self.I["in1"].value*self.I["in2"].value
		
