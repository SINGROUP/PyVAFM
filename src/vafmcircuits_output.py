from collections import OrderedDict
from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
from ctypes import *
import matplotlib.pyplot as plt
import numpy as np


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

		if not('file' in list(keys.keys())):
			raise SyntaxError("Output circuit file not specified!")
		self.filename = keys['file']

		if not('dump' in list(keys.keys())):
			raise SyntaxError("Output circuit dump rate not specified!")

		##\internal
		## List of channels to dump in the file.
		self.channels = []

		##\internal
		## Dump rate.
		self.dump = keys['dump']

	

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

		
		cclist = [self.machine.GetChannel(tag) for tag in args]
		self.channels.extend(cclist)
		
		for ch in cclist:
			print('PY: registering channel:',ch.owner.cCoreID,ch.cCoreCHID, ch.cisInput)

			Circuit.cCore.output_register(self.cCoreID,ch.owner.cCoreID,ch.cCoreCHID, ch.cisInput)



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
		

		
		self.cCore.output_dump(self.cCoreID)
		
	
	def DumpMessage(self, message):
		
		self.cCore.output_dumpmessage(self.cCoreID, c_char_p(message))
		

	def Initialize (self):

		pass



	def PlotImage(self,interpolation='none',xtickfreq=10,ytickfreq=10):
		f = open(self.filename,'r')

		Data = []

		scanline = []
		x = []
		y = []

		checkx = False
		checky = False

		for line in f:

			if len(line.split())!=0:
				scanline.append(float(line.split()[2]))



				if checkx==False:
					x.append(float(line.split()[0]))

				if checky==False:
					y.append(float(line.split()[1]))
					checky=True


			if len(line.split())==0:
				Data.append(scanline)
				scanline = []
				checkx = True
				checky = False



		dataRev = []


		#Reverse data
		Datasize = len(Data)-1
		while Datasize >0:
			dataRev.append(Data[Datasize])
			Datasize = Datasize-1



		plt.figure()
		plt.set_cmap('hot')
		plt.imshow(dataRev, interpolation='none')
		plt.colorbar()		
		#plt.show()

		tick_locs = np.arange(1,len(x),xtickfreq)
		tick_lbls = x[0::xtickfreq]
		plt.xticks(tick_locs, tick_lbls)


		y = y[::-1]
		tick_locs = np.arange(1,len(y),ytickfreq)
		tick_lbls = y[0::ytickfreq]
		plt.yticks(tick_locs, tick_lbls)
		plt.savefig(self.filename.split('.')[0]+'.png')

	def CloseFile(self):
		self.cCore.output_close(self.cCoreID)

		
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

