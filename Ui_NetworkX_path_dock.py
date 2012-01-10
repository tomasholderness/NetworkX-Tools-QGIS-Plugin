# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NetworkX_path_dock.ui'
#
# Created: Tue Jan 10 18:03:48 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NetworkXPath(object):
    def setupUi(self, NetworkXPath):
        NetworkXPath.setObjectName(_fromUtf8("NetworkXPath"))
        NetworkXPath.resize(424, 404)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NetworkXPath.sizePolicy().hasHeightForWidth())
        NetworkXPath.setSizePolicy(sizePolicy)
        NetworkXPath.setWindowTitle(QtGui.QApplication.translate("NetworkXPath", "NetworkX Plugin - Shortest Path", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.labelNodes = QtGui.QLabel(self.dockWidgetContents)
        self.labelNodes.setEnabled(True)
        self.labelNodes.setGeometry(QtCore.QRect(10, 70, 171, 17))
        self.labelNodes.setText(QtGui.QApplication.translate("NetworkXPath", "Node layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNodes.setObjectName(_fromUtf8("labelNodes"))
        self.labelTargetNode = QtGui.QLabel(self.dockWidgetContents)
        self.labelTargetNode.setGeometry(QtCore.QRect(10, 240, 91, 31))
        self.labelTargetNode.setText(QtGui.QApplication.translate("NetworkXPath", "Target Node", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTargetNode.setObjectName(_fromUtf8("labelTargetNode"))
        self.labelEdges = QtGui.QLabel(self.dockWidgetContents)
        self.labelEdges.setGeometry(QtCore.QRect(10, 110, 171, 17))
        self.labelEdges.setText(QtGui.QApplication.translate("NetworkXPath", "Edge layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges.setObjectName(_fromUtf8("labelEdges"))
        self.lineEditSourceNode = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditSourceNode.setGeometry(QtCore.QRect(150, 200, 261, 27))
        self.lineEditSourceNode.setObjectName(_fromUtf8("lineEditSourceNode"))
        self.labelEdges_2 = QtGui.QLabel(self.dockWidgetContents)
        self.labelEdges_2.setGeometry(QtCore.QRect(10, 150, 171, 17))
        self.labelEdges_2.setText(QtGui.QApplication.translate("NetworkXPath", "Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEdges_2.setObjectName(_fromUtf8("labelEdges_2"))
        self.comboBoxInputEdges = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputEdges.setGeometry(QtCore.QRect(110, 100, 301, 31))
        self.comboBoxInputEdges.setObjectName(_fromUtf8("comboBoxInputEdges"))
        self.btnOK = QtGui.QPushButton(self.dockWidgetContents)
        self.btnOK.setEnabled(True)
        self.btnOK.setGeometry(QtCore.QRect(330, 340, 81, 27))
        self.btnOK.setText(QtGui.QApplication.translate("NetworkXPath", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.lineEditTargetNode = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditTargetNode.setGeometry(QtCore.QRect(150, 240, 261, 27))
        self.lineEditTargetNode.setObjectName(_fromUtf8("lineEditTargetNode"))
        self.comboBoxInputWeight = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputWeight.setGeometry(QtCore.QRect(110, 140, 301, 31))
        self.comboBoxInputWeight.setObjectName(_fromUtf8("comboBoxInputWeight"))
        self.btnCancel = QtGui.QPushButton(self.dockWidgetContents)
        self.btnCancel.setGeometry(QtCore.QRect(240, 340, 81, 27))
        self.btnCancel.setText(QtGui.QApplication.translate("NetworkXPath", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.btnSourceNode = QtGui.QPushButton(self.dockWidgetContents)
        self.btnSourceNode.setGeometry(QtCore.QRect(110, 200, 31, 27))
        self.btnSourceNode.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSourceNode.setIcon(icon)
        self.btnSourceNode.setObjectName(_fromUtf8("btnSourceNode"))
        self.btnTargetNode = QtGui.QPushButton(self.dockWidgetContents)
        self.btnTargetNode.setGeometry(QtCore.QRect(110, 240, 31, 27))
        self.btnTargetNode.setText(_fromUtf8(""))
        self.btnTargetNode.setIcon(icon)
        self.btnTargetNode.setObjectName(_fromUtf8("btnTargetNode"))
        self.comboBoxInputNodes = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputNodes.setEnabled(True)
        self.comboBoxInputNodes.setGeometry(QtCore.QRect(110, 60, 301, 31))
        self.comboBoxInputNodes.setObjectName(_fromUtf8("comboBoxInputNodes"))
        self.labelSourceNode = QtGui.QLabel(self.dockWidgetContents)
        self.labelSourceNode.setGeometry(QtCore.QRect(10, 200, 91, 31))
        self.labelSourceNode.setText(QtGui.QApplication.translate("NetworkXPath", "Source Node", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSourceNode.setObjectName(_fromUtf8("labelSourceNode"))
        self.LabelSave = QtGui.QLabel(self.dockWidgetContents)
        self.LabelSave.setGeometry(QtCore.QRect(10, 300, 101, 31))
        self.LabelSave.setText(QtGui.QApplication.translate("NetworkXPath", "Output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.LabelSave.setObjectName(_fromUtf8("LabelSave"))
        self.lineEditSave = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditSave.setGeometry(QtCore.QRect(150, 300, 261, 27))
        self.lineEditSave.setObjectName(_fromUtf8("lineEditSave"))
        self.btnSave_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.btnSave_2.setGeometry(QtCore.QRect(110, 300, 31, 27))
        self.btnSave_2.setText(_fromUtf8(""))
        self.btnSave_2.setIcon(icon)
        self.btnSave_2.setObjectName(_fromUtf8("btnSave_2"))
        self.checkBoxOverwrite = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBoxOverwrite.setGeometry(QtCore.QRect(10, 340, 181, 22))
        self.checkBoxOverwrite.setText(QtGui.QApplication.translate("NetworkXPath", "Overwrite existing files", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOverwrite.setObjectName(_fromUtf8("checkBoxOverwrite"))
        self.labelNodes_2 = QtGui.QLabel(self.dockWidgetContents)
        self.labelNodes_2.setEnabled(True)
        self.labelNodes_2.setGeometry(QtCore.QRect(10, 20, 171, 17))
        self.labelNodes_2.setText(QtGui.QApplication.translate("NetworkXPath", "Algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNodes_2.setObjectName(_fromUtf8("labelNodes_2"))
        self.comboBoxInputNodes_2 = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBoxInputNodes_2.setEnabled(True)
        self.comboBoxInputNodes_2.setGeometry(QtCore.QRect(110, 10, 301, 31))
        self.comboBoxInputNodes_2.setObjectName(_fromUtf8("comboBoxInputNodes_2"))
        NetworkXPath.setWidget(self.dockWidgetContents)

        self.retranslateUi(NetworkXPath)
        QtCore.QMetaObject.connectSlotsByName(NetworkXPath)

    def retranslateUi(self, NetworkXPath):
        pass

