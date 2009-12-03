#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from messung import *
from math import sqrt, pi, exp
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TGraphErrors
from tools import *

gROOT.SetStyle("Plain")
sU = 0.1

# Lade Messdaten, in Liste: Amplitude Sigma Schwerpunkt Offset
print '\nLoading Data ...'
msf = lade_Daten('data/haynes_shockley/varDistance/table.dat')
#Fitte alles, zeichnen speichern ... 
print '\nFitting now ... '
amps, samps = [], []
sigs, ssigs = [] , []
means, smeans = [], []
dists, sdists = [], []
Es, sEs = [],[]
for m in msf :
    #doof aber einer brauchte andere initParams sonst gabs keine Glocke:
    if (m.name == 'varDistance/csv/F0006CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.952e-5,-0.0075])
        m.draw()
    else:
        m.fit( [1e-5,1e-05,1e-5,0])
    print 'Fit on Data %s: Chisquare = %g, Rchisquare= %g '%(m.name, m.chisq, m.rchisq)
    amps.append(float(m.amp))
    sigs.append(float(m.sigma))
    means.append(float(m.ort))
    dists.append(float(m.dist))
    samps.append(float(m.samp))
    ssigs.append(float(m.ssigma))
    smeans.append(float(m.sort))
    sdists.append(float(m.sdist))
    Es.append(float(m.U)/float(m.dist))
    sEs.append(Es[len(Es)-1]*((sU/float(m.U))+(float(m.sdist)/float(m.dist))))
    m.draw()

#Berechne Physik

#Fitte die Schwerpunkte
gMean = TGraphErrors(len(means), array('d',means) ,array('d',dists), array('d',smeans) ,array('d',sdists))
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
vel, svel = flin.GetParameter(0), flin.GetParError(0)
cMean.Update()

#Fitte die Amplituden
gAmp = TGraphErrors(len(means), array('d',means) ,array('d',amps), array('d',smeans) ,array('d',samps))
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
cAmp.Update()

#Fitte die Breiten
gsig = TGraphErrors(len(means), array('d',means) ,array('d',sigs), array('d',smeans) ,array('d',ssigs))
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
csig.Update()

# Endlich:
print '\nCalculating ...'
E, sE = gew_mittel()

   
print'\Done. Press any Key.' 
raw_input();


# Erzeuge TeX Tabellen
#import texgen
#texgen.write_table_schleife(msf)
#texgen.write_table_schleife_fit(msf)
#texgen.write_table_z(msf)
#texgen.write_table_schleife_dipol(msf)
