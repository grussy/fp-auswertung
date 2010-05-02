#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import pi, cos, sin, sqrt
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")

########################################################
#                   Energie eichung des Multikanalanalysators
# Dieses Programm nimmt die Energieeichung des MCA bei dem Mössbauer-Effekt im FP II vor
#########################################################

# Messübersichtdatei (Dateinamen der Datendateien und alle nötigen Einstellungen der jeweiligen Messreihen)
messuebersicht = 'messuebersicht_eichung.dat'

#Klasse Messung (zum auslesen der Messdaten, plotten, fitten)
class Messung:

    def __init__(self, name, K_energie, fitparams, fitrange, fitdouble):
        self.name = name
        self.kenergie = K_energie
        self.fitparameter = fitparams
        self.counts = []
        self.fitrange = fitrange
        self.double = fitdouble
        dataline = 0
        for line in open(name+'.IEC','r'):
            if dataline == 0:
                if 'A004USERDEFINED' in line:
                    dataline = 1
            else:
                for word in line.split()[2:]:
                    if word != "":
                        self.counts.append(float(word))
        self.count = len(self.counts)
        self.channel = [i for i in range(self.count)]
        self.scounts = [200]*self.count
        self.schannel = [1]*self.count
        # Erzeuge Graphen
        g = TGraphErrors(self.count, array('d',self.channel) ,array('d',self.counts),
            array('d',self.schannel) ,array('d',self.scounts))
        g.SetTitle(';Channel;Counts')
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
        self.graph.Draw('APX')
        lg = TLegend(0.47, 0.64, 0.88, 0.84)
        lg.SetFillColor(0)
        lg.AddEntry(self.graph, 'Messreihe:'+ self.name, 'p')
        lg.AddEntry(self.fitfkt, 'Gaußfit', 'l')
        lg.AddEntry(self.fitfkt, 'Schwerpkt = %.4f #pm %.4f' % (self.ort,self.sort), '')
        lg.AddEntry(self.fitfkt, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
            self.chisq, self.ndf, self.rchisq), '')
        self.legend = lg
        self.legend.Draw()
        c.Update()

    # Gaussfit ohne Korrektur
    def fit(self):
        if (self.double == 1):
            f = TF1('f_'+self.name, '(([0]/(sqrt(2*pi)*[1])) * exp(-0.5*(((x-[2])/[1])^2))) + (([4]/(sqrt(2*pi)*[5])) * exp(-0.5*(((x-[6])/[5])^2))) + [3]', self.fitrange[0], self.fitrange[1])
            f.SetMarkerColor(2)
            f.SetParameters(array('d', self.fitparameter))
            self.graph.Fit(f, 'MQR')
            self.fitfkt = f
            self.amp, self.samp = f.GetParameter(0), f.GetParError(0)
            self.sigma, self.ssigma = f.GetParameter(1), f.GetParError(1)
            self.ort, self.sort = f.GetParameter(2), f.GetParError(2)
            self.off, self.soff = f.GetParameter(3), f.GetParError(3)
            self.chisq = f.GetChisquare()
            self.ndf = f.GetNDF()
            self.rchisq = self.chisq/self.ndf
        else:
            f = TF1('f_'+self.name, '(([0]/sqrt(2*pi*[1])) * exp(-0.5*(((x-[2])/[1])^2))) + [3]', self.fitrange[0], self.fitrange[1])
            f.SetMarkerColor(2)
            f.SetParameters(array('d', self.fitparameter))
            self.graph.Fit(f, 'MQR')
            self.fitfkt = f
            self.amp, self.samp = f.GetParameter(0), f.GetParError(0)
            self.sigma, self.ssigma = f.GetParameter(1), f.GetParError(1)
            self.ort, self.sort = f.GetParameter(2), f.GetParError(2)
            self.off, self.soff = f.GetParameter(3), f.GetParError(3)
            self.chisq = f.GetChisquare()
            self.ndf = f.GetNDF()
            self.rchisq = self.chisq/self.ndf

def load(dateiname=messuebersicht):
    m = []
    # readlines()[1:] means start at index 1 so second row
    for line in open(dateiname, 'r').readlines()[1:]:
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        double = 0
        pars = [float(v[4]), float(v[3]), float(v[2])]
        if (v[7] == 'yes'):
            double = 1
            pars = [float(v[4]), float(v[3]), float(v[2]),float(v[10]), float(v[9]), float(v[8])]
        mi = Messung(
            name = v[0],
            K_energie = v[1],
            fitparams = pars, #hoehe, breite, ort
            fitrange = [float(v[5]), float(v[6])],
            fitdouble = double)
        m += [mi]
    return m

print "\nLoading ..."
messungen = load()

x,y,sy,sx=[],[],[],[]
print "\nFiting and Drawing ..."
for m in messungen:
    m.fit()
    m.draw()
    x.append(float(m.kenergie))
    sx.append(0.01)
    y.append(float(m.ort))
    sy.append(float(m.sort))

print "\nCalculating ..."
g = TGraphErrors(len(x), array('d',x) ,array('d',y),array('d',sx),array('d',sy))
g.SetTitle(';Energie [keV];Kanal')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
f = TF1('Eichgerade', '[0]*x+[1]')
f.SetMarkerColor(2)
f.SetMarkerStyle(6)
f.SetParameters(120,1000)
g.Fit(f, 'MQE', 'X')
a, sa = f.GetParameter(0), f.GetParError(0)
b, sb = f.GetParameter(1), f.GetParError(1)
chisq = f.GetChisquare()
ndf = f.GetNDF()
rchisq = chisq/ndf
c = TCanvas('Eichung', 'eichung')
c.SetGrid()
g1.Draw('APX')
lg = TLegend(0.47, 0.14, 0.88, 0.34)
lg.SetFillColor(0)
##lg.AddEntry(g1, 'Messreihe: Energieeichung.dat', 'p')
##lg.AddEntry(f1, 'Linearer Fit: ax+b', 'l')
##lg.AddEntry(f1, 'a = %.4f #pm %.4f' % (a,sa), '')
##lg.AddEntry(f1, 'b = %.4f #pm %.4f' % (b,sb), '')
##lg.AddEntry(f1, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
##    chisq, ndf, rchisq), '')
lg.Draw()
c.Update()
print "\nDone. Press Enter to continue ..."
raw_input();




