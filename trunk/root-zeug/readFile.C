readFile(){
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  ifstream in;          //Input Stream
  in.open("6Volt.data"); //Oeffnen der Datei
  Float_t xi;
  Int_t nlines = 0;

  TH1F* _histo = new TH1F("_histo","Peaks", 1250, 0., 125 );

  while( !in.eof() ){   //Bis zum Ende der Datei
    if(in >> xi){           //Einlesen einer Zeile
      _histo->SetBinContent( nlines, xi ); //Setzen des Bin Inhalts
      nlines++;
      cout << nlines << ": " << xi <<endl;
    }
  }

  cout<<"found "<<nlines<<" data points"<<endl;
  
  in.close();
  _histo->Draw();
}

