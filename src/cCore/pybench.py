
from ctypes import *
import threading
import math



testlib = cdll.LoadLibrary("./vafmcore.so")
print testlib

#calls the function in the library
testlib.INIT()

widx = testlib.Add_waver()
testlib.SetInput(widx,0,c_double(2.0))
testlib.SetInput(widx,1,c_double(1.0))



for i in range(1000):
    idx = testlib.Add_Math("opADD",2)
    testlib.Connect(0,i%2,idx,1)
    testlib.Connect(idx-1,1,idx,0)

#outidx = testlib.Add_output("log.log",2);
#testlib.output_register(outidx,-1,0)
#testlib.output_register(outidx,widx,0)
#testlib.output_register(outidx,widx,1)
#testlib.output_register(outidx,widx+1,0)

#testlib.DebugCircuit(outidx)

#testlib.Status()
t = threading.Thread(target=testlib.Update, args=[10000000])
t.daemon = True
t.start()
while t.is_alive(): # wait for the thread to exit
    t.join(.1)

#testlib.output_close(outidx);

#print testlib.SUM()

"""
Benchmark 10M steps
ADDs	time
10		1.1
20		1.6
40		2.75
100		6.2
1000	73
1000	68 with function pointers updatef
"""

