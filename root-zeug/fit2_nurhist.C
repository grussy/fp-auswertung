void fit2_nurhist(){
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

  cout "found "<< nlines << " data points."<<endl;
  in.close();
  gStyle->SetOptFit();
  _histo->Rebin(5);
  _histo->Draw("E");
}

