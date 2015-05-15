/**********************************************************
Arithmetic circuits definitions.
 *********************************************************/
#include <math.h>
#include <stdlib.h>
#include <time.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREMATHS
#include "core_maths.h"
#endif


int MathStart, MathEnd;
void INIT_MATHS(int* counter) {

    int i = *counter; MathStart = i;
    pynames[i] = "opADD"; ufunctions[i] = opADD; i++;
    pynames[i] = "opSUB"; ufunctions[i] = opSUB; i++;
    pynames[i] = "opMUL"; ufunctions[i] = opMUL; i++;
    pynames[i] = "opDIV"; ufunctions[i] = opDIV; i++;
    pynames[i] = "opABS"; ufunctions[i] = opABS; i++;
    pynames[i] = "opPOW"; ufunctions[i] = opPOW; i++;
    pynames[i] = "opLINC"; ufunctions[i] = opPOW; i++;
    pynames[i] = "opSIN"; ufunctions[i] = opSIN; i++;
    pynames[i] = "opCOS"; ufunctions[i] = opCOS; i++;

    MathEnd = i-1;
    *counter = i;

}

int Add_Math(int owner, char* type, int ni) {
    
    circuit c = NewCircuit();

    c.nI = ni;
    c.nO = 1;

    //c.plen = 1;
    //c.params = (double*)calloc(c.plen,sizeof(double));

    int template = GetCircuitIndex(type);
    if(template < MathStart || template > MathEnd) {
        printf("cERROR! type [%s] is not a maths circuit!\n",type);
        errorflag++;
    }
    
    //c.update = template;
    c.updatef = ufunctions[template];
    
    int index = AddToCircuits(c,owner);
    
    //printf("Added maths [%s].\n",type);
    return index;
    
}


void opADD( circuit *c ) {
  
    double result = 0;
    for(int i=0; i < c->nI; i++){
        result += GlobalSignals[c->inputs[i]];
        
    }

    GlobalBuffers[c->outputs[0]] = result;
    
}

void opSUB( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]-GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opMUL( circuit *c ) {
  double result = 1;
  for (int i=0; i<c->nI; i++){

  result *= GlobalSignals[c->inputs[i]];

}
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opDIV( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]/GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opABS( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = fabs(GlobalSignals[c->inputs[0]]);
 
}

void opPOW( circuit *c ) {

  double result = pow(GlobalSignals[c->inputs[0]],GlobalSignals[c->inputs[1]]);
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opLINC( circuit *c ) {

    double result = 0;
    
    for(int i=0; i < c->nI; i+=2) {
        result += GlobalSignals[c->inputs[i]]*GlobalSignals[c->inputs[i+1]];
    }
    
    GlobalBuffers[c->outputs[0]] = result;
 
}

void opSIN( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = sin(GlobalSignals[c->inputs[0]]);
 
}

void opCOS( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = cos(GlobalSignals[c->inputs[0]]);
 
}


int Add_Perlin(int owner, double amp, double p, int oct, double period) {
    
    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 1;

    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0] = amp;
    c.params[1] = p;

    
    c.iplen = 3;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = oct;
    c.iparams[1] = (int)floor(period/dt); //duration
    c.iparams[2] = 0;
    
    c.vplen = oct;
    c.vpparams = (double**)malloc(c.vplen*sizeof(double*));
    //each pointer points to an array for the octave
    int len = 1;
    for (int i = 0; i < oct; i++) {
        double* octave = (double*)calloc(len+1,sizeof(double));
        c.vpparams[i] = octave;
        
        for (int j = 0; j < len+1; j++) {
            
            octave[j] = (2*(rand()/(double)RAND_MAX)-1);
            printf("cCore: %i %i %lf\n",i,j,((double*)c.vpparams[i])[j]);
        }
        
        len *=2;
    }
    
    c.updatef = perlin;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: Added perlin noise \n");
    return index;
    
}

void perlin_repopulate(void** array, int oct) {

    int len = 1;
    for (int i = 0; i < oct; i++) {
        
        double* w = (double*)array[i];
        w[0] = w[len]; //copy the last value to make the noise smooth
        
        for (int j = 1; j < len+1; j++) {
            w[j] = (2*(rand()/(double)RAND_MAX)-1);
            //printf("cCore: %i %i %lf\n",i,j,((double*)c.vpparams[i])[j]);
        }
        len *=2;
    }
    
}

void perlin(circuit* c) {
    
    c->iparams[2]++;
    if(c->iparams[2] >= c->iparams[1]) {
        c->iparams[2] = 0;
        //reinit
        perlin_repopulate(c->vpparams, c->iparams[0]);
    }
        
    double t = ((double)c->iparams[2]/c->iparams[1]);
    double tin, result = 0, *w, amp = c->params[0];
    int idx;
    
    int len = 1;
    for (int i = 0; i < c->iparams[0]; i++) { //loop over octaves
        
        w = c->vpparams[i];
        
        idx = (int)floor(t*len);
        tin = (t-(double)idx/len)*len;
        
        //lin interp
        result += (tin*w[idx+1] + (1.0-tin) * w[idx])*amp;
        //cos interp
        //tin = (1 - cos(tin * 3.1415927)) * 0.5;
        //result += w[idx]*(1-tin) + w[idx+1]*tin;
        
        //printf("t %lf  oct %i -> %i = %lf \n",t,i, idx,tin);
        
        len *= 2;
        amp *= c->params[1];
    }
    
    GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[0]] + result;
    //printf("t %lf \n",t);
    
}







int Add_ComplexMagAndPhase(int owner) {
    circuit c = NewCircuit();

    c.nI = 2;
    c.nO = 2;

    c.updatef = ComplexMagAndPhase;

    int index = AddToCircuits(c,owner);
    printf("cCore: Added Complex Mag And Phase \n");
    return index;
    
}


void ComplexMagAndPhase(circuit* c) {
    double real = GlobalSignals[c->inputs[0]];
    double img  = GlobalSignals[c->inputs[1]];


    GlobalBuffers[c->outputs[0]] = sqrt(real*real + img*img);

    double phase = atan(img/real);

    if (real<0 && img >=0){phase = phase + 3.14159265359;}
    if (real<0 && img <0){phase = phase - 3.14159265359;}
    if (real==0 && img <0){phase = -3.14159265359/2;}
    if (real==0 && img >0){phase =3.14159265359/2;}

    GlobalBuffers[c->outputs[1]] = phase;
}


/*
void opSUB( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]-GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opMUL( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]*GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opDIV( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]/GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
inline void opABS( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = fabs(GlobalSignals[c->inputs[0]]);
 
}

void opPOW( circuit *c ) {

  double result = pow(GlobalSignals[c->inputs[0]],GlobalSignals[c->inputs[1]]);
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opLINC( circuit *c ) {

    double result = 0;
    
    for(int i=0; i < c->nI; i+=2) {
        result += GlobalSignals[c->inputs[i]]*GlobalSignals[c->inputs[i+1]];
    }   
    
    GlobalBuffers[c->outputs[0]] = result;
 
}
*/

