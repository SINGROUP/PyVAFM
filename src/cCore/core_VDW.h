#ifndef coreVDW
#define coreVDW

int Add_VDW(int owner, double gamma, double hamaker, double radius, double offset);
void VDW( circuit *c );

int Add_VDWtorn(int owner, double A1, double A2, double A3, double A4, double A5,double tipoffset );
void VDWtorn( circuit *c );


#endif
