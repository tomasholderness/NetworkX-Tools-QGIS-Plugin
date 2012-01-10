"""
/***************************************************************************
Name			 	 : NetworkX Plugin
Description          : Perform network analysis using the NetworkX package
Date                 : 03/Jan/12 
copyright            : (C) 2012 by Tom Holderness / Newcastle University
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
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "NetworkX Plugin" 
def description():
  return "Perform network analysis using the NetworkX package"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.7"
def classFactory(iface): 
  # load NetworkX class from file NetworkX
  from NetworkX import NetworkX 
  return NetworkX(iface)
