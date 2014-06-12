import math

TipAngle=0.28658
TipHamak=39.6e-20
TipRadius=3.9487
TipOffset=0

g2r = math.pi/180
sing = math.sin(TipAngle*g2r);
tang = math.tan(TipAngle*g2r);
cosg = math.cos(TipAngle*g2r);
cos2g= math.cos(TipAngle*g2r*2.0);


TR2 = TipRadius*TipRadius;
TRC = TipRadius*cos2g;
TRS = TipRadius*sing;
TipHamak = TipHamak* 1.0e18;

for ztip in range(100, 1000):
	ztip = ztip*0.01
	vdw = (TipHamak*TR2)*(1.0-sing)*(TRS-ztip*sing-TipRadius-ztip);
	vdw/= (6.0*(ztip*ztip)*(TipRadius+ztip-TRS)*(TipRadius+ztip-TRS));
	vdw-= (TipHamak*tang*(ztip*sing+TRS+TRC))/(6.0*cosg*(TipRadius+ztip-TRS)*(TipRadius+ztip-TRS));
	print ztip, vdw