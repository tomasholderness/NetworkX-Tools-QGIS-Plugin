# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NetworkX_build.ui'
#
# Created: Fri Jan 13 12:11:12 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NetworkXBuild(object):
    def setupUi(self, NetworkXBuild):
        NetworkXBuild.setObjectName("NetworkXBuild")
        NetworkXBuild.resize(431, 179)
        NetworkXBuild.setAccessibleName("")
        self.comboBoxInput = QtGui.QComboBox(NetworkXBuild)
        self.comboBoxInput.setGeometry(QtCore.QRect(170, 20, 251, 31))
        self.comboBoxInput.setObjectName("comboBoxInput")
        self.labelInput = QtGui.QLabel(NetworkXBuild)
        self.labelInput.setGeometry(QtCore.QRect(20, 30, 171, 17))
        self.labelInput.setObjectName("labelInput")
        self.labelOutput = QtGui.QLabel(NetworkXBuild)
        self.labelOutput.setGeometry(QtCore.QRect(20, 70, 171, 31))
        self.labelOutput.setObjectName("labelOutput")
        self.lineEditSave = QtGui.QLineEdit(NetworkXBuild)
        self.lineEditSave.setGeometry(QtCore.QRect(210, 70, 211, 31))
        self.lineEditSave.setObjectName("lineEditSave")
        self.btnOK = QtGui.QPushButton(NetworkXBuild)
        self.btnOK.setEnabled(True)
        self.btnOK.setGeometry(QtCore.QRect(340, 140, 81, 27))
        self.btnOK.setObjectName("btnOK")
        self.btnCancel = QtGui.QPushButton(NetworkXBuild)
        self.btnCancel.setGeometry(QtCore.QRect(250, 140, 81, 27))
        self.btnCancel.setObjectName("btnCancel")
        self.btnSave = QtGui.QPushButton(NetworkXBuild)
        self.btnSave.setGeometry(QtCore.QRect(170, 70, 31, 31))
        self.btnSave.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/NetworkX/icon/mActionFolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon)
        self.btnSave.setObjectName("btnSave")
        self.checkBoxOverwrite = QtGui.QCheckBox(NetworkXBuild)
        self.checkBoxOverwrite.setGeometry(QtCore.QRect(20, 110, 181, 22))
        self.checkBoxOverwrite.setObjectName("checkBoxOverwrite")
        self.checkBoxAdd = QtGui.QCheckBox(NetworkXBuild)
        self.checkBoxAdd.setGeometry(QtCore.QRect(210, 110, 181, 22))
        self.checkBoxAdd.setObjectName("checkBoxAdd")

        self.retranslateUi(NetworkXBuild)
        QtCore.QMetaObject.connectSlotsByName(NetworkXBuild)

    def retranslateUi(self, NetworkXBuild):
        NetworkXBuild.setWindowTitle(QtGui.QApplication.translate("NetworkXBuild", "NetworkX Plugin - Build Network", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInput.setText(QtGui.QApplication.translate("NetworkXBuild", "Input shapefile layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutput.setText(QtGui.QApplication.translate("NetworkXBuild", "Output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("NetworkXBuild", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("NetworkXBuild", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOverwrite.setText(QtGui.QApplication.translate("NetworkXBuild", "Overwrite existing files", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAdd.setText(QtGui.QApplication.translate("NetworkXBuild", "Add new files to QGIS", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
