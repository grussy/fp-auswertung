from pylab import *
import os, glob, time
root = '/home/paule/fp-auswertung/fp2/moesbauer/openMouseSpeed/data' # one specific folder
date_file_list = []

for folder in glob.glob(root):
    print "WW"
    for file in glob.glob(folder + '/*.*'):
        print "WW"
        stats = os.stat(file)
        lastmod_date = time.localtime(stats[8])
        date_file_tuple = lastmod_date, file
        date_file_list.append(date_file_tuple)
        print "WW"
print "WW"
date_file_list.sort()
date_file_list.reverse() # newest mod date now first

for file in date_file_list:
    folder, file_name = os.path.split(file[1])
    break

datenList = [] # leere Liste
f = open('/home/paule/fp-auswertung/fp2/moesbauer/avr/speed.dat','r')
for line in f:
    line = line.split()[1].strip()
    #(float(line) < 3.26e-3)&(float(line) > 3.24e-3)
    if (1):
            datenList.append(float(line))
hist(datenList,100)
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