#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hanle-Signal-Abhaengigkeit zum Gasdruck
# -------------------------------------------------------------------

# Die Lorentz-Verteilung mit linearem Term
# lorentz(x) = y0 + 2*A/pi * w/(4*(x-xc)^2 + w^2) + b*x
#
# [0] y0 : Offset
# [1] A  : Flaeche
# [2] w  : Breite
# [3] xc : Peak
# [4] b  : lineare Steigung
lorentz = '[0] + 2*[1]/pi * [2]/(4*(x-[3])^2 + [2]^2) + [4]*x'

class Messung:
    '''Klasse zur Handhabung der Messungen'''

    def __init__(self, name, temp):
        '''name: Dateiname der Messwerte
        t12: Tupel aus Anfangs- und Endtemperatur'''
        
        self.name = name
        self.temperatur = float(temp)
        self.fitted = False

        # Lese Messdaten ein
	i = 0
        t, y, x = array('d'), array('d'), array('d')
        for line in open(name, 'r'):
	    if i == 0:
 		i = 2
            else:
		linenew = line.replace(',', '.')
            	tl, yl, xl = map(float, linenew.split())
            	x.append(xl); y.append(yl); t.append(tl)
        sx = array('d', [0.00001]*len(x))
        sy = array('d', [0.01]*len(x))

        # Erzeuge Graphen aus den Messdaten
        g = TGraphErrors(len(x), x ,y, sx, sy)
        g.SetTitle(';Spulenstrom [A];Intensit#ddot{a}t')
        g.SetMarkerColor(2)
        g.SetMarkerStyle(3)
        self.graph = g

    def fit(self, params, fitopt='QR'):
        '''Fittet Messdaten und berechnet die FWHM
        params: Anfangswerte der Fitparameter
        fitopt: Fitoptionen fuer ROOT'''

        self.fitted = True
        params = array('d', params)
	p = array('d')

        # Erstelle Lorentzfunktion-Objekt
        f = TF1('f'+self.name, lorentz, -0.76, 0.64)
        f.SetNpx(1000)
        f.SetParameters(params)
        self.fcn = f

        # Fitte und speichere Ergebnisse
        self.graph.Fit(f, fitopt)
        f.GetParameters(params)
        self.y0, self.A, self.w, self.xc, self.b = float(params[0]),float(params[1]),float(params[2]),float(params[3]),float(params[4])
        p = f.GetParErrors()
        self.sy0, self.sA = p[0], p[1]
	self.sw = f.GetParError(2)
        self.sxc,self.sb = p[3], p[4]
        self.rchisq = f.GetChisquare() / float(f.GetNDF())
        self.fwhm = abs(self.w)
        self.sfwhm = self.sw

    def draw(self, drawopt='AP'):
        '''Zeichnet den Graph der Messung
        drawopt: Zeichenoptionen fuer ROOT'''
        
        c = TCanvas('c'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        
        self.graph.Draw(drawopt)

        l = TLegend(0.55, 0.14, 0.88, 0.34)
        l.SetFillColor(0)
        l.AddEntry(self.graph,'Messreihe '+self.name, 'p')
        l.AddEntry(self.fcn,'Fit: Lorenzkurve', 'l')
        l.AddEntry(self.fcn,'y_{0} = %.4g #pm %s.4g' % (self.y0,self.sy0),'')
        l.AddEntry(self.fcn,'A = %.4g #pm %s.4g' % (self.A,self.sA),'')
        l.AddEntry(self.fcn,'w = %.4g #pm %s.4g' % (self.w,self.sw),'')
        l.AddEntry(self.fcn,'x_{c} = %.4g #pm %s.4g' % (self.xc,self.sxc),'')
        l.AddEntry(self.fcn,'#chi^{2}/ndf = %.4g' % self.rchisq,'')
        l.Draw()
        self.legend = l
            
        c.Update()

# lese Temperaturen und Messdaten zur 90° Messung ein
#t90 = [map(float,line.split()) for line in open('90/temp.dat','r')]
m90 = [Messung('data/90GRAD/%s.tab'%i, (float(i)-36.)*5./9.) for i in range(17, 57)]

# lese Temperaturen und Messdaten zur 0° Messung ein
#t0 = [map(float,line.split()) for line in open('0/temp.dat','r')]
m0 = [Messung('data/0GRAD/%s.tab'%i, (float(i)-36.)*5./9.) for i in range(23, 57)]

# Anfangswerte fuer die Fit-Parameter
params0 = [0.4, 0.16, 0.2, -0.05, -0.02]
params90 = [0.85, -0.14, 0.2, -0.06, 0.02]

# Fitte die Messwerte der 90° Messreihe an die Lorentzverteilung und
# sichere Temperatur und Halbwertsbreite in einer Datei
f = open('fwhm90.dat', 'w')
for m in m90:
    m.fit(params90)
    #m.draw()
    if m.rchisq < 10:
        tm = m.temperatur
        print '%s: chisq/ndf=%.2f, t=%.2f, fwhm=%.3f' % (
            m.name, m.rchisq, tm, m.fwhm)
        f.write(m.name)
        f.write(' %f %f %s %f\n' % (tm, m.fwhm, m.sfwhm, m.rchisq))
    else:
        print '%s: Fit nicht möglich!' % m.name
f.close()

# Fitte die Messwerte der 0° Messreihe an die Lorentzverteilung und
# sichere Temperatur und Halbwertsbreite in einer Datei
f = open('fwhm0.dat', 'w')
for m in m0:
    m.fit(params0)
    if m.rchisq < 10:
        tm = float(m.temperatur)
        print '%s: chisq/ndf=%.2f, tm%.2f, fwhm=%.3f' % (
            m.name, m.rchisq, tm, m.fwhm)
        f.write(m.name)
        f.write(' %f %f %s %f\n' % (tm, m.fwhm, m.sfwhm, m.rchisq))
    else:
        print '%s: Fit nicht möglich!' % m.name
f.close()
line = sys.stdin.readline()
