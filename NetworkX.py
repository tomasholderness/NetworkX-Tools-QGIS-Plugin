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
__version__ = "0.1"

# Import the PyQt and QGIS libraries
#from PyQt4.QtCore import * 
#from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
#from PyQt4.QtCore import * 
from qgis.core import *
# Initialize Qt resources from file resources.py
# Import the code for the dialog
#from NetworkXDialog import NetworkXDialog
from NetworkXDialog import NetworkXDialogPath
from NetworkXDialog import NetworkXDialogBuild
import resources
NAME = "NetworkX Tools"

class NetworkX: 

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
  
    
    def initGui(self):
        try:
            import networkx
        except ImportError:
            QMessageBox.critical(self.iface.mainWindow(),"NetworkX Plugin Error", "NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/")
        #raise ImportError("NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/") 
        
        # Create action that will start plugin configuration    
        self.actionBuild = QtGui.QAction(QtGui.QIcon(":/plugins/NetworkX/icon/plugin.png"),"Build Network",
                                    self.iface.mainWindow())
        self.actionPath = QtGui.QAction(QtGui.QIcon(":/plugins/NetworkX/icon/plugin.png"),"Shortest Path",
                                    self.iface.mainWindow())
        # connect the action to the run method
        QtCore.QObject.connect(self.actionBuild, QtCore.SIGNAL("triggered()"), self.runBuild)
        QtCore.QObject.connect(self.actionPath, QtCore.SIGNAL("triggered()"), self.runPath)
      
        self.iface.addPluginToMenu("&NetworkX Tools", self.actionBuild)
        self.iface.addPluginToMenu("&NetworkX Tools", self.actionPath)
  

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&NetworkX Tools",self.actionBuild)
        self.iface.removePluginMenu("&NetworkX Tools",self.actionPath)    

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
        self.iface.mainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_window)
