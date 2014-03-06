from collections import OrderedDict
from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
from ctypes import *


## \package vafmcircuits_output
# \brief This module contains the circuits that handle outputs.
#

## \brief Output circuit.
#
# \image html output.png "schema"
#
# Use this to dump the values of channels in a log file. 
# The channel values that are printed to the file are added/removed using the
# \link output.Register Register\endlink and \link output.Unregister Unregister\endlink
# functions. The input channel \a record, if connected will make the circuit
# print to file only when its value is positive.
#
# \b Initialisation \b parameters:
# 	- \a file = name of the log file
# 	- \a dump = #  rate at which data is printed in the file
#
# \b Input \b channels:
# 	- \a record = if connected, the output will be printed only when this input is 1
#
# \b Output channels:
# This circuit has no output channel.
#
# 
# \b Example:
# \code
# logger = machine.AddCircuit(type='output', name='logger', dump=1)
# logger = machine.AddCircuit(type='output', name='logger', dump=100)
# \endcode
#
class output(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if not('file' in keys.keys()):
			raise SyntaxError("Output circuit file not specified!")
		self.filename = keys['file']

		if not('dump' in keys.keys()):
			raise SyntaxError("Output circuit dump rate not specified!")

		##\internal
		## List of channels to dump in the file.
		self.channels = []

		##\internal
		## Dump rate.
		self.dump = keys['dump']

		#self._file = open(self.filename, 'w')

		self._cnt = 0

		self.AddInput("record")
		
		self.cCoreID = Circuit.cCore.Add_output(self.machine.cCoreID,self.filename,c_int(self.dump))
		

		self.SetInputs(**keys)


	def Start(self):
		Circuit.cCore.output_start(self.cCoreID);
	
	def Stop(self):
		Circuit.cCore.output_stop(self.cCoreID);

	## Register an output channel for file output.
	#
	# If the channel is already registered in this output circuit, it won't be registered again.
	#
	# @param *args Channel tags to be printed in the output.
	#
	# \b Example:
	# \code{.py}
	# logger = machine.AddCircuit(type='output', name='logger', dump=100)
	# logger.Register('global.time','waver.sin','adder.out', ...)
	# \endcode
	#
	def Register(self, *args):

		#if type(channel) is list:
		#cclist = [j.split(".",1) for j in channel]
		cclist = [self.machine.GetChannel(tag) for tag in args]
		self.channels.extend(cclist)
		
		for ch in cclist:
			print 'PY: registering channel:',ch.owner.cCoreID,ch.cCoreCHID, ch.cisInput
			#(int outer, int cindex, int chindex, int isInput)
			#Circuit.cCore.output_register_feed(self.cCoreID,ch.signal.cCoreFEED)
			Circuit.cCore.output_register(self.cCoreID,ch.owner.cCoreID,ch.cCoreCHID, ch.cisInput)
		
		#else :

		#	if not(channel in self.channels):
		#		self.channels.append(channel)


	## Unregister a channel from the output.
	#
	# If the channel is already unregistered, it won't be unregistered again.
	#
	# @param *args Channel tags to be removed from the output.
	#
	# \b Example:
	# \code{.py}
	# logger = machine.AddCircuit(type='output', name='logger', dump=100)
	# logger.RegisterChannel('global.time','waver.sin','adder.out', ...)
	# ...
	# logger.Unregister('adder.out', ...)
	# \endcode
	#
	def Unregister(self, *args):
		
		cclist = [self.machine.GetChannel(tag) for tag in args]
		cclist = [x for x in self.channels.extend if x not in cclist]

		self.channels = cclist
	
	## \brief Write the output to the file.
	# Use this function to write one record in the output file.
	#
	#
	# \b Example:
	#
	# \code
	# logger = machine.AddCircuit(type='output', name='logger', dump=100)
	# logger.RegisterChannel('global.time','waver.sin','filter.out', ...)
	# ...
	# logger.Dump()
	# \endcode
	#
	def Dump(self):
		
		#for i in self.channels:
		#	self._file.write(str(i.value)+" ")
		#self._file.write('\n')
		
		self.cCore.output_dump(self.cCoreID)
		
	
	def DumpMessage(self, message):
		
		self.cCore.output_dumpmessage(self.cCoreID, c_char_p(message))
		

	def Initialize (self):

		pass

	

	def Update (self):


		if self.I['record'].signal.owner != self: #check if the record signal is connected to something else

			#if the record channel is connected and it is positive valued
			#write to file
			if self.I['record'].value > 0:
				for i in self.channels:
					self._file.write(str(i.value)+" ")
				self._file.write('\n')

		else: #if not connected...

			#if the dumprate is 0, do not print!
			if self.dump == 0:
				return

			self._cnt += 1

			if self._cnt == self.dump:
				self._cnt = 0
				#dump the data

				for i in self.channels:
					self._file.write(str(i.value)+" ")
				self._file.write('\n')



