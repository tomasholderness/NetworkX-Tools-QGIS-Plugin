"""
/******************************************************************************
Name		            : NetworkX Tools
Description          : Perform network analysis using the NetworkX package 
Date                 : 03/01/2012
copyright            : (C) 2012 Tom Holderness & Newcastle University
contact              : http://www.students.ncl.ac.uk/tom.holderness
email		            : tom.holderness@ncl.ac.uk 
license		         : Relseased under Simplified BSD license (see LICENSE.txt)
******************************************************************************/
"""

__author__ = """Tom Holderness (tom.holderness@ncl.ac.uk)"""

import sys
import os
import glob
from decimal import Decimal

import qgis
from qgis.gui import *
from qgis.core import *
import qgis.utils
from qgis.core import QgsMapLayerRegistry

from PyQt4 import QtCore, QtGui

from Ui_NetworkX_path_dock import Ui_NetworkXPath
from Ui_NetworkX_build import Ui_NetworkXBuild

# Checked for networkx module in NetworkX.initGui so can safely import here.
import networkx as nx
import nx_shp 

class NetworkXDialogPath(QtGui.QDockWidget, Ui_NetworkXPath):
   def __init__(self, parent):
      QtGui.QDockWidget.__init__(self, parent.iface.mainWindow()) 
      self.iface = qgis.utils.iface
      # Set up the user interface from Designer. 
      
      
      self.ui = Ui_NetworkXPath()
      self.ui.setupUi(self)
      self.loadMenus()
      
      
      # Cancel button closes
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),
         self.exit)
      
      QtCore.QObject.connect(self.ui.comboBoxInputEdges, QtCore.SIGNAL("activated(const QString&)"), self.attributeWeights)
      QtCore.QObject.connect(self.ui.btnSourceNode, QtCore.SIGNAL("pressed()"),
         self.sourcePoint)
      QtCore.QObject.connect(self.ui.btnTargetNode, QtCore.SIGNAL("clicked()"),
         self.targetPoint)
      QtCore.QObject.connect(self.ui.btnOK, QtCore.SIGNAL("clicked()"),
         self.shortestPath)
      QtCore.QObject.connect(self.ui.btnSave, QtCore.SIGNAL("clicked()"),self.outputFile)
      QtCore.QObject.connect(self.ui.btnReload, QtCore.SIGNAL("clicked()"),self.clearReload)
   
   def loadMenus(self):   
      # List available algorithms
      self.algorithms = {'Shortest Path':'shortest_path','Dijkstra':'dijkstra_path','A*':'astar_path'}
      print self.algorithms
      for key in self.algorithms:
         self.ui.comboBoxAlgorithm.addItem(key)
      self.ui.comboBoxAlgorithm.setCurrentIndex(0)

      # Add available layers to the input combo box.
      self.pointfilelist = ["Shapefile point layers:"]
      self.linefilelist = ["Shapefile line layers:"]            
      self.ui.comboBoxInputNodes.addItem(self.pointfilelist[0])
      self.ui.comboBoxInputEdges.addItem(self.linefilelist[0])
      self.layermap = QgsMapLayerRegistry.instance().mapLayers()
      # Loop through loaded QGIS layers 
      for (key, layer) in self.layermap.iteritems():
         # Check layer type is vector
         if layer.type() == 0:
            #Check layer is from shapefile
            if str(layer.source()).endswith('.shp'):
            # Add to comboBox and filelist
                if layer.geometryType() == 0:
                   self.ui.comboBoxInputNodes.addItem(layer.name())
                   self.pointfilelist.append(layer.source())
                elif layer.geometryType() == 1:
                   self.ui.comboBoxInputEdges.addItem(layer.name())
                   self.linefilelist.append(layer.source())
                self.ui.comboBoxInputNodes.setCurrentIndex(1)
                self.ui.comboBoxInputEdges.setCurrentIndex(1)
         else:
             self.ui.comboBoxInputNodes.setCurrentIndex(0)
             self.ui.comboBoxInputEdges.setCurrentIndex(0)
      # Updated comboBoxEdges internally so updated weights.
      self.attributeWeights()
      
   def clearInputs(self):
       self.ui.checkBoxUndirected.setChecked(False)
       self.ui.checkBoxOverwrite.setChecked(False)
       self.ui.lineEditSourceNode.clear()
       self.ui.lineEditTargetNode.clear()
       self.ui.lineEditSave.clear()
       
   def clearReload(self):
       self.clearInputs()
       self.loadMenus()
      
   def attributeWeights(self):
      # Clear the attributeComboBoxList
      self.ui.comboBoxInputWeight.clear()
      self.ui.comboBoxInputWeight.addItem('None')
      
      # Add new attributes of layer to weights.         
      for (key, layer) in self.layermap.iteritems():
          edges = str(self.ui.comboBoxInputEdges.currentText())
          print layer.name(), edges
          if layer.name() == edges:
              provider = layer.dataProvider()
              try:
                  fields = provider.fields() 
                  for name in fields:
                      if fields[name].typeName() == 'Integer' or fields[name].typeName() == 'Real':
                              self.ui.comboBoxInputWeight.addItem(fields[name].name())
                              self.ui.comboBoxInputWeight.setCurrentIndex(0)
              except TypeError:
                   self.ui.comboBoxInputWeight.setCurrentIndex(0)
                   QtGui.QMessageBox.warning( self.iface.mainWindow(),
                        "NetworkX Plugin Error", 
                           "Error reading %s attribute table." % edges)
          else:
              self.ui.comboBoxInputWeight.setCurrentIndex(0)
   def sourcePoint(self):
      self.output = self.ui.lineEditSourceNode
      self.collectPoint()

   def targetPoint(self):
      self.output = self.ui.lineEditTargetNode
      self.collectPoint()

   def collectPoint(self):
      self.canvas = qgis.utils.iface.mapCanvas()
      self.point=QgsMapToolEmitPoint(qgis.utils.iface.mapCanvas())
      mapCanvas=qgis.utils.iface.mapCanvas()
      # Create the appropriate map tool and connect the gotPoint() signal.
      #self.emitPoint = [[QgsMapToolEmitPoint]](mapCanvas)
      mapCanvas.setMapTool(self.point)
      QtCore.QObject.connect(self.point, 
         QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), 
         self.selectFeature)

   def selectFeature(self, point, button):
       # Select Features function from 
       # http://www.qgisworkshop.org/html/workshop/plugins_tutorial.html
       # setup the provider select to filter results based on a rectangle
       pntGeom = QgsGeometry.fromPoint(point)
       # scale-dependent buffer of 3 pixels-worth of map units
       pntBuff = pntGeom.buffer( (self.canvas.mapUnitsPerPixel() * 3),0)
       rect = pntBuff.boundingBox()
       layers = qgis.utils.iface.mapCanvas().layers()
       nodes = str(self.ui.comboBoxInputNodes.currentText())
       for layer in layers:
         if layer.name() == nodes:
            provider = layer.dataProvider()
            if layer.geometryType() == QGis.Point:
               # clear any previous selection
               layer.removeSelection()
               feat = QgsFeature()
               # create the select statement
               provider.select([],rect) 
               # the arguments mean no attributes returned, and do a bbox filter 
               # with our buffered rectangle to limit the amount of features.
               while provider.nextFeature(feat):
               # if the feat geom returned from the selection intersects 
               #our point then put it in a list
                   if feat.geometry().intersects(rect):
                       layer.select(feat.id())
                       self.output.clear()
                       self.output.insert(
                           str(feat.geometry().asPoint().x())+','
                               +str(feat.geometry().asPoint().y()))
                       break
                       # stop here so as to select one point only. 
                       
   def outputFile(self):
       try:
          self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Output Directory"))
          self.ui.lineEditSave.insert(self.fd)
       except IOError as e:
           self.ui.lineEditSave.clear()
           QtGui.QMessageBox.warning( self.iface.mainWindow(), "NetworkX Plugin Error",                         "%s" % str(e))
           
  
   def writeNetworkShapefiles(self, network):
       try:
           nodes = self.fd+'/nodes.*'
           edges = self.fd+'/edges.*'
           # test if files there
           if glob.glob(nodes):
               if self.ui.checkBoxOverwrite.isChecked():
                   for filename in glob.glob(nodes):
                       os.remove(filename)
               else:
                   raise IOError, "Node files already exist in output folder."
           if glob.glob(edges):
               if self.ui.checkBoxOverwrite.isChecked():
                   for filename in glob.glob(edges):
                       os.remove(filename)
               else:
                   raise IOError, "Edge files already exist in output folder."
           
           nx_shp.write_shp(network, str(self.ui.lineEditSave.text()))   
       except AttributeError:
           raise AttributeError, "No output file specified."
           # raise last to pass to next method (shortestPath)
               
   def shortestPath(self):
      try: 
          #read source/target points from gui
          source = str(self.ui.lineEditSourceNode.text())
          target = str(self.ui.lineEditTargetNode.text())
          if source: 
              source = source.split(',')
              if target:
                  target = target.split(',')
                  if str(self.linefilelist[self.ui.comboBoxInputEdges.currentIndex()]) != None:
                      DG1 = nx.read_shp(str(self.linefilelist[
                                                 self.ui.comboBoxInputEdges.currentIndex()]))
                      
                      # Test for undirected network.
                      if self.ui.checkBoxUndirected.isChecked() == True:
                         print 'undirected'
                         DG1 = DG1.to_undirected()
                      #print DG1.nodes[0]
                      #sourceNode, targetNode = None
                      for node in DG1.nodes():
                      #print node[0]
                         if str(node[0]) == source[0] and str(node[1] == source[1]):
                            print 'Identified source node in network'
                            sourceNode = node
                            print sourceNode
                         elif str(node[0]) == target[0] and str(node[1] == target[1]):
                            print 'Identified target node in network'
                            targetNode = node
                            print targetNode 
                      try: 
                            targetNode
                      except NameError:
                            raise UnboundLocalError, "Specified target node not found in edge layer."
                              #QtGui.QMessageBox.information( self.iface.mainWindow(), "NetworkX Plugin Information", "Specified target node not found in edge layer.")
                      try: 
                            sourceNode
                      except NameError:
                              raise UnboundLocalError, "Specified source node not found in edge layer."                        
                              
                      key = str(self.ui.comboBoxAlgorithm.currentText())
                      #print key
                      algorithm = self.algorithms[key]
                      method = getattr(nx, algorithm)
                      weight = str(self.ui.comboBoxInputWeight.currentText()) 
                      if weight == 'None':
                        p = method(DG1, sourceNode, targetNode)
                      else:
                        p = method(DG1, sourceNode, targetNode, weight)
                      DG2 = nx.DiGraph()
                      for i in range(0,len(p)-1):
                       DG2.add_edge(p[i],p[i+1])
                       DG2.edge[p[i]][p[i+1]]['Wkt'] = DG1.edge[p[i]][p[i+1]]['Wkt']
                      self.writeNetworkShapefiles(DG2)
                      nodes = self.fd+'/nodes.shp'
                      edges = self.fd+'/edges.shp'
                      qgis.utils.iface.addVectorLayer(edges, "Shortest Route Network Edges", "ogr")
                      qgis.utils.iface.addVectorLayer(nodes, "Shortest Route Network Nodes", "ogr")
                        
                  else:
                      QtGui.QMessageBox.information( self.iface.mainWindow(), "NetworkX Plugin Information", "Please select an edge layer")       
              else:
                  QtGui.QMessageBox.information( self.iface.mainWindow(), "NetworkX Plugin Information", "Please select a target node")
          else:
              QtGui.QMessageBox.information( self.iface.mainWindow(), "NetworkX Plugin Information", "Please select a source node")
              
      except (IOError, AttributeError,UnboundLocalError,  nx.NetworkXNoPath) as e:
          QtGui.QMessageBox.warning( self.iface.mainWindow(),
                                    "NetworkX Plugin Error", 
                                       "%s" % str(e))      
   def exit(self):
       self.close() 
      
class NetworkXDialogBuild(QtGui.QDialog):
   def __init__(self):
      QtGui.QDialog.__init__(self) 
      # Set up the user interface from Designer. 
      self.ui = Ui_NetworkXBuild()
      self.ui.setupUi(self)
      self.iface = qgis.utils.iface

      # Cancel button closes
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL(
         "clicked()"),self.exit)
      QtCore.QObject.connect(self.ui.btnSave, QtCore.SIGNAL("clicked()"),self.outputFile)
      
      # Add available layers to the input combo box.
      self.filelist = ["Available layers:"]      
      self.ui.comboBoxInput.addItem(self.filelist[0])
      self.layermap = QgsMapLayerRegistry.instance().mapLayers()
      # Loop through loaded QGIS layers 
      for (key, layer) in self.layermap.iteritems():
         # Check layer type is vector
         if layer.type() == 0:
            #Check layer is from shapefile
            if str(layer.source()).endswith('.shp'):
            # Add to comboBox and filelist
                   self.filelist.append(layer.source())
                   self.ui.comboBoxInput.addItem(layer.name())
                   self.ui.comboBoxInput.setCurrentIndex(1)

      # Accept button "OK" press      
      QtCore.QObject.connect(self.ui.btnOK,QtCore.SIGNAL("clicked()"),
         self.buildNetwork)
         
   def outputFile(self):
       try:
          self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Output Directory"))
          self.ui.lineEditSave.insert(self.fd)
       except IOError as e:
           self.ui.lineEditSave.clear()
           QtGui.QMessageBox.warning( self.iface.mainWindow(), "NetworkX Plugin Error",                         "%s" % str(e))         

   def writeNetworkShapefiles(self, network):
       try:
           nodes = self.fd+'/nodes.*'
           edges = self.fd+'/edges.*'
           # test if network shapefiles already exist in target dir.
           if glob.glob(nodes):
               if self.ui.checkBoxOverwrite.isChecked():
                   for filename in glob.glob(nodes):
                       os.remove(filename)
               else:
                   raise IOError, "Node files already exist in output folder."
           if glob.glob(edges):
               if self.ui.checkBoxOverwrite.isChecked():
                   for filename in glob.glob(edges):
                       os.remove(filename)
               else:
                   raise IOError, "Edge files already exist in output folder."
           
           nx_shp.write_shp(network, str(self.ui.lineEditSave.text()))   
       except AttributeError:
           raise AttributeError, "No output file specified."

   def buildNetwork(self):
         try:
             DG1 = nx.read_shp(str(self.filelist[
                                 self.ui.comboBoxInput.currentIndex()]))
             self.writeNetworkShapefiles(DG1)                        
             if self.ui.checkBoxAdd.isChecked():
                 # Get created files
                 nodes = self.fd+"/nodes.shp"
                 edges = self.fd+"/edges.shp"
                 # Add to QGIS instance
                 qgis.utils.iface.addVectorLayer(edges, "Network Edges", "ogr")
                 qgis.utils.iface.addVectorLayer(nodes, "Network Nodes", "ogr")
             
             self.close()
         except (AttributeError, IOError) as e:
               
               QtGui.QMessageBox.warning( self, "NetworkX Plugin Error", "%s" % e)
   def exit(self):
       self.close()   
      
