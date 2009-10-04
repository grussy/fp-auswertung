void function(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  TF1 *myFunc = new TF1("myFunction","gaus(0)",0.,6.5.);
  myFunc->SetParameter(0,1);
  myFunc->SetParameter(1,0);
  myFunc->SetParameter(2,1);
  myFunc->Draw();
  myFunc->GetXaxis()->SetTitle("x");
  myFunc->GetYaxis()->SetTitle("f(x)=sin(x)/x");
  myFunc->SetTitle("Funktion");
}
