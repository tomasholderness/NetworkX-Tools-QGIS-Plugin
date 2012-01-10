# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NetworkX_path_dock.ui'
#
# Created: Tue Jan 10 14:55:00 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NetworkXPath(object):
    def setupUi(self, NetworkXPath):
        NetworkXPath.setObjectName("NetworkXPath")
        NetworkXPath.resize(424, 270)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.labelNodes = QtGui.QLabel(self.dockWidgetContents)
        self.labelNodes.setEnabled(True)
        self.labelNodes.setGeometry(QtCore.QRect(10, 10, 171, 17))
        self.labelNodes.setObjectName("labelNodes")
        self.labelTargetNode = QtGui.QLabel(self.dockWidgetContents)
        self.labelTargetNode.setGeometry(QtCore.QRect(10, 170, 91, 31))
        self.labelTargetNode.setObjectName("labelTargetNode")
        self.labelEdges = QtGui.QLabel(self.dockWidgetContents)
        self.labelEdges.setGeometry(QtCore.QRect(10, 50, 171, 17))
        self.labelEdges.setObjectName("labelEdges")
        self.lineEditSourceNode = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditSourceNode.setGeometry(QtCore.QRect(150, 130, 261, 27))
        self.lineEditSourceNode.setObjectName("lineEditSourceNode")
        self.labelEdges_2 = QtGui.QLabel(self.dockWidgetContents)
        self.labelEdges_2.setGeometry(QtCore.QRect(10, 90, 171, 17))
        self.labelEdges_2.setObjectName("labelEdges_2")
        self.comboBoxInputEdges = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputEdges.setGeometry(QtCore.QRect(110, 40, 301, 31))
        self.comboBoxInputEdges.setObjectName("comboBoxInputEdges")
        self.btnOK = QtGui.QPushButton(self.dockWidgetContents)
        self.btnOK.setEnabled(True)
        self.btnOK.setGeometry(QtCore.QRect(330, 210, 81, 27))
        self.btnOK.setObjectName("btnOK")
        self.lineEditTargetNode = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditTargetNode.setGeometry(QtCore.QRect(150, 170, 261, 27))
        self.lineEditTargetNode.setObjectName("lineEditTargetNode")
        self.comboBoxInputWeight = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputWeight.setGeometry(QtCore.QRect(110, 80, 301, 31))
        self.comboBoxInputWeight.setObjectName("comboBoxInputWeight")
        self.btnCancel = QtGui.QPushButton(self.dockWidgetContents)
        self.btnCancel.setGeometry(QtCore.QRect(240, 210, 81, 27))
        self.btnCancel.setObjectName("btnCancel")
        self.btnSourceNode = QtGui.QPushButton(self.dockWidgetContents)
        self.btnSourceNode.setGeometry(QtCore.QRect(110, 130, 31, 27))
        self.btnSourceNode.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSourceNode.setIcon(icon)
        self.btnSourceNode.setObjectName("btnSourceNode")
        self.btnTargetNode = QtGui.QPushButton(self.dockWidgetContents)
        self.btnTargetNode.setGeometry(QtCore.QRect(110, 170, 31, 27))
        self.btnTargetNode.setText("")
        self.btnTargetNode.setIcon(icon)
        self.btnTargetNode.setObjectName("btnTargetNode")
        self.comboBoxInputNodes = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputNodes.setEnabled(True)
        self.comboBoxInputNodes.setGeometry(QtCore.QRect(110, 0, 301, 31))
        self.comboBoxInputNodes.setObjectName("comboBoxInputNodes")
        self.labelSourceNode = QtGui.QLabel(self.dockWidgetContents)
        self.labelSourceNode.setGeometry(QtCore.QRect(10, 130, 91, 31))
        self.labelSourceNode.setObjectName("labelSourceNode")
        NetworkXPath.setWidget(self.dockWidgetContents)

        self.retranslateUi(NetworkXPath)
        QtCore.QMetaObject.connectSlotsByName(NetworkXPath)

    def retranslateUi(self, NetworkXPath):
        NetworkXPath.setWindowTitle(QtGui.QApplication.translate("NetworkXPath", "NetworkX Plugin - Shortest Path", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNodes.setText(QtGui.QApplication.translate("NetworkXPath", "Node layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTargetNode.setText(QtGui.QApplication.translate("NetworkXPath", "Target Node", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges.setText(QtGui.QApplication.translate("NetworkXPath", "Edge layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges_2.setText(QtGui.QApplication.translate("NetworkXPath", "Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("NetworkXPath", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("NetworkXPath", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSourceNode.setText(QtGui.QApplication.translate("NetworkXPath", "Source Node", None, QtGui.QApplication.UnicodeUTF8))

