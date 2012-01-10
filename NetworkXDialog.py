"""
/***************************************************************************
Name			 	 : NetworkX Plugin
Description          : Perform network analysis using the NetworkX package
Date                 : 03/Jan/12 
copyright            : (C) 2012 by Tom Holderness /Newcastle University
email                : tom.holderness@ncl.ac.uk 
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
import sys
import qgis
#from qgis import *
from qgis.gui import *
import qgis.utils
from qgis.core import QgsMapLayerRegistry
from PyQt4 import QtCore, QtGui 
from Ui_NetworkX import Ui_NetworkX
from Ui_NetworkX_path import Ui_NetworkXPath
from Ui_NetworkX_build import Ui_NetworkXBuild
from qgis.core import *
# Import networkx
import networkx as nx
from decimal import Decimal

# create the dialog for NetworkX
class NetworkXDialog(QtGui.QDialog):
   def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_NetworkX()
    self.ui.setupUi(self)

class NetworkXDialogPath(QtGui.QDialog):
   def __init__(self): 
      QtGui.QDialog.__init__(self) 
      # Set up the user interface from Designer. 
      self.ui = Ui_NetworkXPath()
      self.ui.setupUi(self)

      # Cancel button closes
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),self.exit)

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
      QtCore.QObject.connect(self.ui.btnSourceNode,QtCore.SIGNAL("clicked()"),self.sourcePoint)
      QtCore.QObject.connect(self.ui.btnTargetNode,QtCore.SIGNAL("clicked()"),self.targetPoint)
      QtCore.QObject.connect(self.ui.btnOK,QtCore.SIGNAL("clicked()"),self.shortestPath)

   def sourcePoint(self):
      self.output = self.ui.lineEditSourceNode
      self.collectPoint()

   def targetPoint(self):
      self.output = self.ui.lineEditTargetNode
      self.collectPoint()

   def collectPoint(self):
      self.iface = qgis.utils.iface
      self.canvas = qgis.utils.iface.mapCanvas()
      self.clickTool = QgsMapToolEmitPoint(self.canvas)
      # out click tool will emit a QgsPoint on every click
      # connect our custom function to a clickTool signal that the canvas was clicked
      print "loaded path"
      self.point=QgsMapToolEmitPoint(qgis.utils.iface.mapCanvas())
      #print "self.point"
      print self.point
      #QtCore.QObject.connect(self.point, QtCore.SIGNAL("canvasClicked(const QgsPoint &,Qt::MouseButton)"),self.dmfunc)

      mapCanvas=qgis.utils.iface.mapCanvas()
      # Create the appropriate map tool and connect the gotPoint() signal.
      #self.emitPoint = [[QgsMapToolEmitPoint]](mapCanvas)
      mapCanvas.setMapTool(self.point)
      QtCore.QObject.connect(self.point, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)
      #handleMouseDown. selectFeature
   def dmfunc(self):
      print "dmfunc"
      #result = QtCore.QObject.connect(self.clickTool, QtColineEdit_3re.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDown)
      #print result
        #QMessageBox.information( self.iface.mainWindow(),"Info", "connect = %s"%str(result) )

        # connect our select function to the canvasClicked signal
      #result = QtCore.QObject.connect(self.clickTool, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)
      #print result

      #QtGui.QMessageBox.information( self.iface.mainWindow(),"Info", "connect = %s"%str(result) )
      
      #print "Path class"
      #print DG1.edges()
      # connect our select function to the canvasClicked signal
      #result = QtCore.QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)
      #QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),self.exit)
      #result = QtCore.QObject.connect(self.clickTool, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)
      #print result

   def handleMouseDown(self, point, button):
       #self.dlg.clearTextBrowser()
       #self.dlg.setTextBrowser( str(point.x()) + " , " +str(point.y()) )
       #QMessageBox.information( self.iface.mainWindow(),"Info", "X,Y = %s,%s" % (str(point.x()),str(point.y())) )
       print "handleMouseDown"
       self.ui.lineEditSourceNode.insert(str(point.x()), str(point.y()))

   def selectFeature(self, point, button):
       # Select Features function from http://www.qgisworkshop.org/html/workshop/plugins_tutorial.html
       #QtGui.QMessageBox.information( self.iface.mainWindow(),"Info", "in selectFeature function" )
       # setup the provider select to filter results based on a rectangle
       pntGeom = QgsGeometry.fromPoint(point)
       # scale-dependent buffer of 2 pixels-worth of map units
       pntBuff = pntGeom.buffer( (self.canvas.mapUnitsPerPixel() * 3),0)
       rect = pntBuff.boundingBox()
       # get currentLayer and dataProvider
       cLayer = self.canvas.currentLayer()
       
       #selectList = []
       if cLayer:
               provider = cLayer.dataProvider()
	       if cLayer.geometryType() == QGis.Point:
		       # clear any previous selection
		       cLayer.removeSelection()
		       feat = QgsFeature()
		       # create the select statement
		       provider.select([],rect) # the arguments mean no attributes returned, and do a bbox filter with our buffered rectangle to limit the amount of features
		       while provider.nextFeature(feat):
		               # if the feat geom returned from the selection intersects our point then put it in a list
		               if feat.geometry().intersects(rect):
				       cLayer.select(feat.id())
		                       #print float(feat.geometry().asPoint().x())
		                       #self.ui.lineEditSourceNode.clear()
		                       self.output.clear()
		                       #self.ui.lineEditSourceNode.insert(str(feat.geometry().asPoint().x())+','+str(feat.geometry().asPoint().y()))
		                       self.output.insert(str(feat.geometry().asPoint().x())+','+str(feat.geometry().asPoint().y()))
				       #print 'here: %f' % (feat.geometry().asPoint())
				       break 
		                       #selectList.append(feat.id())

		       # make the actual selection (select the first feature to avoid multiple selections)
		       #cLayer.setSelectedFeatures(selectList[0])
		       ##print help(cLayer)
		       #if len(selectList) > 0:
			       #cLayer.select(selectList[0])
	       else:
                       QtGui.QMessageBox.warning( self.iface.mainWindow(),"Error", "Selected node layer must be point geometry")	               
       else:
               QtGui.QMessageBox.information( self.iface.mainWindow(),"Info", "No layer currently selected in TOC" )

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
         #   QtGui.QMessageBox.information( self.iface.mainWindow(),"Info", "Node not found in Network") 
      #elif str(node[1]) == y:
      #	print 
     	#str_node = str(node)
     	#str_node = str_node.split(', ')
     	#print str_node[0] 
      p = nx.shortest_path(DG1, sourceNode, targetNode)
      print len(p)
      print p
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
      qgis.utils.iface.addVectorLayer(edges, "Shortest Route Network Edges", "ogr")
      qgis.utils.iface.addVectorLayer(nodes, "Shortest Route Network Nodes", "ogr")
	
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
      QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("clicked()"),self.exit)

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
      
