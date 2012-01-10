# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NetworkX_path.ui'
#
# Created: Fri Jan  6 15:29:52 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NetworkXPath(object):
    def setupUi(self, NetworkXPath):
        NetworkXPath.setObjectName("NetworkXPath")
        NetworkXPath.resize(428, 269)
        self.comboBoxInputNodes = QtGui.QComboBox(NetworkXPath)
        self.comboBoxInputNodes.setEnabled(False)
        self.comboBoxInputNodes.setGeometry(QtCore.QRect(120, 20, 301, 31))
        self.comboBoxInputNodes.setObjectName("comboBoxInputNodes")
        self.labelNodes = QtGui.QLabel(NetworkXPath)
        self.labelNodes.setEnabled(False)
        self.labelNodes.setGeometry(QtCore.QRect(20, 30, 171, 17))
        self.labelNodes.setObjectName("labelNodes")
        self.comboBoxInputEdges = QtGui.QComboBox(NetworkXPath)
        self.comboBoxInputEdges.setGeometry(QtCore.QRect(120, 60, 301, 31))
        self.comboBoxInputEdges.setObjectName("comboBoxInputEdges")
        self.labelEdges = QtGui.QLabel(NetworkXPath)
        self.labelEdges.setGeometry(QtCore.QRect(20, 70, 171, 17))
        self.labelEdges.setObjectName("labelEdges")
        self.labelEdges_2 = QtGui.QLabel(NetworkXPath)
        self.labelEdges_2.setGeometry(QtCore.QRect(20, 110, 171, 17))
        self.labelEdges_2.setObjectName("labelEdges_2")
        self.comboBoxInputWeight = QtGui.QComboBox(NetworkXPath)
        self.comboBoxInputWeight.setGeometry(QtCore.QRect(120, 100, 301, 31))
        self.comboBoxInputWeight.setObjectName("comboBoxInputWeight")
        self.labelSourceNode = QtGui.QLabel(NetworkXPath)
        self.labelSourceNode.setGeometry(QtCore.QRect(20, 150, 171, 31))
        self.labelSourceNode.setObjectName("labelSourceNode")
        self.lineEditSourceNode = QtGui.QLineEdit(NetworkXPath)
        self.lineEditSourceNode.setGeometry(QtCore.QRect(160, 150, 261, 27))
        self.lineEditSourceNode.setObjectName("lineEditSourceNode")
        self.lineEditTargetNode = QtGui.QLineEdit(NetworkXPath)
        self.lineEditTargetNode.setGeometry(QtCore.QRect(160, 190, 261, 27))
        self.lineEditTargetNode.setObjectName("lineEditTargetNode")
        self.labelTargetNode = QtGui.QLabel(NetworkXPath)
        self.labelTargetNode.setGeometry(QtCore.QRect(20, 190, 171, 31))
        self.labelTargetNode.setObjectName("labelTargetNode")
        self.btnSourceNode = QtGui.QPushButton(NetworkXPath)
        self.btnSourceNode.setGeometry(QtCore.QRect(120, 150, 31, 27))
        self.btnSourceNode.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSourceNode.setIcon(icon)
        self.btnSourceNode.setObjectName("btnSourceNode")
        self.btnTargetNode = QtGui.QPushButton(NetworkXPath)
        self.btnTargetNode.setGeometry(QtCore.QRect(120, 190, 31, 27))
        self.btnTargetNode.setText("")
        self.btnTargetNode.setIcon(icon)
        self.btnTargetNode.setObjectName("btnTargetNode")
        self.btnOK = QtGui.QPushButton(NetworkXPath)
        self.btnOK.setEnabled(True)
        self.btnOK.setGeometry(QtCore.QRect(340, 230, 81, 27))
        self.btnOK.setObjectName("btnOK")
        self.btnCancel = QtGui.QPushButton(NetworkXPath)
        self.btnCancel.setGeometry(QtCore.QRect(250, 230, 81, 27))
        self.btnCancel.setObjectName("btnCancel")

        self.retranslateUi(NetworkXPath)
        QtCore.QMetaObject.connectSlotsByName(NetworkXPath)

    def retranslateUi(self, NetworkXPath):
        NetworkXPath.setWindowTitle(QtGui.QApplication.translate("NetworkXPath", "NetworkX Plugin - Shortest Path", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNodes.setText(QtGui.QApplication.translate("NetworkXPath", "Node layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges.setText(QtGui.QApplication.translate("NetworkXPath", "Edge layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges_2.setText(QtGui.QApplication.translate("NetworkXPath", "Weight", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSourceNode.setText(QtGui.QApplication.translate("NetworkXPath", "Source Node", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTargetNode.setText(QtGui.QApplication.translate("NetworkXPath", "Target Node", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("NetworkXPath", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("NetworkXPath", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

