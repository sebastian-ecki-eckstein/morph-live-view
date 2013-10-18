# -*- coding: utf-8 -*-
"""
/***************************************************************************
 morph_live_view
                                 A QGIS plugin
 MORPH live view
                              -------------------
        begin                : 2013-08-06
        copyright            : (C) 2013 by ecki
        email                : ecki@ecki-netz.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from morph_live_viewdialog import morph_live_viewDialog
import threading
import socket
import time

class morph_live_view:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        #self.m = QgsVertexMarker(self.canvas)
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/morph_live_view"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
        #anzahl vehicle
        self.anzvehicle = 0
        #port
        self.port = 2805  # where do you expect to get a msg?
        self.liste = []
        self.vehicle_list = []
        self.max_listen = 10240
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_ned = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = QTimer()
        #threads
        self.t = threading.Thread(target=self.thread_read_socket)
        self.t_ned = threading.Thread(target=self.thread_read_socket_ned)

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/morph_live_view_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = morph_live_viewDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/morph_live_view/icon.png"),
            u"MORPH live view", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&MORPH live view", self.action)
        
        self.timer.timeout.connect(self.addvehicle)
        QObject.connect(self.dlg.ui.chkActivate,SIGNAL("stateChanged(int)"),self.changeActive)

    def changeActive(self,state):
        if (state==Qt.Checked):
             # enable
             #sockets
             self.s.bind(("", self.port))
             self.s_ned.bind(("", self.port + 1))
             #timer
             self.timer.start(1000)
             #threads
             self.t_stop = 0
             self.t_ned_stop = 0
             if self.t.isAlive() == False:
                self.t.start()
             if self.t_ned.isAlive() == False:
                self.t_ned.start()
        else:
             #disable
             #timer
             self.timer.stop()
             #threads
             self.t_stop = 1
             self.t_ned_stop = 1
             while self.t.isAlive() == True:
                 msg = "ende\n"
                 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                 sock.sendto(msg, ("127.0.0.1",self.port))
                 sock.close()
                 self.t.join(1)
             while self.t_ned.isAlive() == True:
                 msg = "ende\n"
                 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                 sock.sendto(msg, ("127.0.0.1",self.port + 1))
                 sock.close()
                 self.t_ned.join(1)
             #sockets
             self.s.close()
             self.s_ned.close()

    def unload(self):
        self.changeActive(Qt.Unchecked)
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&MORPH live view", self.action)
        self.iface.removeToolBarIcon(self.action)

    def addvehicle(self):
        #print "Timer abgelaufen"
        #print self.dlg.ui.tableVehicle.rowCount()
        #print self.anzvehicle
        count = self.dlg.ui.tableVehicle.rowCount()
        if count < self.anzvehicle:
          #print "neue Tabellenzeile"
          self.dlg.ui.tableVehicle.setRowCount(count + 1)
          #print self.vehicle_list[count][0]
          name = QTableWidgetItem(self.vehicle_list[count][0])
          self.dlg.ui.tableVehicle.setItem(count, 0, name)
          btn = QPushButton("reset")
          self.dlg.ui.tableVehicle.setCellWidget(count, 1, btn)
          btn.clicked.connect(lambda: self.resetVehicle(count))
          counter = QSpinBox()
          counter.setMinimum(1)
          counter.setMaximum(self.max_listen)
          #print "setValue "+str(self.vehicle_list[count][3])
          counter.setValue(self.vehicle_list[count][3])
          self.dlg.ui.tableVehicle.setCellWidget(count, 4, counter)
          counter.valueChanged.connect(lambda: self.changeSpinValue(count,counter.value()))
          chkbox = QCheckBox()
          chkbox.setCheckState(Qt.Unchecked)
          self.dlg.ui.tableVehicle.setCellWidget(count, 2, chkbox)
          chkbox.stateChanged.connect(lambda: self.changeCheckBox(count,chkbox.checkState()))
          colorbtn = QPushButton("color")
          self.dlg.ui.tableVehicle.setCellWidget(count, 3, colorbtn)
          colorbtn.clicked.connect(lambda: self.showcolordialog(count))

    def showcolordialog(self,count):
        element = self.vehicle_list[count]
        color = QColorDialog.getColor()
        if color.isValid():
           element[2]=color
        self.vehicle_list.pop(count)
        self.vehicle_list.insert(count,[element[0],element[1],element[2],element[3],element[4],element[5],element[6]])

    def resetVehicle(self,count):
        print self.vehicle_list[count]
        self.reduce_liste(self.vehicle_list[count][0])

    def changeCheckBox(self,count,state):
        if (state==Qt.Checked):
          wert = 1
        else:
          wert = 0
        #print self.vehicle_list[count]
        element = self.vehicle_list[count]
        self.vehicle_list.pop(count)
        self.vehicle_list.insert(count,[element[0],wert,element[2],element[3],element[4],element[5],element[6]])

    def changeSpinValue(self,count,value):
        #print self.vehicle_list[count]
        #print "SpinValue "+str(value)
        element = self.vehicle_list[count]
        self.vehicle_list.pop(count)
        self.vehicle_list.insert(count,[element[0],element[1],element[2],value,element[4],element[5],element[6]])

    def thread_addvehicle(self,name):
        #print "neues Fahrzeug: "+name
        newrubberband = QgsRubberBand(self.canvas, False)
        newmarker = QgsRubberBand(self.canvas,QGis.Polygon)
        #QgsVertexMarker(self.canvas)
        self.anzvehicle = self.anzvehicle + 1
        self.vehicle_list.append([name,0,QColor(0,255,0),1000,"Pi",newrubberband, newmarker])

    def colorvehicle(self):
        print "change vehicle color"
        #do something

    def maskvehicle(self):
        print "hide vehicle"
        #do something

    def setpxminvehicle(self):
        print "set something"
        #do something

    def dellasttrackpointvehicle(self,name):
        j = self.getvehiclelist(name)
        self.vehicle_list[j][5].removeLastPoint()

    def addPoint(self, name, pointx, pointy, yaw):
        #create rubberband for vehicle
        j = self.getvehiclelist(name)
        #width vielleicht einstellbar machen
        #self.vehicle_list[j][5].setWidth(5)
        self.vehicle_list[j][5].setColor(self.vehicle_list[j][2])
        self.vehicle_list[j][5].addPoint(QgsPoint(float(pointx),float(pointy)), True)

    def sort_paket(self,value):
      self.liste.insert(0,[value[1],value[2],value[3],value[8],value[4],value[5]])
      zahl = self.anzahl_liste(value[1])
      if zahl == 1:
        #print "new vehicle: "+value[1]
        self.thread_addvehicle(value[1])
      j = self.getvehiclelist(value[1])
      if self.vehicle_list[j][1] == 1:
        self.addPoint(value[1],value[3],value[2],value[4])
      self.reduce_liste(value[1],self.vehicle_list[j][3])
      return 0

    def anzahl_liste(self,name):
      zahl = 0
      for index, item in enumerate(self.liste):
        if name == item[0]:
          zahl = zahl +1
      return zahl

    def reduce_liste(self,name,maxanz=1):
      zahl = self.anzahl_liste(name)
      if maxanz < 1:
         maxanz = 1
      while zahl > maxanz:
        for index, item in enumerate(self.liste):
          if name == item[0]:
            #print index, item
            i = index
        self.liste.pop(i)
        self.dellasttrackpointvehicle(name)
        zahl = zahl - 1

    def getvehiclelist(self,name):
        for index, item in enumerate(self.vehicle_list):
          if name == item[0]:
            j = index
        return j

    def read_socket(self):
        packet = self.s.recv(80)
        getrennt = packet.split(',')
        if getrennt[0] == "$PISE" and getrennt[10] == "00.0*ff\n":
          #print "Vehicle: "+getrennt[1]+", Latitude: "+getrennt[2]+", Longtitude: "+getrennt[3]+", Yaw: "+getrennt[8]+", Date: "+getrennt[4]+", Time: "+getrennt[5]
          self.sort_paket(getrennt)
        return packet

    def read_socket_ned(self):
        packet = self.s_ned.recv(80)
        getrennt = packet.split(',')
        if getrennt[0] == "$PISE" and getrennt[10] == "00.0*ff\n":
          #print "Vehicle: "+getrennt[1]+", Latitude: "+getrennt[2]+", Longtitude: "+getrennt[3]+", Yaw: "+getrennt[8]+", Date: "+getrennt[4]+", Time: "+getrennt[5]
          self.sort_paket(getrennt)
        return packet

    def thread_read_socket(self):
        print "Thread to read socket started normal"
        while self.t_stop == 0:
          self.read_socket()
        print "Thread closed normal"

    def thread_read_socket_ned(self):
        print "Thread to read socket started ned"
        while self.t_ned_stop == 0:
          self.read_socket_ned()
        print "Thread closed ned"

    # run method that performs all the real work
    def run(self):
        # make our clickTool the tool that we'll use for now
        self.canvas.setMapTool(self.clickTool)
        #timer
        self.timer.start(5000)
        # show the dialog
        self.dlg.show()

