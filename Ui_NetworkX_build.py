# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_NetworkX_build.ui'
#
# Created: Tue Jan  3 20:14:54 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NetworkXBuild(object):
    def setupUi(self, NetworkXBuild):
        NetworkXBuild.setObjectName(_fromUtf8("NetworkXBuild"))
        NetworkXBuild.resize(431, 158)
        NetworkXBuild.setWindowTitle(QtGui.QApplication.translate("NetworkXBuild", "NetworkX Plugin - Build Network", None, QtGui.QApplication.UnicodeUTF8))
        NetworkXBuild.setAccessibleName(_fromUtf8(""))
        self.comboBoxInput = QtGui.QComboBox(NetworkXBuild)
        self.comboBoxInput.setGeometry(QtCore.QRect(180, 20, 241, 31))
        self.comboBoxInput.setObjectName(_fromUtf8("comboBoxInput"))
        self.labelInput = QtGui.QLabel(NetworkXBuild)
        self.labelInput.setGeometry(QtCore.QRect(20, 30, 171, 17))
        self.labelInput.setText(QtGui.QApplication.translate("NetworkXBuild", "Input shapefile layer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInput.setObjectName(_fromUtf8("labelInput"))
        self.labelOutput = QtGui.QLabel(NetworkXBuild)
        self.labelOutput.setGeometry(QtCore.QRect(20, 70, 171, 31))
        self.labelOutput.setText(QtGui.QApplication.translate("NetworkXBuild", "Output shapefile folder", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutput.setObjectName(_fromUtf8("labelOutput"))
        self.lineEdit = QtGui.QLineEdit(NetworkXBuild)
        self.lineEdit.setGeometry(QtCore.QRect(180, 70, 241, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.btnOK = QtGui.QPushButton(NetworkXBuild)
        self.btnOK.setEnabled(True)
        self.btnOK.setGeometry(QtCore.QRect(340, 120, 81, 27))
        self.btnOK.setText(QtGui.QApplication.translate("NetworkXBuild", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.btnCancel = QtGui.QPushButton(NetworkXBuild)
        self.btnCancel.setGeometry(QtCore.QRect(250, 120, 81, 27))
        self.btnCancel.setText(QtGui.QApplication.translate("NetworkXBuild", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.retranslateUi(NetworkXBuild)
        QtCore.QMetaObject.connectSlotsByName(NetworkXBuild)

    def retranslateUi(self, NetworkXBuild):
        pass

