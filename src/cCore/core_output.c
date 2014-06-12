/**********************************************************
Output circuits definitions.
 *********************************************************/
#include <stdio.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREOUTPUT
#include "core_output.h"
#endif



int Add_output(int owner, char* filename, int dump) {

    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 0;

    c.iplen = 4;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = dump;
    c.iparams[1] = 0; //step counter
    c.iparams[2] = 0; //number of channels to print
    c.iparams[3] = 1; // 0|1 stop|start

    c.vplen = 2;
    c.vpparams = (void**)malloc(sizeof(FILE*));//one element
    c.vpparams[0] = (void*)fopen(filename, "w");
    c.vpparams[1] = (int*)calloc(3,sizeof(int));//channels info
    

    c.updatef = output;

    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c, owner);

    printf("Added output %i.\n",index);
    return index;
    
}

int output_start(int c) {
    printf("cCore: output start\n");
    circuits[c].iparams[3] = 1;
    circuits[c].iparams[1] = 0;
    return 0;
}
int output_stop(int c) {
    printf("cCore: output stop\n");
    circuits[c].iparams[3] = 0;
    return 0;
}


int output_register(int outer, int cindex, int chindex, int isInput) {

    circuits[outer].iparams[2]++; //increment the number of registered channels
    //circuits[outer].iplen+=3;
    //circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
     //   circuits[outer].iplen*sizeof(int));
    circuits[outer].vpparams[1] = (int*)realloc(circuits[outer].vpparams[1],
        3*circuits[outer].iparams[2]*sizeof(int));
    //printf("reallocating to size: %d\n",(2+circuits[outer].iparams[1]));
    
    int* regs = (int*)circuits[outer].vpparams[1];
    int reglen = 3*circuits[outer].iparams[2];
    
    circuit *owner = &(circuits[cindex]);
    if(owner->isContainer == 1) {
        
        int dummy = (isInput==1)? owner->dummyin[chindex] : owner->dummyout[chindex];
        //circuits[outer].iparams[circuits[outer].iplen-3] = dummy;
        regs[reglen-3] = dummy;
        //circuits[outer].iparams[circuits[outer].iplen-2] = 0;
        regs[reglen-2] = 0;
        //circuits[outer].iparams[circuits[outer].iplen-1] = isInput;
        regs[reglen-1] = isInput;
        
    }
    else {
        //circuit ID
        //circuits[outer].iparams[circuits[outer].iplen-3] = cindex;
        regs[reglen-3] = cindex;
        //circuits[outer].iparams[circuits[outer].iplen-2] = chindex;
        regs[reglen-2] = chindex;
        //circuits[outer].iparams[circuits[outer].iplen-1] = isInput;
        regs[reglen-1] = isInput;
    }
    
    //printf("cCore: registering done\n");
    
    return 0;
}

int output_register_feedasd(int outer, int feedid) {

    circuits[outer].iparams[2]++;
    circuits[outer].iplen++;
    circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
            circuits[outer].iplen*sizeof(int));

    circuits[outer].iparams[circuits[outer].iplen-1] = feedid;
    
    return 0;
}

void output_dump( int index ) {
    
    //circuits[index].updatef(&(circuits[index]));
    output_printout( &(circuits[index]) );
}
void output_dumpmessage( int index, char* message ) {
    
    //circuits[index].updatef(&(circuits[index]));
    fprintf(circuits[index].vpparams[0], "%s\n",message);
    fflush(circuits[index].vpparams[0]);
}

/*void output_printout( circuit *c ) {
    
    for(int i=3; i < c->iplen; i++){
        
        //printf("%lf ",GlobalSignals[c->iparams[i]]);
        fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[c->iparams[i]]);
        
    }
    //printf("\n");
    fprintf((c->vpparams[0]), "\n");
}*/
void output_printout( circuit *c ) {
    
    int* regs = (int*)c->vpparams[1];
    
    for(int i=0; i < c->iparams[2]; i++){
        
        //printf("%lf ",GlobalSignals[regs[3*i]]);
        int feedidx;
        if(regs[3*i+2] == 1) 
            feedidx = circuits[regs[3*i]].inputs[regs[3*i+1]];
        else
            feedidx = circuits[regs[3*i]].outputs[regs[3*i+1]];
        
        fprintf((c->vpparams[0]), "%e ", GlobalSignals[feedidx]);
        
    }
    //printf("\n");
    fprintf((c->vpparams[0]), "\n");
}

void output_printout_old( circuit *c ) {
    
    int* regs = (int*)c->vpparams[1];
    
    for(int i=0; i < c->iplen; i++){
        
        //printf("%lf ",GlobalSignals[c->iparams[i]]);
        printf("%lf ",GlobalSignals[regs[3*i]]);
        int feedidx;
        if(c->iparams[i+2] == 1) 
            feedidx = circuits[c->iparams[i]].inputs[c->iparams[i+1]];
        else
            feedidx = circuits[c->iparams[i]].outputs[c->iparams[i+1]];
        
        fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[feedidx]);
        
    }
    printf("\n");
    fprintf((c->vpparams[0]), "\n");
}

int output_close(int outer) {
  
  fclose(circuits[outer].vpparams[0]);
  
  return 0;
}

void output( circuit *c ) {

    //printf("update output...\n");

    if(c->iparams[3] == 0) {
        return;
    }

    if(c->iparams[0] <= 0) {
        //printf("asd!\n");
        if(GlobalSignals[c->inputs[0]] > 0) {
            output_printout(c); //do the print out
        }
        
        return;
    }
    
    c->iparams[1]++;
    
    if(c->iparams[1] >= c->iparams[0]) {
        //printf("asd!\n");
        output_printout(c); //do the print out
        c->iparams[1] = 0;
    
    }

}


