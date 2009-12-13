#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import pi, sqrt, exp
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TGraphErrors

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Fehler der Treiberspannung
sU = 0.1
sDist = 2.08e-3

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name, distance, voltage, lowerFitrange, upperFitrange):
        self.name = name
        self.dist = distance
        self.volts = voltage
        self.lower = float(lowerFitrange)
        self.upper = float(upperFitrange)
        self.sdist = 0.5e-3

    # Lese Messdaten ein	
        data = []
        for line in open('data/haynes_shockley/'+ name, 'r').readlines()[18:]:
            data.append(line.strip().strip(',').split())
        self.time = [float(z[0].strip(',')) for z in data]
        self.U = [float(z[1]) for z in data]
        self.count = len(self.time)
        print 'Found %i datapoints in %s'%(self.count, name)
        xerrors = [1e-20 for i in range(self.count)]
        yerrors = [8.67e-4 for i in range(self.count)]
            
    # Erzeuge Graphen
        g = TGraphErrors(self.count, array('d',self.time) ,array('d',self.U), 
            array('d',xerrors), array('d',yerrors))
        g.SetTitle(';Zeit t [s];Spannung U [V]')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(20)
        g.SetMarkerColor(2)
        g.SetMarkerSize(0.4)
        self.graph = g

    # Gaussfit ohne Korrektur
    def fit(self, initParams):
        f = TF1('f_'+self.name, '[0]/sqrt(2*pi*[1]) * exp(-0.5*((x-[2])/[1])^2) + [3]', self.lower, self.upper)
        f.SetMarkerColor(2)
        f.SetParameters(array('d', initParams))
##        f.SetParLimits(0,5e-6,1e-3);
##        f.SetParLimits(1,1e-7,5e-4);
##        f.SetParLimits(2,1e-7,1e-4);
##        f.SetParLimits(3,-1,1);
        self.graph.Fit(f, 'QR')
        self.amp, self.samp = f.GetParameter(0), f.GetParError(0)
        self.sigma, self.ssigma = f.GetParameter(1), f.GetParError(1)
        self.ort, self.sort = f.GetParameter(2), f.GetParError(2)
        self.off, self.soff = f.GetParameter(3), f.GetParError(3)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        self.f = f


    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('APX')
        #self.f.Draw('SAME')
        c.Update()


    # Speichere Plots
    def savePlot(self):
        self.canvas.SaveAs('eps/%s.eps' % self.name[16:-7])

            
# Hilfsroutine zum Einlesung der Daten bei Messung variablen Abstandes
# dateiname ist tabelle.dat mit Infos �ber messungen. Dabei ist der Aufbau:
# Dateiname der CSV, nicht gelesen, nicht gelesen, Abstand, Treiberspannung, 
# untere Grenze des Fits, obere Grenze des Fits. initParams sind die
# Initialparameter des Fits

def lade_Daten(dateiname):
    m = []
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = Messung(
            name = v[0],
            distance = float(v[3])*1e-3,
            voltage = v[4],
            lowerFitrange = v[5],
            upperFitrange = v[6])
        m += [mi]
    return m

# Hilfsroutine zur Berechnung des gewichteten Mittelwerts
def GewMittel(werte, fehler):
    suma = sumb = 0.
    for i in range(len(werte)):
        suma += werte[i] / fehler[i]**2
        sumb += 1. / fehler[i]**2
    return (suma/sumb, 1/sqrt(sumb))
