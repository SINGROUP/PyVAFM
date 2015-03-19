
  PROG = ./dftd3 

#--------------------------------------------------------------------------
 OSTYPE=LINUXL
# source /usr/qc/lf95/csh_setup nicht vergessen (Lahey compiler)
# source /usr/qc/intel/compiler70/ia32/bin/ifcvars.csh (Intel compiler)
#--------------------------------------------------------------------------

 OBJS1=dftd3.o copyc6.o 

OBJS2 = 

OBJS = $(OBJS1) $(OBJS2)
#--------------------------------------------------------------------------

ifeq ($(OSTYPE),LINUXL)
# FC = lf95 
#  FC = ifort
  FC = gfortran
# CC = gcc
# LINKER = lf95
#  LINKER = ifort
  LINKER = gfortran
  PREFLAG = -E -P
  CCFLAGS = -O -DLINUX 
	FFLAGS= -O
#  FFLAGS = -O -openmp -I$(MKLROOT)/include -mkl=parallel
#  LFLAGS = -openmp -I$(MKLROOT)/include -mkl=parallel
#  FFLAGS = -O  --chk a,e,s,u
#  FFLAGS = -O0 -g 
#  LFLAGS = -O0 -g
endif

ifeq ($(OSTYPE),LINUXI)
  PREOPTS =
  FC = ifort 
  CC = gcc
  LINKER = ifort   
  LIBS    = 
# LIBS    = -lmkl_ia32 -lmkl_lapack -lmkl_solver -lguide -lpthread -L/usr/qc/intel/mkl701/lib/32
  PREFLAG = -E -P
  CCFLAGS = -O -DLINUX
  FFLAGS = -w90 -O
endif                     

# diese ziele gibts:
.PHONY: all
.PHONY: clean
# dieses ist das erste auftretende,
# wird also beim aufruf von make erzeugt (default)
all: $(PROG)


#--------------------------------------------------------------------------
# example.f: printversion.h
# example.f haengt von printversion.h ab
# wenn sich also  printversion.h aendert, wird example.f
# (und damit auch example.o) neu gemacht.
# was auch geht:

#--------------------------------------------------------------------------
# implizite Regel zur Erzeugung von *.o aus *.F ausschalten
%.o: %.F

# aus *.F mache ein *.f
%.f: %.F
	@echo "making $@ from $<"
	$(CC) $(PREFLAG) $(PREOPTS) $< -o $@

# aus *.f mache ein *.o
%.o: %.f
	@echo "making $@ from $<"
	$(FC) $(FFLAGS) -c $< -o $@

# aus *.c mache ein *.o
%.o: %.c
	@echo "making $@ from $<"
	$(CC) $(CCFLAGS) -c $< -o $@

# linken
$(PROG): $(OBJS) 
	$(LINKER) $(OBJS) $(LIBS) -o $(PROG) $(LFLAGS)


#aufraeumen
clean:
	rm -f *.o $(PROG) 
	rm -f $(patsubst %.F, %.f, $(wildcard *.F))


