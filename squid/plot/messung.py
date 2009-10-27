#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph

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
        deg = [z[0] for z in data]
        U = [z[1] for z in data]

        # Erzeuge Graphen
        g = TGraph(count, array('d',deg) ,array('d',U))
        g.SetTitle(';Winkel [#circ];Spannung U [V]')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(1)
        g.SetMarkerSize(3.0)
        self.graph = g

        # Erzeuge Vektordiagramm
        Um = 1./len(U) * sum(U)
        x = [abs(Ui - Um)*cos(pi/180.*degi) for Ui,degi in zip(U,deg)]
        y = [abs(Ui - Um)*sin(pi/180.*degi) for Ui,degi in zip(U,deg)]
        vg = TGraph(count, array('d',x), array('d',y))
        vg.SetTitle('')
        self.vgraph = vg

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
        self.R = {'R1':100, 'R2':510, 'R3':1000, 'R4':5100, 'R5':10000}[bez]
        self.si = 1 / phi0 # former :{'x1':10., 'x10':1., 'x100':0.1}[sens]
        self.Ibat = self.Ubat/self.R

# Spezialisierung fuer die Gegenstaende
class MessungGegenstand(Messung):
    def __init__(self, name, bez, mode, nrot, fitable,
                 filt='-', geschw=10, sens='x1'):
        Messung.__init__(self, name)
        self.bez = bez
        self.sens = sens
        self.mode = mode
        self.fitable = fitable
        self.filt = filt
        self.geschw = geschw
        self.nrot = nrot
        self.si = {'x1':10., 'x10':1., 'x100':0.1}[sens] / phi0
        
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
def lade_gegenstaende(dateiname='gegenstaende.dat'):
    m = []
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = MessungGegenstand(
            bez = v[0].replace('_',' '),
            mode = v[1],
            nrot = v[2],
            name = v[3],
            fitable = int(v[4]))
        m += [mi]
    return m
