#!/usr/bin/env python
import os, glob, time, sys, string
import gobject
import gtk
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import rcParams
from pylab import *

root = '/home/paule/fp-auswertung/fp2/moesbauer/openMouseSpeed/data/' # one specific folder
samples = 50

lines = []
histo= [] # leere Liste
xdata = []
ydata = []

class BackwardsReader:
  def readline(self):
    while len(self.data) == 1 and ((self.blkcount * self.blksize) < self.size):
      self.blkcount = self.blkcount + 1
      line = self.data[0]
      try:
        self.f.seek(-self.blksize * self.blkcount, 2) # read from end of file
        self.data = string.split(self.f.read(self.blksize) + line, '\n')
      except IOError:  # can't seek before the beginning of the file
        self.f.seek(0)
        self.data = string.split(self.f.read(self.size - (self.blksize * (self.blkcount-1))) + line, '\n')

    if len(self.data) == 0:
      return ""

    # self.data.pop()
    # make it compatible with python <= 1.5.1
    line = self.data[-1]
    self.data = self.data[:-1]
    return line + '\n'

  def __init__(self, file, blksize=4096):
    """initialize the internal structures"""
    # get the file size
    self.size = os.stat(file)[6]
    # how big of a block to read from the file...
    self.blksize = blksize
    # how many blocks we've read
    self.blkcount = 1
    self.f = open(file, 'rb')
    # if the file is smaller than the blocksize, read a block,
    # otherwise, read the whole thing...
    if self.size > self.blksize:
      self.f.seek(-self.blksize * self.blkcount, 2) # read from end of file
    self.data = string.split(self.f.read(self.blksize), '\n')
    # strip the last item if it's empty...  a byproduct of the last line having
    # a newline at the end of it
    if not self.data[-1]:
      # self.data.pop()
      self.data = self.data[:-1]

def updateData(*args):
    bw = BackwardsReader('%s%s'%(root, file_name))
    line = bw.readline() #last line is often incomplete 
    for i in range(samples):
        line = bw.readline()
        lines.append(bw.readline())
    for line in lines:
        xdata.append(line.split('\t')[0].strip('\n'))
        ydata.append(line.split('\t')[3].strip('\n'))
        h = (line.split('\t')[0].strip('\n'))
    if (h < 4000)&(h > -4000):
            histo.append(h)
    return True

def updatePlot(*args):
    print ydata

    return True

os.chdir(root)
l = [(os.path.getmtime(x), x)for x in os.listdir(".")]
l.sort()
file_name = "%s%s"%(root, l[-1][1])
print "Using newest log file: %s"%(file_name)


x_data = [] # leere Listen
y_data = []
f = open(file_name,'r')
for line in f:
    data = line.strip('\n').split('\t')
    print data
    if ((len(data) == 4)):
        if (len(data[3]) > 11):
            x_data.append(float(line.split('\t')[0].strip('\n')))
            y_data.append(float(line.split('\t')[3].strip('\n')))
##            if ((y_data[-1] > -4e3)&(y_data[-1] < 4e3)):
##                histo.append(y_data[-1])
        histo.append(y_data[-1])
figure(0)
hist(histo, 20)
figure(1)
plot(y_data)
show()

##bw = BackwardsReader('%s%s'%(root, file_name))
##
##while(1):
##    xdata = []
##    ydata = []
##    histo = []
##    bw = BackwardsReader('%s%s'%(root, file_name))
##    line = bw.readline() #last line is often incomplete 
##    for i in range(samples):
##        line = bw.readline()
##        lines.append(bw.readline())
##    for line in lines:
##        xdata.append(line.split('\t')[0].strip('\n'))
##        ydata.append(line.split('\t')[3].strip('\n'))
##        h=float(line.split('\t')[3].strip('\n'))
##        print h
##        if (h < 4000)&(h >-4000):
##            histo.append(float(h))
##    figure(0)
##    hist(histo, 20)
##    figure(1)
##    plot(ydata)
##    show()
##    time.sleep(10)


##while(1):
##    bw = BackwardsReader('%s%s'%(root, file_name))
##    line = bw.readline() #last line is often incomplete 
##    for i in range(samples):
##        line = bw.readline()
##        lines.append(bw.readline())
##    for line in lines:
##        x.append(line.split()[0].strip())
##        y.append(line.split()[3].strip())
##        if ((len(line.split()) < 4)&( line.split()[-1].split() == 'e' )):
##            continue
##        if (float(line.split()[3].strip()) < 4000)&(float(line.split()[3].strip()) > -4000):
##            histo.append(float(line.split()[3].strip()))
##    figure(0)
##    hist(histo,100)
##    figure(1)
##    plot(y)
##    show()
##    time.sleep(.5)