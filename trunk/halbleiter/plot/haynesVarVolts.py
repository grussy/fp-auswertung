#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from messung import *
from math import sqrt, pi, exp
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TGraphErrors

gROOT.SetStyle("Plain")

# Listendeklarationen
amps, samps = [], []
sigs, ssigs = [] , []
means, smeans = [], []
dists, sdists = [], []
Es, sEs = [],[]

# Lade Messdaten
print '\nLoading Data ...'
msf = lade_Daten('data/haynes_shockley/varVolts/table.dat')

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
        Es.append(float(m.volts)/float(L))
        sEs.append(Es[len(Es)-1]*((sU/float(m.volts))+(float(sL)/float(L))))
    m.draw()
    #m.savePlot()


#Fitte die Schwerpunkte
gMean = TGraphErrors(len(Es), array('d',Es) ,array('d',means), array('d',sEs) ,array('d',smeans))
gMean.SetTitle(';E-Feld an Halbleiter [V/m];Zeit bis Schwerpunktsdetektion[t]')
gMean.GetHistogram().SetTitleOffset(1.3, 'Y')
gMean.SetMarkerStyle(20)
gMean.SetMarkerColor(2)
gMean.SetMarkerSize(0.5)
cMean = TCanvas('MeanFit', 'MeanFit')
cMean.SetGrid()
gMean.Draw('AP')
flin = TF1('MeanFit', '([1]/([0]*x))+[2]')
flin.SetParameters(array('d', [100,1,1e-5]))
flin.SetMarkerStyle(20)
flin.SetMarkerColor(2)
flin.SetMarkerSize(0.5)
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
gAmp.SetMarkerSize(0.5)
cAmp = TCanvas('AmpFit', 'AmpFit')
cAmp.SetGrid()
gAmp.Draw('AP')
fe = TF1('MeanFit', '[0]*exp(-x/[1])')
fe.SetParameters(array('d', [5e-4,1e-5]))
fe.SetMarkerStyle(20)
fe.SetMarkerColor(2)
fe.SetMarkerSize(0.5)
gAmp.Fit(fe, 'Q')
tau, stau = fe. GetParameter(1)*10, fe.GetParError(1)*10
cAmp.Update()
chisq = fe.GetChisquare()
ndf = fe.GetNDF()
rchisq = chisq / ndf
print 'Fit on Amplitudes: Chisquare = %g, Rchisquare= %g '%(chisq, ndf)


#Fitte die Breiten
#--> leider ergabs bei uns keine Wurzelabhängikeit ...
gsig = TGraphErrors(len(means), array('d',means) ,array('d',sigs), array('d',smeans) ,array('d',ssigs))
gsig.SetTitle(';Zeit t [s];Breite der Gauskurve[s]')
gsig.GetHistogram().SetTitleOffset(1.3, 'Y')
gsig.SetMarkerStyle(20)
gsig.SetMarkerColor(2)
gsig.SetMarkerSize(0.5)
csig = TCanvas('SigFit', 'SigFit')
csig.SetGrid()
gsig.Draw('AP')
fs = TF1('MeanFit', 'sqrt(2*[0]*x)', 8e-6, 16e-6)
fs.SetParameters(array('d', [5e-8]))
fs.SetMarkerStyle(20)
fs.SetMarkerColor(2)
fs.SetMarkerSize(0.2)
gsig.Fit(fs, 'QR')
D, sD = fs.GetParameter(0), fs.GetParError(0)
csig.Update()
chisq = fs.GetChisquare()
ndf = fs.GetNDF()
rchisq = chisq / ndf
print 'Fit on Sigmas: Chisquare = %g, Rchisquare= %g '%(chisq, ndf)

# Endlich: Berechnung der physikalischen Grössen
print '\nCalculating ...'

#Last and Least Ergebniss
PrintSol(vel, svel, tau, stau, D, sD)    
raw_input();