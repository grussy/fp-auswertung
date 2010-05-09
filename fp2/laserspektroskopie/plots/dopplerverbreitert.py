#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from math import pi, cos, sin, sqrt, exp
import sys; sys.path.append('/usr/lib/root/')
from messung import Messung
from fits import nGauss, nLorenz
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
import os.path
from frequenz_eichung import mw, gew_mittel


#############################################################################
# frequenzeichung (Umrechnung von s in Hz bei Fsr)
umrechnungsfaktor = 1e12
sumrechnungsfaktor = 0.00624e12

#############################################################################
### fsr
##fsr = Messung('14', 'Frequenzlineal', 0.02)
##fsr.plot()
### Frequenzabstand in s
##freqLinealSec = fsr.freqLineal
##print freqLinealSec
##freqLinealHz = freqLinealSec * umrechnungsfaktor
##print 'FSR / Hz: %.4e' % freqLinealHz
##
### Finesse
###finesse = nLorenz('14', 'Finesse der Cavity', 1)
##raw_input();
###finesse.saveParameters()
#############################################################################
# Dopplerverbreitertes Spektrum
doppler1 = nGauss('39', 'Spektrum mit 4 Gauss', 4, 0.005, 2)
raw_input();
doppler1.saveParameters()
doppler1.readParameters()
#doppler1.printParameters()

# FSR
fsrS = doppler1.messung.freqLineal
sfsrS = doppler1.messung.sfreqLineal
fsrHz = fsrS * umrechnungsfaktor
sfsrHz = fsrHz * sqrt((sumrechnungsfaktor/umrechnungsfaktor)**2 + (sfsrS/fsrS)**2)

print 'FSR: %e +- %e Hz' % (fsrHz, sfsrHz)

# Finesse
halbwertsbreiten = [35e-6, 33e-6, 33e-6, 34e-6, 34e-6]
hwbS, shwbS = mw(halbwertsbreiten)
hwbHz = hwbS * umrechnungsfaktor
shwbHz = hwbHz * sqrt((sumrechnungsfaktor/umrechnungsfaktor)**2 + (shwbS/hwbS)**2)
print 'Halbwertsbreite eines Peaks: %e +- %e Hz' % (hwbHz, shwbHz)
finess = fsrHz / hwbHz
sfiness = finess * sqrt((sfsrHz/fsrHz)**2 + (shwbHz/hwbHz)**2)
print 'Finess der ext. Cavity: %e +- %e' % (finess, sfiness)

#Resonatorlänge 
n = 1.000292
c = 3e8
L = c /  (4 * fsrHz * n)
sL = L * sfsrHz / fsrHz

print 'Resonatorlänge: %e +- %e cm' % (L*1e2, sL*1e2)
#Hole die Orte
orte = []
sorte = []
sigma = []
ssigma = []
hoehe = []
shoehe = []
for parameter in doppler1.params:
    if parameter[1] == 'u':
        orte.append(float(parameter[2]))
        sorte.append(float(parameter[3]))
    if parameter[1] == 'o':
        sigma.append(float(parameter[2]))
        ssigma.append(float(parameter[3]))
    if parameter[1] == 'A':
        hoehe.append(float(parameter[2]))
        shoehe.append(float(parameter[3]))
abstaende = []
sabstaende = []
for i in range(len(orte)-1):
    value = abs((orte[i] - orte[i+1]))
    abstaende.append(value)
    sabstaende.append(value*sqrt((sorte[i]/orte[i])**2 + (sorte[i+1]/orte[i+1])**2))
    
fwhmS = [2.3548 * sig for sig in sigma]
sfwhmS = [2.3548 * ssig for ssig in ssigma]

fwhmHz = [f * umrechnungsfaktor for f in fwhmS]
sfwhmHz = []
for i in range (len(fwhmHz)):
    sfwhmHz.append(fwhmHz[i] * sqrt((sfwhmS[i]/fwhmS[i])**2 + (sumrechnungsfaktor/umrechnungsfaktor)**2))
print 'Halbwertsbreiten: [Hz]'
for i in range(4):
    print 'Peak %i: %e +- %e Hz' % (i+1, fwhmHz[i], sfwhmHz[i])
mittelfwhm, smittelfwhm = gew_mittel(fwhmHz, sfwhmHz)
print 'gew. Mittel der Halbwertsbreiten: %e +- %e Hz' % (mittelfwhm, smittelfwhm)
#Absorptionsquerschnitte
sig = [(780.2e-9)**2 / (2 * pi) * h for h in hoehe]
ssig = [(780.2e-9)**2 / (2 * pi) * sh for sh in shoehe]
print 'Absorptionsquerschnitte:'
for i in range(4):
    print 'Peak %i: %e +- %e m**2' % (i+1, sig[i], ssig[i])
###rausnehmen!##################################################################
##sollabstaende = [2.660e9, 3.036e9, 1.138e9]  # in Hz
##g = TGraphErrors(3, array('d',abstaende) ,array('d',sollabstaende),array('d',[1e-7]*3),
##                 array('d',[1e7]*3))
##g.SetTitle(';time;frequency')
##g.SetMarkerStyle(1)
##g.SetMarkerColor(2)
##g.SetMarkerSize(3.0)
##f = TF1('Eichgerade', '[0]*x')
##f.SetMarkerColor(3)
##f.SetParameter(0, 1)
##g.Fit(f, 'M')
##c = TCanvas('Eichung', 'eichung')
##c.SetGrid()
##g.Draw('AP')
##c.Update()    
##raw_input();
###bis hier rausnehmen!#########################################################
abstaendeGauss = [a*umrechnungsfaktor for a in abstaende]
sabstaendeGauss = []
for i in range(len(sabstaende)):
    sabstaendeGauss.append(abstaendeGauss[i] * sabstaende[i] / abstaende[i])
    print 'Peakabstand %i: (%e +- %e)' % (i+1, abstaendeGauss[i], sabstaendeGauss[i])
    
