#ifndef CORESCANNER
#define CORESCANNER

int Scanner( int owner);
void Scanner_DoIdle( circuit *c );
int Scanner_Move (int index, double x,double y, double z, double v);
void Scanner_DoMove( circuit *c );
int Scanner_Place (int index, double x,double y, double z);
void Scanner_DoPlace( circuit *c );
int Scanner_MoveTo (int index, double x,double y, double z, double v);
void Scanner_DoMoveTo( circuit *c );
int Scanner_Scan (int index, double x,double y, double z, double v, int points);
void Scanner_DoScan( circuit *c );

void Scanner_DoMove_RecordF( circuit *c );


#endif
