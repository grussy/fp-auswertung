#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")

##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Eisenabsorber
# 
##########################################################################################

# Messdatei 
messdaten = 'eisen_all.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert

velo = []
time = []
counts = []
rates = []

for line in open(messdaten):
    buffer = line.split()
    print buffer
    velo.append(float(buffer[0]))
    time.append(float(buffer[1]))
    counts.append(float(buffer[2]))
    rates.append(float(buffer[2]) / (float(buffer[1]) / 1000))
    

length = len(velo)


#Plotte die Daten:
Fenster = TCanvas('cr', 'Eisenabsorber')
Fenster.SetGrid()
gr = TGraph(length, array('d',velo), array('d', rates))
gr.SetTitle(';Geschwindigkeit / mm/s; Zählrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')


# 6-Fach Loretzfit -----------------------------------------------------------

#erzeuge Fitfunktion
lorentz = '[0]'  #Offset
for i in range(1,7):
    j = 3*i
    lorentz += '+ 2*[%i]/pi * [%i]/(4*(x-[%i])^2 + [%i]^2)' % (j-2,j-1,j,j-1)

f = TF1('f', lorentz)

params = [
    (0, 'y_{0}',   317),
    (1, 'A1',       -13),
    (2, '#w1',    0.6),
    (3, '#wc1',  -5),
    
    (4, 'A2',       -6),
    (5, '#w2',    0.4),
    (6, '#wc2',  -3), 

    (7, 'A3',       -4.5),
    (8, '#w3',    0.2),
    (9, '#wc3',  -0.7), 

    (10, 'A4',       -4),
    (11, '#w4',    0.25),
    (12, '#wc4',  0.9), 

    (13, 'A5',       -8),
    (14, '#w5',    0.3),
    (15, '#wc5',  3), 

    (16, 'A6',       -16),
    (17, '#w6',    0.9),
    (18, '#wc6',  5)]


for i, pn, pv in params:
    f.SetParName(i, pn)
    f.SetParameter(i, pv)

gr.Fit(f, 'Q+')

Fenster.Update()

print "\nDone. Press Enter to continue ..."
raw_input();



