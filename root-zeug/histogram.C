void histogram(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  TH1F* myHist = new TH1F("myHist","Distribution from 0 to 1",10,0.,1.);
  myHist->Fill(0.37); //Bin 4
  myHist->Fill(0.35); //Bin 4
  myHist->Fill(0.78); //Bin 8
  myHist->Fill(0.51); //Bin 6
  myHist->Draw("HF1");
}
