
from ctypes import *
import threading
import math



testlib = cdll.LoadLibrary("./vafmcore.so")
print testlib

#calls the function in the library
testlib.INIT()

#this waver is outside of composite
widx = testlib.Add_waver()
testlib.SetInput(widx,0,c_double(2.0))
testlib.SetInput(widx,1,c_double(1.0))
testlib.SetInput(widx,2,c_double(1.0))
testlib.SetPushed(widx,1)
#testlib.DebugCircuit(widx)

#testlib.Update(1)
#testlib.DebugCircuit(widx)

# make a composite circuit #############################################
extin1 = testlib.Add_Dummy() #returns the index of external input dummy circuit
extin2 = testlib.Add_Dummy() #returns the index of external input dummy circuit

testlib.DebugCircuit(extin1)

addidx = testlib.Add_Math("opADD",2)
testlib.DebugCircuit(addidx)

extout = testlib.Add_Dummy() #returns the index of external output dummy circuit

testlib.Connect(extin1,0,addidx,0)
testlib.Connect(extin2,0,addidx,1)
testlib.Connect(addidx,0,extout,0)
testlib.DebugCircuit(addidx)


testlib.Connect(widx,0,extin1,0)
testlib.Connect(widx,1,extin2,0)
testlib.DebugCircuit(extin1)
testlib.DebugCircuit(addidx)
testlib.SetPushed(addidx,1)

#testlib.DebugCircuit(extin1)

#testlib.DebugCircuit(widx)

#andidx = testlib.Add_Logic("opOR",2)
#addidx = testlib.Add_Math("opADD",2)
#testlib.DebugCircuit(andidx)

#testlib.Connect(widx,0,andidx,0)
#testlib.Connect(widx,1,andidx,1)

#ridx = testlib.Add_Math("opABS",1)
#testlib.Connect(widx,0,ridx,0)

#fidx = testlib.Add_SKLP(c_double(0.2), c_double(math.sqrt(2.0)*0.5), c_double(math.pi*0.5))
#testlib.Connect(ridx,0,fidx,0)

outidx = testlib.Add_output("log.log",2);
testlib.output_register(outidx,-1,0)
testlib.output_register(outidx,widx,0)
testlib.output_register(outidx,widx,1)
testlib.output_register(outidx,extin1,0)
testlib.output_register(outidx,extin2,0)
testlib.output_register(outidx,extout,0)
testlib.output_register(outidx,addidx,0)
#testlib.output_register(outidx,andidx,0)

#testlib.DebugCircuit(outidx)

#testlib.Update(10000)

#testlib.DebugCircuit(widx)

"""
for i in range(10):
    idx = testlib.Add_Math("opADD",2)
    testlib.Connect(0,i%2,idx,1)
    testlib.Connect(idx-1,1,idx,0)
"""
#outidx = testlib.Add_output("log.log",2);
#testlib.output_register(outidx,-1,0)
#testlib.output_register(outidx,widx,0)
#testlib.output_register(outidx,widx,1)
#testlib.output_register(outidx,widx+1,0)

#testlib.DebugCircuit(outidx)

#testlib.Status()
t = threading.Thread(target=testlib.Update, args=[10000])
t.daemon = True
t.start()
while t.is_alive(): # wait for the thread to exit
    t.join(.1)

#testlib.output_close(outidx);

#print testlib.SUM()




