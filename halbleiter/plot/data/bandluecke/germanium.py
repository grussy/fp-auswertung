#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import pi, cos, sin, sqrt
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")
mid = []
smid = []


# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name, links, rechts, haupt):
	global mid
	global smid
        self.name = name
	self.ugrund = 0
    	self.lampe = 0
	self.xmin = 0.5
	self.xmax = 1.
	self.ymax = 1.6
	self.links = links
	self.rechts = rechts
	self.haupt = haupt
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
	self.sabsor = [8.4788e-03]*count
	self.strans = [6.1214e-03]*count
	self.senergie = [0.0001]*count

 	# Erzeuge Graphen
        g = TGraphErrors(count, array('d',self.energie) ,array('d',self.absor), array('d', self.senergie), array('d', self.sabsor))
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
        g2 = TGraphErrors(count, array('d',self.energie) ,array('d',self.trans), array('d', self.senergie), array('d', self.strans))
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
	

	a = f3.GetParameter(1)
	b = f3.GetParameter(0)
	c = f.GetParameter(0)
	d = f4.GetParameter(1)
	e = f4.GetParameter(0)
	g = f2.GetParameter(0)

	errabsor = f3.GetParError(1)
	errtrans = f4.GetParError(1)

	if self.haupt:
		mittel, smittel = gew_mittel([abs(Schnittpunkt(a, b, c)), abs(Schnittpunkt(d, e, g))], [errabsor, errtrans])
		print "Messung %s: %.2f +- %.2f" % (self.name, mittel, smittel)
		mid += [mittel]
		smid += [smittel]
		

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
    
    def setAxis(self, xmin,xmax,ymax):
	xa = self.graph.GetXaxis()
        xa.SetLimits(xmin, xmax)
	h = self.graph.GetHistogram()
	h.SetMinimum(0)
        h.SetMaximum(ymax)

		

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

def ladeMessung(messung, untergrund, spektrum, xmin, xmax, ymax, links, rechts):
	mess1 = Messung(messung, links, rechts, 1)
	mess1.setAxis(xmin, xmax, ymax)
	
	# Lade Untergrund
	mess1.ugrund = Messung(untergrund, links, rechts, 0)
	# Lade Lampenspektrum
	mess1.lampe = Messung(spektrum, links, rechts, 0)

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
	#print actual
	return actual

def Schnittpunkt(a, b, c):
	return (c - b) / a

def gew_mittel(werte, fehler):
##    gew_mittel(list(float), list(float)) -> (float, float)
##    werte  : Liste der Messwerte 
##    fehler : Liste der Fehler
##    ->   Tupel (gx, sgx) aus gewichtetem Mittel und dessen Fehler
    suma = sumb = 0.
    for i in range(len(werte)):
        suma += werte[i] / fehler[i]**2
        sumb += 1. / fehler[i]**2
    return (suma/sumb, 1/sqrt(sumb))




grge1 = ladeMessung( "grge1.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", 0.63, 0.75, 1.6, 0.665, 0.72)
grge1b = ladeMessung( "grge1.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", -0.76, -0.63, 1.1, -0.725, -0.665)

grge2 = ladeMessung("grge2.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", 0.63, 0.76, 1.6, 0.675, 0.72)
grge2b = ladeMessung("grge2.txt", "Germanium_Untergrund.txt", "LampeLeistung.txt", -0.75, -0.63, 1.1, -0.72, -0.665)

grgeb1 = ladeMessung("grgeblende1cm.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", 0.63, 0.74, 0.9, 0.67, 0.72)
grgeb1b = ladeMessung("grgeblende1cm.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", -0.76, -0.63, 0.6, -0.72, -0.665)

grgeb2 = ladeMessung("grgeblende1cm2.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", 0.62, 0.75, 0.9, 0.67, 0.715)
grgeb2b = ladeMessung("grgeblende1cm2.txt", "Germanium_Untergrund.txt", "grspektrumblende1cm.txt", -0.76, -0.63, 0.6, -0.72, -0.674)


grge1.draw("grge1")

grge1b.draw("grge1b")

grge2.draw("grge2")

grge2b.draw("grge2b")
grgeb1.draw("grgeb1")
grgeb1b.draw("grgeb1b")
grgeb2.draw("grgeb2")
grgeb2b.draw("grgeb2b")

mittelwert, smittelwert = gew_mittel(mid, smid)
print "Mittelwert: %.3f +- %.3f" % (mittelwert, smittelwert)

line = sys.stdin.readline()
     




















