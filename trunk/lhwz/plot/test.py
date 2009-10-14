#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraph, TF1, TLegend

gROOT.SetStyle("Plain")



# Lese Messdaten ein

i = 0
x, y = array('d'), array('d')
for line in open("data/uran1.txt", 'r'):
	linenew = line.replace(',', '.')
	xl, yl = map(float, linenew.split())
	x.append(xl); y.append(yl)
count = len(x)

c = TCanvas('c', 'Uran')
c.SetGrid()
c.SetLogy()

g = TGraph(count, x, y)
g.SetTitle('; Zaehlrohrspannung / V; Zaehlrate')
g.GetYaxis().CenterTitle()
g.SetMarkerColor(2)
g.SetMarkerStyle(3)
g.Draw('AP')

line = sys.stdin.readline()
     
