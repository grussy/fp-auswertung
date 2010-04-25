#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis

gROOT.SetStyle("Plain")

##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Edelstahlabsorber
# 
##########################################################################################

# Messdatei 
messdaten = 'messdaten.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert

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
Fenster = TCanvas('cr', 'Edelstahlabsorber')
Fenster.SetGrid()
gr = TGraph(length, array('d',velo), array('d', rates))
gr.SetTitle(';Geschwindigkeit / mm/s; Zählrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')


# Fuehre Lorentz-Fit durch ------------------------------------------------

fl = TF1('fl', '[0] + [1]*TMath::BreitWigner(x, [2], [3])')
fl.SetLineColor(1); fl.SetLineStyle(2); fl.SetLineWidth(2)

params = [
    (0, 'y_{0}',   320),
    (1, 'A',       28),
    (2, '#mu',    0.2),
    (3, '#Gamma',  -0.4) ]

for i, pn, pv in params:
    fl.SetParName(i, pn)
    fl.SetParameter(i, pv)

print '\nLorentz-Fit:'
gr.Fit(fl, 'Q+')
#print_fit_result(fl)
##lgl = create_fit_legend(
##    fl, 'f(x)', 'Lorentz-Fit', lpos = (0.58, 0.41, 0.88, 0.64))
##lgl.Draw()


# Fuehre Gauss-Fit durch --------------------------------------------------

fg = TF1('fg', '[0] + [1]*TMath::Gaus(x, [2], [3])')
fg.SetLineColor(4); fg.SetLineStyle(4); fg.SetLineWidth(2)

params = [
    (0, 'y_{0}',   317),
    (1, 'A',       -38),
    (2, '#mu',    0.2),
    (3, '#sigma',  0.2) ]

for i, pn, pv in params:
    fg.SetParName(i, pn)
    fg.SetParameter(i, pv)

print '\nGauss-Fit:'
gr.Fit(fg, 'Q+')
##print_fit_result(fg)
##lgg = create_fit_legend(
##    fg, 'f(x)', 'Gauss-Fit', lpos = (0.58, 0.16, 0.88, 0.38))
##lgg.Draw()


# Fuehre Voigt-Fit durch --------------------------------------------------

fv = TF1('fv', '[0] + [1]*TMath::Voigt(x-[2], [3], [4], 5)')
fv.SetLineColor(1); fv.SetLineStyle(1); fv.SetLineWidth(2)
fv.SetNpx(1000)

params = [
    (0, 'y_{0}',   320), # 135
    (1, 'A',       28),
    (2, '#mu',    0.2),
    (3, '#sigma',  0.2),
    (4, '#Gamma',  -0.4) ]

for i, pn, pv in params:
    fv.SetParName(i, pn)
    fv.SetParameter(i, pv)

## fv.FixParameter(3, 0.078)

print '\nVoigt-Fit:'
gr.Fit(fv, 'Q+')
##print_fit_result(fv)
##lgv = create_fit_legend(
##    fv, 'f(x)', 'Faltung von Lorentz und Gauss',
##    lpos = (0.13, 0.16, 0.43, 0.38))
##lgv.Draw()

##m.draw_energy_axis()



Fenster.Update()

print "\nDone. Press Enter to continue ..."
raw_input();



