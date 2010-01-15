#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import pi, cos, sin, exp
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------
x = []
y = []
i = 0
a = 0

for line in open("Si_Am.mca"):
	y += [float(line)]
	x += [i]
	i += 1
count = len(x)
# Erzeuge Graphen
g = TGraph(count, array('d',x) ,array('d',y))
g.SetTitle(';Kanal;Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(250, 350)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(20)

#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 280, 350)
fr.SetParameter(0, 200)
fr.SetParameter(1, 1)
fr.SetParameter(2, 300)
fr.SetNpx(1000)
g.Fit(fr, 'QR')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

print " Data of 59,5 keV Peak:"
print "Center: %.2f+-%.2f" % (fr.GetParameter(2), fr.GetParError(2))
print "Hoehe: %.2f+-%.2f" % (fr.GetParameter(0), fr.GetParError(0))
print "Breite: %.2f+-%.2f" % (fr.GetParameter(1), fr.GetParError(1))
	
line = sys.stdin.readline()
     




















