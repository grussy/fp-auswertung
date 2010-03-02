#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph

gROOT.SetStyle("Plain")

#Energie eichung des Multikanalanalysators

#Messübersichtdatei (hier stehen die Dateinamen der Datendateien und alle nötigen Einstellungen der jeweiligen Messreihen)
messuebersicht = 'messuebersicht_eichung.dat'

#Klasse Messung (zum auslesen der Messdaten, plotten, fitten)
class Messung:
	#name(string):Dateiname, K_energie(float):Energie des
    def __init__(self, name, K_energie, initheight, initwidth, initplace):
        self.name = name
	self.kenergie = K_energie
	self.fitparameter = fitparameter
	self.counts = []
	dataline = 0
	for line in open('data/'+name+'.ICE','r'):
		if dataline == 0:
			if line == 'A004USERDEFINED':
				dataline = 1
		else:
			for word in line[1:]:
				self.counts.append(word)
	self.channel = []*len(self.counts)
		
	# Erzeuge Graphen
        g = TGraph(count, array('d',self.channel) ,array('d',self.counts))
        g.SetTitle(';Counts;Channel')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(1)
	g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g

	# Zeichnen des 'normalen Graphen'
    def draw(self):
	c = TCanvas('c_'+self.name, self.name)
	self.canvas = c
	c.SetGrid()
	self.graph.Draw('AP')
	c.Update()

def load(dateiname=messuebersicht):
	m = []
	# readlines()[1:] means start at index 1 so second row
	for line in open(dateiname, 'r').readlines()[1:]:
		if not line.strip() or line.strip()[0] == '#': continue
		v = line.split()
		mi = Messung(
			name = v[0],
			K_energie = v[1],
			initplace = v[2],
			initwidth = v[3],
			initheight = v[4])
		m += [mi]
	return m

messungen = load()
for m in messungen:
	m.draw()

raw_input();




