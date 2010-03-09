#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Mar  8 21:19:21 2010
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TGraphErrors
import wx
import serial
import SerialConfigDialog
import threading
from collections import deque
import time
import os, glob, sys, string
import gobject
import gtk
from math import pi, sqrt, exp
from array import array
from operator import div, mod

# begin wxGlade: extracode
# end wxGlade

class myNotebook(wx.Notebook):
    def __init__(self, *args, **kwds):
        # begin wxGlade: myNotebook.__init__
        kwds["style"] = 0
        wx.Notebook.__init__(self, *args, **kwds)
        self.notebook_2_pane_1 = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.notebook_2_pane_1, -1, "Histogramm X Minimum")
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_2_pane_1, -1, "-4e3")
        self.panel_1 = wx.Panel(self.notebook_2_pane_1, -1)
        self.label_2 = wx.StaticText(self.notebook_2_pane_1, -1, "Histogramm X Maximum")
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_2_pane_1, -1, "")
        self.button_1 = wx.Button(self.notebook_2_pane_1, -1, "Draw Histo")
        self.label_3 = wx.StaticText(self.notebook_2_pane_1, -1, "Velocity Samples")
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_2_pane_1, -1, "")
        self.button_2 = wx.Button(self.notebook_2_pane_1, -1, "Draw Velocity")
        self.txtArea = wx.TextCtrl(self.notebook_2_pane_1, -1, "Gui started.\n", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.onDrawHisto, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.onDrawVel, self.button_2)
        self.drawHisto = 0
        self.drawVel = 0
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: myNotebook.__set_properties
        self.AddPage(self.notebook_2_pane_1, "Meassurement")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: myNotebook.__do_layout
        sizerOne = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 3, 0, 0)
        grid_sizer_1.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_3, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_2, 0, wx.ADJUST_MINSIZE, 0)
        sizerOne.Add(grid_sizer_1, 1, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizerOne.Add(self.txtArea, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.notebook_2_pane_1.SetSizer(sizerOne)
        # end wxGlade

    def onDrawHisto(self, event): # wxGlade: myNotebook.<event_handler>
        self.drawHisto = 1

    def onDrawVel(self, event): # wxGlade: myNotebook.<event_handler>
        self.drawVel = 1
# end of class myNotebook


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(1, "Settings", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(2, "Connect", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(3, "Quit", "", wx.ITEM_NORMAL)
        self.menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(4, "About", "", wx.ITEM_NORMAL)
        self.menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.menubar)
        # Menu Bar end
        self.statusbar = self.CreateStatusBar(2, 0)
        self.tabsMain = myNotebook(self, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.menuSetiingsHandler, id=1)
        self.Bind(wx.EVT_MENU, self.menuConnectHandler, id=2)
        self.Bind(wx.EVT_MENU, self.menuQuitHandler, id=3)
        self.Bind(wx.EVT_MENU, self.menuAboutHandler, id=4)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # end wxGlade
        
        
        self.ser = serial.Serial()
        self.serAlive = threading.Event()
        self.rawData = deque(['1','i','100','t','0','o','\n'])#sample data
        self.buffer = ""
        self.saved_buffer = ""
        self.vel = []
        self.time = []
        self.elapsedTime = 0
        self.count = 0


    def draw(self):
        print self.time
        print self.vel
        self.count = len(self.time)
        g = TGraph(self.count, array('d',self.time) ,array('d',self.vel))
        g.SetTitle(';Zeit t [ms];Geschwindigkeit []')
        g.GetHistogram().SetTitleOffset(1.3, 'Y')
        g.SetMarkerStyle(20)
        g.SetMarkerColor(2)
        g.SetMarkerSize(0.4)
        self.graph = g
        c = TCanvas('Velocity over Time')
        self.canvas = c
        c.SetGrid()
        self.graph.Draw('APX')
        #self.f.Draw('SAME')
        c.Update()
        
        #sorting Velocities for Histogram in channels
        numberOfChannels = 100
        channels = [0]*numberOfChannels
        channelWidth = (max(vel) - min(vel)) / numberOfChannels
        for velo in vel:
            channelNumber = int(div(velo - min(vel), channelWidth))
            channels[channelNumber] += 1
            
        xlistdump = range(1,100)
        
        #drawing Histogramm
        h = TGraph(numberOfChannels, array('d',xlistdump) ,array('d',channels))
        h.SetTitle(';Zeit t [ms];Geschwindigkeit []')
        h.GetHistogram().SetTitleOffset(1.3, 'Y')
        h.SetMarkerStyle(20)
        h.SetMarkerColor(2)
        h.SetMarkerSize(0.4)
        
        lg = TLegend()
        lg.addEntry('Kanalbreite:',channelWidth)
        lg.addEntry('Anfangskanal:', min(vel))
        
        self.histo = h
        ch = TCanvas('Histogramm of Velocities')
        self.histoCanvas = ch
        ch.SetGrid()
        self.histo.Draw('APX')
        lg.Draw()
        #self.f.Draw('SAME')
        ch.Update()
        
        
    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("openMouseSpeed")
        self.SetSize((470, 290))
        self.statusbar.SetStatusWidths([-1, 100])
        # statusbar fields
        statusbar_fields = ["Welcome to openMouseSpeed 0.1a", "not connected"]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.tabsMain, 1, wx.EXPAND, 0)
        self.SetSizer(sizerMain)
        self.Layout()
        self.SetSize((470, 290))
        # end wxGlade
        
    
    def StartComPortThread(self):      
        self.serThread = threading.Thread(target=self.ComPortThread)
        self.serThread.setDaemon(1)
        self.serAlive.set()
        self.serThread.start()

    def StopComPortThread(self):
        if self.serThread is not None:
            self.serAlive.clear()          #clear alive event for thread
            self.serThread.join()          #wait until thread has finished
            self.serThread = None

    def menuSetiingsHandler(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `menuSetiingsHandler' not implemented!"
        event.Skip()

    def menuConnectHandler(self, event): # wxGlade: MainFrame.<event_handler>
        dialog_serial_cfg = SerialConfigDialog.SerialConfigDialog(None, -1, "", serial=self.ser)
        result = dialog_serial_cfg.ShowModal()
        dialog_serial_cfg.Destroy()
        if (result == wx.ID_OK) :
            try:
                self.ser.open()
            except serial.SerialException:
                self.statusbar.SetStatusText("Welcome to OpenMouseSpeed")
                self.statusbar.SetStatusText("not connected", 2)
                dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.StartComPortThread()
                self.statusbar.SetStatusText("connected to %s with %i baud"%
                    (self.ser.portstr, self.ser.baudrate))
                self.statusbar.SetStatusText("connected", 2)
        event.Skip()

    def menuQuitHandler(self, event): # wxGlade: MainFrame.<event_handler>
        self.Close(1)
        event.Skip()

    
    def OnClose(self, event):
        #self.StopComPortThread()
        self.ser.close()
        exit()

    def menuAboutHandler(self, event): # wxGlade: MainFrame.<event_handler>
        dlg = wx.MessageDialog(self, "   Open Mouse Speed\n Version 0.1 alpha \n"+
            "written by Paul Kremser", "OpenMouseSpeed 0.1a", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ComPortThread(self):
        """Thread that handles the incomming traffic. Does the basic input
           transformation (newlines) and generates an SerialRxEvent"""
        while self.serAlive.isSet():               #loop while alive event is true
            if (self.tabsMain.drawHisto):
                print "Drawing Histo ..."
                self.draw()
                self.tabsMain.drawHisto = 0
            if (self.tabsMain.drawVel):
                print "Drawing Velocity ..."
                self.draw()
                self.tabsMain.drawVel = 0
            text = self.ser.read(1)          #read one, with timoutself.buffer.split('i')[0]
            if text:                            #check if not timeout
                n = self.ser.inWaiting()     #look if there is more to read
                if n:
                    text = text + self.ser.read(n) #get it
                for byte in text:
                    self.rawData.append(byte)
            if (len(self.rawData) != 0):
                byte  = self.rawData.popleft()
                self.buffer += byte
                if (byte == '\n'):
                    self.saved_buffer = self.buffer
                    str = ""
                    for char in self.saved_buffer:
                        if (char  == 'i')&(str != ''):
                            interrupts = int(str.strip('i'))
                            str = ""
                            continue
                        if (char == "t")&(str != ''):
                            timer = int(str.strip('t'))
                            str = ""
                            continue
                        if (char == "o")&(str != ''):
                            overflows = int(str.strip('\n').strip('o'))
                            continue
                        str += char
                    if (interrupts == 1):
                        time = (65535*overflows + timer)/16e3  #ms
                        self.elapsedTime += float(time)
                        self.vel.append(float(1/(time*100)))
                        self.time.append(self.elapsedTime)
                        self.tabsMain.txtArea.AppendText("Time: %.6e\tVelocity:%.6e\n"%(self.elapsedTime, self.vel[-1]))
                    self.buffer = ""
# end of class MainFrame


class wxGladeApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        openMouseSpeed = MainFrame(None, -1, "")
        self.SetTopWindow(openMouseSpeed)
        openMouseSpeed.Show()
        return 1

# end of class wxGladeApp

if __name__ == "__main__":
    app = wxGladeApp(0)
    app.MainLoop()
