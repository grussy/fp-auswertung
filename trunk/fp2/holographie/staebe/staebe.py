#!/usr/bin/python
# -*- coding: utf-8 -*-


#from konst import phi0, omega, somega
from math import pi, cos, sin, log
##from konst import Q, c, hbar, E0, omega0
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis
from fit_tools import *

gROOT.SetStyle("Plain")

##########################################################################
#                   Doppelbelichtungsholographie mit 3 Metallstaeben
# 
##########################################################################

class Stab:

    def __init__(self, name, fehler, stablaenge,deltad):
        self.name = name
        self.fehler = fehler
        self.stablaenge = stablaenge
        self.positions = []
        
        for line in open(self.name, 'r'):
            if (not line.strip()) or (line.strip()[0] == '#'): continue
            self.positions.append(float(line.split()[0]))
        
        self.oberkante = self.positions[0]
        self.unterkante = self.oberkante - self.stablaenge
        self.minima = []
        
        for pos in range(1, len(self.positions)):
            self.minima.append( self.positions[pos] - self.unterkante )
        # Erzeuge Graphen
        self.count = len(self.minima)
        self.lambd = 0.632816 #um
        self.x =[]
##        self.x.append(0.)
        self.cosines = 1.9#1.866
        self.d0 = 0
        self.d = []
##        self.d.append(0)
        self.d.append(self.d0)
        #deltad=0.5
        
        self.minima.reverse()
        self.x = [i for i in self.minima]
        self.count = len(self.x)
        self.sx = [0.05]*self.count
        for i in range(self.count):
            self.d.append(deltad/1)
            deltad += (2*self.lambd/self.cosines)
        self.sd = [self.fehler*d for d in self.d]
        
        g = TGraphErrors(self.count, array('d',self.x) ,array('d',self.d), array('d',self.sx) ,array('d',self.sd))
        g.SetTitle(';Abstand zum Einspannpunkt [cm]; Abstand zum ungebogenen Bild [um]')
        g.GetHistogram().SetTitleOffset(1, 'Y')
        g.SetMarkerStyle(1)
        g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g
        
    # Zeichne Graphen
    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('A*')
        c.Update()
        
    def ausgabe(self):
        print self.name
        print "Unterkante ist bei: %s" % self.unterkante
        print "Oberkante ist bei:  %s" % self.oberkante
        print "Stablaenge:          %s" % self.stablaenge
        print "biegung:"
        print self.d
        print "Positionen der Minima:"
        print self.x
        
    def fit(self):
        f = TF1('f', '[0]*(5*x**2 - ((x**3)/6))+[1]*x+[2]')
        #f = TF1('f', '[0]*(5*x**2 - ((x**3)/6))')
        f.SetParameters(0.01, 0.1, 0)
        f.SetLineColor(4); f.SetLineStyle(4); f.SetLineWidth(2)
        self.graph.Fit(f, 'IEQ+')
        lgg = create_fit_legend(
            f, 'f(x)', 'Polynomieller Fit', lpos = (0.58, 0.16, 0.88, 0.38))
        self.legend = lgg
        lgg.Draw()
        self.canvas.Update()
        b = 0.01
        c = 0.005
        self.Ela = (-12 * 0.03*9.81 )/(f.GetParameter(0)*b*c**3)
        self.sEla = self.Ela * f.GetParError(0)/f.GetParameter(0)
        print "%s : %g +- %g"% (self.name, self.Ela,self.sEla)

test = Stab("1.stab", 1e-2, 10.0, 0.55)
#test.ausgabe()
test.draw()
test.fit()

test2 = Stab("2.stab", 1e-2, 10.0, 1.1)
#test2.ausgabe()
test2.draw()
test2.fit()

test3 = Stab("3.stab", 1e-2, 10.0, 1.8)
#test3.ausgabe()
test3.draw()
test3.fit()

print "\nDone. Press Enter to continue ..."
raw_input();
