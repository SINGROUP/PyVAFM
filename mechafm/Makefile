## Parameters and files
EXEC = mechafm-mpi
CFILES = mechafm-mpi.c

## Compiler
# On local machine
CC = /usr/bin/mpicc

## Local directory tree ##
INCDIR = .

## Flag settings ##
OPTIM    = -O3 -fomit-frame-pointer
MATHFLAG = -lm
WARNFLAG = -Wshadow
FULLFLAG = $(OPTIM) $(WARNFLAG) -I$(INCDIR)

## Parallel thingies
MPI_INC  = -I/usr/lib/openmpi/include/
MPI_PATH = -L/usr/lib/openmpi/lib/
MPI_LIB  = 

## Reshuffle all files ##
FILES = $(CFILES)

############################################
## Actual make code below (do not change) ##
############################################

## Make the executable (MPI) ##
$(EXEC): $(FILES)
	$(CC) $(FULLFLAG) $(MPI_INC) $(MPI_PATH) $^ $(MATHFLAG) $(MPI_LIB) -o $(EXEC)
	mkdir -p bin
	mv $(EXEC) bin

## Make clean ##
clean:
	rm -rf bin/$(EXEC) *~

## Make all ##
all: $(EXEC) 