#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from math import pi, cos, sin, sqrt, exp
import sys; sys.path.append('/usr/lib/root/')
from messung import Messung
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
import os.path

class nGauss:
    def __init__(self, nummer, beschreibung, n, freqLineal, fitgraph):
        self.nummer = nummer
        self.beschreibung = beschreibung
        self.n = n
        self.params = self.readParameters()
        self.messung = Messung(nummer, beschreibung, freqLineal)
        self.messung.plot()
        self.fit2 = nGaussFit(self.n, self.params)
        if fitgraph == 2: self.messung.graph2.Fit(self.fit2.fitFunc, 'Q+')
        if fitgraph == 1: self.messung.graph1.Fit(self.fit2.fitFunc, 'Q+')
        self.messung.canvas.Update()
    
    def saveParameters(self):
        file = open('../daten/oszi/ALL00%s/parameters.dat' % self.nummer,'w')
        for i in range(self.fit2.fitFunc.GetNumberFreeParameters()):
            file.write('%i  %s  %f %f\n' % (i, self.fit2.fitFunc.GetParName(i), self.fit2.fitFunc.GetParameter(i), self.fit2.fitFunc.GetParError(i)))
        file.close()
    
    def readParameters(self):
        params = []
        if os.path.isfile('../daten/oszi/ALL00%s/parameters.dat' % self.nummer):
            for line in open('../daten/oszi/ALL00%s/parameters.dat' % self.nummer,'r'):
                params.append((int(line.split()[0]),line.split()[1],float(line.split()[2]), float(line.split()[3])))
        else:
            for i in range(self.n*3 +3):
                params.append((i, 'p%i' %i, 0., 0.))
        return params
    
    def printParameters(self):
        for i in range(self.fit2.fitFunc.GetNumberFreeParameters()):
            print ('%i  %s  %f\n' % (i, self.fit2.fitFunc.GetParName(i), self.fit2.fitFunc.GetParameter(i)))
          
        
class nGaussFit:
    def __init__(self, n, params):
        self.n = n
        self.params = params
        
        self.fitFunc = TF1('f', createNGauss(self.n))
        if self.params != 0:
            for i, pn, pv, pe in self.params:
                self.fitFunc.SetParName(i, pn)
                self.fitFunc.SetParameter(i, pv)

def createNGauss(n):
    gauss = '[0]+[1]*x+[2]*x**2'
    for i in range(1,n+1):
        j = 3*i + 2
        gauss += '+[%i]/(2.50662827463100024*[%i])*exp(-0.5*((x-[%i])/[%i])**2)' % (j-2, j-1, j, j-1)
##    print gauss
    return gauss

class nLorenz:
    def __init__(self, nummer, beschreibung, n):
        self.nummer = nummer
        self.beschreibung = beschreibung
        self.n = n
        self.params = self.readParameters()
        self.fixParams = [0,1,2]
        self.messung = Messung(nummer, beschreibung, 0)
        self.messung.plot()
        self.fit1 = nLorenzFit(self.n, self.params, self.fixParams)
        self.messung.graph1.Fit(self.fit1.fitFunc, 'Q+')
        self.messung.canvas.Update()
    
    def saveParameters(self):
        file = open('../daten/oszi/ALL00%s/parameters.dat' % self.nummer,'w')
        for i in range(self.fit1.fitFunc.GetNumberFreeParameters()):
            file.write('%i  %s  %f\n' % (i, self.fit1.fitFunc.GetParName(i), self.fit1.fitFunc.GetParameter(i)))
        file.close()
    
    def readParameters(self):
        params = []
        if os.path.isfile('../daten/oszi/ALL00%s/parameters.dat' % self.nummer):
            for line in open('../daten/oszi/ALL00%s/parameters.dat' % self.nummer,'r'):
                params.append((int(line.split()[0]),line.split()[1],float(line.split()[2])))
        else:
            for i in range(self.n*3 +3):
                params.append((i, 'p%i' %i, 0.))
        return params
            
        
class nLorenzFit:
    def __init__(self, n, params, fixParams):
        self.n = n
        self.params = params
        self.fixParams = fixParams
        
        self.fitFunc = TF1('f', createNLorenz(self.n))
        if self.params != 0:
            for i, pn, pv in self.params:
                self.fitFunc.SetParName(i, pn)
                self.fitFunc.SetParameter(i, pv)
        for i in self.fixParams:
            self.fitFunc.FixParameter(i, 0.)

def createNLorenz(n):
    Lorenz = ''
    for i in range(1,n+1):
        j = 3*i + 2
        Lorenz += '+ 2*[%i]/pi * [%i]/(4*([6]*(x-[%i]))^2 + [%i]^2)' % (j-2,j-1,j,j-1)
##    print Lorenz
    return Lorenz


def test():
    #tt = nGauss('39', 'Ein test mit 4 Gauss', 4)
    tt = Messung('14', 'Frequenzlineal', 0.02)
    tt.plot()
    raw_input();
    
#test()