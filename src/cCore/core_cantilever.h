#ifndef CORECANTILEVER
#define CORECANTILEVER

int Add_Cantilever(int owner, double Q, double k, double M, double f0, double startingz, double cantiz);
void RunCantilever(circuit *c);

int Add_AdvancedCantilever(int owner, int numberofmodesV, int numberofmodesL);
void RunAdvancedCantilever(circuit *c);

#endif
