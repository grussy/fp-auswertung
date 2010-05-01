#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis
from fit_tools import *

gROOT.SetStyle("Plain")

##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Edelstahlabsorber
# 
##########################################################################################

# Variablen, Datenfelder etc
messdaten = 'edelstahl_all.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert
untergrund = 50.38              #Untergrundrate für das Messfenster in cps
velo = []                       #Geschwindigkeiten des Schlittens
time = []                       #Dauer der Messung
counts = []                     #Gezählte Ereignisse
rates = []                      #Raten [counts/second]
srates = []                     #Fehler auf Raten
svelo = []                      #Fehler auf Geschwindigkeiten (bestimmt mit Maussensor)

#Lade Daten:
print "Loading Data in %s ..."%(messdaten)
for line in open(messdaten):
    buffer = line.split()
    velo.append(float(buffer[0]))
    time.append(float(buffer[1]))
    counts.append(float(buffer[2]))
    rates.append((float(buffer[2]) / (float(buffer[1]) / 1000)) - untergrund)
length = len(velo)
assert length > 0
print "   found %i datapoints."%(length)

#print "Edelstahlabsorber, Messdaten: %s, Untergrund: %s cps" % (messdaten, untergrund)

#Plotte die Daten:
print "\nFitting and Drawing ..."
Fenster = TCanvas('cr', 'Edelstahlabsorber')
Fenster.SetGrid()
gr = TGraph(length, array('d',velo), array('d', rates))
gr.SetTitle('Edelstahlabsorber ( 1 Linie );Geschwindigkeit / mm/s; Zählrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')

# Fuehre Lorentz-Fit durch:
fl = TF1('fl', '[0] + [1]*TMath::BreitWigner(x, [2], [3])')
fl.SetLineColor(3); fl.SetLineStyle(2); fl.SetLineWidth(2)
params = [
    (0, 'y_{0}',   270),
    (1, 'A',       -28),
    (2, '#mu',    0.2),
    (3, '#Gamma',  0.4) ]
for i, pn, pv in params:
    fl.SetParName(i, pn)
    fl.SetParameter(i, pv)
gr.Fit(fl, 'Q+')
#print_fit_result(fl)
lgl = create_fit_legend(
    fl, 'f(x)', 'Lorentz-Fit', lpos = (0.58, 0.41, 0.88, 0.64))
lgl.Draw()
print "   done with lorentz."

# Fuehre Gauss-Fit durch:
fg = TF1('fg', '[0] + [1]*TMath::Gaus(x, [2], [3])')
fg.SetLineColor(4); fg.SetLineStyle(4); fg.SetLineWidth(2)
params = [
    (0, 'y_{0}',   267),
    (1, 'A',       -38),
    (2, '#mu',    0.2),
    (3, '#sigma',  0.2) ]
for i, pn, pv in params:
    fg.SetParName(i, pn)
    fg.SetParameter(i, pv)
gr.Fit(fg, 'Q+')
#print_fit_result(fg)
lgg = create_fit_legend(
    fg, 'f(x)', 'Gauss-Fit', lpos = (0.58, 0.16, 0.88, 0.38))
lgg.Draw()
print "   done with gauss."

# Fuehre Voigt-Fit durch:
fv = TF1('fv', '[0] + [1]*TMath::Voigt(x-[2], [3], [4])')
fv.SetLineColor(1); fv.SetLineStyle(1); fv.SetLineWidth(2)
fv.SetNpx(1000)
params = [
    (0, 'y_{0}',   269), # 135
    (1, 'A',       -25),
    (2, '#mu',    0.22),
    (3, '#sigma',  0.13),
    (4, '#Gamma',  0.26) ]
for i, pn, pv in params:
    fv.SetParName(i, pn)
    fv.SetParameter(i, pv)
gr.Fit(fv, 'Q+')
#print_fit_result(fv)
lgv = create_fit_legend(
    fv, 'f(x)', 'Faltung von Lorentz und Gauss',
    lpos = (0.13, 0.16, 0.43, 0.38))
lgv.Draw()
print "   done with voigt."
Fenster.Update()
print "   all done."


print "\nDone. Press Enter to continue ..."
raw_input();
