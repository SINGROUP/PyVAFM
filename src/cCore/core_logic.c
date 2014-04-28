/**********************************************************
Logical circuits definitions.
 *********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORELOGIC
#include "core_logic.h"
#endif


int LogicStart, LogicEnd;

void INIT_LOGIC(int* counter) {

    int i = *counter;
    LogicStart = i;

    pynames[i] = "opAND"; ufunctions[i] = opAND; i++;
    pynames[i] = "opNAND"; ufunctions[i] = opNAND; i++;
    pynames[i] = "opOR";  ufunctions[i] = opOR;  i++;
    pynames[i] = "opNOT"; ufunctions[i] = opNOT; i++;
    pynames[i] = "opXOR"; ufunctions[i] = opXOR; i++;
    pynames[i] = "opNOR"; ufunctions[i] = opNOR; i++;

    LogicEnd = i-1;
    *counter = i;

}


int Add_Logic(int owner, char* type, int ni) {
    
    circuit c = NewCircuit();

    c.nI = ni;
    c.nO = 1;

    int template = GetCircuitIndex(type);
    if(template < LogicStart || template > LogicEnd) {
        printf("cERROR! type [%s] is not a logic circuit!\n",type);
        errorflag++;
    }
    
    c.updatef = ufunctions[template];
    
    int index = AddToCircuits(c,owner);
    
    printf("Added logic [%s].\n",type);
    return index;
    
}


void opAND( circuit *c ) {

  double result = 1;
  for(int i=0; i < c->nI; i++){
    if(GlobalSignals[c->inputs[i]] <= 0) {
      result = 0;
      break;
    }
  }
  GlobalBuffers[c->outputs[0]] = result;
}

void opNAND( circuit *c ) {

  double result = 1;
  
  if(GlobalSignals[c->inputs[0]] > 0 && GlobalSignals[c->inputs[1]] > 0) {
    result = 0;
  }
  
  GlobalBuffers[c->outputs[0]] = result;
}


void opOR( circuit *c ) {

  double result = 0;
  for(int i=0; i < c->nI; i++){
    if(GlobalSignals[c->inputs[i]] > 0) {
      result = 1;
      break;
    }
  }
  GlobalBuffers[c->outputs[0]] = result;
}

void opNOT( circuit *c ) {

  double result = 1;
    if(GlobalSignals[c->inputs[0]] > 0) {
        result = 0;
    }

    GlobalBuffers[c->outputs[0]] = result;
}

void opXOR( circuit *c ) {

    double result = 0;
    double counter = 0;

    for(int i=0; i < c->nI; i++){
    
        if(GlobalSignals[c->inputs[i]] > 0) {
            result = 1;
            counter = counter +1;
        }
    }

    if (counter >= 2){
        result = 0;
    }

    GlobalBuffers[c->outputs[0]] = result;
}

void opNOR( circuit *c ) {

  double result = 1;
  for(int i=0; i < c->nI; i++){
    if(GlobalSignals[c->inputs[i]] > 0) {
      result = 0;
      break;
    }
  }

  GlobalBuffers[c->outputs[0]] = result;
}