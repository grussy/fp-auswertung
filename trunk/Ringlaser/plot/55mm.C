//Plot
{
//Standart Settings
gROOT->Reset();
gROOT->SetStyle("Plain");
gStyle->SetOptFit();
//Load Data
#include "Riostream.h"
ifstream in;
in.open("/home/paule/FP/trunk/Ringlaser/plot/data/55mm.dat");
const Int_t ndata = 10;
Float_t x[ndata];
Float_t y[ndata];
Float_t sx[ndata];
Float_t sy[ndata];
Int_t line = 0;
while (1) 
{
  in >> x[line] >> sx[line] >> y[line] >> sy[line];
  cout<<"sy:"<<sy[line]<<" y:"<<y[line]<<" sx:"<<sx[line]<<" x:"<<x[line]<<endl;
  if (!in.good()) break;
  line++;
}
cout<<"Found "<<line<<" Data Points."<<endl;
in.close();
//plot&fit
TGraphErrors* gr = new TGraphErrors(line,x,y,sx,sy);
TF1* lin = new TF1("linear","pol1",x[0],x[ndata]);
lin->SetLineWidth(2);
lin->SetLineColor(2);
gr->SetTitle("Constant Distance of 55mm");
gr->GetXaxis()->SetTitle("Motorfrequenz[Hz]");
gr->GetYaxis()->SetTitle("Schwebungsfrequenz[kHz]");
gr->SetMarkerColor(4);
gr->SetMarkerStyle(20);
gr->Fit("linear");
gr->Draw("ALP");
}
