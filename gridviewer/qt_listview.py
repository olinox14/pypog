# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_listview.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(380, 477)
        window.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_list = QtWidgets.QTextEdit(window)
        self.txt_list.setMinimumSize(QtCore.QSize(183, 0))
        self.txt_list.setObjectName("txt_list")
        self.verticalLayout.addWidget(self.txt_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cancel = QtWidgets.QPushButton(window)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(window)
        self.btn_ok.setAutoDefault(True)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "List View"))
        self.btn_cancel.setText(_translate("window", "Cancel"))
        self.btn_ok.setText(_translate("window", "Ok"))

