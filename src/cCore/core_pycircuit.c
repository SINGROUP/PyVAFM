/**********************************************************
Python circuits interface
*********************************************************/
#include <Python.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREPY
#include "core_pycircuit.h"
#endif


int Add_PYCircuit(int* owner, PyObject* self, void (*pyupd)(), int nI, int nO ) {
	
	
    circuit c = NewCircuit();
    c.nI = nI;
    c.nO = nO;
    
    c.plen = 3;
    c.params = (double*)calloc(c.plen,sizeof(double));
	
    //c.vplen = 2;
    //c.vpparams = (void**)malloc(c.vplen*sizeof(PyObject*));
    //c.vpparams[0] = self; //reference to the python object
    
    c.pyupdater = pyupd;
    //printf("PyC init 1 %ld...\n",(c.pyupdater));
    //int* (update)(void) = updfun;
    //c.vpparams[1] = updfun; //reference to its update function
    //void (*updatef)(circuit*);
	
    c.updatef = PYUpdate;
    
    //printf("PyC init 1 %ld...\n",(PyObject*)(c.vpparams[0]));
    //printf("PyC init 1 %ld...\n",(PyObject*)(c.vpparams[1]));
    
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added PYCircuit\n");
    return index;
}

void PYUpdate(circuit* c) {
	
    //printf("cCore: PYCircuit update: %ld...\n",c->pyupdater);
    
    c->pyupdater();
    //printf("cCore: PYCircuit update returned: %d\n",a);
    
    
    /*
    PyObject *func, *res, *test;
    printf("PyC update...\n");
    printf("PyC update 1 %ld...\n",(PyObject*)(c->vpparams[0]));
    //function getAddress of python object
    //func = PyObject_GetAttrString((PyObject*)(c->vpparams[0]), "Update");
    //printf("PyC update 2 %ld...\n",func);
    
    PyObject_CallMethod((PyObject*)(c->vpparams[0]), "ASD", "()");
    //PyObject_CallFunction(func,NULL);
    printf("PyC update 3...\n");
    */
	
}
