/**********************************************************
Signal generators circuits definitions.
 *********************************************************/
#include <math.h>


#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESIGNALS
#include "core_signals.h"
#define ONEoverTWOPI 0.159154943

#endif

/*************************************
    in[0]: freq
    in[1]: amp
    in[2]: phi
    in[3]: offset
    params[0]: phase
    out[0]: sin
    out[1]: cos
    out[2]: saw
 * **********************************/
int Add_waver(int owner) {
    
    circuit c = NewCircuit();
    
    c.nI = 4;
    c.nO = 3;
    
    
    c.plen = 1;
    c.params = (double*) calloc(c.plen,sizeof(double));
    
    c.updatef = waver;

    
    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c,owner);
    
    printf("cCore: added waver %d\n",index);
    
    return index;
}

void waver( circuit *c ) {


    //printf("waving...\n");

    c->params[0] += dt*GlobalSignals[c->inputs[0]];
    //c->params[0] -= floor(c->params[0]);
    c->params[0] -= (int)(c->params[0]); //this is slightly faster than floor and itz the same for positive numbers!
    //printf("waving2...\n");

    double amp = GlobalSignals[c->inputs[1]];
    double off = GlobalSignals[c->inputs[3]];
    
    
    double phase = 2*PI*(c->params[0]) + GlobalSignals[c->inputs[2]];
    //printf("waving2... %i %lf\n",c->inputs[2],GlobalSignals[c->inputs[2]]);
    GlobalBuffers[c->outputs[0]] = amp*sin(phase) + off;
    GlobalBuffers[c->outputs[1]] = amp*cos(phase) + off;
    
    phase = c->params[0] + ONEoverTWOPI*GlobalSignals[c->inputs[2]];
    phase -= (int)(phase);
    GlobalBuffers[c->outputs[2]] = amp*(phase) + off;
    //self.O['saw'].value = self.I['amp'].value * (self.machine.time *self.I["freq"].value - math.floor(self.machine.time *self.I["freq"].value)) + self.I['offset'].value
    
}

/*************************************
    in[0]: freq
    in[1]: amp
    in[2]: offset
    in[3]: duty
    params[0]: phase
    out[0]: out
 * **********************************/
int Add_square(int owner) {
    
    circuit c = NewCircuit();
    
    c.nI = 4;
    c.nO = 1;
    
    
    c.plen = 1;
    c.params = (double*) calloc(c.plen,sizeof(double));
    
    c.updatef = square;

    
    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c,owner);
    
    printf("cCore: added square wave %d\n",index);
    
    return index;
}
void square(circuit *c) {
    
    c->params[0] += dt*GlobalSignals[c->inputs[0]];
    c->params[0] -= (int)(c->params[0]);
    
    double out = (c->params[0] < GlobalSignals[c->inputs[3]])? 1.0 : 0.0;
    out = out * GlobalSignals[c->inputs[1]] - GlobalSignals[c->inputs[2]];
    GlobalBuffers[c->outputs[0]] = out;
    
    
}



