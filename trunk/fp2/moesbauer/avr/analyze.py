#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin, sqrt
from array import array
import os, sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1D, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")

root = '/home/grussy/trunk/fp2/moesbauer/avr/data/' # one specific folder
sxirel = 0.1 # 10% error on mouse sensor 
ready = 0
while (ready == 0):
    print "Enter Way our Sensor moved [mm]:"
    answer = sys.stdin.readline()
    try:
        real_moved = float(answer)
        ready = 1
    except ValueError:
        print "Please enter a Number like 1.23 or 1.23e123"

print "Searching Data Folder (%s) ..."%(root)
os.chdir(root)
l = [(os.path.getmtime(x), x)for x in os.listdir(".")]
l.sort()
file_name = "%s%s"%(root, l[-1][1])
print "Using newest log file: %s"%(file_name)
print "... or enter other filename:"
answer = sys.stdin.readline()
try:
    file_name = "%s%s"%(root, answer)
    open(file_name, 'r')
except IOError:
    print "Could not find File %s"%(answer)
    print " ...using newest, called %s."%(l[-1][1])
    file_name = "%s%s"%(root, l[-1][1])
factor = 1
DPI = 400
Fcpu = 16e6
num_samples = 8
mm_per_inch = 25.4
avg = 0
err= 0

way_incs = mm_per_inch/DPI
sxrel = sxirel * sqrt(1/num_samples)
moved = 0
time = []
stime = []
vel = []
svel = []
movements = []
elapsed = 0
    
def readData():
    global factor, DPI,Fcpu, num_samples, mm_per_inch, way_incs, sxrel, moved 
    global time, stime, vel, svel, movements, elapsed, avg, err, file_name
    way_incs = mm_per_inch/DPI
    sxrel = sxirel * sqrt(1/num_samples)
    moved = 0
    time = []
    stime = []
    vel = []
    svel = []
    movements = []
    elapsed = 0
    firstline = 0
    for line in open(file_name, "r"):
        if (line.strip() == "started"):
            moved = 0
            firstline = 1
            continue
        if (line.strip() == "stopped"):
            print "Moved %f mm"%(moved)
            movements.append(moved)
            continue
        if (firstline):
            firstline = 0        
            continue
        try:
            moved += num_samples*way_incs
            timer = int(line.split()[0])
            overflows = int(line.split()[1])
            t = (((overflows * 65535) + timer)/16e3) #time since last event in ms 
            stime.append(sxrel*t) 
            elapsed += t
            time.append(elapsed)
            v = (num_samples*way_incs)/(t/1e3)
            vel.append(v)
            svel.append(sqrt(2)*sxrel)
        except ValueError:
            print "skipping unreadable line in Datafile:"
            print "%s\n"%(line)
        except IndexError:
            print "skipping unreadable line in Datafile:"
            print "%s\n"%(line)
            
    sum = 0
    sumsquare = 0
    count = len(movements)-1
    for moved in movements[1:]:
        sum += moved
        sumsquare += (moved*moved)
    avg = sum/count
    err = sqrt((sumsquare/count) - (avg*avg))
    print "Average Movement was %f +- %f (%f per cent)"%(avg, err, (err/avg)*100)
readData()
factor = real_moved/avg
sf = factor * (err/avg)
print "calibrating ... "
DPI = DPI / factor
print " think we go better when calculating with %i DPI"%(DPI)
readData()





#sorting Velocities for Histogram in channels

bins = 20
rangeMin = 1e9
rangeMax = 0

for val in vel:
    if (val < 14):
        if (val < rangeMin): 
            rangeMin = val
        if (val > rangeMax): 
            rangeMax = val

#drawing Histogramm
h = TH1D('h', 'Histogramm of Velocities', bins, rangeMin, rangeMax)
for value in vel:
    h.Fill(value)
h.SetTitle(';Geschwindigkeit [];Häufigkeit [counts]')
h.GetXaxis().SetTitle("Velocity");
h.GetYaxis().SetTitle("Anzahl");
lg = TLegend()
ch = TCanvas('Histogramm of Velocities')
ch.SetGrid()
h.Draw('')
ch.Update()


scaledTime = []
scaledVel = []
count = len(time)
rangeMin = 0
rangeMax = max(time)
g = TGraphErrors(count, array('d',time) ,array('d',vel), array('d', stime), array('d', svel))
g.SetTitle(';Zeit t [ms];Geschwindigkeit []')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(20)
g.SetMarkerColor(2)
g.SetMarkerSize(0.4)
c = TCanvas('Velocity over Time')
c.SetGrid()
g.Draw('APX')
#self.f.Draw('SAME')
c.Update()
raw_input();