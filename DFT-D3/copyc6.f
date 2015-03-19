CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
c copy from machine generated data statements inside pars.f
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

      subroutine copyc6(fname,maxc,max_elem,c6ab,maxci,
     .                  minc6,minc6list,maxc6,maxc6list) 
      implicit none
      integer maxc,max_elem,maxci(max_elem),nlines,mima
      real*8  c6ab(max_elem,max_elem,maxc,maxc,3)
      character*(*) fname
      logical minc6,maxc6,minc6list(max_elem),maxc6list(max_elem)

      character*1  atmp 
      character*80 btmp 
      real*8  x,y,f,cn1,cn2,cmax,xx(10)
      integer iat,jat,i,n,l,j,k,il,iadr,jadr,nn,kk
      logical special
      include 'pars.f'
      c6ab=-1
      maxci=0
c read file
      kk=1
      if(minc6.or.maxc6) then   !only use values for cn=minimum
        DO i=1,94
          if (minc6list(i))then
            c6ab(i,:,1,:,2)=10000000.0
            c6ab(:,i,:,1,3)=10000000.0
          endif
        enddo


      do nn=1,nlines
      special=.false.
       iat=int(pars(kk+1))
       jat=int(pars(kk+2))
       call limit(iat,jat,iadr,jadr)

       if (minc6list(iat)) then  !only CN=minimum for iat
         special=.true.
         maxci(iat)=1
         maxci(jat)=max(maxci(jat),jadr)

         if(pars(kk+3).le.c6ab(iat,jat,1,jadr,2)) then

           c6ab(iat,jat,1,jadr,1)=pars(kk)  
           c6ab(iat,jat,1,jadr,2)=pars(kk+3)
           c6ab(iat,jat,1,jadr,3)=pars(kk+4)

           c6ab(jat,iat,jadr,1,1)=pars(kk) 
           c6ab(jat,iat,jadr,1,2)=pars(kk+4)
           c6ab(jat,iat,jadr,1,3)=pars(kk+3)
         endif
       endif

       if (minc6list(jat)) then  !only CN=minimum for jat
         special=.true.
         maxci(iat)=max(maxci(iat),iadr)
         maxci(jat)=1

         if(pars(kk+4).le.c6ab(iat,jat,iadr,1,3)) then

           c6ab(iat,jat,iadr,1,1)=pars(kk)  
           c6ab(iat,jat,iadr,1,2)=pars(kk+3)
           c6ab(iat,jat,iadr,1,3)=pars(kk+4)

           c6ab(jat,iat,1,iadr,1)=pars(kk) 
           c6ab(jat,iat,1,iadr,2)=pars(kk+4)
           c6ab(jat,iat,1,iadr,3)=pars(kk+3)
         endif
       endif


       if (minc6list(iat).and.minc6list(jat)) then  !only CN=minimum for iat and jat
         special=.true.
         maxci(jat)=1
         maxci(iat)=1

         if(pars(kk+4).le.c6ab(iat,jat,1,1,3).and.
     .      pars(kk+3).le.c6ab(iat,jat,1,1,2)) then

           c6ab(iat,jat,1,1,1)=pars(kk)  
           c6ab(iat,jat,1,1,2)=pars(kk+3)
           c6ab(iat,jat,1,1,3)=pars(kk+4)

           c6ab(jat,iat,1,1,1)=pars(kk) 
           c6ab(jat,iat,1,1,2)=pars(kk+4)
           c6ab(jat,iat,1,1,3)=pars(kk+3)
         endif
       endif



       if (maxc6list(iat)) then !only CN=maximum for iat
         special=.true.

         maxci(iat)=1
         maxci(jat)=max(maxci(jat),jadr)

         if(pars(kk+3).ge.c6ab(iat,jat,1,jadr,2)) then

           c6ab(iat,jat,1,jadr,1)=pars(kk)  
           c6ab(iat,jat,1,jadr,2)=pars(kk+3)
           c6ab(iat,jat,1,jadr,3)=pars(kk+4)

           c6ab(jat,iat,jadr,1,1)=pars(kk) 
           c6ab(jat,iat,jadr,1,2)=pars(kk+4)
           c6ab(jat,iat,jadr,1,3)=pars(kk+3)
         endif
       endif
       if (maxc6list(jat)) then !only CN=maximum for jat
         special=.true.

         maxci(jat)=1
         maxci(iat)=max(maxci(iat),iadr)

         if(pars(kk+4).ge.c6ab(iat,jat,iadr,1,3)) then

           c6ab(iat,jat,iadr,1,1)=pars(kk)  
           c6ab(iat,jat,iadr,1,2)=pars(kk+3)
           c6ab(iat,jat,iadr,1,3)=pars(kk+4)

           c6ab(jat,iat,1,iadr,1)=pars(kk) 
           c6ab(jat,iat,1,iadr,2)=pars(kk+4)
           c6ab(jat,iat,1,iadr,3)=pars(kk+3)
         endif
       endif

       if (maxc6list(iat).and.maxc6list(jat)) then  !only CN=maximum for iat and jat
         special=.true.
         maxci(jat)=1
         maxci(iat)=1

         if(pars(kk+4).ge.c6ab(iat,jat,1,1,3).and.
     .      pars(kk+3).ge.c6ab(iat,jat,1,1,2)) then

           c6ab(iat,jat,1,1,1)=pars(kk)  
           c6ab(iat,jat,1,1,2)=pars(kk+3)
           c6ab(iat,jat,1,1,3)=pars(kk+4)

           c6ab(jat,iat,1,1,1)=pars(kk) 
           c6ab(jat,iat,1,1,2)=pars(kk+4)
           c6ab(jat,iat,1,1,3)=pars(kk+3)
         endif
       endif

       if (minc6list(iat).and.maxc6list(jat)) then  !only CN=minimum for iat 
         special=.true.                            !and CN=maximum jat
         maxci(jat)=1
         maxci(iat)=1

         if(pars(kk+4).ge.c6ab(iat,jat,1,1,3).and.
     .      pars(kk+3).le.c6ab(iat,jat,1,1,2)) then

           c6ab(iat,jat,1,1,1)=pars(kk)  
           c6ab(iat,jat,1,1,2)=pars(kk+3)
           c6ab(iat,jat,1,1,3)=pars(kk+4)

           c6ab(jat,iat,1,1,1)=pars(kk) 
           c6ab(jat,iat,1,1,2)=pars(kk+4)
           c6ab(jat,iat,1,1,3)=pars(kk+3)
         endif
       endif

       if (maxc6list(iat).and.minc6list(jat)) then  !only CN=maximum for iat
         special=.true.                             !  and CN=minimum for jat
         maxci(jat)=1
         maxci(iat)=1

         if(pars(kk+4).le.c6ab(iat,jat,1,1,3).and.
     .      pars(kk+3).ge.c6ab(iat,jat,1,1,2)) then

           c6ab(iat,jat,1,1,1)=pars(kk)  
           c6ab(iat,jat,1,1,2)=pars(kk+3)
           c6ab(iat,jat,1,1,3)=pars(kk+4)

           c6ab(jat,iat,1,1,1)=pars(kk) 
           c6ab(jat,iat,1,1,2)=pars(kk+4)
           c6ab(jat,iat,1,1,3)=pars(kk+3)
         endif
       endif

       if (.not.special) then

         maxci(iat)=max(maxci(iat),iadr)
         maxci(jat)=max(maxci(jat),jadr)

         c6ab(iat,jat,iadr,jadr,1)=pars(kk)  
         c6ab(iat,jat,iadr,jadr,2)=pars(kk+3)
         c6ab(iat,jat,iadr,jadr,3)=pars(kk+4)

         c6ab(jat,iat,jadr,iadr,1)=pars(kk) 
         c6ab(jat,iat,jadr,iadr,2)=pars(kk+4)
         c6ab(jat,iat,jadr,iadr,3)=pars(kk+3)
       endif
       kk=(nn*5)+1
      enddo



      else !no min/max at all 
      do nn=1,nlines
       iat=int(pars(kk+1))
       jat=int(pars(kk+2))
       call limit(iat,jat,iadr,jadr)
       maxci(iat)=max(maxci(iat),iadr)
       maxci(jat)=max(maxci(jat),jadr)

       c6ab(iat,jat,iadr,jadr,1)=pars(kk)  
       c6ab(iat,jat,iadr,jadr,2)=pars(kk+3)
       c6ab(iat,jat,iadr,jadr,3)=pars(kk+4)

       c6ab(jat,iat,jadr,iadr,1)=pars(kk) 
       c6ab(jat,iat,jadr,iadr,2)=pars(kk+4)
       c6ab(jat,iat,jadr,iadr,3)=pars(kk+3)
       kk=(nn*5)+1
      enddo
      endif
      end subroutine copyc6
