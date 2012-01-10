"""
/******************************************************************************
Name		            : NetworkX Plugin
Description          : Perform network analysis using the NetworkX package 
Date                 : 03/01/2012
copyright            : (C) 2012 Tom Holderness & Newcastle University
contact              : http://www.students.ncl.ac.uk/tom.holderness
email		            : tom.holderness@ncl.ac.uk 
license		         : Relseased under Simplified BSD license (see LICENSE.txt)
******************************************************************************/
"""

__author__ = """Tom Holderness (tom.holderness@ncl.ac.uk)"""
def name(): 
  return "NetworkX Plugin" 
def description():
  return "Perform network analysis using the NetworkX package"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.7"
def classFactory(iface):
#  # load NetworkX class from file NetworkX
  from NetworkX import NetworkX 
  return NetworkX(iface)
