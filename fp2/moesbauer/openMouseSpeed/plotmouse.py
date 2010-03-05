from pylab import *
import os, glob, time
root = '/home/paule/fp-auswertung/fp2/moesbauer/openMouseSpeed/data/' # one specific folder
os.chdir(root)
l = [(os.path.getmtime(x), x)for x in os.listdir(".")]
l.sort()
file_name = l[-1][1]
lines = []
histo= [] # leere Liste
x = []
y = [] 
f = open('%s%s'%(root, file_name),'r')
for line in f:
    lines.append(line)
lines.pop()
for line in lines:
    x.append(line.split()[0].strip())
    y.append(line.split()[3].strip())
    if ((len(line.split()) < 4)&( line.split()[-1].split() == 'e' )):
        continue
    if (float(line.split()[3].strip()) < 4000)&(float(line.split()[3].strip()) > -4000):
        histo.append(float(line.split()[3].strip()))

figure(0)
hist(histo,100)
figure(1)
plot(y)
show()

##from array import array
##import sys; sys.path.append('/usr/lib/root/')
##import time
##from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
##
##Xrange = 20
##
##x, y, buffer =[]
### Erzeuge Graphen
##g = TGraph(self.count, array('d',self.channel) ,array('d',self.counts))
##g.SetTitle(';Channel;Counts')
##g.GetHistogram().SetTitleOffset(1.3, 'Y')
##g.SetMarkerStyle(1)
##g.SetMarkerColor(2)
##g.SetMarkerSize(3.0)
##c = TCanvas('c_'+self.name, self.name)
##c.SetGrid()
##graph.Draw('AP')
##c.Update()
##counter = 0
##
##def update():
##    i = counter - Xrange
##    x = []
##    while(i < counter):
##        x.append(i)
##        y.append(
##    
##while(1):
##    counter += 1
##    for line in open('/home/paule/fp-auswertung/fp2/moesbauer/avr/speed.dat','r'):
##        buffer.append(line)        
##    update()
##    time.sleep(.1)
##    