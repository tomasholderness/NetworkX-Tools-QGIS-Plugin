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

# Import the PyQt and QGIS libraries
import qgis
from PyQt4 import QtGui
from PyQt4 import QtCore
# Import the code for the dialog
from NetworkXDialog import NetworkXDialogPath
from NetworkXDialog import NetworkXDialogBuild
# Initialize Qt resources from file resources.py
import resources_rc
NAME = "NetworkX Tools"

class NetworkX: 
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
    def initGui(self):
        try:
            import networkx
        except ImportError:
            QtGui.QMessageBox.critical(self.iface.mainWindow(),
"NetworkX Plugin Error", 
"NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/")
        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
        ":/plugins/NetworkX/icon/plugin_small.png"), QtGui.QIcon.Normal, 
            QtGui.QIcon.Off)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
        ":/plugins/NetworkX/icon/mActionHelpContents.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
         
        # Create action that will start plugin configuration    
        self.actionBuild = QtGui.QAction(icon1,"Build Network", 
                                         self.iface.mainWindow())
        self.actionPath = QtGui.QAction(icon1,"Shortest Path", 
                                        self.iface.mainWindow())
        self.actionHelp = QtGui.QAction(icon2, "Documentation",
                                        self.iface.mainWindow())
        
        # connect the action to the run method
        QtCore.QObject.connect(self.actionBuild, QtCore.SIGNAL(
                                                "triggered()"), self.runBuild)
        QtCore.QObject.connect(self.actionPath, QtCore.SIGNAL(
                                                "triggered()"), self.runPath)
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL(
                                                "triggered()"), self.runHelp)
      
        self.iface.addPluginToMenu("&NetworkX Tools", self.actionBuild)
        self.iface.addPluginToMenu("&NetworkX Tools", self.actionPath)
        self.iface.addPluginToMenu("&NetworkX Tools", self.actionHelp)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&NetworkX Tools", self.actionBuild)
        self.iface.removePluginMenu("&NetworkX Tools", self.actionPath)
        self.iface.removePluginMenu("&NetworkX Tools", self.actionHelp)

  # run methods that performs all the real work (one run method per tool)
    def runBuild(self): 
        # create and show the dialog 
        dlg = NetworkXDialogBuild() 
        # show the dialog
        dlg.show()
        result = dlg.exec_() 
    
    def runPath(self): 
        # create and show the dialog
        self.dock_window = NetworkXDialogPath(self)
        self.iface.mainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, 
                                                self.dock_window)
    
    def runHelp(self):
        qgis.utils.showPluginHelp()