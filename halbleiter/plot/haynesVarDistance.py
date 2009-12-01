#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from messung import *
from math import sqrt, pi, exp
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Plotten und Fitten der Messungen mit Leiterschleife
# -------------------------------------------------------------------

# Lade Messdaten
print '\nLoading Data ...'
msf = lade_varDist('data/haynes_shockley/varDistance/table.dat')
#Fitte alles, zeichnen speichern ... 
print '\nFitting now ... '
amps = []
sigs = [] 
means = []
dists = []
for m in msf :
    m.fit()
    print 'Fit on Data %s: Chisquare = %g, Rchisquare= %g '%(m.name, m.chisq, m.rchisq)
    amps.append(float(m.amp))
    sigs.append(float(m.sigma))
    means.append(float(m.ort))
    dists.append(float(m.dist))
  #  m.draw()

#Berechne Physik

#Fitte die Schwerpunkte
gMean = TGraph(len(means), array('d',means) ,array('d',dists))
gMean.SetTitle(';Zeit t [s];Spannung U [V]')
gMean.GetHistogram().SetTitleOffset(1.3, 'Y')
gMean.SetMarkerStyle(20)
gMean.SetMarkerColor(2)
gMean.SetMarkerSize(1.0)
cMean = TCanvas('MeanFit', 'MeanFit')
cMean.SetGrid()
gMean.Draw('AP')
flin = TF1('MeanFit', '[0]*x+[1]')
flin.SetParameters(array('d', [0,0]))
gMean.Fit(flin, 'Q')
#self.test.Draw('AP')
cMean.Update()

#Fitte die Amplituden
gAmp = TGraph(len(means), array('d',means) ,array('d',amps))
gAmp.SetTitle(';Zeit t [s];Spannung U [V]')
gAmp.GetHistogram().SetTitleOffset(1.3, 'Y')
gAmp.SetMarkerStyle(20)
gAmp.SetMarkerColor(2)
gAmp.SetMarkerSize(1.0)
cAmp = TCanvas('AmpFit', 'AmpFit')
cAmp.SetGrid()
gAmp.Draw('AP')
fe = TF1('MeanFit', '[0]*exp(-x/[1])')
fe.SetParameters(array('d', [0,0]))
gAmp.Fit(fe, 'Q')
#self.test.Draw('AP')
cAmp.Update()

#Fitte die Breiten
gsig = TGraph(len(means), array('d',means) ,array('d',sigs))
gsig.SetTitle(';Zeit t [s];Spannung U [V]')
gsig.GetHistogram().SetTitleOffset(1.3, 'Y')
gsig.SetMarkerStyle(20)
gsig.SetMarkerColor(2)
gsig.SetMarkerSize(1.0)
csig = TCanvas('SigFit', 'SigFit')
csig.SetGrid()
gsig.Draw('AP')
fs = TF1('MeanFit', 'sqrt(2*[0]*x)')
fs.SetParameters(array('d', [0]))
gsig.Fit(fs, 'Q')
#self.test.Draw('AP')
csig.Update()
    
raw_input();


# Erzeuge TeX Tabellen
#import texgen
#texgen.write_table_schleife(msf)
#texgen.write_table_schleife_fit(msf)
#texgen.write_table_z(msf)
#texgen.write_table_schleife_dipol(msf)