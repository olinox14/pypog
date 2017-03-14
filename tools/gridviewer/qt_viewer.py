# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(909, 658)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(8)
        window.setFont(font)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")
        self.verticalLayout.addWidget(self.lbl_title)
        self.frame_tools = QtWidgets.QFrame(self.centralwidget)
        self.frame_tools.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_tools.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tools.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tools.setObjectName("frame_tools")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_tools)
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_new_grid = QtWidgets.QPushButton(self.frame_tools)
        self.btn_new_grid.setMinimumSize(QtCore.QSize(80, 0))
        self.btn_new_grid.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btn_new_grid.setObjectName("btn_new_grid")
        self.horizontalLayout_2.addWidget(self.btn_new_grid)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cb_jobs = QtWidgets.QComboBox(self.frame_tools)
        self.cb_jobs.setMinimumSize(QtCore.QSize(150, 0))
        self.cb_jobs.setObjectName("cb_jobs")
        self.horizontalLayout_2.addWidget(self.cb_jobs)
        self.btn_run_job = QtWidgets.QToolButton(self.frame_tools)
        self.btn_run_job.setMinimumSize(QtCore.QSize(0, 20))
        self.btn_run_job.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btn_run_job.setObjectName("btn_run_job")
        self.horizontalLayout_2.addWidget(self.btn_run_job)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_list_view = QtWidgets.QPushButton(self.frame_tools)
        self.btn_list_view.setObjectName("btn_list_view")
        self.horizontalLayout_2.addWidget(self.btn_list_view)
        self.verticalLayout.addWidget(self.frame_tools)
        self.stack_job = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack_job.setMinimumSize(QtCore.QSize(0, 30))
        self.stack_job.setMaximumSize(QtCore.QSize(16777215, 30))
        self.stack_job.setObjectName("stack_job")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stack_job.addWidget(self.page_2)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_job_previous = QtWidgets.QToolButton(self.page)
        self.btn_job_previous.setObjectName("btn_job_previous")
        self.horizontalLayout_3.addWidget(self.btn_job_previous)
        self.btn_job_next = QtWidgets.QToolButton(self.page)
        self.btn_job_next.setObjectName("btn_job_next")
        self.horizontalLayout_3.addWidget(self.btn_job_next)
        self.lbl_job_number = QtWidgets.QLabel(self.page)
        self.lbl_job_number.setObjectName("lbl_job_number")
        self.horizontalLayout_3.addWidget(self.lbl_job_number)
        self.txt_job_run = QtWidgets.QLineEdit(self.page)
        self.txt_job_run.setReadOnly(True)
        self.txt_job_run.setObjectName("txt_job_run")
        self.horizontalLayout_3.addWidget(self.txt_job_run)
        self.lbl_job_exectime = QtWidgets.QLabel(self.page)
        self.lbl_job_exectime.setObjectName("lbl_job_exectime")
        self.horizontalLayout_3.addWidget(self.lbl_job_exectime)
        self.btn_job_validate = QtWidgets.QPushButton(self.page)
        self.btn_job_validate.setObjectName("btn_job_validate")
        self.horizontalLayout_3.addWidget(self.btn_job_validate)
        self.stack_job.addWidget(self.page)
        self.verticalLayout.addWidget(self.stack_job)
        self.view = QtWidgets.QGraphicsView(self.centralwidget)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.view.setFont(font)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.btn_zoom_plus = QtWidgets.QToolButton(self.centralwidget)
        self.btn_zoom_plus.setObjectName("btn_zoom_plus")
        self.horizontalLayout_4.addWidget(self.btn_zoom_plus)
        self.btn_zoom_view = QtWidgets.QToolButton(self.centralwidget)
        self.btn_zoom_view.setObjectName("btn_zoom_view")
        self.horizontalLayout_4.addWidget(self.btn_zoom_view)
        self.btn_zoom_minus = QtWidgets.QToolButton(self.centralwidget)
        self.btn_zoom_minus.setObjectName("btn_zoom_minus")
        self.horizontalLayout_4.addWidget(self.btn_zoom_minus)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.chk_displayCoords = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_displayCoords.setChecked(True)
        self.chk_displayCoords.setObjectName("chk_displayCoords")
        self.horizontalLayout_4.addWidget(self.chk_displayCoords)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 2)
        window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionQuitter = QtWidgets.QAction(window)
        self.actionQuitter.setObjectName("actionQuitter")

        self.retranslateUi(window)
        self.stack_job.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)
        window.setTabOrder(self.view, self.btn_new_grid)
        window.setTabOrder(self.btn_new_grid, self.cb_jobs)
        window.setTabOrder(self.cb_jobs, self.btn_list_view)
        window.setTabOrder(self.btn_list_view, self.btn_zoom_plus)
        window.setTabOrder(self.btn_zoom_plus, self.btn_zoom_minus)
        window.setTabOrder(self.btn_zoom_minus, self.chk_displayCoords)
        window.setTabOrder(self.chk_displayCoords, self.lbl_title)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "GridViewer"))
        self.lbl_title.setText(_translate("window", "Grid Viewer"))
        self.btn_new_grid.setText(_translate("window", "New Grid"))
        self.btn_run_job.setText(_translate("window", "Run job"))
        self.btn_list_view.setText(_translate("window", "List View"))
        self.btn_job_previous.setText(_translate("window", "<"))
        self.btn_job_next.setText(_translate("window", ">"))
        self.lbl_job_number.setText(_translate("window", "Test 1 / 1"))
        self.lbl_job_exectime.setText(_translate("window", "Exec. in 1000.000 ms. (saved: 10000.000 ms.)"))
        self.btn_job_validate.setText(_translate("window", "Validate"))
        self.label_3.setText(_translate("window", "Zoom"))
        self.btn_zoom_plus.setText(_translate("window", "+"))
        self.btn_zoom_view.setText(_translate("window", "X"))
        self.btn_zoom_minus.setText(_translate("window", "-"))
        self.chk_displayCoords.setText(_translate("window", "Display coordinates"))
        self.actionQuitter.setText(_translate("window", "Quitter"))

