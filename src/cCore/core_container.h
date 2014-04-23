#ifndef CORECONTAINER
#define CORECONTAINER

//int Add_SKLP( double fcut, double Q, double gain );
//void SKLP( circuit *c );


int Add_Container(int owner, int isMain);
void ContainerUpdate(circuit* c);
void ContainerUpdate_Main(circuit* c);
void DoNothing(circuit *c);

#endif
