#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
import sys; sys.path.append('/usr/lib/root/')
from oszi import OsziData
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors


#######################################################
#
# Zeigt die Verwendung von oszi.py
#
#######################################################


# Oszidata ( String dateinummer XX, String Beschreibung )
#test = OsziData('04', 'Dopplerverbreitert Messung 3')
class Messung:
    def __init__(self, dateiNummer, beschreibung):
        self.nummer = dateiNummer
        self.beschreibung = beschreibung
        self.data = OsziData(self.nummer, self.beschreibung)
        if self.data.ch1 != 0:
            self.graph1 = TGraph(len(self.data.ch1.x), array('d',self.data.ch1.x), array('d', self.data.ch1.y))
        if self.data.ch2 != 0:
            self.graph2 = TGraph(len(self.data.ch2.x), array('d',self.data.ch2.x), array('d', self.data.ch2.y))

    def createCanvas(self, can):
        self.canvas = can
        self.canvas.SetGrid()
        self.mgraph = TMultiGraph()
    def draw1(self):
        #c = TCanvas('cre', 'lalala')
        #self.can = c
        self.graph1.SetTitle(';Zeit / %s; Spannung / %s' % (self.data.ch1.xUnits, self.data.ch1.yUnits))
        self.graph1.GetHistogram().SetTitleOffset(1.3, 'Y')
        self.graph1.GetYaxis().CenterTitle()
        self.graph1.SetMarkerColor(2)
        self.graph1.SetMarkerStyle(3)
        self.mgraph.Add(self.graph1, 'P')
        #self.can.Update()
        
    def draw2(self):
        #self.graph2.SetTitle(';Zeit / %s; Spannung / %s' % (self.data.ch2.xUnits, self.data.ch2.yUnits))
        #self.graph2.GetHistogram().SetTitleOffset(1.3, 'Y')
        #self.graph2.GetYaxis().CenterTitle()
        self.graph2.SetMarkerColor(3)
        self.graph2.SetMarkerStyle(2)
        self.mgraph.Add(self.graph2, 'P')
        
    def plot(self):
        self.createCanvas(TCanvas(self.nummer, self.beschreibung))
        if self.data.ch1 != 0:
            self.draw1()
        if self.data.ch2 != 0:
            self.draw2()
        self.mgraph.Draw('A')
        self.canvas.Update()
def test():
    testmess = Messung('04', 'Dopplerverbreitert Messung 3')
    testmess.plot()
    raw_input();
    
#test()
#raw_input();