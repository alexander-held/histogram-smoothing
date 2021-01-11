#include "TMath.h"

void print_results(int nbins, double *xx) {
   for (int i=0; i<nbins; i++) {
         std::cout << xx[i] << "   ";
      }
   std::cout << std::endl;
}

// taken from ROOT https://root.cern.ch/doc/master/TH1_8cxx_source.html#l06723
void SmoothArray(int nbins, double *xx)
{
   if (nbins < 3 ) {
       std::cout << "Need at least 3 points for smoothing, nbins = " << nbins << std::endl;
       return;
   }

   int ii;
   double hh[6] = {0,0,0,0,0,0};

   std::vector<double> yy(nbins);
   std::vector<double> zz(nbins);
   std::vector<double> rr(nbins);

   // first copy original data into temp array
   std::copy(xx, xx+nbins, zz.begin() );

   for (int noent = 0; noent < 2; ++noent) { // run algorithm two times

      //  do 353 i.e. running median 3, 5, and 3 in a single loop
      for  (int kk = 0; kk < 3; kk++)  {
         std::copy(zz.begin(), zz.end(), yy.begin());
         int medianType = (kk != 1)  ?  3 : 5;
         int ifirst      = (kk != 1 ) ?  1 : 2;
         int ilast       = (kk != 1 ) ? nbins-1 : nbins -2;
         // do all elements beside the first and last point for median 3
         //  and first two and last 2 for median 5
         for  ( ii = ifirst; ii < ilast; ii++)  {
            assert(ii - ifirst >= 0);
            for  (int jj = 0; jj < medianType; jj++)   {
               hh[jj] = yy[ii - ifirst + jj ];
            }
            zz[ii] = TMath::Median(medianType, hh);
         }

         if  (kk == 0)  {   // first median 3
            // first point
            hh[0] = zz[1];
            hh[1] = zz[0];
            hh[2] = 3*zz[1] - 2*zz[2];
            zz[0] = TMath::Median(3, hh);
            // last point
            hh[0] = zz[nbins - 2];
            hh[1] = zz[nbins - 1];
            hh[2] = 3*zz[nbins - 2] - 2*zz[nbins - 3];
            zz[nbins - 1] = TMath::Median(3, hh);
         }

         if  (kk == 1)  {   //  median 5
            for  (ii = 0; ii < 3; ii++) {
               hh[ii] = yy[ii];
            }
            zz[1] = TMath::Median(3, hh);
            // last two points
            for  (ii = 0; ii < 3; ii++) {
               hh[ii] = yy[nbins - 3 + ii];
            }
            zz[nbins - 2] = TMath::Median(3, hh);
         }

      }

      std::cout << "end of median step" << std::endl;
      std::cout << "zz: ";
      for (auto i: zz) std::cout << i << " ";
      std::cout << std::endl;
      std::cout << "hh: ";
      for (auto i: hh) std::cout << i << " ";
      std::cout << std::endl;
      return;

      std::copy ( zz.begin(), zz.end(), yy.begin() );

      // quadratic interpolation for flat segments
      for (ii = 2; ii < (nbins - 2); ii++) {
         if  (zz[ii - 1] != zz[ii]) continue;
         if  (zz[ii] != zz[ii + 1]) continue;
         hh[0] = zz[ii - 2] - zz[ii];
         hh[1] = zz[ii + 2] - zz[ii];
         if  (hh[0] * hh[1] <= 0) continue;
         int jk = 1;
         if  ( TMath::Abs(hh[1]) > TMath::Abs(hh[0]) ) jk = -1;
         yy[ii] = -0.5*zz[ii - 2*jk] + zz[ii]/0.75 + zz[ii + 2*jk] /6.;
         yy[ii + jk] = 0.5*(zz[ii + 2*jk] - zz[ii - 2*jk]) + zz[ii];
      }

      // running means
      for  (ii = 1; ii < nbins - 1; ii++) {
         zz[ii] = 0.25*yy[ii - 1] + 0.5*yy[ii] + 0.25*yy[ii + 1];
      }
      zz[0] = yy[0];
      zz[nbins - 1] = yy[nbins - 1];

      if (noent == 0) {
         // first time algorithm is run

         // save computed values
         std::copy(zz.begin(), zz.end(), rr.begin());

         // COMPUTE  residuals
         for  (ii = 0; ii < nbins; ii++)  {
            zz[ii] = xx[ii] - zz[ii];
         }
      }

   }  // end loop on noent


   double xmin = TMath::MinElement(nbins,xx);
   for  (ii = 0; ii < nbins; ii++) {
      if (xmin < 0) xx[ii] = rr[ii] + zz[ii];
      // make smoothing defined positive - not better using 0 ?
      else  xx[ii] = TMath::Max((rr[ii] + zz[ii]),0.0 );
   }
}

void smooth(){
   // const int nbins = 5;
   // double hist[nbins] = {10, 12, 16, 13, 16};

   const int nbins = 16;
   double hist[nbins] = {7.82272339, 20.79126453, 55.58607231, 80.9790969 , 61.72924992,
       48.02962419, 55.53139849, 38.1122083 , 37.5203016 , 24.89442078,
       33.42130301, 34.15961964, 11.99455817, 90.5479646 , 18.71481196,
       88.95821081};

   double *xx = hist;
   std::cout<<xx<<std::endl;

   print_results(nbins, xx);
   SmoothArray(nbins, xx);
}
