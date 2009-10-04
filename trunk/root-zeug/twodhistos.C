void twodhistos(){
  gROOT->Reset();
  gStyle->SetPalette(1);
  TCanvas *c1 = new TCanvas("c1","Canvas fuer viele Histogramme",800,800);
  c1->Divide(2,2);
  TH2F *h2 = new TH2F("h2","Energie vs Impuls",40,-5.,5.,40,-5.,5.);
  h2->FillRandom("gaus",6000);
  h2->GetXaxis()->SetTitle("Energie E (GeV)");
  h2->GetYaxis()->SetTitle("Impuls p (GeV)");
  h2->GetZaxis()->SetTitle("Ereignisse");
  TF2* f2=new TF2("func2","sin(x)*sin(y)/(x*y)",-10.,10.,-10.,10.);
  c1->cd(1);
  h2->GetXaxis()->SetTitleOffset(1.5);
  h2->GetYaxis()->SetTitleOffset(1.5);
  h2->GetZaxis()->SetTitleOffset(1.2);
  h2->Draw("LEGO2");
  c1->cd(2);
  h2->Draw("COL");
  c1->cd(3);
  f2->Draw("SURF1");
  c1->cd(4);
  f2->Draw("COLZ");
}
