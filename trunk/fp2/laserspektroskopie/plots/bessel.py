#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import pi, cos, sin, sqrt
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
from Scientific.Physics.PhysicalQuantities import PhysicalQuantity as Q
from scipy.special import jn
gROOT.SetStyle("Plain")
# ROOT verfuegt leider nur ueber die Besselfunktionen J0 und J1,
# deshalb wird hier die Jn Implementierung von SciPy verwendet.
from scipy.special import jn
drawopts = 'AP'
sv = 1
draw = [0,1,2,3]
def load(index):
    retval = []
    retval.append([])
    retval.append([])
    if (index == -1): 
        for line in open('../daten/bessel.dat'):
            if (not line.strip()) or (line.strip()[0] == '#'): continue
            retval[0].append(float(line.split()[0]))
            retval[1] = [0]*len(retval[0])
    else:
        faktor = 48.4
        for line in open('../daten/bessel.dat'):
            if (not line.strip()) or (line.strip()[0] == '#'): continue
            data = line.split()[index+1]
            value = 0
            if (len(data.split(':')) > 1):
                value = (float(data.split(':')[1]) + float(data.split(':')[0]))/2
            else : value = float(data)
            retval[0].append(value/faktor)
            if (value != 0): retval[1].append((value/faktor)*sqrt((sv/value)**2+(sv/faktor)**2))
            else: retval[1].append(0.01)
    return retval
modulations = load(-1)[0]
xtheo = [float(x/20.) for x in range(0, 102)]
count = len(modulations)
smodulations = [0.01]*count
sdata = [0.01]*count
rawdata = [] #bessel index, data
srawdata = [] #bessel index, data
Fenster = TCanvas('cr', 'Charakterisierung der Frequenzmodulation')
Fenster.SetGrid()
theodata =[]
for i in draw:
    rawdata.append(load(i)[0])
    srawdata.append(load(i)[1])
    theodata.append([])
    for m in xtheo:
        theodata[i].append(float(jn(i,m))**2)

datagraphs = []
theographs = []
gr = TMultiGraph()
gr.SetTitle('Charakterisierung der Frequenzmodulation;Modulationsindex M; relative Intensitaet bzw J_n^2')
lg = TLegend(0.7, 0.8, 1, 1)
lg.SetFillColor(0)
lg.SetHeader('')
for i in draw:
    datagraphs.append(TGraphErrors(count, array('d',modulations), 
        array('d', rawdata[i]), array('d',smodulations), array('d', srawdata[i])))
    datagraphs[i].SetMarkerStyle(3)
    datagraphs[i].SetMarkerColor(6+i)
    lg.AddEntry(datagraphs[i], 'relative Intensitaet des %i-ten Seitenands'%i, 'p') 
    theographs.append(TGraph(len(xtheo), array('d',xtheo), array('d', theodata[i])))
    theographs[i].SetMarkerStyle(7)
    theographs[i].SetMarkerColor(6+i)
    lg.AddEntry(theographs[i], 'theoretischer Wert von J_%i^2'%i, 'p')
    gr.Add(datagraphs[i], 'P')
    gr.Add(theographs[i], 'P')
gr.Draw(drawopts)
lg.Draw()
Fenster.Update()
raw_input();