#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import pi, sqrt, exp
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name, distance, voltage, lowerFitrange, upperFitrange):
        self.name = name
        self.dist = distance
        self.volts = voltage
        self.lower = float(lowerFitrange)
        self.upper = float(upperFitrange)

    # Lese Messdaten ein	
        data = []
        for line in open('data/haynes_shockley/'+ name, 'r').readlines()[18:]:
            data.append(line.strip().strip(',').split())
        self.time = [float(z[0].strip(',')) for z in data]
        self.U = [float(z[1]) for z in data]
        count = len(self.time)
        print 'Found %i datapoints in %s'%(count, name)
        
    # Erzeuge Graphen
        g = TGraph(count, array('d',self.time) ,array('d',self.U))
        g.SetTitle(';Zeit t [s];Spannung U [V]')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(1)
        g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g

    # Gaussfit ohne Korrektur
    def fit(self):
        f = TF1('f_'+self.name, '[0]/sqrt(2*pi*[1]) * exp(-0.5*((x-[2])/[1])^2) + [3]', self.lower, self.upper)
        f.SetParameters(array('d', [1e-5,1e-05,1e-5,0]))
        self.graph.Fit(f, 'QR')
        self.amp, self.samp = f.GetParameter(0), f.GetParError(0)
        self.sigma, self.ssigma = f.GetParameter(1), f.GetParError(1)
        self.ort, self.sort = f.GetParameter(2), f.GetParError(2)
        self.off, self.soff = f.GetParameter(3), f.GetParError(3)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        #print 'Amplitude: %g, sigma: %g, ort: %g, off: %g'%(self.amp, self.sigma, self.ort, self.off)


    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('AP')
        #self.test.Draw('AP')
        c.Update()


    # Speichere Plots
    def save_plot(self):
        self.canvas.SaveAs('eps/%s.eps' % self.name[:-4])

            
# Hilfsroutine zum Einlesung der Daten bei Messung variablen Abstandes
def lade_varDist(dateiname):
    m = []
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = Messung(
            name = v[0],
            distance = v[3],
            voltage = v[4],
            lowerFitrange = v[5],
            upperFitrange = v[6])
        m += [mi]
    return m
