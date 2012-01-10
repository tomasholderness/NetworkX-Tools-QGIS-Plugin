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
# 07-01-2012 - TH - Added check for NetworkX module in initGui

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
import qgis
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
#from NetworkXDialog import NetworkXDialog
from NetworkXDialog import NetworkXDialogPath
from NetworkXDialog import NetworkXDialogBuild

class NetworkX: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    try:
        import networkx as nx
    except ImportError:
        QMessageBox.warning(self.iface.mainWindow(),"NetworkX Plugin Error", "NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/")
        raise ImportError("NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/") 
    # Create actions that will start plugin configuration (seperate action for each tool)
    self.actionBuild = QAction(QIcon(":/plugins/NetworkX/icon.png"), \
        "Build Network", self.iface.mainWindow())
    self.actionPath = QAction(QIcon(":/plugins/NetworkX/icon.png"), \
        "Find Shortest Path", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.actionBuild, SIGNAL("activated()"), self.runBuild) 
    QObject.connect(self.actionPath, SIGNAL("activated()"), self.runPath)
    # Add toolbar button and menu item
    #self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&NetworkX Plugin", self.actionBuild)
    self.iface.addPluginToMenu("&NetworkX Plugin", self.actionPath)
  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&NetworkX Plugin",self.actionBuild)
    self.iface.removePluginMenu("&NetworkX Plugin",self.actionPath)    
    #self.iface.removeToolBarIcon(self.action)




  # run methods that performs all the real work (one run method per tool)
  def runBuild(self): 
    # create and show the dialog 
    dlg = NetworkXDialogBuild() 
    # show the dialog
    dlg.show()
    result = dlg.exec_() 
    # See if OK was pressed
    #if result == 1:
    	#dlg.comboBoxInput.setEnabled(False)
    	

  def runPath(self): 
    # create and show the dialog 
    dlg = NetworkXDialogPath() 
    # show the dialog
    dlg.show()
    result = dlg.exec_() 
    # See if OK was pressed
    #if result == 1:
    	#process here. 
	#  pass       
