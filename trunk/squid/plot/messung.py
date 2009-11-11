#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Hilfsroutinen und Klassen zur Handhabung der Messungen
# -------------------------------------------------------------------

# Klasse zum Einlesen, Fitten und Plotten der Messungen
class Messung:
    def __init__(self, name):
        self.name = name

        # Lese Messdaten ein	
	data = []
	for l in open('data/'+name,'r'):
		data.append(map(float,[float(l.strip().strip(',').split(',')[0])*omega*360./(2.*pi),l.strip().strip(',').split(',')[1]]))
        count = len(data)
        self.deg = [z[0] for z in data]
        self.U = [z[1] for z in data]

        # Erzeuge Graphen
        g = TGraph(count, array('d',self.deg) ,array('d',self.U))
        g.SetTitle(';Winkel [#circ];Spannung U [V]')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(1)
	g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g

        # Erzeuge Vektordiagramm
        self.Um = 1./len(self.U) * sum(self.U)
        self.x = [abs(Ui - self.Um)*cos(pi/180.*degi) for Ui,degi in zip(self.U,self.deg)]
        y = [abs(Ui - self.Um)*sin(pi/180.*degi) for Ui,degi in zip(self.U,self.deg)]
	mg = TMultiGraph()
        vg = TGraph(count, array('d',self.x), array('d',y))
	mg.Add(vg)
        vg.SetTitle('')
        self.vgraph = mg

        # Auf beiden Achsen den selben Wertebereich für das Vektordiagramm
        xa = vg.GetXaxis()
        h = vg.GetHistogram()
        mmin = min(xa.GetXmin(), h.GetMinimum())
        mmax = max(xa.GetXmax(), h.GetMaximum())
        xa.SetLimits(mmin, mmax)
        h.SetMinimum(mmin)
        h.SetMaximum(mmax)

    # Sinusfit mit Steigung an die Messdaten
    def fitm(self):
        f = TF1('f_'+self.name, '[0] + [3] * x + [1]*sin(pi/180*x + [2])')
        f.SetParameters(array('d', [0,0,0,0]))
        self.fcn = f
        self.graph.Fit(f, 'Q')
        self.a, self.sa = f.GetParameter(0), f.GetParError(0)
        self.b, self.sb = f.GetParameter(1), f.GetParError(1)
        self.c, self.sc = f.GetParameter(2), f.GetParError(2)
        self.d, self.sd = f.GetParameter(3), f.GetParError(3)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        self.dU = 2.*abs(self.b)
        self.sdU = 2.*self.sb

    # Sinusfit ohne Steigung an die Messdaten
    def fito(self):
        f = TF1('f_'+self.name, '[0] + [1]*sin(pi/180*x + [2])')
        f.SetParameters(array('d', [0,0,0]))
        self.fcn = f
        self.graph.Fit(f, 'Q')
        self.a, self.sa = f.GetParameter(0), f.GetParError(0)
        self.b, self.sb = f.GetParameter(1), f.GetParError(1)
        self.c, self.sc = f.GetParameter(2), f.GetParError(2)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        self.dU = 2.*abs(self.b)
        self.sdU = 2.*self.sb

    # Sinusfit ohne Steigung an die Messdaten
    def fits(self):
        f = TF1('f_'+self.name, '[0] + [1]*sin([3]*x+[4])*sin(pi/180*x + [2])')
        f.SetParameters(array('d', [0.1,1000,0,5,0]))
        self.fcn = f
        self.graph.Fit(f, 'Q')
        self.a, self.sa = f.GetParameter(0), f.GetParError(0)
        self.b, self.sb = f.GetParameter(1), f.GetParError(1)
        self.c, self.sc = f.GetParameter(2), f.GetParError(2)
        self.chisq = f.GetChisquare()
        self.ndf = f.GetNDF()
        self.rchisq = self.chisq/self.ndf
        self.dU = 2.*abs(self.b)
        self.sdU = 2.*self.sb
    # Zeichnen des 'normalen Graphen'
    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('AP')
        c.Update()

    # Zeichnen des Vektordiagramms
    def vdraw(self):
        cv = TCanvas('cv_'+self.name, self.name+' (Vektordiagramm)',600,600)
        self.vcanvas = cv
	ytheo = [self.a + self.d * xi + self.b*sin(pi/180*xi + self.c) for xi in self.x]
	vf = TGraph(len(self.x), array('d',self.x), array('d',ytheo))
	vf.SetMarkerColor(2)
	#self.vgraph.Add(vf)
        self.vgraph.Draw('AL')
        cv.Update()

    # Speichere Plots
    def save_plots(self):
        self.canvas.SaveAs('plots/%s.eps' % self.name[:-4])
        self.vcanvas.SaveAs('plots/%s_v.eps' % self.name[:-4])

# Spezialisierung fuer Schleifenmessungen
class MessungSchleife(Messung):
    def __init__(self, name, bez, time, volts, speed):
        Messung.__init__(self, name)
        self.bez = bez
        self.time = time
	self.volts = volts
	self.speed = speed
	self.Ubat = 2.92
	self.omega = 0.8741
        self.R = {'R1':51.47, 'R2':100.8, 'R3':300.8, 'R4':510.6, 'R5':1000}[bez]
        self.si = 1900e-3 # former :{'x1':10., 'x10':1., 'x100':0.1}[sens] They did Bullshit!! We used 100kOhm = 1900 mV/Phi_0
        self.Ibat = self.Ubat/self.R

# Spezialisierung fuer die Gegenstaende
class MessungGegenstand(Messung):
    def __init__(self, name, bez, FeedbR):
        Messung.__init__(self, name)
        self.bez = bez
        self.si = {'1':21., '3':60., '6':120., '10':195., '15':290., '20':380., '50':950., '100':1900. }[FeedbR] / (phi0*1e3)
        
# Hilfsroutine zum Einlesen aller Schleifenmessungen
def lade_schleife(dateiname='data/schleife.dat'):
    m = []
    # readlines()[1:] means start at index 1 so second row
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = MessungSchleife(
            bez = v[0],
            name = v[1],
            time = v[2],
            volts = v[3],
            speed = v[4])
        m += [mi]
    return m
            
# Hilfsroutine zum Einlesung aller Gegenstandsmessungen
def lade_gegenstaende(dateiname='data/gegenstaende.dat'):
    m = []
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = MessungGegenstand(
            bez = v[0],
            name = v[1] + '.csv',
            FeedbR = v[2])
        m += [mi]
    return m
