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
# Treiberspannung, hier konstant
Utreib, sUtreib = 51.2,0.1

# Lade Messdaten
print '\nLoading Data ...'
msf = lade_Daten('data/haynes_shockley/varDistance/table.dat')

#Fitten, zeichnen, rechnen, speichern ... 
print '\nFitting now ... '
for m in msf :
    #doof aber eiige brauchten andere initParams sonst gabs keine Glocken:
     # in Liste: Amplitude Sigma Schwerpunkt Offset
    if (m.name == 'varDistance/csv/F0000CH1.CSV'): 
        m.fit([0.000025,0.7e-6,4.75e-6,0.05])
    elif (m.name == 'varDistance/csv/F0001CH1.CSV'): 
        m.fit([0.000025,0.7e-6,9e-6,-0.0025])
    elif (m.name == 'varDistance/csv/F0002CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.3e-5,-0.0025])
    elif (m.name == 'varDistance/csv/F0003CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.75e-5,-0.0075])
    elif (m.name == 'varDistance/csv/F0004CH1.CSV'): 
        m.fit([0.000025,0.7e-6,2.2e-5,-0.0075])
    elif (m.name == 'varDistance/csv/F0005CH1.CSV'): 
        m.fit([0.000025,0.7e-6,2.4e-5,-0.0075])
    elif (m.name == 'varDistance/csv/F0006CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.952e-5,-0.0075])
    elif (m.name == 'varDistance/csv/F0007CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.7e-5,-0.0025])
    elif (m.name == 'varDistance/csv/F0008CH1.CSV'): 
        m.fit([0.000025,0.7e-6,1.1e-5,-0.0025])
    elif (m.name == 'varDistance/csv/F0009CH1.CSV'): 
        m.fit([0.000025,0.7e-6,7.5e-6,-0.0025])
    else:
        m.fit( [1e-5,1e-05,1e-5,0])
    print 'Fit on Data %s: Chisquare = %g, Rchisquare= %g '%(m.name, m.chisq, m.rchisq)
    print m.amp
    amps.append(float(m.amp))
    sigs.append(float(m.sigma))
    means.append(float(m.ort))
    dists.append(float(m.dist))
    samps.append(float(m.samp))
    ssigs.append(float(m.ssigma))
    smeans.append(float(m.sort))
    sdists.append(float(m.sdist))
    m.draw()
#    m.savePlot()

#Fitte die Schwerpunkte -> Beweglichkeit 
gMean = TGraphErrors(len(means), array('d',means) ,array('d',dists), array('d',smeans) ,array('d',sdists))
gMean.SetTitle(';Zeit t [s];Ort des Schwerpunktes[m]')
gMean.GetHistogram().SetTitleOffset(1.3, 'Y')
gMean.SetMarkerStyle(20)
gMean.SetMarkerColor(2)
gMean.SetMarkerSize(0.5)
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
print '\nFit on Mass Center: Chisquare = %g, Rchisquare= %g '%(chisq, rchisq)

#Fitte die Amplituden -> Lebensdauer
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
fe.SetParameters(array('d', [5e-6,1e-5]))
gAmp.Fit(fe, 'Q')
tau, stau = fe. GetParameter(1)*10, fe.GetParError(1)*10
cAmp.Update()
chisq = fe.GetChisquare()
ndf = fe.GetNDF()
rchisq = chisq / ndf
print 'Fit on Amplitudes: Chisquare = %g, Rchisquare= %g '%(chisq, rchisq)


#Fitte die Breiten -> Diffusionskonstante
gsig = TGraphErrors(len(means), array('d',means) ,array('d',sigs), array('d',smeans) ,array('d',ssigs))
gsig.SetTitle(';Zeit t [s];Breite der Gauskurve [s]')
gsig.GetHistogram().SetTitleOffset(1.3, 'Y')
gsig.SetMarkerStyle(20)
gsig.SetMarkerColor(2)
gsig.SetMarkerSize(0.5)
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
print 'Fit on Sigmas: Chisquare = %g, Rchisquare= %g '%(chisq, rchisq)

# Endlich: Berechnung der physikalischen Grössen
print '\nCalculating ...'
E = Utreib/L
sE = E*sqrt((sUtreib/Utreib)**2+(sL/L)**2)
mu = vel/E
smu = mu*sqrt((svel/vel)**2+(sE/E)**2)

#Last and Least Ergebniss
PrintSol(mu, smu, tau, stau, D,sD)
raw_input();