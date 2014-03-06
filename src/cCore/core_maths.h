#ifndef COREMATHS
#define COREMATHS

void opADD( circuit *c );
void opSUB( circuit *c );
void opMUL( circuit *c );
void opDIV( circuit *c );
void opABS( circuit *c );
void opPOW( circuit *c );
void opLINC( circuit *c );
void opSIN( circuit *c );
void opCOS( circuit *c );


void perlin( circuit* c );
void perlin_repopulate(void** array, int oct);

#endif
