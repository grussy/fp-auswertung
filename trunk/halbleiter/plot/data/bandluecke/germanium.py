#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import pi, cos, sin
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name):
        self.name = name

        # Lese Messdaten ein	
	self.time = []
	self.winkel = []
	self.trans = []
	self.absor = []
	self.wellenl = []
	self.energie = []
	z = 0
	for line in open(name,'r'):
		if z < 7:
	 		z += 1
	        else:
    			linenew = line.replace(',', '.')
    			datarow = map(float, linenew.split())
    			self.time.append(datarow[0])
			self.winkel.append(datarow[1])
			self.trans.append(datarow[2])
			self.absor.append(datarow[3])
			self.wellenl.append(datarow[4])
			self.energie.append(datarow[5])

	count = len(self.time)
	
 	# Erzeuge Graphen
        g = TGraph(count, array('d',self.energie) ,array('d',self.absor))
        g.SetTitle(';Energie [eV];Spannung [V]')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(2)
	g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g
	xa = g.GetXaxis()
        xa.SetLimits(0.64, 0.74)
	ya = g.GetYaxis()
        ya.SetLimits(0, 2)

 	# Erzeuge Graphen
        g2 = TGraph(count, array('d',self.energie) ,array('d',self.trans))
        g2.SetTitle(';Winkel [#circ];Spannung U [V]')
        g2.GetHistogram().SetTitleOffset(1.3, 'Y')
        g2.SetMarkerStyle(2)
	g2.SetMarkerColor(4)
        g2.SetMarkerSize(3.0)
        self.graph2 = g2
	xa = g2.GetXaxis()
        xa.SetLimits(-1, 1)
	h = g.GetHistogram()
	h.SetMinimum(0)
        h.SetMaximum(1.6)

	# Zeichnen des 'normalen Graphen'
    def draw(self):
       	c = TCanvas('c_'+self.name, self.name)
       	self.canvas = c
       	c.SetGrid()
       	self.graph.Draw('AP')
	self.graph2.Draw('P')
       	c.Update()
		
# Lade Untergrund
ugrund = Messung("Germanium_Untergrund.txt")
# Lade Messung	
test = Messung("grge1.txt")
# Lade Lampenspektrum
lampe = Messung("LampeLeistung.txt")
# Untergrund abziehen
def winkellinks(winkel, grund):
	i = 0
	countugrund = len(grund.winkel)
	while(grund.winkel[i] > winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] > winkel and i != countugrund -1):
			i += 1
	return grund.winkel[i]

def winkelrechts(winkel, grund):
	i = 0
	countugrund = len(grund.winkel)
	while(grund.winkel[i] < winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] < winkel and i != countugrund -1):
			i += 1
	return grund.winkel[i]

def translinks(winkel, grund):
	i = 0
	countugrund = len(grund.winkel)
	while(grund.winkel[i] > winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] > winkel and i != countugrund -1):
			i += 1
	return grund.trans[i]

def absorrechts(winkel, grund):
	i = 0
	countugrund = len(ugrund.winkel)
	while(grund.winkel[i] < winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] < winkel and i != countugrund -1):
			i += 1
	return grund.absor[i]

def absorlinks(winkel, grund):
	i = 0
	countugrund = len(grund.winkel)
	while ( grund.winkel[i] > winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] > winkel and i != countugrund -1):
			i += 1
	return grund.absor[i]

def transrechts(winkel, grund):
	i = 0
	countugrund = len(grund.winkel)
	while(grund.winkel[i] < winkel and i != countugrund -1):
		i += 1
	if i == 0:
		while(grund.winkel[countugrund -1 - i] < winkel and i != countugrund -1):
			i += 1
	return grund.trans[i]

def tugrund(winkel):
	xlinks = winkellinks(winkel, ugrund)
	xrechts = winkelrechts(winkel, ugrund)
	ylinks = translinks(winkel, ugrund)
	yrechts = transrechts(winkel, ugrund)
	steigung = (yrechts - ylinks) / (xrechts - xlinks)
	return (winkel - xlinks) * steigung + ylinks

def augrund(winkel):
	xlinks = winkellinks(winkel, ugrund)
	xrechts = winkelrechts(winkel, ugrund)
	ylinks = absorlinks(winkel, ugrund)
	yrechts = absorrechts(winkel, ugrund)
	steigung = (yrechts - ylinks) / (xrechts - xlinks)
	return (winkel - xlinks) * steigung + ylinks

def leistunglampe(winkel):
	xlinks = winkellinks(winkel, lampe)
	xrechts = winkelrechts(winkel, lampe)
	ylinks = translinks(winkel, lampe)
	yrechts = transrechts(winkel, lampe)
	steigung = (yrechts - ylinks) / (xrechts - xlinks + 1)
	return (winkel - xlinks) * steigung + ylinks

for i in range(len(test.time)):
	winkel = test.winkel[i]
	trans = (test.trans[i]-tugrund(winkel)) / leistunglampe(winkel)
	absor = (test.absor[i]-augrund(winkel)) / leistunglampe(winkel)
	test.trans[i] = trans
	test.absor[i] = absor
# normierung auf Lampenstrahlungsleistung








test.draw()
line = sys.stdin.readline()
     




















