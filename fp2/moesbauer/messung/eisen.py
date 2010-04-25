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
gr.SetTitle(';Geschwindigkeit / mm/s; Z�hlrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')


# 6-Fach Loretzfit -----------------------------------------------------------

#erzeuge Fitfunktion
lorentz = '[0]'  #Offset
for i in range(1,6):
    j = 3*i
    lorentz += '+ 2*[%i]/pi * [%i]/(4*(x-[%i])^2 + [%i]^2)' % (j-2,j-1,j,j-1)

f = TF1('f', lorentz)

gr.Fit(f, 'Q+')

Fenster.Update()

print "\nDone. Press Enter to continue ..."
raw_input();



