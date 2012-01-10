# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_NetworkX.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NetworkX(object):
    def setupUi(self, NetworkX):
        NetworkX.setObjectName("NetworkX")
        NetworkX.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(NetworkX)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(NetworkX)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NetworkX.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NetworkX.reject)
        QtCore.QMetaObject.connectSlotsByName(NetworkX)

    def retranslateUi(self, NetworkX):
        NetworkX.setWindowTitle(QtGui.QApplication.translate("NetworkX", "NetworkX", None, QtGui.QApplication.UnicodeUTF8))
