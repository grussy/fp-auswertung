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


for line in open("Si_co57.asc"):
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
xa.SetLimits(550, 750)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(300)

#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr1 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 600, 650)
fr1.SetParameters(300, 620, 20)
fr2 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 650, 750)
fr2.SetParameters(300, 700, 20)
g.Fit(fr1, 'QR')
g.Fit(fr2, 'QR')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

##location = fr.GetParameter(2)
##height = fr.GetParameter(0)
##breite = fr.GetParameter(1)
##print "Center: %.2f" % location
##print "Hoehe: %.2f" % height
##print "Breite: %.2f" % breite
	
line = sys.stdin.readline()
     




















