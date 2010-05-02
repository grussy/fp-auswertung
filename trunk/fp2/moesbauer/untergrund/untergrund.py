#!/usr/bin/python 
# -*- coding: utf-8 -*-

from math import pi, cos, sin, exp, sqrt
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")

####################################################
#                   Untergrundmessung
# 
####################################################

# Messübersichtdatei (Dateinamen der Datendateien und alle nötigen Einstellungen der jeweiligen Messreihen)
messuebersicht = 'messuebersicht_untergrund.dat'

#Klasse Messung (zum auslesen der Messdaten, plotten, fitten)
class Messung:
    def __init__(self, name, Dicke, Messzeit, FehlerDicke, FehlerZeit):
        self.name = name
        self.dicke = float(Dicke)
        self.time = float(Messzeit)
        self.sdicke = float(FehlerDicke)
        self.stime = float(FehlerZeit)
        self.counts = []
        dataline = 0
        for line in open(name,'r'):
            if dataline == 0:
                if 'A004USERDEFINED' in line:
                    dataline = 1
            else:
                for word in line.split()[2:]:
                    if word != "":
                        self.counts.append(float(word))
        self.count = len(self.counts)
        self.channel = [i for i in range(self.count)]
            
        # Erzeuge Graphen
        g = TGraph(self.count, array('d',self.channel) ,array('d',self.counts))
        g.SetTitle(';Channel;Counts')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(1)
        g.SetMarkerColor(2)
        g.SetMarkerSize(3.0)
        self.graph = g

    # Zeichne Graphen
    def draw(self):
        c = TCanvas('c_'+self.name, self.name)
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('AP')
        c.Update()
    
    def getCounts(self, vonKanal, bisKanal):
        summe = sum(self.counts[vonKanal:bisKanal])
        return summe
    
    def getCps(self, vonKanal, bisKanal):
        cps = self.getCounts(vonKanal, bisKanal)/ self.time
        return float(cps)
    
    def getScps(self, vonKanal, bisKanal):
        scps = self.getCps(vonKanal, bisKanal) * sqrt((self.stime/self.time)**2 + (1/self.getCounts(vonKanal, bisKanal)))
        return scps
    
    def getDicke():
        return dicke

def load(dateiname=messuebersicht):
    m = []
    # readlines()[1:] means start at index 1 so second row
    for line in open(dateiname, 'r').readlines():
        if not line.strip() or line.strip()[0] == '#': continue
        v = line.split()
        mi = Messung(
            name = v[0],
            Dicke = v[1],
            Messzeit = v[2],
            FehlerDicke = v[3],
            FehlerZeit = v[4])
        m += [mi]
    return m

print "\nLoading ..."
messungen = load()

x,y,sy,sx=[],[],[],[]
print "\nFiting and Drawing ..."
for m in messungen:
    m.draw()
    print(m.dicke)
    print(m.getCps(900,1400))
    x.append(m.dicke)
    sx.append(m.sdicke)
    y.append(m.getCps(900,1400))
    sy.append(m.getScps(900,1400))

print "\nCalculating ..."
g = TGraphErrors(len(x), array('d',x) ,array('d',y),array('d',sx),array('d',sy))
g.SetTitle('Untergrundmessung;Dicke / mm;Counts / s')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1)
f = TF1('fit', '[0]*exp([1]*x) + [2]*exp([3]*x)')
f.SetMarkerColor(2)
g.Fit(f, 'QEW')
c = TCanvas('Eichung', 'eichung')
c.SetGrid()
g.Draw('AP')
c.Update()

# Hole Fitergebnisse
a1, sa1 = f.GetParameter(0), f.GetParError(0)
b1, sb1 = f.GetParameter(1), f.GetParError(1)
a2, sa2 = f.GetParameter(2), f.GetParError(2)
b2, sb2 = f.GetParameter(3), f.GetParError(3)

chisq = f.GetChisquare()
ndf = f.GetNDF()
rchisq = chisq/ndf

# Erzeuge die beiden ueberlagerten exp-Funktionen
exp1 = TF1('exp1', '[0]*exp([1]*x)', 0, 10)
exp1.SetLineColor(2)
exp1.SetParameter(0, a1)
exp1.SetParameter(1, b1)

exp2 = TF1('exp2', '[0]*exp([1]*x)', 0, 10)
exp2.SetLineColor(4)
exp2.SetParameter(0, a2)
exp2.SetParameter(1, b2)

exp1.Draw('same')
exp1.SetLineStyle(2)
exp2.Draw('same')
exp2.SetLineStyle(3)

# Berechne Comptonuntergrund [cps]
ug = a2 * exp(0)
sug = 1#ug*sqrt((sa2/a2)**2 + (sb2*b2)**2)

# Erzeuge und zeichne Legende
lg = legend = TLegend(0.47, 0.43, 0.88, 0.88)
lg.SetFillColor(0)
lg.AddEntry(g, 'Messwerte, Untergrund', 'p')
lg.AddEntry(f, 'Exp. Fit: f(x) = f_{1}(x) + f_{2}(x)','l')
lg.AddEntry(exp1, 'f_{1}(x) = a_{1} exp(b_{1} x)', 'l')
lg.AddEntry(exp2, 'f_{2}(x) = a_{2} exp(b_{2} x)', 'l')
lg.AddEntry(f, 'a_{1} = %.1f #pm %.1f' % (a1,sa1), '')
lg.AddEntry(f, 'b_{1} = %.3f #pm %.3f' % (b1,sb1), '')
lg.AddEntry(f, 'a_{2} = %.2f #pm %.2f' % (a2,sa2), '')
lg.AddEntry(f, 'b_{2} = %.4f #pm %.4f' % (b2,sb2), '')
lg.AddEntry(f, 'f_{2}(0) = %.2f #pm %.2f' % (ug,sug), '')
lg.AddEntry(f, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
    chisq, ndf, rchisq), '')
lg.Draw()       

c.Update()

print "\nDone. Press Enter to continue ..."
raw_input();




