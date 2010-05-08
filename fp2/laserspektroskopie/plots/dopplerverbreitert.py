#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from math import pi, cos, sin, sqrt, exp
import sys; sys.path.append('/usr/lib/root/')
from messung import Messung
from fits import nGauss, nLorenz
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
import os.path

#############################################################################
# frequenzeichung (Umrechnung von s in Hz bei Fsr)
umrechnungsfaktor = 0.1

#############################################################################
# fsr
fsr = Messung('14', 'Frequenzlineal', 0.02)
fsr.plot()
# Frequenzabstand in s
freqLinealSec = fsr.freqLineal
freqLinealHz = freqLinealSec * umrechnungsfaktor
print 'FSR / Hz: %.4e' % freqLinealHz

# Finesse
finesse = nLorenz('14', 'Finesse der Cavity', 1)
raw_input();
finesse.saveParameters()
#############################################################################
# Dopplerverbreitertes Spektrum