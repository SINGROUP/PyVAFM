/**********************************************************
Circuits container definitions.
 *********************************************************/
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECONTAINER
#include "core_container.h"
#endif



int Add_Container(int owner, int isMain) {
	
	printf("cCore: adding container...\n");
	
	circuit c = NewCircuit();
	c.isContainer = 1;
	
	c.dummyin = (int*)calloc(1,sizeof(int));
	c.dummyout = (int*)calloc(1,sizeof(int));
	
	c.updatef = (isMain == 1)? ContainerUpdate_Main : ContainerUpdate;
	
	
	int index = AddToCircuits(c,owner);
	printf("cCore: added container %i (main:%i)\n",index,isMain);
	return index;
	
}

void ExternalRelay( circuit *c ) {
    GlobalSignals[c->outputs[0]] = GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[0]];
}
/***********************************************************************
 * This function creates dummy circuits representing composites external
 * channels.
 * ********************************************************************/
int Add_Dummy( int container ) {
    
    printf("cCore: adding dummy\n");
    
    circuit c = NewCircuit();
	
    c.nI = 1;
    c.nO = 1;

    c.updatef = ExternalRelay;
    
    int index = AddToCircuits(c, -1);
    
    //the output is the same as the input
    //circuits[index].outputs = circuits[index].inputs;
    
    
    printf("cCore: added dummy %i \n",index);
    return index;
    
}


int Add_ChannelToContainer(int c, int isInput) {
	
	/*
	int chindex = GlobalChannelCounter;
	GlobalChannelCounter++;
	GlobalSignals = (double*)realloc(GlobalSignals,GlobalChannelCounter*sizeof(double));
	*/
	
	//allocate a new dummy
	int dummyindex = Add_Dummy(-1); //dummy goes in no container, only in global circuits
	
	//allocate the index slot
	if(isInput == 1) {
		
		circuits[c].nI++;
		circuits[c].dummyin = (int*)realloc(circuits[c].dummyin, circuits[c].nI*sizeof(int));
		circuits[c].dummyin[circuits[c].nI-1] = dummyindex;
		
	} else {
		circuits[c].nO++;
		circuits[c].dummyout = (int*)realloc(circuits[c].dummyout, circuits[c].nO*sizeof(int));
		circuits[c].dummyout[circuits[c].nO-1] = dummyindex;
	}
	
	
	return dummyindex;
}

/*********************************************************
 * Container update function
 * ******************************************************/
void ContainerUpdate(circuit* c) {
	
	//printf("updating container with %i subcirc\n",c->nsubcircs);
		
	//relay all external inputs
	for (int i = 0; i < c->nI; i++)
	{
		//the signal of the dummy.out takes the value of the dummy.in
		GlobalSignals[circuits[c->dummyin[i]].outputs[0]] = GlobalSignals[circuits[c->dummyin[i]].inputs[0]];
		GlobalBuffers[circuits[c->dummyin[i]].outputs[0]] = GlobalSignals[circuits[c->dummyin[i]].inputs[0]];
	}
	
	//update subcircuits
	for (int i = 0; i < c->nsubcircs; i++) {
		//printf("   updating: %i\n",c->subcircuits[i]);
		circuits[c->subcircuits[i]].updatef(&(circuits[c->subcircuits[i]]));
		//push normal circuits only
		if(circuits[c->subcircuits[i]].pushed == 1 && circuits[c->subcircuits[i]].nsubcircs == 0) {
			//update signals
			//printf("   pushing %i\n",c->subcircuits[i]);
			for (int k = 0; k < circuits[c->subcircuits[i]].nO; k++) {
				GlobalSignals[circuits[c->subcircuits[i]].outputs[k]] = GlobalBuffers[circuits[c->subcircuits[i]].outputs[k]];
			}
			
		}
		//printf("   done: %i\n",c->subcircuits[i]);
	}
	
	
	//relay all external outputs
	int idx;
	for (int i = 0; i < c->nO; i++)
	{
		
		idx = circuits[c->dummyout[i]].outputs[0];
		GlobalBuffers[idx] = GlobalSignals[circuits[c->dummyout[i]].inputs[0]];
		
		//printf("container relay feed of dummy: %d %d -> %lf\n",c->dummyout[i],idx,GlobalBuffers[idx]);
		if(c->pushed == 1)
			GlobalSignals[idx] = GlobalBuffers[idx];
		
	}
	
	
	//printf("done\n");
	
	
}

void ContainerUpdate_Main(circuit* c) {
	
	//printf("updating cCore time!\n");
	//printf("updating cCore time container with %i subcirc\n",c->nsubcircs);
	//printf("container dummy for time: %d %d\n",c->dummyout[0],circuits[c->dummyout[0]].inputs[0]);
	//update time
	GlobalBuffers[circuits[c->dummyout[0]].inputs[0]] += dt;
	GlobalSignals[circuits[c->dummyout[0]].inputs[0]] += dt;
	
	ContainerUpdate(c);
	
	//printf("DONE updating cCore time!\n");
}

void DoNothing(circuit *c) {
	
}



