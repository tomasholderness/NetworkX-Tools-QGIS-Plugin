"""
/******************************************************************************
Name		 : NetworkX Tools
Description          : Perform network analysis using the NetworkX package 
Date                 : 03/01/2012
copyright            : (C) 2012 Tom Holderness & Newcastle University
contact              : http://www.students.ncl.ac.uk/tom.holderness
email		 : tom.holderness@ncl.ac.uk 
license		 : Relseased under Simplified BSD license (see LICENSE.txt)
******************************************************************************/
"""

__author__ = """Tom Holderness (tom.holderness@ncl.ac.uk)"""

import os
import glob
import qgis
from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsGeometry, QGis, QgsFeature, QgsMapLayerRegistry
from PyQt4 import QtCore, QtGui
from Ui_NetworkX_path_dock import Ui_NetworkXPath
from Ui_NetworkX_build import Ui_NetworkXBuild

# Checked for networkx module in NetworkX.initGui so can safely import here.
import networkx as nx
import nx_shp 

class ShapeLayersToCombo:
    '''Abstract class to support loading of layers from QGIS TOC to Qt combo
    box.'''
    def __init__(self, comboLayers, filelist, geomtype=None):
        '''Method to add current shapefile layers to QT combo box, takes 
        comboBox ui reference and file list and adds suitable TOC layers to 
        both.
        '''
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        # Loop through loaded QGIS layers 
        for (key, layer) in layermap.iteritems():
         # Check layer type is vector
         if layer.type() == 0:
            # Check layer is from shapefile
            if str(layer.source()).endswith('.shp'):
            # Check layer is correct geom
                if geomtype is None:
                        # Add to comboBox and filelist
                        comboLayers.addItem(layer.name())
                        comboLayers.setCurrentIndex(1)
                        filelist.append(layer.source())
                else:
                    if layer.geometryType() == geomtype:
                        # Add to comboBox and filelist
                        comboLayers.addItem(layer.name())
                        comboLayers.setCurrentIndex(1)
                        filelist.append(layer.source())
         else:  
             comboLayers.setCurrentIndex(0)
             
class WriteNetworkShapefiles:
    '''Abstract class to support writing of shapefiles from NetworkX'''
    def __init__(self, network, fileDir, overwrite=False):
       nodes = fileDir+'/nodes.*'
       edges = fileDir+'/edges.*'
       # Test/remove existing files as required
       if glob.glob(nodes):
           if overwrite == True:
               for filename in glob.glob(nodes):
                   os.remove(filename)
           else:
               raise IOError, "Node files already exist in output folder."
       if glob.glob(edges):
           if overwrite == True:
               for filename in glob.glob(edges):
                   os.remove(filename)
           else:
               raise IOError, "Edge files already exist in output folder."
       
       nx_shp.write_shp(network, fileDir)   


class NetworkXDialogPath(QtGui.QDockWidget, Ui_NetworkXPath, 
                         ShapeLayersToCombo):
   def __init__(self, parent):
      QtGui.QDockWidget.__init__(self, parent.iface.mainWindow()) 
      self.iface = qgis.utils.iface
      # Set up the user interface from Designer. 
      self.ui = Ui_NetworkXPath()
      self.ui.setupUi(self)
      self.loadMenus()
      
      # Counters for selected nodes on canvas which need to persist in the 
          #class.
      self.selectedNodes = {'source':None, 'target':None}
      
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),
                             self.exit)
      QtCore.QObject.connect(self.ui.comboBoxInputEdges, 
        QtCore.SIGNAL("activated(const QString&)"), self.attributeWeights)
      QtCore.QObject.connect(self.ui.btnSourceNode, QtCore.SIGNAL("clicked()"),
                             self.sourcePoint)
      QtCore.QObject.connect(self.ui.btnTargetNode, QtCore.SIGNAL("clicked()"),
                             self.targetPoint)
      QtCore.QObject.connect(self.ui.btnOK, QtCore.SIGNAL("clicked()"),
                             self.shortestPath)
      QtCore.QObject.connect(self.ui.btnSave, QtCore.SIGNAL("clicked()"),
                             self.outputFile)
      QtCore.QObject.connect(self.ui.btnReload, QtCore.SIGNAL("clicked()"),
                             self.clearReload)
   
   def loadMenus(self):   
      # List available algorithms
      self.algorithms = {'Shortest Path':'shortest_path',
                         'Dijkstra':'dijkstra_path','A*':'astar_path'}
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
      ShapeLayersToCombo(self.ui.comboBoxInputNodes, self.pointfilelist, 0)
      ShapeLayersToCombo(self.ui.comboBoxInputEdges, self.linefilelist, 1)

      # Updated comboBoxEdges internally so updated weights.
      self.attributeWeights()
      
   def clearInputs(self):
       self.ui.checkBoxUndirected.setChecked(False)
       self.ui.checkBoxOverwrite.setChecked(False)
       self.ui.comboBoxAlgorithm.clear()
       self.ui.comboBoxInputEdges.clear()
       self.ui.comboBoxInputNodes.clear()
       self.ui.comboBoxInputWeight.clear()
       self.ui.lineEditSourceNode.clear()
       self.ui.lineEditTargetNode.clear()
       self.ui.lineEditSave.clear()
       
   def clearReload(self):
       # First clear any existing node selection on canvas
       layers = qgis.utils.iface.mapCanvas().layers()
       nodes = str(self.ui.comboBoxInputNodes.currentText())
       for layer in layers:
         if layer.name() == nodes:
               layer.removeSelection()
       self.selectedNodes = {'source':None, 'target':None}
       # Clear menus and inputs
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
                      if (fields[name].typeName() == 'Integer' or 
                          fields[name].typeName() == 'Real'):
                              self.ui.comboBoxInputWeight.addItem(
                                  fields[name].name())
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
      self.nodetype = 'source'
   def targetPoint(self):
      self.output = self.ui.lineEditTargetNode
      self.nodetype = 'target'
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
         
   def selectFeature(self, point):
   #def selectFeature(self, point, button):
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
               feat = QgsFeature()
               # create the select statement
               provider.select([],rect) 
               # the arguments mean no attributes returned, and do a bbox filter 
               # with our buffered rectangle to limit the amount of features.
               while provider.nextFeature(feat):
               # if the feat geom returned from the selection intersects 
                #our point then put it in a list for selection
                   if feat.geometry().intersects(rect):
                       #layer.removeSelection(self.selectedNodes[self.nodetype])
                       self.selectedNodes[self.nodetype] = feat.id()
                       self.output.clear()
                       self.output.insert(
                           str(feat.geometry().asPoint().x())+','
                               +str(feat.geometry().asPoint().y()))
                       layer.removeSelection()
                       for nodetype, featid in self.selectedNodes.iteritems():
                           if featid is not None:
                               layer.select(featid)
                   break # stop here so as to select one point only. 
                       
   def outputFile(self):
       try:
          self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, 
                                                    "Select Output Directory"))
          self.ui.lineEditSave.insert(self.fd)
       except IOError as e:
           self.ui.lineEditSave.clear()
           QtGui.QMessageBox.warning( self.iface.mainWindow(), 
                                     "NetworkX Plugin Error", "%s" % str(e))
           
   '''
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
   '''            
   def shortestPath(self):
      try: 
          #read source/target points from gui
          source = str(self.ui.lineEditSourceNode.text())
          target = str(self.ui.lineEditTargetNode.text())
          if source == '':
              raise IOError, "Please specify source node."
          source = source.split(',')
          if target == '':
              raise IOError, "Please specify target node."
          target = target.split(',')

          edges = str(self.linefilelist[
                          self.ui.comboBoxInputEdges.currentIndex()])
          if edges == "Shapefile line layers:":
                  raise IOError, "Please specify input edge layer."

          DG1 = nx.read_shp(str(self.linefilelist[
                  self.ui.comboBoxInputEdges.currentIndex()]))
          
          if self.ui.checkBoxUndirected.isChecked() == True:
             DG1 = DG1.to_undirected()
             
          for node in DG1.nodes():
             if str(node[0]) == source[0] and str(node[1] == source[1]):
                sourceNode = node
             elif str(node[0]) == target[0] and str(node[1] == target[1]):
                targetNode = node
             try: 
                    targetNode
             except NameError:
                raise (UnboundLocalError,
                           "Specified target node not found in edge layer.")
             try: 
                sourceNode
             except NameError:
                raise (UnboundLocalError,
                       "Specified source node not found in edge layer.")    
                      
             key = str(self.ui.comboBoxAlgorithm.currentText())
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
               
             if self.ui.lineEditSave == '':
                 raise IOError, "No output directory specified." 
              
             if self.ui.checkBoxOverwrite.isChecked():
                 WriteNetworkShapefiles(DG2, self.fd, overwrite=True)
             else:
                 WriteNetworkShapefiles(DG2, self.fd)
            
             nodes = self.fd+'/nodes.shp'
             edges = self.fd+'/edges.shp'
             qgis.utils.iface.addVectorLayer(edges, 
                                        "Shortest Route Network Edges", "ogr")
             qgis.utils.iface.addVectorLayer(nodes, 
                                        "Shortest Route Network Nodes", "ogr")
  
              
      except (IOError, AttributeError, UnboundLocalError, 
                  nx.NetworkXNoPath) as e:
                      QtGui.QMessageBox.warning( self.iface.mainWindow(),
                                    "NetworkX Plugin Error", "%s" % str(e))      
   def exit(self):
       self.close() 
      
class NetworkXDialogBuild(QtGui.QDialog, ShapeLayersToCombo, 
                          WriteNetworkShapefiles):
   def __init__(self):
      QtGui.QDialog.__init__(self) 
      
      self.ui = Ui_NetworkXBuild()
      self.ui.setupUi(self)
      self.iface = qgis.utils.iface

      QtCore.QObject.connect(self.ui.btnOK,QtCore.SIGNAL("clicked()"),
         self.buildNetwork)
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL(
         "clicked()"),self.exit)
      QtCore.QObject.connect(self.ui.btnSave, QtCore.SIGNAL(
          "clicked()"),self.outputFile)
          
      # Add available layers to the input combo box.
      self.filelist = ["Available layers:"]      
      self.ui.comboBoxInput.addItem(self.filelist[0])
      ShapeLayersToCombo(self.ui.comboBoxInput, self.filelist, 1)
         
   def outputFile(self):
       try:
          self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, 
                                                    "Select Output Directory"))
          self.ui.lineEditSave.insert(self.fd)
       except IOError as e:
           self.ui.lineEditSave.clear()
           QtGui.QMessageBox.warning( self.iface.mainWindow(), 
                                     "NetworkX Plugin Error", "%s" % str(e))         

   def buildNetwork(self):
         try:
             layer = str(self.filelist[self.ui.comboBoxInput.currentIndex()])
             if layer == "Available layers:":
                     raise IOError, "Please specify input shapefile layer."
                 
             DG1 = nx.read_shp(layer)
             if str(self.ui.lineEditSave.text()) == '':
                 raise IOError, "No output directory specified."
                 
             WriteNetworkShapefiles(DG1, self.fd, overwrite=True)
             #self.writeNetworkShapefiles(DG1)                        
             if self.ui.checkBoxAdd.isChecked():
                 # Get created files
                 nodes = self.fd+"/nodes.shp"
                 edges = self.fd+"/edges.shp"
                 # Add to QGIS instance
                 qgis.utils.iface.addVectorLayer(edges, "Network Edges", "ogr")
                 qgis.utils.iface.addVectorLayer(nodes, "Network Nodes", "ogr")
             
             self.close()
         except (AttributeError, IOError) as e:
               QtGui.QMessageBox.warning( self, "NetworkX Plugin Error", 
                                             "%s" % e)
   def exit(self):
       self.close()