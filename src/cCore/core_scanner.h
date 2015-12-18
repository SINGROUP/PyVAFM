#ifndef CORESCANNER
#define CORESCANNER

int Scanner( int owner);
void Scanner_DoIdle( circuit *c );
unsigned long long int  Scanner_Move (int index, double x,double y, double z, double v);
void Scanner_DoMove( circuit *c );
int Scanner_Place (int index, double x,double y, double z);
void Scanner_DoPlace( circuit *c );
unsigned long long int Scanner_MoveTo (int index, double x,double y, double z, double v);
void Scanner_DoMoveTo( circuit *c );
int Scanner_Scan (int index, double x,double y, double z, double v, int points);
void Scanner_DoScan( circuit *c );

unsigned long long int SinScan(int index, double freq, double amp,int cycles);
void DoSinScan(circuit *c);


unsigned long long int Scanner_Move_Record(int index, double x, double y, double z, double v, int npts);
void Scanner_DoMove_RecordF( circuit *c );

int CoordTransform(int owner, double Lvxx,double Lvxy,double Lvxz,   double Lvyx,double Lvyy,double Lvyz,   double Lvzx,double Lvzy,double Lvzz);
void RunCoordTrans( circuit *c ) ;



#endif
