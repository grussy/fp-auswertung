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
        self.sdist = 0.5

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
        g.SetMarkerStyle(20)
        g.SetMarkerColor(2)
        g.SetMarkerSize(0.2)
        self.graph = g

    # Gaussfit ohne Korrektur
    def fit(self, initParams):
        f = TF1('f_'+self.name, '[0]/sqrt(2*pi*[1]) * exp(-0.5*((x-[2])/[1])^2) + [3]', self.lower, self.upper)
        f.SetParameters(array('d', initParams))
        self.graph.Fit(f, 'QR')
        self.amp, self.samp = f.GetParameter(0), f.GetParError(0)
        self.sigma, self.ssigma = f.GetParameter(1), f.GetParError(1)
        self.ort, self.sort = f.GetParameter(2), f.GetParError(2)
        self.off, self.soff = f.GetParameter(3), f.GetParError(3)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        self.f = f
        #print 'Amplitude: %g, sigma: %g, ort: %g, off: %g'%(self.amp, self.sigma, self.ort, self.off)


    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('AP')
        #self.f.Draw('SAME')
        #self.test.Draw('AP')
        c.Update()


    # Speichere Plots
    def save_plot(self):
        self.canvas.SaveAs('eps/%s.eps' % self.name[:-4])

            
# Hilfsroutine zum Einlesung der Daten bei Messung variablen Abstandes
def lade_Daten(dateiname):
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

def arith_mittel(x):
    '''arith_mittel(list(float)) -> float
    x  : Liste aus Messwerte
    ->   arithmetisches Mittel der Messwerte'''
    sumx = 0.
    for xi in x:
        sumx += xi
    return sumx / len(x)
