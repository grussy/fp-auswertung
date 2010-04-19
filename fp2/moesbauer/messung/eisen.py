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
messdaten = 'eisen_1.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert

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
gr.SetTitle(';Geschwindigkeit / mm/s; Z�hlrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')

Fenster.Update()

print "\nDone. Press Enter to continue ..."
raw_input();


