# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_new_grid.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(247, 172)
        window.setMinimumSize(QtCore.QSize(247, 172))
        window.setMaximumSize(QtCore.QSize(247, 172))
        self.opt_square = QtWidgets.QRadioButton(window)
        self.opt_square.setGeometry(QtCore.QRect(30, 37, 119, 28))
        self.opt_square.setMinimumSize(QtCore.QSize(0, 28))
        self.opt_square.setMaximumSize(QtCore.QSize(140, 28))
        self.opt_square.setObjectName("opt_square")
        self.spb_width = QtWidgets.QSpinBox(window)
        self.spb_width.setGeometry(QtCore.QRect(23, 73, 80, 28))
        self.spb_width.setMinimumSize(QtCore.QSize(38, 28))
        self.spb_width.setMaximumSize(QtCore.QSize(80, 28))
        self.spb_width.setMinimum(1)
        self.spb_width.setMaximum(999)
        self.spb_width.setProperty("value", 30)
        self.spb_width.setObjectName("spb_width")
        self.btn_create = QtWidgets.QPushButton(window)
        self.btn_create.setGeometry(QtCore.QRect(153, 120, 75, 31))
        self.btn_create.setAutoDefault(True)
        self.btn_create.setObjectName("btn_create")
        self.btn_cancel = QtWidgets.QPushButton(window)
        self.btn_cancel.setGeometry(QtCore.QRect(23, 120, 75, 31))
        self.btn_cancel.setAutoDefault(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.spb_height = QtWidgets.QSpinBox(window)
        self.spb_height.setGeometry(QtCore.QRect(133, 73, 80, 28))
        self.spb_height.setMinimumSize(QtCore.QSize(38, 28))
        self.spb_height.setMaximumSize(QtCore.QSize(80, 28))
        self.spb_height.setMinimum(1)
        self.spb_height.setMaximum(999)
        self.spb_height.setProperty("value", 30)
        self.spb_height.setObjectName("spb_height")
        self.label_2 = QtWidgets.QLabel(window)
        self.label_2.setGeometry(QtCore.QRect(113, 70, 10, 35))
        self.label_2.setMinimumSize(QtCore.QSize(10, 0))
        self.label_2.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_2.setObjectName("label_2")
        self.opt_hex = QtWidgets.QRadioButton(window)
        self.opt_hex.setGeometry(QtCore.QRect(30, 10, 121, 28))
        self.opt_hex.setMinimumSize(QtCore.QSize(0, 28))
        self.opt_hex.setMaximumSize(QtCore.QSize(140, 28))
        self.opt_hex.setChecked(True)
        self.opt_hex.setObjectName("opt_hex")

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "New Grid"))
        self.opt_square.setText(_translate("window", "Square grid"))
        self.btn_create.setText(_translate("window", "Create"))
        self.btn_cancel.setText(_translate("window", "Cancel"))
        self.label_2.setText(_translate("window", "X"))
        self.opt_hex.setText(_translate("window", "Flat Hexagonal grid"))

