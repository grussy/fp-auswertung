void fit2(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  ifstream in;         //Input Stream
  in.open("peak.dat"); //Oeffnen der Datei
  Float_t xi;
  Float_t yi;
  Int_t nlines = 0;

  TH1F* _histo = new TH1F("_histo","Peaks", 350, 0., 350 );

  while( !in.eof() ){   	//Bis zum Ende der Datei
    if(in >> xi >> yi){         //Einlesen einer Zeile
      _histo->SetBinContent( xi, yi ); //Setzen des Bin Inhalts
      nlines++;
      cout << nlines << ": " << xi << " " << yi << endl;
    }
  }

  cout<<"found "<<nlines<<" data points"<<endl;
  TF1* fitFunc = new TF1("fitFunc","pol1(0)+gaus(2)",0,300);
  //Polynom ersten Grades [0]+[1]*x (Parameternummerierung startet bei 0) multipliziert mit Gaussfunktion [2]*exp(-((x-[3])/(2*[4]))^2) (Parameternummerierung startet bei 2)
  fitFunc->SetParameter(3,175);
  fitFunc->SetParameter(4,20);
  in.close();
  gStyle->SetOptFit();
  _histo->Rebin(5);
  _histo->Fit("fitFunc");
  _histo->Draw("E");
}

