#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin, log
##from konst import Q, c, hbar, E0, omega0
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis
##from fit_tools import *

gROOT.SetStyle("Plain")

##########################################################################################
#                   Doppelbelichtungsholographie mit 3 Metallstäben
# 
##########################################################################################

class Stab:

    def __init__(self, name, fehler, stablaenge):
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
        self.x = range(1,self.count+1)
        self.sx = [1e-15]*self.count
        self.sminima = [self.fehler]*self.count
        
        g = TGraphErrors(self.count, array('d',self.x) ,array('d',self.minima), array('d',self.sx) ,array('d',self.sminima))
        g.SetTitle('%s;x;y' % self.name)
        g.GetHistogram().SetTitleOffset(1.45, 'Y')
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
##        lg = TLegend(0.47, 0.64, 0.88, 0.84)
##        lg.SetFillColor(0)
##        lg.AddEntry(self.graph, 'Messreihe:'+ self.name, 'p')
##        lg.AddEntry(self.fitfkt, 'Gaußfit', 'l')
##        lg.AddEntry(self.fitfkt, 'Schwerpkt = %.4f #pm %.4f' % (self.ort,self.sort), '')
##        lg.AddEntry(self.fitfkt, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
##            self.chisq, self.ndf, self.rchisq), '')
##        self.legend = lg
##        self.legend.Draw()
        c.Update()
        
    def ausgabe(self):
        print self.name
        print "Unterkante ist bei: %s" % self.unterkante
        print "Oberkante ist bei:  %s" % self.oberkante
        print "Stablänge:          %s" % self.stablaenge
        print "Minima:"
        print self.minima
        print "Positionen der Minima:"
        print self.positions
        
    def fit(self):
        f = TF1('f', '[0]*(5*x**2 - x**3)/6+[1]*x+[2]')
        f.SetLineColor(4); f.SetLineStyle(4); f.SetLineWidth(2)
        self.graph.Fit(f, 'Q+')
        self.canvas.Update()

test = Stab("1.stab", 1e-2, 12.0)
test.ausgabe()
test.draw()
test.fit()

test2 = Stab("2.stab", 1e-2, 12.0)
test2.ausgabe()
test2.draw()
test2.fit()

test3 = Stab("3.stab", 1e-2, 12.0)
test3.ausgabe()
test3.draw()
test3.fit()


print "\nDone. Press Enter to continue ..."
raw_input();