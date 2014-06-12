import abc
import itertools
import inspect
import sys
import math
import io
from collections import OrderedDict
from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel

from ctypes import *
import threading

import vafmcircuits_math, vafmcircuits_output, vafmcircuits_signal_gens, vafmcircuits_Cantilever
import vafmcircuits_Logic, vafmcircuits_Filters, vafmcircuits_control, vafmcircuits_Interpolation
import vafmcircuits_signal_processing, vafmcircuits_Scanner, vafmcircuits_FlipFlop
import vafmcircuits_pycirc, vafmcircuits_Comparison, vafmcircuits_avg
import vafmcircuits_VDW


## \package vafmcircuits
# \brief This file contains the main Machine circuit.
#


## Virtual %Machine main class.
#
# This is the main virtual machine object. It can also be used as a conventional \link vafmbase.Circuit circuit \endlink, acting as a
# circuit container. Every Machine circuit has one default output channel \a 'time', but other input/output
# channels can be added.
#
#
# \b Initialisation \b parameters:
#	- \a dt = timestep (only for main machine)
#	- \a assembly = constructor function (only for composites)
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- custom inputs (only for composites)
#
# \b Output \b channels:
# 	- \a time = global simulation time
# 	- custom outputs (only for composites)
#
#
# \b Example:
# \code{.py}
# #create the main virtual machine
# machine = Machine(name='machine', dt=1.0e-8)
#
# #create a machine circuit inside the main machine
# composite = machine.AddCircuit(type="Machine", name='pll', assembly=PLL, ...)
# 
# \endcode
#
#
class Machine(Circuit):

	singleton = False
	main = None
	#cCore = None
	
	
	## Class contructor.
	# This should be used only to create the main virtual machine circuit.
	#
	# \b Example:
	# \code{.py}
	#
	# machine = Machine(name='machine', dt=1.0e-8)
	#
	# \endcode
	#
	# \note Only one machine can be initialised this way.
	#
	def __init__(self, machine=None, name="machine", **keys):
		
		isMain = 0
		
		if (Machine.singleton == True and machine == None):
			raise NameError ("ERROR! Only one main machine can be initialised!")
		
		if(Machine.singleton == False and machine == None):
			#if this is the absolute first machine to be added
			print "Init main machine..."
			Machine.singleton = True
			Machine.main = self
			isMain = 1
			

		print "adding circuit",name,": machine == None =>",machine == None
		
		print "init of Machine..."
		
		super(self.__class__, self).__init__( machine, name )


		## \brief Ordered dictionary of the circuits in the setup.
		# Ordered dictionary of the circuits in the setup. The dictionary keys are the circuit names, the values are
		# references to the circuit objects.
		#
		# \b Example:
		#
		# \code
		# waver = machine.circuits['oscillator']
		#
		# \endcode
		self.circuits = OrderedDict()

		## Integration timestep
		self.dt = 0.0
		if not ('dt' in keys.keys()):
			if(machine!=None):
				self.dt = machine.dt
				print 'WARNING! No timestep dt was given, using main machine one!'
			else:
				print 'WARNING! No timestep dt was given in the initialisation parameters.'
		else:
			self.dt = keys['dt']
		
		## Integer number of update steps so far.
		self._idt = 0;
		
		if(machine == None):
			Circuit.cCore.SetTimeStep(c_double(self.dt))
		
		self._MetaI = OrderedDict()
		self.cCoreI = []
		#self.cCoreIx= OrderedDict() #dictionary <name,feedindex>
		
		self._MetaO = OrderedDict()
		self.cCoreO = []
		#self.cCoreOx= OrderedDict() #dictionary <name,feedindex>
		
		# create a container in the cCore
		owneridx = -1
		if self.machine == None:
			#print 'Allocating main machine!'
			owneridx = -1
		else:
			owneridx = self.machine.cCoreID
		
		self.cCoreID = Circuit.cCore.Add_Container(owneridx,isMain)
		#print 'machine cCoreID: ',self.cCoreID
		
		if self.machine == None:
			self.AddOutput('time')
		

		if 'assembly' in keys.keys():
			self.Assemble = keys['assembly']
			self.Assemble(self,**keys)

		
		#self.SetCCoreChannels()
		self.SetInputs(**keys)


		

	##\internal
	## Get the feed indexes from the cCore
	#
	#
	def SetCCoreChannels(self):
		
		#for a container, Circuit.cCore.GetInputs gives the indexes of the dummy
		#relay circuits that represents external channels
		
		
		getins = Circuit.cCore.GetInputs
		getins.restype = POINTER(c_int)
		getouts = Circuit.cCore.GetOutputs
		getouts.restype = POINTER(c_int)
		
		# get the indexes of input(original) channels
		dummyins = getins(self.cCoreID) #indexes of the dummy circuits
		for i in range(len(self.I)):
			
			feedin = getins(dummyins[i])[0]
			feedout= getouts(dummyins[i])[0]
			
			self.I.values()[i].signal.cCoreFEED = feedin
			self._MetaI.values()[i].signal.cCoreFEED = feedout
		
		# --------------------------------------------------------------
		
		# get the indexes of output channels
		dummyouts = getouts(self.cCoreID) #indexes of the dummy circuits
		for i in range(len(self.O)):
			
			feedin = getins(dummyouts[i])[0]
			feedout= getouts(dummyouts[i])[0]
			
			self.O.values()[i].signal.cCoreFEED = feedout
			self._MetaO.values()[i].signal.cCoreFEED = feedin
			
		#print self.I.values(), self.O.values()
		print 'PY: SetCCoreChannels done!'

	def SetInputs_fromKeys(self, **kwargs):
		
		for key in kwargs.keys():
			
			if key in self.I.keys():
				
				
				self.I[key].Set(kwargs[key]) #deprecated... sets the value in python!
				
				idx = self.I.keys().index(key) #find the position of the key
				print "PY: "+key+" is an input channel, calling cCore(c):",idx,c_double(kwargs[key])
				
				Circuit.cCore.SetContainerInput(self.cCoreID, idx, c_double(kwargs[key]))
				
				
				print "   input "+key+" -> "+str(kwargs[key])
				
			else:
				#print the init parameter even if not an input flag
				print " ??" + key + " " + str(kwargs[key])
				pass



	## Fabricator function.
	# 
	# This function is called when the machine is instantiated, only if
	# the "assembly" parameter was given among initialisation arguments.
	# The function is originally left unimplemented, so the user can build
	# the setup after the machine is instantiated.
	#
	# \b Example:
	#
	# Assembly function definition:
	#
	# \code{.py}
	# 
	# def MyAssembly(compo):
	# 
	# 	# add global channels
  	#   compo.AddInput("signal1")
  	#   ...
  	#   # add internal circuits
  	#   compo.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
  	#   ...
  	#   # connect internal circuits to global input and outputs
  	#   compo.Connect("global.signal1","adder.in1")
  	#   compo.Connect("adder.out","global.out")
	#   ...
	# \endcode
	#
	# Main script:
	#
	# \code
	#
	# def main():
	#  
	#   main = Machine(name='machine', dt=0.01, pushed=True);
	#   
	#   # add a Machine circuit to main, and set it up with the MyAssembly function
  	#   main.AddCircuit(type='Machine', name='compo1', assembly=MyAssembly, pushed=True)
  	#   ...
	#  
	# if __name__ == '__main__':
	#   main()
	#
	# \endcode
	#
	def Assemble(self):
		pass

	## \internal
	## \brief Total simulation time.
	# Total simulation time elapsed.
	@property
	def time(self):
		return self._idt*self.dt


	## Create an input channel with the given name.
	#
	# Add a global input channel to the machine. This is done when the
	# machine is intended to be used as a composite circuit inside another machine,
	# and thus it needs to communicate with other circuits.
	#
	# @param name Name of the new input channel.
	#
	# \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	# composite = machine.AddCircuit(type='Machine', name='compo', ...)
	# composite.AddInput('signal')
	# \endcode
	#
	def AddInput(self, name):
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in composite circuit "+ str(self))

		self.I[name] = Channel(name,self,True)
		self._MetaI[name] = Channel(name,self,False)
		
		# add the channel also on the cCore
		self.cCoreI.append(Circuit.cCore.Add_ChannelToContainer(self.cCoreID, 1)) #1 for input
		#print 'out idx:',idx
		#print 'machine added output: ',idx
		#self.cCoreI.append(idx) 
		print "Circuit ",self.name," added channel",name

	## Create an output channel with the given name.
	#
	# Add a global output channel to the machine. This is done when the
	# machine is intended to be used as a composite circuit inside another machine,
	# and thus it needs to communicate with other circuits.
	#
	# @param name Name of the new output channel.
	#
	# \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	# composite = machine.AddCircuit(type='Machine', name='compo', ...)
	# composite.AddOutput('outsignal')
	# \endcode
	#
	def AddOutput(self, name):
		
		#print "py adding output..."
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in composite circuit "+ str(self))

		self.O[name] = Channel(name,self,False)
		self._MetaO[name] = Channel(name,self,True)
		
		# add the channel also on the cCore
		self.cCoreO.append(Circuit.cCore.Add_ChannelToContainer(self.cCoreID, 0))#1 for input
		#print 'out idx:',idx
		#print 'machine added output: ',idx
		#self.cCoreO.append(idx) 
		

	## \internal
	## Add a circuit of type 'ctype' named 'name' to the setup.
	#
	# This looks into all the loaded modules whose name starts with
	# 'vafmcircuits' and finds the first class named 'ctype'. 
	# It then instantiate the class.
	# - Mandatory arguments:\n
    # 	- type = string: type name of the circuit class\n
    # 	- name = string: name to use for the new instance of the circuit\n
    #	- others: specific arguments depending on the particular circuit to add.
    #
	# - Optional arguments:\n
    # 	- pushed = bool: defined the output behaviour model.\n
    #	- others: specific arguments depending on the particular circuit to add.
    #
    # 
    # @param **argkw Keyworded arguments for circuit initialisation.
    #
	# @return Reference to the created circuit.
	#
    # \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	#
	# machine.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
	# machine.AddCircuit(type='output',name='log',file='log.log', dump=1)
	# \endcode
	#
	def AddCircuit(self, **argkw):
		
		
		
		lst = sys.modules.keys()
		classobj = None

		#check for mandatory arguments, type and name
		if not ("type" in argkw.keys()):
			raise SyntaxError("The circuit type was not specified.")
		ctype = argkw["type"]
		
		if not ("name" in argkw.keys()):
			raise SyntaxError("The circuit name was not specified.")
		cname = argkw["name"]

		print "new circuit: " + ctype + "  " + cname
		for i in range(len(lst)): #loop over the modules

			if lst[i].startswith('vafmcircuits'): #if the module is a vafmcircuits module

				#extract classes from the module, except the abstract one
				c = [s for s in inspect.getmembers(sys.modules[lst[i]], inspect.isclass) if s[0]==ctype]

				if len(c)!=0:
					classobj = c[0]
					break

		#check if the type was good
		if classobj == None:
			raise NotImplementedError("Circuit "+ctype+" was not implemented or imported!")

		#check if the name was good
		if cname in self.circuits.keys():
			raise NameError("A circuit named '"+cname+"' already exists in the setup!")

		#instantiate
		instance = classobj[1](machine=self, **argkw)
		self.circuits[cname] = instance
		return instance

	##\internal
	## Find the channel with the given tag among the subcircuits.
	# The tag of a channel is a string containing the name of the circuit to which it belongs
	# and the name of the channel separated by a dot.
	# The function raises an error if the circuit does not exist in the dictionary, or if the channel
	# does not exist inside the circuit.
	# The argument chtype is given as enum ChannelType, and if used it will limit the search for the channel
	# only in the input or output channels of the circuit.
	# @param tag Channel tag.
	# @param chtype Type of the channel: ChannelType.Input | ChannelType.Output | ChannelType.Any
	# @return Reference to the channel.
	#
	# \b Example:
	# \code{.py}
	# vafm._GetInternalChannel("oscillator.sin", vafmcore.ChannelType.Output)
	# vafm._GetInternalChannel("integrator.out", vafmcore.ChannelType.Output)
	# vafm._GetInternalChannel("mycircuit.mychannel", vafmcore.ChannelType.Any)
	# \endcode
	def _GetInternalChannel(self, tag, chtype=ChannelType.Any):

		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("GetInternalChannel error: channel tag "+tag+ " is invalid.")

		cname = ctag[0]
		chname = ctag[1]

		allchs = {}

		# handle the case where we are looking for a channel of the machine, and not
		# one in a subcircuit.
		if cname == 'global':

			raise SyntaxError ("GetInternalChannel error: the VAFM can only perform connections between internal circuits")

		#check the name of the circuit
		if not(cname in self.circuits.keys()):
			raise NameError( "GetInternalChannel error: circuit "+cname+" not found." )

		#get the circuit
		circ = self.circuits[cname] 

		if chtype == ChannelType.Input or chtype == ChannelType.Any:
			allchs.update(circ.I)
		if chtype == ChannelType.Output or chtype == ChannelType.Any:
			allchs.update(circ.O)

		return allchs[chname]


	def _GetMetaChannel(self, tag, chtype=ChannelType.Any):

		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("GetMetaChannel error: channel tag "+tag+ " is invalid.")

		cname = ctag[0]
		chname = ctag[1]

		allchs = {}

		# handle the case where we are looking for a channel of the machine, and not
		# one in a subcircuit.

		if chtype == ChannelType.Input or chtype == ChannelType.Any:
			allchs.update(self._MetaI)
		if chtype == ChannelType.Output or chtype == ChannelType.Any:
			allchs.update(self._MetaO)

		return allchs[chname]


	## \internal
	## Find a channel by tag.
	#
	# The tag is given in the string format: "circuitname.channelname".
	# Global circuits of the machine are named "global.channelname".
	#
	# @param tag Channel tag
	#
	# @return Reference to the channel.
	#
	# \b Example:
	# \code{.py}
	# sinwave = machine.GetChannel('waver.sin')
	# time = machine.GetChannel('global.time')
	# \endcode
	#
	def GetChannel(self, tag):

		#check if the tag has the correct syntax
		chname = tag.split(".",1)
		if len(chname) != 2:
			raise SyntaxError ("Machine.GetChannel error: channel tag "+tag+ " is invalid.")
		cname = chname[0]
		chname = chname[1]


		if self._IsGlobal(tag):
			circ = self #if the tag is global, the circuit is the machine itself
		else:
			circ = self.circuits
			if not (cname in circ.keys()):
				raise NameError( "Machine.GetChannel error: circuit "+cname+" not found." )
			circ = circ[cname]

		#create a global dictionary
		allch = {}
		allch.update(circ.I)
		allch.update(circ.O)



		if not( chname in allch.keys() ):
			raise NameError( "Machine.GetChannel error: channel "+chname+" not found." )

		return allch[chname]

	def GetOutputChannel(self, tag):

		#check if the tag has the correct syntax
		chname = tag.split(".",1)
		if len(chname) != 2:
			raise SyntaxError ("Machine.GetOutputChannel error: channel tag "+tag+ " is invalid.")
		cname = chname[0]
		chname = chname[1]


		

		if self._IsGlobal(tag):
			circ = self #if the tag is global, the circuit is the machine itself
		else:
			circ = self.circuits
			if not (cname in circ.keys()):
				raise NameError( "Machine.GetOutputChannel error: circuit "+cname+" not found." )
			circ = circ[cname]
			
		allch = {} #create a dictionary
		allch.update(circ.O)


		if not( chname in allch.keys() ):
			raise NameError( "Machine.GetOutputChannel error: channel "+chname+" not found." )

		return allch[chname]


	## Checks whether the given channel tag points to a global channel.
	# Global channels are marked as "global.channelname".
	# @param tag String with the channel tag.
	# @return True if the tag points to a global channel, False otherwise.
	def _IsGlobal(self, tag):

		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("IsGlobal error: channel tag "+tag+ " is invalid.")

		if ctag[0] == 'global':
			return True
		else:
			return False


	## \internal
	## Connect the output of a circuit to the input of another.
	#
	# The I/O channels to connect are specified with the syntax: "circuit.channel", in the *args arguments
	# array. The first element has to be the output channel to use as source, while all
	# the following elements refer to the destination channels.
	#
	# @param *args Name of the channels to connect: "circuit.channel"
	#
	# \b Example:
	# \code{.py}
  	# main = Machine(name='machine', dt=0.01, pushed=True);
  	# 
  	# main.AddCircuit(type='waver', name='osc', amp=1, freq=1)
  	# main.AddCircuit(type='opAdd', name='adder', factors=3)
  	#
  	# main.Connect("osc.sin", "adder.in1")
  	# main.Connect("osc.cos", "adder.in2", adder.in3)
  	#
	# \endcode
	def Connect_OLD(self, *args):

		#if the output is a global, then it means that we want to connect
		#the global input to input channels in the machine
		
		ccSrcID = -1
		ccDstID = -1
		ccSrcCH = -1
		ccDstCH = -1
		
		#find the output channel
		if self._IsGlobal(args[0]):
			#look in MetaI
			outsignal = self._GetMetaChannel(args[0], ChannelType.Input)
			
			print 'PY: connect src - out channel name ',outsignal.name
			print 'PY: connect src - index ',self.I.keys().index(outsignal.name)
			ccSrcID = self.cCoreI[self.I.keys().index(outsignal.name)]
			ccSrcCH = 1 #dummy has only one in and one out!
			print 'PY: connect src - dummyidx ',ccSrcID
			print self.cCoreI
			#the global output is the dummy output
			
		else:
			#otherwise, just look for the channel in the normal circuits
			outsignal = self._GetInternalChannel(args[0], ChannelType.Output)
			ccSrcID = outsignal.owner.cCoreID
			ccSrcCH = outsignal.owner.O.keys().index(outsignal.name)
			
		
		

		for tag in args[1:]: #for each target input tag
			
			print "PY: connecting " + args[0] + " -> " + tag
			
			# find the target channel
			if self._IsGlobal(tag):
				target = self._GetMetaChannel(tag, ChannelType.Output)
				#print 'PY: connect dst - out channel name ',target.name
				#print 'PY: connect dst - index ',self.O.keys().index(target.name)
				ccDstID = self.cCoreO[self.O.keys().index(target.name)]
				ccDstCH = 0 #dummy has only one in and one out!
				#print 'PY: connect dst - dummyidx ',ccDstID
				#the global output is the dummy input
			else:
				target = self._GetInternalChannel(tag, ChannelType.Input)
				ccDstID = target.owner.cCoreID
				ccDstCH = target.owner.I.keys().index(target.name)

			print "  -> " + tag
			target.signal = outsignal.signal
			
			#connect in cCore: Connect(int c1, int out, int c2, int in)
			#outidx = outsignal.owner.O.keys().index(outsignal.name)
			#inidx = target.owner.I.keys().index(target.name)
			print 'PY: connecting ',ccSrcID,ccSrcCH,ccDstID,ccDstCH
			
			Circuit.cCore.Connect(ccSrcID,ccSrcCH, ccDstID, ccDstCH)

			print 'PY: connection done!'

	def Connect(self, *args):

		#if the output is a global, then it means that we want to connect
		#the global input to input channels in the machine
		
		ccSrcID = -1
		ccDstID = -1
		ccSrcCH = -1
		ccDstCH = -1
		
		metaSrc = 0
		
		chname = args[0].split('.',2)[1];
		#find the output channel
		if self._IsGlobal(args[0]):
			
			ccSrcID = self.cCoreID
			ccSrcCH = self.I.keys().index(chname)
			outsignal = self._MetaI[chname]
			metaSrc = 1
		else:
			#otherwise, just look for the channel in the normal circuits
			outsignal = self._GetInternalChannel(args[0], ChannelType.Output)
			ccSrcID = outsignal.owner.cCoreID
			ccSrcCH = outsignal.owner.O.keys().index(outsignal.name)

		for tag in args[1:]: #for each target input tag
			
			#print "PY: connecting " + args[0] + " -> " + tag
			
			# find the target channel
			metaDst = 0
			chname = tag.split('.',2)[1];
			if self._IsGlobal(tag):
				ccDstID = self.cCoreID
				ccDstCH = self.O.keys().index(chname)
				target = self._MetaO[chname]
				metaDst = 1
			else:
				target = self._GetInternalChannel(tag, ChannelType.Input)
				ccDstID = target.owner.cCoreID
				ccDstCH = target.owner.I.keys().index(chname)

			#print "  -> " + tag
			
			target.signal = outsignal.signal
			
			#connect in cCore: Connect(int c1, int out, int c2, int in)
			#outidx = outsignal.owner.O.keys().index(outsignal.name)
			#inidx = target.owner.I.keys().index(target.name)
			#print 'PY: connecting ',ccSrcID,ccSrcCH,ccDstID,ccDstCH
			
			Circuit.cCore.Connect(ccSrcID,ccSrcCH, metaSrc, ccDstID, ccDstCH,metaDst)

			#print 'PY: connection done!'

	# Disconnects the input channels listed in the arguments. Each channel must be given as
	# a string in the format "circuit.channel".
	#
	# @param *args Input channels given as list of strings of format: "circuit.channel"
	#
	# \b Example:
	# \code{.py}
	# machine.Disconnect('waver.amp')
	# machine.Disconnect('adder.in1', 'adder.in2')
	# \endcode
	#
	def Disconnect(self, *args):

		#print "disconnecting: "
		for tag in args:

			if self._IsGlobal(tag):
				target = self._GetMetaChannel(tag, ChannelType.Output)
			else:
				target = self._GetInternalChannel(tag, ChannelType.Input)
			#print "  - "+ target.name
			target.Disconnect()

	
	## \brief Set the value of an input channel.
	# Immediately sets the value of an input channel.
	#
	# @param channel Tag of the channel to set as a 'circuit.channel' string.
	# @param value Value to be assigned.
	#
	# \b Example:
	# \code{.py}
	# machine.SetInput(channel='waver.freq', value=10)
	# \endcode
	#
	def SetInput(self, channel=None, value=None):
		
		ch = self.GetChannel(channel)
		ch.Set(value)
		circ = ch.owner
		
		key = ch.name
		
		if ch.isInput == True:
			idx = circ.I.keys().index(key) #find the position of the key
		else:
			idx = circ.O.keys().index(key)
		print "PY: setinput "+circ.name+"."+key+": "+str(value),circ.cCoreID,idx
		Circuit.cCore.SetInput(circ.cCoreID, idx, c_double(value))
		
		#print tag,val,ch

	## \internal
	## Initialization.
	#
	# Use this after all circuits and connections are setup.
	# Calls the initialize on each circuit... this is actually useless at the moment!
	def Initialize(self):

		for kw in self.circuits.keys():
			self.circuits[kw].Initialize()

	## \internal
	## Update cycle.
	#
	# Calls the update routine of each circuit in the setup.
	# 
	def UpdateOLD(self):

		#print 'updating machine ' +self.name

		for key in self.O.keys(): self.O[key].Push()

		# pass the global inputs to metainput
		for key in self.I.keys():
			self._MetaI[key].Set(self.I[key].value)
		#for key in self.I.keys():
		#	self._MetaI[key].Set(self.I[key].value)

		for kw in self.circuits.keys():
			
			if(self.circuits[kw].enabled):
				self.circuits[kw].Update()
				if self.circuits[kw].pushed: #push if needed
					self.circuits[kw].Push()

		self._idt += 1
		self._MetaO['time'].Set(self.time)
		self.O['time'].Set(self.time)
		#print 'before post' + str(self.O['time'].value)

		self._PostUpdate()

		#print 'after post' + str(self.O['time'].value)

	def Update(self):
		
		Circuit.cCore.Update(1)
		
		


	## \internal
	## Post Update cycle.
	#
	# Called after the Update is finished, to push all buffers.
	def _PostUpdate(self):

		# pass the metaoutput value to the global output
		for key in self._MetaO.keys():
			self.O[key].value = self._MetaO[key].value
			self._MetaO[key].Push()

		#print 'in post 1' + str(self.O['time'].value)

		#push the output in the global output if pushed
		if self.pushed:
			for key in self._MetaO.keys(): self.O[key].Push()

		#print 'in post 2' + str(self.O['time'].value)

		for kw in self.circuits.keys():
			if(self.circuits[kw].enabled):
				self.circuits[kw].Push()


	## Integrate the machine.
	#
	# Calls the update routine of each circuit in the setup for a given amount of time.
	# 
	def Wait(self, dtime):
		
		Circuit.cCore.Update(c_int(int(math.floor(dtime/self.dt))))
	
	## Integrate the machine.
	#
	# Calls the update routine of each circuit in the setup for a given amount of steps.
	# 
	def WaitSteps(self, nsteps):

		Circuit.cCore.Update(c_int(nsteps))
		
	def Wait2(self, dtime):
		
		for i in xrange(int(math.floor(dtime/self.dt))):
			Circuit.cCore.Update(1)
	
	def WaitPY(self, dtime):
		
		i = 0
		imax = int(math.floor(dtime/self.dt))
		while i < imax:
			self.UpdateOLD()
			i += 1
			
	def WaitPY2(self, dtime):
		
		for i in xrange(int(math.floor(dtime/self.dt))):
			self.UpdateOLD()
	




