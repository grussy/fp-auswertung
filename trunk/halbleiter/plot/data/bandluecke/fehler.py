#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import pi, cos, sin, sqrt
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")
mid = []


# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name):
	global mid
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
	self.astdabw = stdabweichung(self.absor)
	self.tstdabw = stdabweichung(self.trans)
	print "Absorption: %.4e" % self.astdabw
	print "Transmission: %.4e" % self.tstdabw
	

		

def stdabweichung(reihe):
	N = len(reihe)
	print N
	mittelwert = Mittelwert(reihe)
	print mittelwert
	nreihe = []
	for i in reihe:
		nreihe += [(i - mittelwert)**2]
	

	s_x = sqrt(sum(nreihe) / (N - 1.))
	#print (1. / (N -1.))
	#print sum(reihe)
	return s_x
	
def Mittelwert(reihe):
	return sum(reihe) / len(reihe)

    


		
fehler = Messung("FehlerBalken.txt")




line = sys.stdin.readline()
     




















