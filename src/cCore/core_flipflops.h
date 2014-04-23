#ifndef COREFLIPFLOP
#define COREFLIPFLOP

int Add_DRFlipFLop(int owner);
void DRFlipFlop( circuit *c );

int Add_JKFlipFLop(int owner);
void JKFlipFlop( circuit *c );

int Add_DFlipFLop(int owner);
void DFlipFlop( circuit *c );

int Add_SRFlipFLop(int owner);
void SRFlipFlop( circuit *c );
#endif
