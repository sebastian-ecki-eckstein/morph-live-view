# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_morph_live_view.ui'
#
# Created: Thu Aug 15 16:09:58 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_morph_live_view(object):
    def setupUi(self, morph_live_view):
        morph_live_view.setObjectName(_fromUtf8("morph_live_view"))
        morph_live_view.resize(629, 282)
        self.chkActivate = QtGui.QCheckBox(morph_live_view)
        self.chkActivate.setGeometry(QtCore.QRect(30, 230, 97, 31))
        self.chkActivate.setObjectName(_fromUtf8("chkActivate"))
        self.tableVehicle = QtGui.QTableWidget(morph_live_view)
        self.tableVehicle.setEnabled(True)
        self.tableVehicle.setGeometry(QtCore.QRect(10, 20, 601, 191))
        self.tableVehicle.setRowCount(0)
        self.tableVehicle.setColumnCount(6)
        self.tableVehicle.setObjectName(_fromUtf8("tableVehicle"))
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableVehicle.setHorizontalHeaderItem(5, item)

        self.retranslateUi(morph_live_view)
        QtCore.QMetaObject.connectSlotsByName(morph_live_view)

    def retranslateUi(self, morph_live_view):
        morph_live_view.setWindowTitle(QtGui.QApplication.translate("morph_live_view", "morph_live_view", None, QtGui.QApplication.UnicodeUTF8))
        self.chkActivate.setText(QtGui.QApplication.translate("morph_live_view", "Activate\n"
"(check)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Name", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Count", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableVehicle.horizontalHeaderItem(5)
        item.setText(QtGui.QApplication.translate("morph_live_view", "Pi/Min", None, QtGui.QApplication.UnicodeUTF8))

