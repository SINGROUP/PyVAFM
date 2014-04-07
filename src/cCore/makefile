CC	= gcc
CFLAGS	= -c -w -std=c99 -fpic -O3
LFLAGS	= -w -lm -shared -fpic -O3 -o vafmcore.so

PYINC	= /usr/include/python2.7/

#CIRCUITS = core_container.o core_signals.o core_output.o core_maths.o core_logic.o  core_filters.o

all: container cantilever siggen scanner interpo outputs rsa flops maths logics filters comparison control sigproc avg vdw pyc main.o 
	$(CC) $(LFLAGS) *.o
	rm *.o
	cp vafmcore.so ../.
	cp vafmcore.so ../../examples/.
	cp vafmcore.so ../../Tutorials/.	
main.o:
	$(CC) $(CFLAGS) main.c
cantilever:
	$(CC) $(CFLAGS) core_cantilever.c
scanner:
	$(CC) $(CFLAGS) core_scanner.c
interpo:
	$(CC) $(CFLAGS) core_interpolation.c
outputs:
	$(CC) $(CFLAGS) core_output.c
rsa:
	$(CC) $(CFLAGS) core_rsa.c
maths: 
	$(CC) $(CFLAGS) core_maths.c
logics: 
	$(CC) $(CFLAGS) core_logic.c
comparison:
	$(CC) $(CFLAGS) core_comparison.c
siggen: 
	$(CC) $(CFLAGS) core_signals.c
filters: 
	$(CC) $(CFLAGS) core_filters.c
control:
	$(CC) $(CFLAGS) core_control.c
flops:
	$(CC) $(CFLAGS) core_flipflops.c
sigproc:
	$(CC) $(CFLAGS) core_signalprocessing.c
container: 
	$(CC) $(CFLAGS) core_container.c
avg: 
	$(CC) $(CFLAGS) core_avg.c
vdw:
	$(CC) $(CFLAGS) core_VDW.c	
pyc:
	$(CC) $(CFLAGS) -I$(PYINC) core_pycircuit.c

clean:
	rm -rf *.o vafmcore.so
