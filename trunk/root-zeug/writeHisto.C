void writeHisto(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  TFile* _file=new TFile("histo.root","RECREATE");
  TH1F* myHist = new TH1F("myHisto","Distribution from 0 to 1",10,0.,1.);
  myHist->Fill(0.37); 
  myHist->Fill(0.35); 
  myHist->Fill(0.78); 
  myHist->Fill(0.51);
  myHist->Write();
  _file->Close();
}
