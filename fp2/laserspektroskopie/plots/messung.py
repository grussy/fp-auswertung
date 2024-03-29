#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
import sys; sys.path.append('/usr/lib/root/')
from oszi import OsziData
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
from frequenz_eichung import mw


#######################################################
#
# Messung aus Oszidaten mit graphen für kanäle und plot funktion
#
#######################################################


# Oszidata ( String dateinummer XX, String Beschreibung )
#test = OsziData('04', 'Dopplerverbreitert Messung 3')
class Messung:
    def __init__(self, dateiNummer, beschreibung, freqLineal):
        self.nummer = dateiNummer
        self.beschreibung = beschreibung
        self.freqLineal = freqLineal
        self.data = OsziData(self.nummer, self.beschreibung)
        if self.data.ch1 != 0:
            if self.freqLineal != 0:
                cutData(self.data.ch1.y, self.freqLineal)
                self.freqLineal, self.sfreqLineal = calcLineal(self.data.ch1)
##                print self.freqLineal
            self.graph1 = TGraphErrors(len(self.data.ch1.x), array('d',self.data.ch1.x), array('d', self.data.ch1.y), array('d', [1e-5]*len(self.data.ch1.x)), array('d', [1e-3]*len(self.data.ch1.x)))
        
        if self.data.ch2 != 0:
            self.graph2 = TGraphErrors(len(self.data.ch2.x), array('d',self.data.ch2.x), array('d', self.data.ch2.y), array('d', [1e-5]*len(self.data.ch1.x)), array('d', [1e-1]*len(self.data.ch1.x)))

    def createCanvas(self, can):
        self.canvas = can
        self.canvas.SetGrid()
        self.mgraph = TMultiGraph()
    def draw1(self):
        #c = TCanvas('cre', 'lalala')
        #self.can = c
        self.graph1.SetTitle('%s;Zeit / %s; Spannung / %s' % (self.beschreibung, self.data.ch1.xUnits, self.data.ch1.yUnits))
        self.graph1.GetHistogram().SetTitleOffset(1.3, 'Y')
        self.graph1.GetYaxis().CenterTitle()
        self.graph1.SetMarkerColor(3)
        self.graph1.SetMarkerStyle(1)
        self.mgraph.Add(self.graph1, 'P')
        #self.can.Update()
        
    def draw2(self):
        #self.graph2.SetTitle(';Zeit / %s; Spannung / %s' % (self.data.ch2.xUnits, self.data.ch2.yUnits))
        #self.graph2.GetHistogram().SetTitleOffset(1.3, 'Y')
        #self.graph2.GetYaxis().CenterTitle()
        self.graph2.SetMarkerColor(2)
        self.graph2.SetMarkerStyle(2)
        self.legend = TLegend(0.7, 0.8, 1, 1)
        self.legend.SetFillColor(0)
        self.legend.SetHeader('Vierfacher Gaussfit')
        self.mgraph.Add(self.graph2, 'P')
        
    def plot(self):
        self.createCanvas(TCanvas(self.nummer, self.beschreibung))
        if self.data.ch1 != 0:
            self.draw1()
        if self.data.ch2 != 0:
            self.draw2()
        self.mgraph.Draw('A')
        self.canvas.Update()
def cutData(data, grenze):
    for i in range(len(data)):
        if data[i] < grenze: data[i] = 0.
##        print data[i]

def calcLineal(channel):
    return mw(findBigSpace(channel))

def findBigSpace(channel):
    liste = []
    for i in range(len(channel.y)):
        if channel.y[i] != 0:
            liste.append(channel.x[i])
    abstaende = []
    for i in range(len(liste)-1):
        abstaende.append(liste[i+1]-liste[i])
    grosseAbstaende = []
    for abstand in abstaende:
        if abstand > 0.5*max(abstaende):
            grosseAbstaende.append(abstand)
    return grosseAbstaende
    
    
    
def test():
    testmess = Messung('04', 'Dopplerverbreitert Messung 3', 0)
    testmess.plot()
    raw_input();
    
#test()
#raw_input();