#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
import sys; sys.path.append('/usr/lib/root/')
import os.path

#if not line.strip() or line.strip()[0] == '#': continue

#######################################################
#
# Liest die Daten eines Tektronik Oszi aus, gibt listen zurück
#
#######################################################

class OsziData:
    def __init__(self, dateiNummer, beschreibung):
        self.dateiNummer = dateiNummer
        self.beschreibung = beschreibung
        if (existsChannel(self.dateiNummer, '1')):
            self.ch1 = Channel(self.dateiNummer, '1')
        else: self.ch1 = 0
        if (existsChannel(self.dateiNummer, '2')):
            self.ch2 = Channel(self.dateiNummer, '2')
        else: self.ch2 = 0
        


class Channel:
    def __init__(self, nummer, kanal):
        self.nummer = nummer
        self.kanal = kanal
        self.recordLength = readOszi(self.nummer, self.kanal, 'Record Length')
        self.sampleIntervall = readOszi(self.nummer, self.kanal, 'Sample Interval')
        self.yUnits = readOszi(self.nummer, self.kanal, 'Vertical Units')
        self.xUnits = readOszi(self.nummer, self.kanal, 'Horizontal Units')
        self.yScale = readOszi(self.nummer, self.kanal, 'Vertical Scale')
        self.xScale = readOszi(self.nummer, self.kanal, 'Horizontal Scale')
        self.yZero = readOszi(self.nummer, self.kanal, 'Yzero')        
        self.yOffset = readOszi(self.nummer, self.kanal, 'Vertical Offset')       
        self.probeFaktor = readOszi(self.nummer, self.kanal, 'Probe Atten')
        
        self.x = []
        self.y = []
        
        self.x, self.y = readOsziData(self.nummer, self.kanal)
    
    def cprint(self):
        print "Filename: %s" % self.nummer
        print "Kanal: %s" % self.nummer
        print "Horizontal Units: %s" % self.xUnits
        print "Vertical Scale: %s" % self.yScale
        print "Probe Atten: %s" % self.probeFaktor
        print "13 first X values" 
        print self.x[0:12]
        print "13 first Y values" 
        print self.y[0:12]


def readOszi(number, channel, value):
    result = 0
    for line in open('../daten/oszi/ALL00%s/F00%sCH%s.CSV' % (number, number, channel)):
        if not line.strip() or line.strip()[0] == '#': continue
        
        felder = line.split(',')
        if felder[0] == value:
            result = felder[1]
    return result

def readOsziData(number, channel):
    x, y = [], []
    
    for line in open('../daten/oszi/ALL00%s/F00%sCH%s.CSV' % (number, number, channel)):
        if not line.strip() or line.strip()[0] == '#': continue
        
        felder = line.split(',')
        x.append(float(felder[3]))
        y.append(float(felder[4]))
    return x, y

def existsChannel(number, channel):
    return os.path.isfile('../daten/oszi/ALL00%s/F00%sCH%s.CSV' % (number, number, channel))

def test():
    x, y = [], []
    x, y = readOsziData('04','1')
    print 'reading Oszi Data from file...'
    print x[1:12]
    print y[1:12]
    print 'if you see numbers, this works'
    
    print 'testing readOszi funciton'
    vertUnit = readOszi('04','1', 'Vertical Units')
    print vertUnit
    print 'if you see a V, this works'
    
    print 'so now we test the channel class'
    ch1 = Channel('04','1')
    ch1.cprint()
  
#test()
