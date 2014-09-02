from collections import OrderedDict
from ctypes import *
import os


## \package vafmbase
# This module contains the definitions of the basic circuit and channel objects.
#

## \internal
## \brief Base Event class
#
class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount


def enum(**enums):
	return type('Enum', (), enums)
	
ChannelType = enum(Input=1, Output=2, Any=0)


## Feed object.
# This class contains the numerical value of a channel
# and its buffered value.
class Feed(object):
	
	def __init__(self, ownercircuit):
		
		self.owner = ownercircuit
		
		self._value = 0.0
		self._buff = 0.0
		self.cCoreFEED = -1
		
	#@property
	def value_get(self):
		return self._value
	
	#@value.setter
	def value_set(self,value):
		self._buff = value
		#print 'buffering value '+str(value)
		
	value = property(value_get, value_set)
	
	def Push(self):
		
		#print 'pushing '+str(self._buff)+' old('+str(self._value)+")"
		self._value = self._buff;
		
	def PushValue(self, value):
		self._value = value
		self._buff = value
	
	def __str__ (self):
		return str(self._value)  #+ "("+str(self._buff)+")"

class Channel(object):
	
	def __init__(self, name, owner, isInput):
		
		self.name = name
		self.owner = owner
		self.signal = Feed(owner)
		self.isInput = isInput
		self.cisInput = 0;
		if isInput == True:
			self.cisInput = 1
		
		#self.cCoreID #index of channel in the circuit.inputs[] of cCore
		self.cCoreCHID = 0
	
	#@property
	def value_get(self):
		#return self.signal.value
		return Circuit.cCore.ChannelToPy(self.owner.cCoreID, self.cCoreCHID, self.cisInput)
	#@value.setter
	def value_set(self,value):
		
		#self.signal.value = value
		#print "setting channel: ",self.owner.cCoreID, self.cCoreCHID,self.cisInput,c_double(value)
		Circuit.cCore.PyToChannel(self.owner.cCoreID, self.cCoreCHID, self.cisInput,c_double(value))
		
		#if(self.signal.owner == self.owner):
		#	self.Push()
		
		#print 'setting value '+str(value)
		
	value = property(value_get, value_set);
	
	def Push(self):
		self.signal.Push()
	
	def Set(self, newvalue):
		#self.signal.PushValue(value)
		self.value = newvalue


	## Renew the Feed object so that it is disconnected from everything.
	def Disconnect(self):
		self.signal = Feed(self.owner)

	def __str__(self):
		return self.owner.name+"."+self.name+" = "+str(self.signal)
		


## \brief Abstract circuit class.
#
#
class Circuit(object):

	#__metaclass__ = abc.ABCMeta;
	cCoreINIT = False
	cCore = None
	#cGetInput = None
	
	
	##\internal
	## Common contructor for all circuits.
	#
	# @param machine Reference to the virtual machine.
	# @param name Name of this instance.
	def __init__(self, machine, name):
		
		#print "PY: initing Circuit"
		
		## Name of the circuit.
		self.name = name
		
		## if it is working...
		self.enabled = True
		
		## Reference to the virtual machine to which this circuit belongs.
		self.machine = machine
		
		## Push output buffer at the end of Update.
		#
		# If the circuit is pushed, all the output channels will
		# expose the computed value right after the Update routine.
		self.pushed = False
		
		## Dictionary of input channels
		self.I = OrderedDict()
		
		self.cCoreI = None
		
		## Dictionary of output channels
		self.O = OrderedDict()
		
		self.cCoreO = None
		
		## index of circuit in cCore
		self.cCoreID = -1
		
		#init the cCore if itz the first time
		if(Circuit.cCoreINIT == False):
			print 'Initializing the cCore...'
			##Circuit.cCore = cdll.LoadLibrary("./vafmcore.so")
			current_dir = os.path.dirname(os.path.realpath(__file__))
			Circuit.cCore = cdll.LoadLibrary(current_dir + "/vafmcore.so")

			Circuit.cCore.INIT()
			Circuit.cCore.ChannelToPy.restype = c_double
			
			
			Circuit.cCoreINIT = True
		
	
	##\internal
	## Default input channels initialisation.
	#
	# Use the keyward arguments **kwargs to set the initial value
	# of input channels. 
	# @param **kwargs Keyworded arguments for circuit initialisation.
	def SetInputs(self, **kwargs):
		
		print 'PY: circuit '+self.name+'('+self.__class__.__name__+') created.'
		
		# setup the cCore ID for the channels
		for ch in self.I.keys():
			idx = self.I.keys().index(ch)
			self.I[ch].cCoreCHID = idx
			#print "PY: input "+ch+" ID:" +str(idx)
		for ch in self.O.keys():
			idx = self.O.keys().index(ch)
			self.O[ch].cCoreCHID = idx
			#print "PY: output "+ch+" ID:" +str(idx)
			
		#self.SetCCoreChannels()
		self.SetInputs_fromKeys(**kwargs)
		
		
		if 'pushed' in kwargs.keys():
			self.pushed = bool(kwargs['pushed'])
			if self.pushed:
				Circuit.cCore.SetPushed(self.cCoreID, 1);
			
		print 'PY: circuit '+self.name+'('+self.__class__.__name__+') initiated.'
	
	def SetInputs_fromKeys(self, **kwargs):
		
		for key in kwargs.keys():
			
			if key in self.I.keys():
				
				
				self.I[key].Set(kwargs[key]) #deprecated... sets the value in python!
				
				idx = self.I.keys().index(key) #find the position of the key
				print "PY: "+key+" is an input channel, calling cCore:",idx,c_double(kwargs[key])
				
				Circuit.cCore.SetInput(self.cCoreID, idx, c_double(kwargs[key]))
				
				
				print "   input "+key+" -> "+str(kwargs[key])
				
			else:
				#print the init parameter even if not an input flag
				print " ??" + key + " " + str(kwargs[key])
				pass

	
	##\internal
	## Get the feed indexes from the cCore
	#
	#
	def SetCCoreChannels(self):
		
		print 'PY: setccorechannels...'
		
		getins = Circuit.cCore.GetInputs
		getins.restype = POINTER(c_int)
		getouts = Circuit.cCore.GetOutputs
		getouts.restype = POINTER(c_int)
		
		
		# get the indexes of input(original) channels
		if len(self.I) > 0:
			self.cCoreI = getins(self.cCoreID)
			#print 'cCoreI ',self.cCoreI,len(self.I)
		
			for i in range(len(self.I)):
				#print i,self.cCoreI[i]
				self.I.values()[i].signal.cCoreFEED = self.cCoreI[i]
		
		# get the indexes of output channels
		if len(self.O) > 0:
			self.cCoreO = getouts(self.cCoreID)
			#print 'cCoreO ',self.cCoreO, len(self.O)
			
			for i in range(len(self.O)):
				#print i,self.cCoreO[i]
				self.O.values()[i].signal.cCoreFEED = self.cCoreO[i]
	
	##\internal
	## Create an input channel with the given name.
	# @param name Name of the new input channel.
	def AddInput(self, name):
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in circuit "+ str(self))
		
		self.I[name] = Channel(name,self,True)
	
	##\internal
	## Create an output channel with the given name.
	# @param name Name of the new output channel.
	def AddOutput(self, name):
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in circuit "+ str(self))
		self.O[name] = Channel(name,self,False)
	
	##\internal
	## Find a channel by name.
	# @param chname Name of the channel to find.
	# @return Reference to the channel.
	def GetChannel(self, chname):
		
		isout = chname in self.O.keys()
		isin = chname in self.I.keys()
		
		if not( isout or isin ):
			raise NameError( "Circuit.GetChannel error: channel "+chname+" not found." )
		
		if isout:
			return self.O[chname];
		if isin:
			return self.I[chname];
	##\internal
	## Find a channel by name.
	# @param chname Name of the channel to find.
	# @return Reference to the channel.
	def GetOutputChannel(self, chname):
		
		isout = chname in self.O.keys()
		if not( isout or isin ):
			raise NameError( "Circuit.GetOutputChannel error: channel "+chname+" not found." )
		
		if isout:
			return self.O[chname];
		
	
	##\internal
	## Push the buffered value for all output channels.
	def Push(self):
		for kw in self.O.keys():
			self.O[kw].Push()


	#def AddEvent(self, eventname, function):
	
	def __str__( self ):
		return "["+self.__class__.__name__+"]"+self.name+"  cCoreID: "+str(self.cCoreID)

	##\internal
	def Initialize (self):
		raise NotImplementedError( "Should have implemented this" )
	
	##\internal
	def Update (self):
		raise NotImplementedError( "Should have implemented this" )
