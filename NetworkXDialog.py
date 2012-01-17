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
__version__ = "0.2"

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
    def __init__(self, combolayers, filelist, geomtype=None):
        '''Method to add current shapefile layers to QT combo box, takes 
        comboBox ui reference and file list and adds suitable TOC layers to 
        both.
        '''
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        # Loop through loaded QGIS layers 
        for (layer) in layermap.itervalues():
            
            # Check layer type is vector
            if layer.type() == 0:
                # Check layer is from shapefile
                if str(layer.source()).endswith('.shp'):
                    # Check layer is correct geom
                    if geomtype is None:
                        
                        # Add to comboBox and filelist
                        combolayers.addItem(layer.name())
                        combolayers.setCurrentIndex(1)
                        filelist.append(layer.source())
                    else:
                        if layer.geometryType() == geomtype:
                            # Add to comboBox and filelist
                            combolayers.addItem(layer.name())
                            combolayers.setCurrentIndex(1)
                            filelist.append(layer.source())
            else:  
                combolayers.setCurrentIndex(0)
             
class WriteNetworkShapefiles:
    '''Abstract class to support writing of shapefiles from NetworkX'''
    def __init__(self, network, filedir, overwrite=False):
        nodes = filedir+'/nodes.*'
        edges = filedir+'/edges.*'
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
       
        nx_shp.write_shp(network, filedir)   


class NetworkXDialogPath(QtGui.QDockWidget, Ui_NetworkXPath, 
                         ShapeLayersToCombo):
    '''Dialog for running path analysis over network as QGIS PyQt plugin.'''
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent.iface.mainWindow()) 
        self.iface = qgis.utils.iface
        # Set up the user interface from Designer. 
        self.ui = Ui_NetworkXPath()
        self.ui.setupUi(self)
        self.loadmenus()
      
       # Counters for selected nodes on canvas which need to persist in the 
        #class.
        self.selected_nodes = {'source':None, 'target':None}
      
        QtCore.QObject.connect(self.ui.btnCancel, QtCore.SIGNAL("clicked()"),
                             self.exit)
        QtCore.QObject.connect(self.ui.comboBoxInputEdges, 
        QtCore.SIGNAL("activated(const QString&)"), self.attribute_weights)
        QtCore.QObject.connect(self.ui.btnSourceNode, 
                               QtCore.SIGNAL("clicked()"), self.source_point)
        QtCore.QObject.connect(self.ui.btnTargetNode, 
                               QtCore.SIGNAL("clicked()"), self.target_point)
        QtCore.QObject.connect(self.ui.btnOK, QtCore.SIGNAL("clicked()"),
                             self.shortest_path)
        QtCore.QObject.connect(self.ui.btnSave, QtCore.SIGNAL("clicked()"),
                             self.output_file)
        QtCore.QObject.connect(self.ui.btnReload, QtCore.SIGNAL("clicked()"),
                             self.clear_reload)
   
    def loadmenus(self): 
        '''Method to load required menus for the shortest path gui widget.'''
        # List available algorithms
        self.algorithms = {'Shortest Path':'shortest_path',
                         'Dijkstra':'dijkstra_path','A*':'astar_path'}
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
        self.attribute_weights()
      
    def clearinputs(self):
        '''Clear form of existing user data.'''
        self.ui.checkBoxUndirected.setChecked(False)
        self.ui.checkBoxOverwrite.setChecked(False)
        self.ui.comboBoxAlgorithm.clear()
        self.ui.comboBoxInputEdges.clear()
        self.ui.comboBoxInputNodes.clear()
        self.ui.comboBoxInputWeight.clear()
        self.ui.lineEditSourceNode.clear()
        self.ui.lineEditTargetNode.clear()
        self.ui.lineEditSave.clear()
       
    def clear_reload(self):
        '''Clear and then reload GUI with default options.'''
        # First clear any existing node selection on canvas
        layers = qgis.utils.iface.mapCanvas().layers()
        nodes = str(self.ui.comboBoxInputNodes.currentText())
        for layer in layers:
            if layer.name() == nodes:
                layer.removeSelection()
        self.selected_nodes = {'source':None, 'target':None}
        # Clear menus and inputs
        self.clearinputs()
        self.loadmenus()
      
    def attribute_weights(self):
        '''Method provides list of weights based on edge feature attributes.'''
        # Clear the attributeComboBoxList
        self.ui.comboBoxInputWeight.clear()
        self.ui.comboBoxInputWeight.addItem('None')
      
        # Add new attributes of layer to weights.         
        for layer in self.layermap.itervalues():
            edges = str(self.ui.comboBoxInputEdges.currentText())
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
                 
    def source_point(self):
        '''Method to setup collection of source node from map canvas.'''
        self.output = self.ui.lineEditSourceNode
        self.collect_point()
        self.nodetype = 'source'
      
    def target_point(self):
        '''Method to setup collection of target node from map canvas.''' 
        self.output = self.ui.lineEditTargetNode
        self.nodetype = 'target'
        self.collect_point()

    def collect_point(self):
        '''Method to collect point location from the QGIS map canvas.'''
        self.canvas = qgis.utils.iface.mapCanvas()
        self.point = QgsMapToolEmitPoint(qgis.utils.iface.mapCanvas())
        mapCanvas = qgis.utils.iface.mapCanvas()
        # Create the appropriate map tool and connect the gotPoint() signal.
        mapCanvas.setMapTool(self.point)
        QtCore.QObject.connect(self.point, 
         QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), 
             self.select_feature)
         
    def select_feature(self, point):
        '''Method to select feature from map canvas based on point location.'''
        # Select Features function from 
        # http://www.qgisworkshop.org/html/workshop/plugins_tutorial.html
        # setup the provider select to filter results based on a rectangle
        pntGeom = QgsGeometry.fromPoint(point)
        # scale-dependent buffer of 3 pixels-worth of map units
        pntBuff = pntGeom.buffer( (self.canvas.mapUnitsPerPixel() * 3), 0)
        rect = pntBuff.boundingBox()
        layers = qgis.utils.iface.mapCanvas().layers()
        nodes = str(self.ui.comboBoxInputNodes.currentText())
        for layer in layers:
            if layer.name() == nodes:
                provider = layer.dataProvider()
                if layer.geometryType() == QGis.Point:
                    feat = QgsFeature()
                    # create the select statement
                    provider.select([], rect) 
                    # the arguments mean no attributes returned and do a bbox 
                    # filter with our buffered rectangle to limit the amount 
                    #of features.
                    while provider.nextFeature(feat):
                        # if the feat geom returned from the selection 
                        #intersects our point then put it in selection list.
                        if feat.geometry().intersects(rect):
                            self.selected_nodes[self.nodetype] = feat.id()
                            self.output.clear()
                            self.output.insert(
                            str(feat.geometry().asPoint().x())+','
                                   +str(feat.geometry().asPoint().y()))
                            layer.removeSelection()
                            for featid in self.selected_nodes.itervalues():
                                if featid is not None:
                                    layer.select(featid)
                        break # stop here to select one point only. 
                       
    def output_file(self):
        '''Get output directory from Qt file dialog.'''
        try:
            self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, 
                                                    "Select Output Directory"))
            self.ui.lineEditSave.insert(self.fd)
        except IOError as e:
            self.ui.lineEditSave.clear()
            QtGui.QMessageBox.warning( self.iface.mainWindow(), 
                                     "NetworkX Plugin Error", "%s" % str(e))

    def shortest_path(self):
        ''' Method to compute shortest path over a graph using NetworkX.'''
        try: 
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
                raise IOError, "Specified target node not found in edge layer."
            try: 
                sourceNode
            except NameError:
                raise IOError, "Specified source node not found in edge layer."   
                      
            key = str(self.ui.comboBoxAlgorithm.currentText())
            algorithm = self.algorithms[key]
            method = getattr(nx, algorithm)
              
            weight = str(self.ui.comboBoxInputWeight.currentText()) 
            if weight == 'None':
                p = method(DG1, sourceNode, targetNode)
            else:
                p = method(DG1, sourceNode, targetNode, weight)
            DG2 = nx.DiGraph()
            for i in range(0, len(p)-1):
                DG2.add_edge(p[i], p[i+1])
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
              
        except (IOError, AttributeError, NameError, 
                  nx.NetworkXNoPath) as e:
            QtGui.QMessageBox.warning( self.iface.mainWindow(),
                                    "NetworkX Plugin Error", "%s" % str(e))
    def exit(self):
        '''Method to close plugin window.'''
        self.close() 
      
class NetworkXDialogBuild(QtGui.QDialog, ShapeLayersToCombo, 
                          WriteNetworkShapefiles):
    '''Class to convert shapefiles to NetworkX format edges.shp and nodes.shp'''
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
          "clicked()"),self.output_file)
          
        self.filelist = ["Available layers:"]      
        self.ui.comboBoxInput.addItem(self.filelist[0])
        ShapeLayersToCombo(self.ui.comboBoxInput, self.filelist, 1)
         
    def output_file(self):
        '''Get output directory from Qt file dialog.'''
        try:
            self.fd = str(QtGui.QFileDialog.getExistingDirectory(self, 
                                                    "Select Output Directory"))
            self.ui.lineEditSave.insert(self.fd)
        except IOError as e:
            self.ui.lineEditSave.clear()
            QtGui.QMessageBox.warning( self.iface.mainWindow(), 
                                     "NetworkX Plugin Error", "%s" % str(e))
    
    def buildNetwork(self):
        '''Method to create NetworkX nodes and edges shapefiles.'''
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
        '''Method to close plugin window.'''
        self.close()