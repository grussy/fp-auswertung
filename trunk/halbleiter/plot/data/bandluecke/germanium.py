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
    def __init__(self, name, links, rechts):
        self.name = name
	self.ugrund = 0
    	self.lampe = 0
	self.xmin = 0.5
	self.xmax = 1.
	self.links = links
	self.rechts = rechts
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
        g.SetMarkerStyle(3)
	g.SetMarkerColor(2)
        g.SetMarkerSize(1.0)
	f = TF1('f', '[0]', -10, 10)
	f.SetParameter(0, findMaximum(self.absor, self.energie, self.links - 0.5, self.rechts + 0.5))
	f2 = TF1('f', '[0]', -10, 10)
	f2.SetParameter(0, findMinimum(self.trans, self.energie, self.links - 0.5, self.rechts + 0.5))

	f3 = TF1('f', '[0] + [1]*x', -10, 10)
	f3.SetParameter(0, 0.5)
	f3.SetParameter(1, 1)
	g.Fit(f3, 'Q', "lalala", self.links, self.rechts)
	f3.SetRange(-10., 10.)



	self.func1 = f
	self.func2 = f2
	self.func3 = f3

        self.graph = g
	

 	# Erzeuge Graphen
        g2 = TGraph(count, array('d',self.energie) ,array('d',self.trans))
        g2.SetTitle(';Winkel [#circ];Spannung U [V]')
        g2.GetHistogram().SetTitleOffset(1.3, 'Y')
        g2.SetMarkerStyle(2)
	g2.SetMarkerColor(4)
        g2.SetMarkerSize(1.0)

	f4 = TF1('f', '[0] + [1]*x', -10, 10)
	f4.SetParameter(0, 0.5)
	f4.SetParameter(1, 1)
	g2.Fit(f4, 'Q', "lalala", self.links, self.rechts)
	f4.SetRange(-10., 10.)

	self.func4 = f4
        self.graph2 = g2
	h = g.GetHistogram()
	h.SetMinimum(0)
        h.SetMaximum(1.6)

	# Zeichnen des 'normalen Graphen'
    def draw(self, title):
       	c = TCanvas('c_'+title, title)
       	self.canvas = c
       	c.SetGrid()
	#self.func1.Draw('C')
       	self.graph.Draw('AP')
	self.graph2.Draw('P')
	#c.Add(self.func1)
	self.func1.Draw('SAME')
	self.func2.Draw('SAME')
	self.func3.Draw('SAME')
	self.func3.Draw('SAME')
	self.func4.Draw('SAME')
       	c.Update()
    
    def setAxis(self, x,y):
	xa = self.graph.GetXaxis()
        xa.SetLimits(x, y)

		

# Untergrund abziehen
def winkellinks(winkel, messung):
	return findWinkel(winkel, "links", messung)

def findWinkel(winkel, richtung, messung):
	return messung.winkel[iToWinkel(winkel, richtung, messung)]

def iToWinkel(winkel, richtung, messung):
	i = 0
	a = 0
	countmess = len(messung.winkel)
	while(messung.winkel[i] > winkel and i != countmess -1):
		i += 1
	if i == 0:
		while(messung.winkel[countmess -1 - i] > winkel and i != countmess -1):
			i += 1
		i = countmess -1 -i
		a = 1
	if richtung == "rechts":
		if a == 0 or i == (countmess -1):
			i -= 1
		elif a == 1 and i != (countmess -1):
			i += 1
	return i

def winkelrechts(winkel, messung):
	return findWinkel(winkel, "rechts", messung)

def translinks(winkel, messung):
	return messung.trans[iToWinkel(winkel, "links", messung)]

def absorrechts(winkel, messung):
	return messung.absor[iToWinkel(winkel, "rechts", messung)]

def absorlinks(winkel, messung):
	return messung.absor[iToWinkel(winkel, "links", messung)]

def transrechts(winkel, messung):
	return messung.trans[iToWinkel(winkel, "rechts", messung)]



def tugrund(winkel, grund):
	xlinks = winkellinks(winkel, grund)
	xrechts = winkelrechts(winkel, grund)
	ylinks = translinks(winkel, grund)
	yrechts = transrechts(winkel, grund)
	steigung = (yrechts - ylinks) / (xrechts - xlinks)
	return (winkel - xlinks) * steigung + ylinks

def augrund(winkel, grund):
	xlinks = winkellinks(winkel, grund)
	xrechts = winkelrechts(winkel, grund)
	ylinks = absorlinks(winkel, grund)
	yrechts = absorrechts(winkel, grund)
	steigung = (yrechts - ylinks) / (xrechts - xlinks)
	return (winkel - xlinks) * steigung + ylinks

def leistunglampe(winkel, lampe):
	xlinks = winkellinks(winkel, lampe)
	xrechts = winkelrechts(winkel, lampe)
	ylinks = translinks(winkel, lampe)
	yrechts = transrechts(winkel, lampe)
	steigung = (yrechts - ylinks) / (xrechts - xlinks)
	return (winkel - xlinks) * steigung + ylinks

def ladeMessung(messung, untergrund, spektrum, xmin, xmax, links, rechts):
	mess1 = Messung(messung, links, rechts)
	mess1.setAxis(xmin, xmax)
	
	# Lade Untergrund
	mess1.ugrund = Messung(untergrund, links, rechts)
	# Lade Lampenspektrum
	mess1.lampe = Messung(spektrum, links, rechts)

	for i in range(len(mess1.time)):
		winkel = mess1.winkel[i]
		trans = (mess1.trans[i]-tugrund(winkel, mess1.ugrund)) / leistunglampe(winkel, mess1.lampe)
		absor = (mess1.absor[i]-augrund(winkel, mess1.ugrund)) / leistunglampe(winkel, mess1.lampe)
		mess1.trans[i] = trans
		mess1.absor[i] = absor
	return mess1

def findMaximum(messreihe, winkel, links, rechts):
	actual = 0.
	a = 0
	for i in messreihe:
		if winkel[a] > links and winkel[a] < rechts and actual < i:
			actual = i
		a += 1
	#print actual
	return actual

def findMinimum(messreihe, winkel, links, rechts):
	actual = 10.
	a = 0
	for i in messreihe:
		if winkel[a] > links and winkel[a] < rechts and actual > i:
			actual = i
		a += 1
	print actual
	return actual



grge1 = ladeMessung( "grge1.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", 0.63, 0.75, 0.68, 0.7)
grge1b = ladeMessung( "grge1.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", -0.76, -0.63, -0.7, -0.68)

grge2 = ladeMessung("grge2.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", 0.63, 0.76, 0.68, 0.7)
grge2b = ladeMessung("grge2.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", -0.75, -0.63, -0.7, -0.68)

grgeb1 = ladeMessung("grgeblende1cm.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", 0.63, 0.74, 0.68, 0.7)
grgeb1b = ladeMessung("grgeblende1cm.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", -0.76, -0.63, -0.7, -0.68)

grgeb2 = ladeMessung("grgeblende1cm2.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", 0.62, 0.75, 0.68, 0.7)
grgeb2b = ladeMessung("grgeblende1cm2.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", -0.76, -0.63, -0.7, -0.68)


grge1.draw("grge1")

grge1b.draw("grge1b")

grge2.draw("grge2")

grge2b.draw("grge2b")
grgeb1.draw("grgeb1")
grgeb1b.draw("grgeb1b")
grgeb2.draw("grgeb2")
grgeb2b.draw("grgeb2b")

line = sys.stdin.readline()
     




















