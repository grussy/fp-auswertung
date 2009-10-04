void function_advanced(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  TF1 *myFunc = new TF1("myFunction","sin(10*x)*gaus(0)",0.,6.5.);
  TF1 *Func1 = new TF1("Func1","gaus(0)",0.,6.5.);
  TF1 *Func2 = new TF1("Func1","-gaus(0)",0.,6.5.);
  myFunc->SetParameter(0,1);//normalization of the gauss function
  myFunc->SetParameter(1,0);//mean of the gauss function
  myFunc->SetParameter(2,1);//sigma of the gauss function
  Func1->SetParameter(0,1);
  Func1->SetParameter(1,0);
  Func1->SetParameter(2,1);
  Func2->SetParameter(0,1);
  Func2->SetParameter(1,0);
  Func2->SetParameter(2,1);
  myFunc->Draw();
  Func1->Draw("SAME");
  Func2->Draw("SAME");
  Func1->SetLineStyle(2);
  Func2->SetLineStyle(2);
  myFunc->GetXaxis()->SetTitle("x");
  myFunc->GetYaxis()->SetTitle("f(x)=sin(10*x)*gauss(0,1)");
  myFunc->GetYaxis()->SetRangeUser(-1.1,1.1);
  myFunc->SetTitle("Funktion");
}
