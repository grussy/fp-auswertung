void fit(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  TH1F* myH1 = new TH1F("myHisto","gaussian distribution 1",100,-5.,5.);
  TF1* myGaus = new TF1("myGaus","gaus",-5,5); // 3 Fitparameter: Konstante, mu, sigma
  myH1->FillRandom("gaus",6000);//Histogramm zufaellig nach Gausverteilung fuellen
  myH1->SetMarkerColor(2);  
  myH1->SetMarkerStyle(20); 

  myH1->Fit("myGaus");  
  myH1->Draw("E");  
  cout<<" --------------------------------" <<endl;
  cout<<" chi2/dof: "<< myGaus->GetChisquare()/myGaus->GetNDF()<<endl;
  cout<<" mean: "<< myGaus->GetParameter(1) <<"+/-"<<myGaus->GetParError(1)<<endl;
  cout<<" sigma: "<< myGaus->GetParameter(2) <<"+/-"<<myGaus->GetParError(2)<<endl;
}
