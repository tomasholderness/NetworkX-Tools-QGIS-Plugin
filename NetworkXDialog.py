"""
/******************************************************************************
Name		            : NetworkX Plugin
Description          : Perform network analysis using the NetworkX package 
Date                 : 03/01/2012
copyright            : (C) 2010 Tom Holderness & Newcastle University
contact              : http://www.students.ncl.ac.uk/tom.holderness
email		            : tom.holderness@ncl.ac.uk 
license		         : Relseased under Simplified BSD license (see LICENSE.txt)
******************************************************************************/
"""

__author__ = """Tom Holderness (tom.holderness@ncl.ac.uk)"""

# Change log
# 07-01-2012 - TH - Updated header metadata.
# 07-01-2012 - TH - Made inital commit to local git repo on 478.
# 07-01-2012 - TH - Moved check for NetworkX module to NetworkX.initGui

import sys
from decimal import Decimal

import qgis
from qgis.gui import *
from qgis.core import *
import qgis.utils
from qgis.core import QgsMapLayerRegistry

from PyQt4 import QtCore, QtGui 

from Ui_NetworkX_path import Ui_NetworkXPath
from Ui_NetworkX_build import Ui_NetworkXBuild

# Checked for networkx module in NetworkX.initGui so can safely import here.
import networkx as nx

class NetworkXDialogPath(QtGui.QDialog):
   def __init__(self):
      QtGui.QDialog.__init__(self) 
      # Set up the user interface from Designer. 
      self.ui = Ui_NetworkXPath()
      self.ui.setupUi(self)
      self.iface = qgis.utils.iface
      # Cancel button closes
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),
         self.exit)

      # Add available layers to the input combo box.
      self.filelist = ["Available layers:"]      
      self.ui.comboBoxInputNodes.addItem(self.filelist[0])
      self.ui.comboBoxInputEdges.addItem(self.filelist[0])
      self.layermap = QgsMapLayerRegistry.instance().mapLayers()
      # Loop through loaded QGIS layers 
      for (key, layer) in self.layermap.iteritems():
         # Check layer type is vector
         if layer.type() == 0:         
            # Add to comboBox and filelist
            self.ui.comboBoxInputNodes.addItem(layer.name())
            self.ui.comboBoxInputEdges.addItem(layer.name())
            self.filelist.append(layer.source())
            self.ui.comboBoxInputNodes.setCurrentIndex(1)
	    self.ui.comboBoxInputEdges.setCurrentIndex(1)
      QtCore.QObject.connect(self.ui.btnSourceNode,QtCore.SIGNAL("clicked()"),
         self.sourcePoint)
      QtCore.QObject.connect(self.ui.btnTargetNode,QtCore.SIGNAL("clicked()"),
         self.targetPoint)
      QtCore.QObject.connect(self.ui.btnOK,QtCore.SIGNAL("clicked()"),
         self.shortestPath)

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
       # get currentLayer and dataProvider
       cLayer = self.canvas.currentLayer()
       if cLayer:
               provider = cLayer.dataProvider()
	       if cLayer.geometryType() == QGis.Point:
		       # clear any previous selection
		       cLayer.removeSelection()
		       feat = QgsFeature()
		       # create the select statement
		       provider.select([],rect) 
		       # the arguments mean no attributes returned, and do a bbox filter 
		       #with our buffered rectangle to limit the amount of features.
		       while provider.nextFeature(feat):
		               # if the feat geom returned from the selection intersects 
		               #our point then put it in a list
		               if feat.geometry().intersects(rect):
				       cLayer.select(feat.id())
		                       self.output.clear()
		                       self.output.insert(
		                           str(feat.geometry().asPoint().x())+','
		                           +str(feat.geometry().asPoint().y()))
				       break
				         # stop here so as to select one point only. 
	       else:
                       QtGui.QMessageBox.warning( self.iface.mainWindow(),
                        "NetworkX Plugin Error", 
                           "Selected node layer must be point geometry")	               
       else:
               QtGui.QMessageBox.information( self.iface.mainWindow(),
                        "NetworkX Plugin Info", 
                           "No layer currently selected in TOC" )

   def shortestPath(self):
      #read source/target points from gui
      source = str(self.ui.lineEditSourceNode.text())
      target = str(self.ui.lineEditTargetNode.text())
      source = source.split(',')
      target = target.split(',')
      #x = float(source[0])
      #y = float(source[1])
      #x = (source[0])
      #y = (source[1])
      #print x,y
      DG1 = nx.read_shp(str(self.filelist[
                                 self.ui.comboBoxInputEdges.currentIndex()]))
      #print DG1.nodes[0]
      for node in DG1.nodes():
      #print node[0]
         if str(node[0]) == source[0] and str(node[1] == source[1]):
            print 'Identified source node in network'
            sourceNode = node
            print sourceNode
         if str(node[0]) == target[0] and str(node[1] == target[1]):
            print 'Identified target node in network'
            targetNode = node
            print targetNode
      #else:
      #   print "tom"
      #elif str(node[1]) == y:
      #	print 
     	#str_node = str(node)
     	#str_node = str_node.split(', ')
     	#print str_node[0]
      try: 
            p = nx.shortest_path(DG1, sourceNode, targetNode)
            DG2 = nx.DiGraph()
            
            for i in range(0,len(p)-1):
               DG2.add_edge(p[i],p[i+1])
               DG2.edge[p[i]][p[i+1]]['Wkt'] = DG1.edge[p[i]][p[i+1]]['Wkt']

            outdir = '/home/a5245228/'
            nx.write_shp(DG2, '/home/a5245228/')
            # Get created files
            nodes = outdir+"nodes.shp"
            edges = outdir+"edges.shp"
            # Add to QGIS instance
            qgis.utils.iface.addVectorLayer(edges, 
               "Shortest Route Network Edges", "ogr")
            qgis.utils.iface.addVectorLayer(nodes, 
               "Shortest Route Network Nodes", "ogr")
      except nx.NetworkXNoPath as e:
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

      ##sys.stdout = qgis.console.QgisOutputCatcher()
      ##sys.stdout.write('testing 1...\r')

      # Cancel button closes
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL(
         "clicked()"),self.exit)

      # Add available layers to the input combo box.
      self.filelist = ["Available layers:"]      
      self.ui.comboBoxInput.addItem(self.filelist[0])
      self.layermap = QgsMapLayerRegistry.instance().mapLayers()
      # Loop through loaded QGIS layers 
      for (name, layer) in self.layermap.iteritems():
         # Check layer type is vector
         if layer.type() == 0:         
            # Add to comboBox and filelist
            self.ui.comboBoxInput.addItem(name)
            self.filelist.append(layer.source())
            self.ui.comboBoxInput.setCurrentIndex(1)

      

      # Accept button "OK" press      
      QtCore.QObject.connect(self.ui.btnOK,QtCore.SIGNAL("clicked()"),
         self.buildNetwork)
      	
   def buildNetwork(self):
       # Method to build network files
       ##sys.stdout = qgis.console.QgisOutputCatcher()
       ##sys.stdout.write('testing 2...\r')	
       # Check that destination exists
       outdir = str(self.ui.lineEdit.text())
       print type(outdir)
       if outdir == None:
         pass
       else:
         
         # Build directed network from loaded shapefile
         print self.ui.comboBoxInput.currentIndex()
         print type(self.filelist[1])
         global DG1
         DG1 = nx.read_shp(str(self.filelist[
                                 self.ui.comboBoxInput.currentIndex()]))
         #print DG1.edges() 
         # Write out directed network to nodes and edges shapefiles using NX
         print outdir
	 print DG1.nodes()
         nx.write_shp(DG1, outdir)
         
         # Get created files
         nodes = outdir+"nodes.shp"
         edges = outdir+"edges.shp"
         # Add to QGIS instance
         qgis.utils.iface.addVectorLayer(edges, "Network Edges", "ogr")
         qgis.utils.iface.addVectorLayer(nodes, "Network Nodes", "ogr")
         
         self.close()
         # get current item from comboBoxInput
         # get filename from dictionary above
         # do nx.read_shp(fname).
         # write to new shapes
         # add to qgis.       
	

      #print fname
      #DG1 = nx.read_shp(
   
   def exit(self):
       self.close()   
      
