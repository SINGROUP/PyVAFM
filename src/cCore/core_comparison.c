/**********************************************************
Comparison circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECOMPARISON
#include "core_comparison.h"
#endif


int CompStart, CompEnd;
void INIT_COMPARISON(int* counter) {

	int i = *counter; CompStart = i;
	pynames[i] = "GreaterOrEqual"; ufunctions[i] = GreaterOrEqual; i++;
	pynames[i] = "LessOrEqual"; ufunctions[i] = LessOrEqual; i++;
	pynames[i] = "Equal"; ufunctions[i] = Equal; i++;

	CompEnd = i-1;
	*counter = i;

}

int Add_Comparison(int owner, char* type, int ni) {
    
    circuit c = NewCircuit();

    c.nI = ni;
    c.nO = 1;

    //c.plen = 1;
    //c.params = (double*)calloc(c.plen,sizeof(double));

    int template = GetCircuitIndex(type);
    if(template < CompStart || template > CompEnd) {
        printf("cERROR! type [%s] is not a Comparison circuit!\n",type);
        errorflag++;
    }
    
    c.updatef = ufunctions[template];
    
    int index = AddToCircuits(c,owner);
    
    //printf("Added maths [%s].\n",type);
    return index;
    
}


void GreaterOrEqual( circuit *c ) {
  
  double result = 0;
  if ( GlobalSignals[c->inputs[0]] >= GlobalSignals[c->inputs[1]]){
    result = 1;
  }
  

    GlobalBuffers[c->outputs[0]] = result;
}

void LessOrEqual( circuit *c ) {
  
  double result = 0;
  if ( GlobalSignals[c->inputs[0]] <= GlobalSignals[c->inputs[1]]){
    result = 1;
  }


    GlobalBuffers[c->outputs[0]] = result;
}

void Equal( circuit *c ) {
  
    double result = 0;
    
    if ( GlobalSignals[c->inputs[0]] == GlobalSignals[c->inputs[1]]){
        result = 1;
    }
    //printf("equals: %i %i - %i %lf\n",c->inputs[0],c->inputs[1],c->outputs[0],result);
    GlobalBuffers[c->outputs[0]] = result;
}
