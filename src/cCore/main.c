#include <stdio.h>

//#include "circuit.c"

//#include "main.h"


/**********************************************************
The python system will just call
functions in the library that will internally setup the vafm
and run it at uberspeed.
***********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

//#include "core_maths.h"

// *** GLOBAL DEFINITIONS **********************************
double dt;
int GlobalChannelCounter = 0; //counter for channels
int GlobalCircuitCounter = 0; //counter for citcuits


int GlobalNFunctions;
void **ifunctions; //list of pointers to function: circuit initialisers
void (**ufunctions)(circuit*); //list of pointers to function: circuit updaters
char **pynames;    //list of python names for the circuits

//array containing all signals I and O
double *GlobalSignals, *GlobalBuffers; 


circuit *circuits;
circuit Machine;

int newcircuits = 1;

int errorflag = 0;

// *********************************************************
int AllocateCircuits(void);


int INIT(void) {
  
    srand(time(NULL));
    AllocateCircuits();
  
    

    printf("VAFMCORE: initialised!\n");


    /*

    //initialize some feeds (includes I and O)
    //... this can be automatized...
    GlobalSignals = (double*) calloc (20,dsize);

    //python could call these function to create 
    //circuits in the C library
    AddCircuit("opMUL",2,1);
    AddCircuit("opADD",2,1);

    circuits[1].inputs[0] = 2;
    GlobalSignals[circuits[1].inputs[1]] = 0.09;

    printf("outputs: %lf %lf\n",
     GlobalSignals[circuits[0].outputs[0]],
     GlobalSignals[circuits[1].outputs[0]]);

    Update();
    printf("outputs: %lf %lf\n",
     GlobalSignals[circuits[0].outputs[0]],
     GlobalSignals[circuits[1].outputs[0]]);

    GlobalSignals[0] = 1.3;
    GlobalSignals[1] = 2;

    Update();
    printf("outputs: %lf %lf\n",
     GlobalSignals[circuits[0].outputs[0]],
     GlobalSignals[circuits[1].outputs[0]]);

    */

    return 0;
}

int SetTimeStep(double value) {
    
    printf("cCore: setting dt: %lf \n",value);
    dt = value;
    
    return 0;
}

int AllocateCircuits() {


  GlobalNFunctions = 100; //correct this!
  ifunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  ufunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  pynames = (char**)malloc(GlobalNFunctions*sizeof(char*));
  
  
  circuits = (circuit*)calloc(1,sizeof(circuit));
  
  GlobalSignals = (double*)calloc(1,sizeof(double)); //signal 0 is the time
  GlobalBuffers = (double*)calloc(1,sizeof(double)); //signal 0 is the time
  GlobalChannelCounter = 0;

  int i=0;
  INIT_MATHS(&i);
  INIT_LOGIC(&i);
  INIT_COMPARISON(&i);
  

  return 0;
}

//deallocate resources
int QUIT() {
  
  free(pynames);
  free(ufunctions); free(ifunctions);
  

}


/***********************************************************************
 * Internal function. Allocates the channel indexers and the signals for
 * circuit c.
***********************************************************************/
int AddChannels( circuit *c ) {
  
  printf("cCore: adding channels: %i %i\n",c->nI,c->nO);
  
  if(c->nI > 0) {
    c->inputs = (int*)calloc(c->nI,sizeof(int));
    c->oinputs = (int*)calloc(c->nI,sizeof(int));
    for(int i=0;i<c->nI;i++) {
      c->inputs[i] = GlobalChannelCounter;
      c->oinputs[i] = GlobalChannelCounter;
      GlobalChannelCounter++;
    }
  }

  if(c->nO > 0) {
    c->outputs= (int*)calloc(c->nO,sizeof(int));
    for(int i=0;i<c->nO;i++) {
      c->outputs[i] = GlobalChannelCounter;
      GlobalChannelCounter++;
    }
  }
  GlobalSignals = (double*)realloc(GlobalSignals,sizeof(double)*GlobalChannelCounter);
  GlobalBuffers = (double*)realloc(GlobalBuffers,sizeof(double)*GlobalChannelCounter);

    //zeroes all the new channels
    for (int i = GlobalChannelCounter-c->nO-c->nI; i < GlobalChannelCounter; i++)
    {
        GlobalSignals[i] = 0;
        GlobalBuffers[i] = 0;
    }
    

    printf("cCore: Global signals tot: %i\n",GlobalChannelCounter);

  return 0;
}


/***********************************************************************
 * Makes a new empty circuit.
***********************************************************************/
circuit NewCircuit() {
    
    circuit c;
    c.iplen = 0;
    c.plen = 0;
    c.vplen = 0;
    //c.updatef = DummyCircuit;
    c.nsubcircs = 0;
    c.isContainer = 0;
    c.nI = 0;
    c.nO = 0;
    c.pushed = 0; //false by default
    
    return c;
}
/***********************************************************************
 * Sets the behaviour of the circuit with index cindex.
 * 0 is not pushed, 1 is pushed.
 * Python callable.
***********************************************************************/
int SetPushed(int cindex, int pushed) {
    
    circuits[cindex].pushed = pushed;
    
    return 0;
}

/***********************************************************************
 * This function makes a new slot in the global circuits list and stores the
 * new one given as argument. Returns the index of the new circuit.
 * The index of the circuit is also stored in the container's subcircuits
***********************************************************************/
int AddToCircuits(circuit c, int containerindex) {
    
    printf("cCore: allocating %i\n",GlobalCircuitCounter);
    //containers do not get inputs/outputs allocated
    if(c.isContainer == 0)
        AddChannels(&c); //allocates the signals
    
    GlobalCircuitCounter++;
    circuits = (circuit*)realloc(circuits, GlobalCircuitCounter*sizeof(circuit));
    circuits[GlobalCircuitCounter-1] = c; //add the circuit to the list
    
    int index = GlobalCircuitCounter-1;
    
    //this is true only for the main machine
    if(containerindex < 0) {
        //letz work under the assumption that circuits[0] is the main machine lol!
        
        return index;
    }
    
    //if c belongs to a container, then add it there too
    circuits[containerindex].nsubcircs++;
    if(circuits[containerindex].nsubcircs == 1) {
        
        //alloc for the first time
        circuits[containerindex].subcircuits = (int*)calloc(
            circuits[containerindex].nsubcircs, sizeof(int));
    } else {
        // else reshape
        circuits[containerindex].subcircuits = (int*)realloc(
            circuits[containerindex].subcircuits, circuits[containerindex].nsubcircs*sizeof(int));
    }
    circuits[containerindex].subcircuits[circuits[containerindex].nsubcircs-1] = index;
    
    
    return index;
}




/***********************************************************************
 * Get the index of a circuit named "type" in the template list.
***********************************************************************/
int GetCircuitIndex(char* type) {
    
    //find the function name in the list
    for(int i=0; i<GlobalNFunctions; i++) {
        if(strcmp(pynames[i],type) == 0) {
            return i;
        }
    } 
    printf("cERROR: circuit of type [%s] was not found!",type);
    return -1; //not found!
}

//create a circuit
/*int AddCircuit(char* type, int ni, int no) {

  //check if the library is initialised! TODO
  
  
  circuit c;
  MakeChannels(&c,ni,no); //make the channels
  GlobalSignals = (double*)realloc(GlobalSignals,sizeof(double)*GlobalChannelCounter);


  //allocate a new slot for circuit
  GlobalCircuitCounter++;
  circuits = (circuit*)realloc(circuits, GlobalCircuitCounter*sizeof(circuit));
  

  //find the function name in the list
  for(int i=0; i<GlobalNFunctions; i++) {
    if(strcmp(pynames[i],type) == 0) {
      
      c.update = i; //set the update function index

      break;
    }
  }
  
  //store the new circuit in the array
  circuits[GlobalCircuitCounter-1] = c;

  //return &(circuits[GlobalCircuitCounter-1]);
  printf("Added circuit: %s\n",type);

  newcircuits = 1;

  //return the index of the circuit
  return GlobalCircuitCounter-1;
}
*/

//connect function source - destination
int Connect(int c1, int out, int metaSrc, int c2, int in, int metaDst) {
  
    int *chout, *chin;


    //if the source is a metainput, 
    if(metaSrc == 1) {
        chout = &(circuits[circuits[c1].dummyin[out]].outputs[0]);
    }
    else {
        //the source is not a meta, but could be a container external...
        //if the source is a container, get the dummy out
        if(circuits[c1].isContainer == 1)
            chout = &(circuits[circuits[c1].dummyout[out]].outputs[0]);
        else
            chout = &(circuits[c1].outputs[out]); //or just a normal output
    }

    //printf("cCore Connecting: SOURCE %i\n",*chout);
    
    if(metaDst == 1) {
        chin = &(circuits[circuits[c2].dummyout[in]].inputs[0]);
    }
    else {
        //if the destination is a container, get the dummy in
        if(circuits[c2].isContainer == 1) {
            chin = &(circuits[circuits[c2].dummyin[in]].inputs[0]);
        }
        else
            chin = &(circuits[c2].inputs[in]);
    }


    //printf("cCore Connecting: DST %i\n",*chin);

    *chin = *chout;
    
    //circuits[c2].inputs[in] = circuits[c1].outputs[out];


    return 0;
}



int SetInput(int c, int inidx, double value){

    //printf("cCore: set input %i -> %lf \n",circuits[c].inputs[inidx],value);

    GlobalSignals[circuits[c].inputs[inidx]] = value;
    GlobalBuffers[circuits[c].inputs[inidx]] = value;
  
    return 0;
}
int SetContainerInput(int c, int inidx, double value){

    //printf("cCore: set input %i -> %lf \n",circuits[c].inputs[inidx],value);
    int dummy = circuits[c].dummyin[inidx];

    GlobalSignals[circuits[dummy].inputs[0]] = value;
    GlobalBuffers[circuits[dummy].inputs[0]] = value;
    GlobalSignals[circuits[dummy].outputs[0]] = value;
    GlobalBuffers[circuits[dummy].outputs[0]] = value;

    return 0;
}

double InputToPy(int cindex, int chindex) {
    printf("cCore: InputToPy reads feed: %d \n",circuits[cindex].inputs[chindex]);
    return GlobalBuffers[circuits[cindex].inputs[chindex]];
}
double ChannelToPy(int cindex, int chindex, int isInput) {
    
    int idx;
    
    if(isInput == 1) {
        //printf("cCore: ChannelToPy reads feed: %d \n",idx);
        idx = circuits[cindex].inputs[chindex];
        return GlobalSignals[idx];
        
    } else {
        //printf("cCore: ChannelToPy reads feed: %d \n",idx);
        idx = circuits[cindex].outputs[chindex];
        return GlobalBuffers[idx];
    }
    return 0.0;
}

int PyToChannel(int cindex, int chindex, int isInput, double value) {
    
    int idx;
    
    //if the circuit is not a container, do as normal
    if(circuits[cindex].isContainer == 0) {
    
        if(isInput == 1) {
            //printf("cCore: PyToChannel write feed: %d [buff/value]\n",idx);
            idx = circuits[cindex].inputs[chindex];
            GlobalBuffers[idx] = value;
            GlobalSignals[idx] = value;
        } else {
            //printf("cCore: PyToChannel write feed: %d [buff]\n",idx);
            idx = circuits[cindex].outputs[chindex];
            GlobalBuffers[idx] = value;
        }
    
    }
    else {
        //if it is a container...
        
        if(isInput == 1) { //and an input
            //printf("cCore: PyToChannel write feed: %d [buff/value]\n",idx);
            idx = circuits[circuits[cindex].dummyin[chindex]].inputs[0];
            GlobalBuffers[idx] = value;
            GlobalSignals[idx] = value;
                    }
        
    }
    
    return 0;
}


int* GetInputs(int c) {
    
    //printf("iscontainer %i\n",circuits[c].isContainer);
    
    if(circuits[c].isContainer == 1) {
        return circuits[c].dummyin;
    }
    
    return circuits[c].oinputs;
}
int* GetOutputs(int c) {
    
    //printf("iscontainer %i\n",circuits[c].isContainer);
    
    if(circuits[c].isContainer == 1) {
        //printf("returning dummyouts!\n");
        return circuits[c].dummyout;
    }
    return circuits[c].outputs;
}

int Update(unsigned long long int  steps) {
 
    for(unsigned long long int t=0; t<steps; t++) {
        
        //printf("step %d\n",t);
        circuits[0].updatef( &circuits[0] ); //this way is faster
        
        
        
/*      for(int i=0; i<GlobalCircuitCounter; i++){
            //printf("circuit[%d] function[%d]\n",i,circuits[i].update);
            //ufunctions[circuits[i].update]( &circuits[i] );
            circuits[i].updatef( &circuits[i] ); //this way is faster
            if(circuits[i].pushed == 1) {
                for (int k = 0; k < circuits[i].nO; k++) {
                    GlobalSignals[circuits[i].outputs[k]] = GlobalBuffers[circuits[i].outputs[k]];
                }
                
            }
        }
*/        
        
        //now push all feeds
        for (int i = 0; i < GlobalChannelCounter; i++)
        {
            GlobalSignals[i] = GlobalBuffers[i];
        }
        /*for(int i=0; i<GlobalCircuitCounter; i++){
            
            if(circuits[i].pushed == 1) continue;
            
            for (int k = 0; k < circuits[i].nO; k++) {
                    GlobalSignals[circuits[i].outputs[k]] = GlobalBuffers[circuits[i].outputs[k]];
                }
        }*/ //this is slower than updating all buffers

        //GlobalBuffers[0] += dt;
        //GlobalSignals[0] = GlobalBuffers[0];

    }
    //printf("steps %d\n",steps);

    return 0;
}


int Status(void) {

  
  for(int i=0; i<GlobalCircuitCounter; i++) {
    
    printf("circuit [%d]:\t%ld\n",i,circuits[i].updatef);
    
  }
  
}


int DebugCircuit(int c){

    printf("-------------------------------\n");
  printf("circuit [%i]: %i in  %i out \n",c,circuits[c].nI,circuits[c].nO);
  
  if(circuits[c].isContainer == 0) {
      
      for(int i=0; i<circuits[c].nI; i++){
        printf("  in[%i]: signal ch[%i] value[%lf] buffered[%lf]\n",i,circuits[c].inputs[i],GlobalSignals[circuits[c].inputs[i]],GlobalBuffers[circuits[c].inputs[i]]);
      }

      for(int i=0; i<circuits[c].nO; i++){
        printf(" out[%i]: signal ch[%i] value[%lf] buffered[%lf]\n",i,circuits[c].outputs[i],
            GlobalSignals[circuits[c].outputs[i]],GlobalBuffers[circuits[c].outputs[i]]);
      }
      
  } else {
      
        printf("   the circuit is a container: \n");
        for (int i = 0; i < circuits[c].nsubcircs; i++) {
            printf("  - circuit[%i]\n",circuits[c].subcircuits[i]);
        }
        printf("\n");
        printf("   external inputs: \n");
        for (int i = 0; i < circuits[c].nI; i++) {
            printf("  -- dummy ch[%i] - %i %i\n",circuits[c].dummyin[i],
                circuits[circuits[c].dummyin[i]].inputs[0],circuits[circuits[c].dummyin[i]].outputs[0]);
        }
        printf("   external outputs: \n");
        for (int i = 0; i < circuits[c].nO; i++) {
            printf("  -- dummy ch[%i] - %i %i\n",circuits[c].dummyout[i],
                circuits[circuits[c].dummyout[i]].inputs[0],circuits[circuits[c].dummyout[i]].outputs[0]);
            
        }
      
  }
  
  for(int i=0; i< circuits[c].iplen; i++){
    printf("  ip[%i]: value[%i]\n",i,circuits[c].iparams[i]);
  }


    printf("-------------------------------\n");

  return 0;
}
