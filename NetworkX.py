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

NAME = "NetworkX Tools"

class NetworkX: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def create_action(self,meta):
    action = QAction(QCoreApplication.translate( NAME, "&%s" % meta['title'] ), self.iface.mainWindow())
    tooltip = meta.get('tooltip')
    if tooltip:
      action.setWhatsThis(tooltip)
      action.setToolTip(tooltip)
      action.setStatusTip(tooltip)
    icon = meta.get('icon')
    if icon:
      action.setIcon(QIcon(icon))
    action_name = '%s_action' % meta['action']
    setattr(self,action_name,action)
    QObject.connect(getattr(self,action_name), SIGNAL("triggered()"), getattr(self,meta['action']))
    return getattr(self,action_name)

  def create_menu(self, actions):
    # Borrowed from OSM tools plugin.
    self.menu = QMenu()
    self.menu.setTitle(QCoreApplication.translate(NAME, "&%s" % NAME))
    for action in actions:
      self.menu.addAction(self.create_action(action))
    #self.menu.addSeparator()    
    menu_bar = self.iface.mainWindow().menuBar()
    actions = menu_bar.actions()
    lastAction = actions[ len( actions ) - 1 ]
    menu_bar.insertMenu( lastAction, self.menu )    
    self.unload = self.unload_menu

  def unload_menu(self):
    pass

  def initGui(self):
    try:
        import networkx as nx
    except ImportError:
        QMessageBox.critical(self.iface.mainWindow(),"NetworkX Plugin Error", "NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/")
        raise ImportError("NetworkX Plugin requires NetworkX: http://networkx.lanl.gov/") 
   
    actions = []
    actions.append({
                  'title':'Build network',
                  'action':'runBuild',
                  'tooltip':'Create edges and node shapefiles from existing lines'
                  #'icon':'/path/'   
                  })
    actions.append({
                  'title':'Find shortest path',
                  'action':'runPath',
                  'tooltip':'Compute shortest path over network'
                  })
    self.create_menu(actions)
    '''
    # Create actions that will start plugin configuration (seperate action for each tool)
    self.actionBuild = QAction(QIcon(":/plugins/NetworkX/icon.png"), \
        "Build Network", self.iface.mainWindow())
    self.actionPath = QAction(QIcon(":/plugins/NetworkX/icon.png"), \
        "Find Shortest Path", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.actionBuild, SIGNAL("activated()"), self.runBuild) 
    QObject.connect(self.actionPath, SIGNAL("activated()"), self.runPath)
    # Add tools to menu
    #self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&NetworkX Plugin", self.actionBuild)
    self.iface.addPluginToMenu("&NetworkX Plugin", self.actionPath)
    '''
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
    from NetworkXDialog import  NetworkXDialogPath
    self.dock_window = NetworkXDialogPath(self)
    self.iface.mainWindow().addDockWidget(Qt.LeftDockWidgetArea, self.dock_window)
    '''
    dlg = NetworkXDialogPath() 
    # show the dialog
    dlg.show()
    result = dlg.exec_() 
    # See if OK was pressed
    #if result == 1:
    	#process here. 
	 #  pass       
	 '''
