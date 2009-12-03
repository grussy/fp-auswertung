#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from messung import *
from math import sqrt, pi, exp
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TGraphErrors

gROOT.SetStyle("Plain")

# Fehler der Treiberspannung
sU = 0.1
# Listendeklarationen
amps, samps = [], []
sigs, ssigs = [] , []
means, smeans = [], []
dists, sdists = [], []
Es, sEs = [],[]

# Lade Messdaten
print '\nLoading Data ...'
msf = lade_Daten('data/haynes_shockley/varVolts/table.dat')

#Berechne Fehler auf Spannung, per StAbw eines "linearen" Bereichs
sx, sy = [], []

#Fitten, zeichnen, rechnen, speichern ... 
print '\nFitting now ... '
for m in msf :
    # doof aber einige brauchten andere initParams sonst gabs keine Glocken:
     # in Liste: Amplitude Sigma Schwerpunkt Offset
    if (m.name == 'varVolts/csv/F0009CH1.CSV'): 
        m.fit([1e-5,2e-6,18e-6,-0.0275])
    elif (m.name == 'varVolts/csv/F0002CH1.CSV'): 
        m.fit([1.5e-4,1e-6,9.5e-6,-0.02])
    elif (m.name == 'varVolts/csv/F0008CH1.CSV'): 
        m.fit([1.5e-5,1e-6,15.5e-6,-0.0454])
    elif (m.name == 'varVolts/csv/F0010CH1.CSV'): 
        m.fit([1e-5,1e-6,18.8e-6,0.025])
    elif (m.name == 'varVolts/csv/F0003CH1.CSV'): 
        m.fit([1e-5,1e-6,11e-6,0.005])
    elif (m.name == 'varVolts/csv/F0004CH1.CSV'): 
        m.fit([1e-5,1e-6,11e-6,0.0065])
    else:
        m.fit( [1e-5,1e-05,1e-5,0])
    print 'Fit on Data %s: Chisquare = %g, Rchisquare= %g '%(m.name, m.chisq, m.rchisq)
    if (m.name != 'varVolts/csv/F0011CH1.CSV'):
        amps.append(float(m.amp))
        sigs.append(float(m.sigma))
        means.append(float(m.ort))
        dists.append(float(m.dist))
        samps.append(float(m.samp))
        ssigs.append(float(m.ssigma))
        smeans.append(float(m.sort))
        sdists.append(float(m.sdist))
        Es.append(float(m.volts)/float(m.dist))
        sEs.append(Es[len(Es)-1]*((sU/float(m.volts))+(float(m.sdist)/float(m.dist))))
    m.draw()
    
print '\n DEBUG: Fehler:'
print 'Amps:'
print samps
print 'Sigs:'
print ssigs
print 'Means:'
print smeans
#Berechne Physik

#Fitte die Schwerpunkte
gMean = TGraphErrors(len(means), array('d',means) ,array('d',dists), array('d',smeans) ,array('d',sdists))
gMean.SetTitle(';Zeit t [s];Ort des Schwerpunktes[m]')
gMean.GetHistogram().SetTitleOffset(1.3, 'Y')
gMean.SetMarkerStyle(20)
gMean.SetMarkerColor(2)
gMean.SetMarkerSize(0.2)
cMean = TCanvas('MeanFit', 'MeanFit')
cMean.SetGrid()
gMean.Draw('AP')
flin = TF1('MeanFit', '[0]*x+[1]')
flin.SetParameters(array('d', [0,0]))
gMean.Fit(flin, 'Q')
vel, svel = flin.GetParameter(0), flin.GetParError(0)
cMean.Update()
chisq = flin.GetChisquare()
ndf = flin.GetNDF()
rchisq = chisq / ndf
print '\nFit on Mass Center: Chisquare = %g, Rchisquare= %g '%(chisq, ndf)

#Fitte die Amplituden
gAmp = TGraphErrors(len(means), array('d',means) ,array('d',amps), array('d',smeans) ,array('d',samps))
gAmp.SetTitle(';Zeit t [s];Amplitude der Gauskurve[V]')
gAmp.GetHistogram().SetTitleOffset(1.3, 'Y')
gAmp.SetMarkerStyle(20)
gAmp.SetMarkerColor(2)
gAmp.SetMarkerSize(0.2)
cAmp = TCanvas('AmpFit', 'AmpFit')
cAmp.SetGrid()
gAmp.Draw('AP')
fe = TF1('MeanFit', '[0]*exp(-x/[1])')
fe.SetParameters(array('d', [5e-4,1e-5]))
gAmp.Fit(fe, 'Q')
tau, stau = fe. GetParameter(1), fe.GetParError(1)
cAmp.Update()
chisq = fe.GetChisquare()
ndf = fe.GetNDF()
rchisq = chisq / ndf
print 'Fit on Amplitudes: Chisquare = %g, Rchisquare= %g '%(chisq, ndf)


#Fitte die Breiten
gsig = TGraphErrors(len(means), array('d',means) ,array('d',sigs), array('d',smeans) ,array('d',ssigs))
gsig.SetTitle(';Zeit t [s];Spannung U [V]')
gsig.GetHistogram().SetTitleOffset(1.3, 'Y')
gsig.SetMarkerStyle(20)
gsig.SetMarkerColor(2)
gsig.SetMarkerSize(0.2)
csig = TCanvas('SigFit', 'SigFit')
csig.SetGrid()
gsig.Draw('AP')
fs = TF1('MeanFit', 'sqrt(2*[0]*x)')
fs.SetParameters(array('d', [5e-8]))
gsig.Fit(fs, 'Q')
D, sD = fs.GetParameter(0), fs.GetParError(0)
csig.Update()
chisq = fs.GetChisquare()
ndf = fs.GetNDF()
rchisq = chisq / ndf
print 'Fit on Sigmas: Chisquare = %g, Rchisquare= %g '%(chisq, ndf)

#csig.SaveAs('eps/sigmasVarDist.eps' % self.name[:-4])
#camp.SaveAs('eps/ampsVarDist.eps' % self.name[:-4])
#cmean.SaveAs('eps/MeansVarDist.eps' % self.name[:-4])

# Endlich: Berechnung der physikalischen Gr�ssen
print '\nCalculating ...'
E, sE = GewMittel(Es, sEs)
mu = vel/E
smu = mu*((svel/vel)+(sE/E))
print ' Mobility:           (%g +- %g) m^2/(Vs)'%(mu, smu)
print ' Lifetime:           (%g +- %g) s'%(tau, stau)
print ' Diffusionconstant:  (%g +- %g)m^2/s'%(D,sD)

   
print'\nDone. Press any Key.' 
raw_input();


# Erzeuge TeX Tabellen
#import texgen
#texgen.write_table_schleife(msf)
#texgen.write_table_schleife_fit(msf)
#texgen.write_table_z(msf)
#texgen.write_table_schleife_dipol(msf)
