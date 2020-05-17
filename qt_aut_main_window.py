#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = "Ali Akdemir 31.03.2020"
#__author__ = "Nisa Ilhan"

#import modules
from PyQt5 import QtCore, QtGui, QtWidgets
from qwt.scale_widget import QwtScaleWidget
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from os import getcwd
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading
from serial import Serial
import serial
import logging
import datetime
from qwt import QwtInterval,QwtLinearColorMap, QwtLinearScaleEngine

#Some constants may transfer into json
#ubuntu
#SERIAL_COM_ADDRESS="/dev/ttyUSB0"#indicates x_bee connection port

#windows
SERIAL_COM_ADDRESS='COM1'

#UiClass -> Contains GUI elemental structure
#SerialComClass -> Serial Communication class
#WarningPopupClass -> Warning pop-up initialization and usage class
#TimerClass -> This class counts each object passage time and related work.
#MainControlClass -> Main Class for all of them.


class UiClass(object):
    def setupUi(self, Form):
        #initialize UI objects
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(1088, 734)
        self.setWindowIcon(QtGui.QIcon('ghex-icon.png'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        #Color part
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(145, 141, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)

        Form.setPalette(palette)
        Form.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Form.setStyleSheet("#Form{\n"
                            "background:#1DB954;\n"
                            "}\n"
                            "")


        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1081, 731))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.main_gridLayout.setObjectName("main_gridLayout")

        self.log_main_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.log_main_group_box.setTitle("")
        self.log_main_group_box.setObjectName("log_main_group_box")

        self.plaintext_log_main = QtWidgets.QPlainTextEdit(self.log_main_group_box)
        self.plaintext_log_main.setGeometry(QtCore.QRect(0, 0, 271, 361))
        self.plaintext_log_main.setStyleSheet("QPlainTextEdit\n"
                                                "{\n"
                                                "background:#191414;\n"
                                                "border-radius:5px;\n"
                                                "color: #ffffff;\n"
                                                "}")
        #self.plaintext_log_main.setText("")
        self.plaintext_log_main.setReadOnly(True)
        self.plaintext_log_main.setObjectName("plaintext_log_main")

        self.label_data_main = QtWidgets.QLabel(self.log_main_group_box)
        self.label_data_main.setGeometry(QtCore.QRect(190, 0, 121, 17))
        self.label_data_main.setStyleSheet("QLabel{\n"
                                            "background:#1DB954;\n"
                                            "border-radius:10px;\n"
                                            "}")
        self.label_data_main.setObjectName("label_data_main")

        self.main_gridLayout.addWidget(self.log_main_group_box, 1, 0, 1, 1)


        self.log_peripheral_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.log_peripheral_group_box.setStyleSheet("QGroupBox\n"
                                                    "{\n"
                                                    "border-radius:5px;\n"
                                                    "}")
        self.log_peripheral_group_box.setObjectName("log_peripheral_group_box")

        self.plaintext_log_peripheral = QtWidgets.QPlainTextEdit(self.log_peripheral_group_box)
        self.plaintext_log_peripheral.setGeometry(QtCore.QRect(0, 0, 271, 361))
        self.plaintext_log_peripheral.setStyleSheet("QPlainTextEdit\n"
                                                    "{\n"
                                                    "background:#191414;\n"
                                                    "border-radius:5px;\n"
                                                    "color: #ffffff;\n"
                                                    "}")

        #self.plaintext_log_peripheral.setText("")
        #self.plaintext_log_peripheral.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.plaintext_log_peripheral.setReadOnly(True)
        self.plaintext_log_peripheral.setObjectName("plaintext_log_peripheral")

        self.label_data_peripheral = QtWidgets.QLabel(self.log_peripheral_group_box)
        self.label_data_peripheral.setGeometry(QtCore.QRect(190, 0, 121, 17))
        self.label_data_peripheral.setStyleSheet("QLabel{\n"
                                                "background:#1DB954;\n"
                                                "border-radius:10px;\n"
                                                "}")

        self.label_data_peripheral.setObjectName("label_data_peripheral")

        self.main_gridLayout.addWidget(self.log_peripheral_group_box, 0, 0, 1, 1)


        self.control_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.control_group_box.setStyleSheet("QGroupBox\n"
                                                "{\n"
                                                "background:#191414;\n"
                                                "border-radius:5px;\n"
                                                "}\n"
                                                "* {\n"
                                                "  font-family: sans-serif; /* Change your font family */\n"
                                                "}\n"
                                                "")
        self.control_group_box.setTitle("")
        self.control_group_box.setFlat(False)
        self.control_group_box.setObjectName("control_group_box")

        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.control_group_box)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 271, 361))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")

        self.control_grid_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.control_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.control_grid_layout.setObjectName("control_grid_layout")
        self.pushButton_connect = QtWidgets.QPushButton(self.gridLayoutWidget_3)


        font = QtGui.QFont()
        font.setFamily("sans-serif")

        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setStyleSheet("QPushButton\n"
                                                "{\n"
                                                "background:#1DB954;\n"
                                                "border-radius:5px;\n"
                                                "}\n"
                                                "")
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.control_grid_layout.addWidget(self.pushButton_connect, 1, 0, 1, 1)


        self.pushButton_start_sys = QtWidgets.QPushButton(self.gridLayoutWidget_3)


        font = QtGui.QFont()
        font.setFamily("sans-serif")

        self.pushButton_start_sys.setFont(font)
        self.pushButton_start_sys.setStyleSheet("QPushButton\n"
                                                "{\n"
                                                "background:#1DB954;\n"
                                                "border-radius:5px;\n"
                                                "}\n"
                                                "")
        self.pushButton_start_sys.setObjectName("pushButton_start_sys")
        self.control_grid_layout.addWidget(self.pushButton_start_sys, 1, 0, 2, 1)

        self.ums_check_button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        self.ums_check_button.setFont(font)
        self.ums_check_button.setStyleSheet("QPushButton\n"
                                            "{\n"
                                            "background:#1DB954;\n"
                                            "border-radius:5px;\n"
                                            "}\n"
                                            "")
        self.ums_check_button.setObjectName("ums_check_button")
        self.control_grid_layout.addWidget(self.ums_check_button, 5, 0, 1, 1)

        self.gas_sensor_check_button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        self.gas_sensor_check_button.setFont(font)
        self.gas_sensor_check_button.setStyleSheet("QPushButton\n"
                                                    "{\n"
                                                    "background:#1DB954;\n"
                                                    "border-radius:5px;\n"
                                                    "}\n"
                                                    "")
        self.gas_sensor_check_button.setObjectName("gas_sensor_check_button")
        self.control_grid_layout.addWidget(self.gas_sensor_check_button, 6, 0, 1, 1)

        self.label_conveyor = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_conveyor.sizePolicy().hasHeightForWidth())
        self.label_conveyor.setSizePolicy(sizePolicy)
        self.label_conveyor.setStyleSheet("QLabel{\n"
                                            "color:white;\n"
                                            "background:#191414;\n"
                                            "border-radius:10px;\n"
                                            "}")
        self.label_conveyor.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_conveyor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_conveyor.setWordWrap(False)
        self.label_conveyor.setObjectName("label_conveyor")
        self.control_grid_layout.addWidget(self.label_conveyor, 0, 0, 1, 1)


        self.pushButton_stop_sys = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        self.pushButton_stop_sys.setFont(font)
        self.pushButton_stop_sys.setStyleSheet("QPushButton\n"
                                    "{\n"
                                    "background:#1DB954;\n"
                                    "border-radius:5px;\n"
                                    "}\n"
                                    "")
        self.pushButton_stop_sys.setObjectName("stop_sys")
        self.control_grid_layout.addWidget(self.pushButton_stop_sys, 2, 0, 1, 1)

        self.label_sys_check = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sys_check.sizePolicy().hasHeightForWidth())
        self.label_sys_check.setSizePolicy(sizePolicy)
        self.label_sys_check.setStyleSheet("QLabel{\n"
                                            "background:#191414;\n"
                                            "border-radius:10px;\n"
                                            "color:white;\n"
                                            "}")
        self.label_sys_check.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sys_check.setObjectName("label_sys_check")

        self.control_grid_layout.addWidget(self.label_sys_check, 3, 0, 1, 1)
        self.main_gridLayout.addWidget(self.control_group_box, 1, 3, 1, 1)

        self.counter_info_panel_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.counter_info_panel_group_box.setAutoFillBackground(False)
        self.counter_info_panel_group_box.setStyleSheet("QGroupBox\n"
                                                        "{\n"
                                                        "background:#555555;\n"
                                                        "border-radius:5px;\n"
                                                        "}")
        self.counter_info_panel_group_box.setTitle("")
        self.counter_info_panel_group_box.setObjectName("counter_info_panel_group_box")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.counter_info_panel_group_box)

        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(59, 1, 411, 351))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")

        self.counter_info_panel_grid_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.counter_info_panel_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.counter_info_panel_grid_layout.setObjectName("counter_info_panel_grid_layout")


        self.counter_table_w = QtWidgets.QTableWidget(self.gridLayoutWidget_2)
        self.counter_table_w.setMinimumSize(QtCore.QSize(0, 0))
        self.counter_table_w.setAutoFillBackground(False)

        self.counter_table_w.setStyleSheet("\n"
                                            "QTableWidget\n"
                                            "{\n"
                                            "  background: #191414;\n"
                                            "  color: #ffffff;\n"
                                            "  text-align: left;\n"
                                            "  font-weight: bold;\n"
                                            "  border-radius:10px;\n"
                                            "}\n"
                                            "")

        self.counter_table_w.setLineWidth(1)
        self.counter_table_w.setMidLineWidth(0)
        self.counter_table_w.setAlternatingRowColors(False)
        self.counter_table_w.setIconSize(QtCore.QSize(0, 0))
        self.counter_table_w.setShowGrid(True)
        self.counter_table_w.setGridStyle(QtCore.Qt.NoPen)
        self.counter_table_w.setCornerButtonEnabled(True)
        self.counter_table_w.setRowCount(11)
        self.counter_table_w.setColumnCount(1)
        self.counter_table_w.setObjectName("counter_table_w")

        item = QtWidgets.QTableWidgetItem()

        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        item.setFont(font)

        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(29, 185, 84))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.NoItemFlags)

        self.counter_table_w.setItem(10, 0, item)#not in the usage for now maybe just leave it blank

        #customize look
        self.counter_table_w.horizontalHeader().setVisible(False)
        self.counter_table_w.horizontalHeader().setCascadingSectionResizes(False)
        self.counter_table_w.horizontalHeader().setDefaultSectionSize(100)
        self.counter_table_w.horizontalHeader().setMinimumSectionSize(32)
        self.counter_table_w.horizontalHeader().setSortIndicatorShown(False)
        self.counter_table_w.horizontalHeader().setStretchLastSection(True)
        self.counter_table_w.verticalHeader().setVisible(False)
        self.counter_table_w.verticalHeader().setHighlightSections(True)
        self.counter_table_w.verticalHeader().setSortIndicatorShown(False)
        self.counter_table_w.verticalHeader().setStretchLastSection(False)

        self.counter_info_panel_grid_layout.addWidget(self.counter_table_w, 1, 0, 1, 1)

        self.scale_widget_ums1 = QwtScaleWidget(self.counter_info_panel_group_box)

        self.scale_widget_ums1.setGeometry(QtCore.QRect(0, 10, 61, 331))
        self.scale_widget_ums1.setStyleSheet("QWidget{\n"
                                            "color:#1DB954;\n"
                                            "}")
        self.scale_widget_ums1.setInputMethodHints(QtCore.Qt.ImhNone)
        self.scale_widget_ums1.setObjectName("scale_widget_ums1")

        self.label_sensor_ums_1_scalewidget = QtWidgets.QLabel(self.counter_info_panel_group_box)
        self.label_sensor_ums_1_scalewidget.setGeometry(QtCore.QRect(0, 340, 67, 17))
        self.label_sensor_ums_1_scalewidget.setObjectName("label_sensor_ums_1_scalewidget")

        self.scale_widget_ums2 = QwtScaleWidget(self.counter_info_panel_group_box)
        self.scale_widget_ums2.setGeometry(QtCore.QRect(470, 10, 60, 331))
        self.scale_widget_ums2.setStyleSheet("QWidget{\n"
                                            "color:#1DB954;\n"
                                            "}")

        self.scale_widget_ums2.setObjectName("scale_widget_ums2")
        self.label_sensor_ums_2_scalewidget = QtWidgets.QLabel(self.counter_info_panel_group_box)
        self.label_sensor_ums_2_scalewidget.setGeometry(QtCore.QRect(470, 340, 67, 17))
        self.label_sensor_ums_2_scalewidget.setObjectName("label_sensor_ums_2_scalewidget")

        self.main_gridLayout.addWidget(self.counter_info_panel_group_box, 1, 1, 1, 2)


        self.anim_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.anim_group_box.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.anim_group_box.sizePolicy().hasHeightForWidth())
        self.anim_group_box.setSizePolicy(sizePolicy)
        self.anim_group_box.setStyleSheet("QGroupBox\n"
                                            "{\n"
                                            "background:#899E97;\n"
                                            "border-radius:5px;\n"
                                            "}")
        self.anim_group_box.setObjectName("anim_group_box")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.anim_group_box)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 811, 361))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.anim_group_box_vlayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.anim_group_box_vlayout.setContentsMargins(0, 0, 0, 0)
        self.anim_group_box_vlayout.setObjectName("anim_group_box_vlayout")


        #TRY ADDING JS-HMTML-CSS PART HERE
        self.html_address=getcwd()
        #self.layout_anim = QtWidgets.QVBoxLayout()
        settings = QtWebEngineWidgets.QWebEngineSettings.defaultSettings() 
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        self.plot = QtWebEngineWidgets.QWebEngineView()
        self.plot.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.plot.load(QtCore.QUrl.fromLocalFile(QtCore.QDir.current().absoluteFilePath(self.html_address+'/html/block_display.html')))

        
        self.anim_group_box_vlayout.addWidget(self.plot)


        #!! IF YOU WANNA ADD ANIMATION USE BELOW LINE
        self.anim_group_box.setLayout(self.anim_group_box_vlayout)
        #still got error
        #end of TRY


        self.main_gridLayout.addWidget(self.anim_group_box, 0, 1, 1, 3)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        #translator
        _translate = QtCore.QCoreApplication.translate

        Form.setWindowTitle(_translate("Form", "Automation"))
        self.label_data_main.setText(_translate("Form", "Software LOG"))
        self.log_peripheral_group_box.setTitle(_translate("Form", "GroupBox"))
        self.label_data_peripheral.setText(_translate("Form", "System LOG"))
        self.pushButton_start_sys.setText(_translate("Form", "Start"))
        self.pushButton_connect.setText(_translate("Form","Connect"))
        self.ums_check_button.setText(_translate("Form", "UMSs-HC-SR04"))
        self.gas_sensor_check_button.setText(_translate("Form", "Gas Sensor-MQ-2"))
        self.label_conveyor.setText(_translate("Form", "Conveyor"))
        self.pushButton_stop_sys.setText(_translate("Form", "Stop"))
        self.label_sys_check.setText(_translate("Form", "Sensor Health Check"))

        self.counter_table_w.setSortingEnabled(False)

        __sortingEnabled = self.counter_table_w.isSortingEnabled()

        self.counter_table_w.setSortingEnabled(False)

        item = self.counter_table_w.item(0, 0)
        item.setText(_translate("Form", "Gas Cylinder Count"))

        item = self.counter_table_w.item(1, 0)
        item.setText(_translate("Form", "NULL"))

        item = self.counter_table_w.item(2, 0)
        item.setText(_translate("Form", "SONAR Count 1 \t SONAR Count 2"))

        item = self.counter_table_w.item(3, 0)
        item.setText(_translate("Form", "NULL \t\t NULL"))

        item = self.counter_table_w.item(4, 0)
        item.setText(_translate("Form", "Sealing Time"))

        item = self.counter_table_w.item(5, 0)
        item.setText(_translate("Form", "NULL"))

        item = self.counter_table_w.item(6, 0)
        item.setText(_translate("Form", "Exit Time"))

        item = self.counter_table_w.item(7, 0)
        item.setText(_translate("Form", "NULL"))

        item = self.counter_table_w.item(8, 0)
        item.setText(_translate("Form", "System Time"))

        item = self.counter_table_w.item(9, 0)
        item.setText(_translate("Form", "NULL"))

        """item = self.counter_table_w.item(10, 0)
                                item.setText(_translate("Form", "NULL"))"""

        self.counter_table_w.setSortingEnabled(__sortingEnabled)

        self.label_sensor_ums_1_scalewidget.setText(_translate("Form", "Sonar1"))
        self.label_sensor_ums_2_scalewidget.setText(_translate("Form", "Sonar2"))
        #self.animation_label_title.setText(_translate("Form", "System Animation"))




class SerialComClass(QtCore.QThread):
    serial_msg_reciever= QtCore.pyqtSignal(str)
    serial_cmd_reciever= QtCore.pyqtSignal(str)
    def __init__(self,UIelements):
        super(SerialComClass,self).__init__()
        #inheritence from logger class object from main class
        self.ser_com_control_object= UIelements
        self.ser_com_logger_object= UIelements.logger_object
        self.ser_com_logger_object.log_info("Initiliazing Serial Communication Class..",1)
        self.ser_com_logger_object.log_info("Done",1)
        self.port_address= 'COM1'#SERIAL_COM_ADDRESS#indicates x_bee connection port
        time.sleep(0.5)
        self.ser_com_line= Serial('COM1', baudrate=9600)
        #signal for updating UI element
        self.serial_msg_reciever.connect(self.handle_msg_update)
        self.serial_cmd_reciever.connect(self.handle_msg_cmds)
        #flag for thread
        self.flag_com_started=False
        #reader thread
        self.thread_reader= threading.Thread(target=self.serial_read)
        self.thread_reader.daemon= True
        #writer thread
        #self.thread_writer= threading.Thread(target=self.serial_write)
        #self.thread_writer.daemon= True
        self.commands_dict={"iCmds":{"gas_danger":"1","distance_1":"x","distance_2":"y"},
                            "oCmds":{"start_conveyor":"1","stop_conveyor":"0"}}
        #locks
        #self.thread_var_lock= threading.Lock()
        time.sleep(0.2)
        self.thread_reader.start()
        """
        try:
            self.ser_com_line= Serial(port= self.port_address, baudrate=9600)#baudrate could be higher, use x bee program to increase
        except:
            print("Could not reach the port.",self.port_address)
            print("Some application or terminal may be blocking it, check for scripts.")
            self.ser_com_logger_object.log_error("Could not reach the port {}.".format(self.port_address),1)
            self.ser_com_logger_object.log_critical("Some application or terminal may be blocking it, check for scripts.",1)"""
        
    def start_com(self):
        try:
            #baudrate could be higher, use x bee program to increase
            time.sleep(1)
            print("Initiliazing thread[s]..")
            if not self.flag_com_started:
                #self.ser_com_logger_object.log_info("Initiliazing thread[s]..")
                self.flag_com_started=True
                print("done")
            #self.thread_writer.start()# ---> if needed, functionality decide s the usage.

        except serial.SerialException:  
            print("[ERROR-Serial] Serial Exception Occured..\n[ERROR] Port is blocked.")
            
        except serial.SerialTimeoutException:
            print("[ERROR-Serial] Writing Timeout..")

        except:
            print("Could not reach the port.",self.port_address)
            print("Some application or terminal may be blocking it, check for scripts.")
            self.ser_com_logger_object.log_error("Could not reach the port {}.".format(self.port_address),1)
            self.ser_com_logger_object.log_critical("Some application or terminal may be blocking it, check for scripts.",1)
        

    @QtCore.pyqtSlot(str)
    def handle_msg_update(self,msg):
        self.ser_com_logger_object.log_info(msg,0)

    @QtCore.pyqtSlot(str)
    def handle_msg_cmds(self,msg):
        self.ser_com_control_object.handle_input_cmds(msg)

    def serial_read(self):
        while True:
            if getattr(self, "flag_com_started", True):#condition may added Afterwards
                #self.thread_var_lock.acquire()
                _msg = self.ser_com_line.readline()#.decode()#read and decode the incoming msg
                #self.thread_var_lock.release()
                msg=_msg.decode('utf-8', errors='replace')
                self.serial_msg_reciever.emit(str(msg))
                self.serial_cmd_reciever.emit(str(msg))
                #self.ser_com_logger_object.log_info(,0)

                sys.stdout.flush()
                #
                # Show data or pass it something needed.
                #
            time.sleep(0.1)
            #else:
            #    print("Error, could not reach port to read")
            #    self.ser_com_logger_object.log_error("Error, could not reach port to read",1)

    def serial_write(self, send_msg):
        #for half dublex usage
        #self.thread_var_lock.acquire()
        if self.ser_com_line:
            self.ser_com_line.write(send_msg.encode())
            time.sleep(0.1)
        else:
            print("Error, could not reach the port for writing")
            self.ser_com_logger_object.log_error("Error, could not reach the port for writing",1)
        #self.thread_var_lock.release()

    def show_data(self):
        pass




class LoggerClass:
    def __init__(self, logtextbox_peripheral, logtextbox_main):
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        # Create a logger instance
        self.logger = logging.getLogger(__name__)

        self.logtextbox_peripheral= logtextbox_peripheral
        self.logtextbox_main= logtextbox_main

        self.text_level_list= ["[ERR] ","[WARN] ","[CRTC] ","[DBG] ","[INFO] "]
        self.log_info("Initiliazing Logger Class..",1)
        self.log_info("Done",1)

    #Stream Handlers
    def debug_logger(self):
        dbg_handler= logging.FileHandler('LOG/AutomationGUI_DEBUG.log')
        dbg_handler.setLevel(logging.DEBUG)
        dbg_format= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.addHandler(dbg_format)

    def err_logger(self):
        err_handler= logging.FileHandler('LOG/AutomationGUI_ERR.log')
        crt_handler= logging.FileHandler('LOG/AutomationGUI_ERR.log')

        err_format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        crt_format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        err_handler.setLevel(logging.ERROR)
        crt_handler.setLevel(logging.CRITICAL)

        err_handler.setFormatter(err_format)
        crt_handler.setFormatter(crt_format)

        logger.addHandler(err_handler)
        logger.addHandler(crt_handler)

    def time_tag(self):
        current_time= datetime.datetime.now()
        timetag= "["+str(current_time.hour) + ":" + str(current_time.minute) +":"+str(current_time.second) +"]"
        return timetag

    def log_to_uı(self,msg,whichone):
        msg=self.time_tag()+" "+msg
        if whichone==0:
            self.logtextbox_peripheral.appendPlainText(msg)
        elif whichone==1:
            self.logtextbox_main.appendPlainText(msg)

    #Terminal logging purposes
    def log_critical(self,log,whichone):
        logging.critical(log)
        log=self.text_level_list[2]+log
        self.log_to_uı(log,whichone)

    def log_warning(self,log,whichone):
        logging.warning(log)
        log=self.text_level_list[1]+log
        self.log_to_uı(log,whichone)

    def log_info(self,log,whichone):
        logging.info(log)
        #input commands coming from peripheral controller unit
        if whichone==0:
            self.update_ui_cmds(log)
        #other ones
        else:
            log=self.text_level_list[4]+log
            self.log_to_uı(log,whichone)

    def log_debug(self,log,whichone):
        logging.debug(log)
        log=self.text_level_list[3]+log
        self.log_to_uı(log,whichone)

    def log_error(self, log,whichone):
        logging.error(log)
        log=self.text_level_list[0]+log
        self.log_to_uı(log,whichone)

    def log_exception(self,log,whichone):
        logging.exception(log)
        self.log_to_uı(log,whichone)

    def update_ui_cmds(self,msg):
        msg_l=msg.split(",")
        #Msg list, [0]->Conveyor State
        #          [1]->Gas Sensor State
        #          [2]->Sonar 1 Measurement
        #          [3]->Sonar 2 Measurement
        msg_conveyor_on="[STATUS] Conveyor working."
        msg_conveyor_off="[STATUS] Conveyor not working."
        msg_gas_on="[CRTC] GAS ALERT!"
        msg_gas_off="[INFO] Gas levels normal."
        msg_sonar_1_on="[INFO] Sonar 1 Measurement: "
        msg_sonar_1_off="[ERROR] Sonar 1 Off."
        msg_sonar_2_on="[INFO] Sonar 2 Measurement: "
        msg_sonar2_off="[ERROR] Sonar 2 Off."
        msg_sonars_on_wait="[INFO] Sonars not initiated."
        #log to user interface peripheral controller log part
        #if conveyor is on
        if msg_l[0]=="1":
            log=msg_conveyor_on
            self.log_to_uı(log,0)
        #else msg is 0 means conveyor is off 
        else:
            log=msg_conveyor_off
            self.log_to_uı(log,0)

        #if gas particle measurements is up to danger level
        if msg_l[1]=="1":
            log=msg_gas_on
            self.log_to_uı(log,0)
        #else gas levels ok
        else:
            log=msg_gas_off
            self.log_to_uı(log,0)

        #check sonar sensors
        #if both of them return -1 that means system is not started they are in wait mode
        if (msg_l[2]=="-1" and msg_l[3]=="-1"):
            log=msg_sonars_on_wait
            self.log_to_uı(log,0)
        #if one of them returning wait mode and the other returns  another value, wait mode sonar is broken
        elif (msg_l[2]=="-1" and msg_l[3] !="-1"):
            log=msg_sonar_1_off
            self.log_to_uı(log,0)
        elif (msg_l[2]!="-1" and msg_l[3]=="-1"):
            log=msg_sonar2_off
            self.log_to_uı(log,0)
        #otherwise, system is working and sensors are healthy and returning range values.
        else:
            self.log_to_uı(msg_sonar_1_on+str(msg_l[2]),0)
            self.log_to_uı(msg_sonar_2_on+str(msg_l[3]),0)

class WarningPopupClass():
    def __init__(self):
        self.msg =QtWidgets.QMessageBox()
        self.msg.setWindowIcon(QtGui.QIcon('ghex-icon.png'))
        self.msg.setStyleSheet("QMessageBox\n"
                                        "{\n"
                                        "background:#191414;\n"
                                        "border-radius:5px;\n"
                                        "}\n"
                                        "QLabel{\n"
                                        "color:#1DB954;}\n"
                                        "QPushButton{\n"
                                        "background:#191414;\n"
                                        "color:#1DB954;}\n")
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Cancel|QtWidgets.QMessageBox.Retry|QtWidgets.QMessageBox.Ignore)
        #self.msg.setDefaultButton(QtWidgets.QMessageBox.Retry)

        #predefined text for now
        self.msg.setWindowTitle("Uretim Bandı Durum Bilgilendirme Penceresi")
        
        #self.msg.setDetailedText("[WARN]US Sensors Detected Anormal Amount of Objects on Conveyor")

        self.msg.buttonClicked.connect(self.debug_buttons)

    def _setInformativeText(self, text):
        self.msg.setInformativeText(text)

    def _setWindowTitle(self, text):
        self.msg.setWindowTitle(text)

    def _setDetailedText(self, text):
        self.msg.setDetailedText(text)

    def _setText(self, text):
        self.msg.setText(text)

    def show_popup(self,sit):
        if sit==0:
            self.msg.setText("Uretim bandında fazla urun tespit edilmistir!")
            self.msg.setInformativeText("Uretim bandi calismaya devam etsin mi?")
        elif sit==1:
            self.msg.setText("GAZ KACAGI ALGILANDI!")
            self.msg.setInformativeText("ALARM VERILDI")
        x= self.msg.exec_()

    def debug_buttons(self, i):
    	print(i.text()+" button clicked")






class TimerClass(QtCore.QThread):
    msg_reciever= QtCore.pyqtSignal(str)
    msg_cTime_error= QtCore.pyqtSignal(str)
    def __init__(self,UIelements):
        super(TimerClass,self).__init__()
        self.timer_logger_object= UIelements.logger_object
        self.exit_time_callback=UIelements.exit_time_callback
        self.timer_logger_object.log_info("Initiliazing Timer Class..",1)
        #variables
        self.var_cylinder_count=0
        self.var_time_elapsed=0
        #flags
        self.flag_start_counting=False
        self.flag_isObjectDetected=False
        self.flag_isThreadStarted= False

        self.UIelement_count_table=UIelements.counter_table_w

        #Thread __init__
        self.thread_updater= threading.Thread(target=self.update_timer_label)
        self.thread_counter= threading.Thread(target=self.counter)
        self.thread_updater.daemon=True
        self.thread_counter.daemon=True
        self.msg_reciever.connect(self.handle_time_update)
        self.msg_cTime_error.connect(self.handle_cTime_error_update)
        self.timer_logger_object.log_info("Done",1)

        timer = QTimer(self)
        timer.timeout.connect(self.show_system_time)
        timer.start(1000)
        self.show_system_time()

    def show_system_time(self):
        time = QTime.currentTime()
        msg = time.toString('hh:mm:ss')
        self.UIelement_count_table.item(9, 0).setText(msg)

    @QtCore.pyqtSlot(str)
    def handle_time_update(self,msg):
        self.UIelement_count_table.item(7, 0).setText(msg)
        if int(msg)==15:
            self.UIelement_count_table.item(5,0).setText(str(1))
        elif int(msg)==14:
            self.UIelement_count_table.item(5,0).setText(str(0))

    @QtCore.pyqtSlot(str)
    def handle_cTime_error_update(self,msg):
        self.exit_time_callback(msg)

    def getTime(self):
        time = QTime.currentTime().toString()
        return time

    def updateTime(self):
        time = QTime.currentTime().toString()
        print("Seconds: " + time[-2:])

        #self.time_label.setText(time)
        return time

    def start_counting(self):
        self.var_cylinder_count+=1
        #self.seal_time_label.setText(str(2))
        #self.cylinder_count_label.setText(str(self.cylinder_count))
        try:
            self.UIelement_count_table.item(5,0).setText(str(2))#UIelements.counter_table_w.item(5, 0).setText(str(2))
            #self.UIelement_count_table.item(1, 0).setText(str(self.var_cylinder_count))#UIelements.counter_table_w.item(1, 0).setText(str(self.var_cylinder_count))
        except:
            print("Error at TimerClas Inheritence")
            self.timer_logger_object.log_error("Error at TimerClas Inheritence",1)
        
        self.flag_start_counting=True
        #self.thread_updater.start()
        
        if not self.flag_isThreadStarted:
            self.thread_counter.start()
            self.flag_isThreadStarted=True
        


    def stop_counting(self):
        self.flag_start_counting=False

    def counter(self):
        seconds=30
        while True:
            if self.flag_start_counting:
                start = time.time()
                time.clock()
                elapsed = 0
                while (elapsed < seconds) and self.flag_start_counting:
                    elapsed = time.time() - start
                    #print("loop cycle time: %f, seconds count: %02d"% (time.clock() , elapsed))
                    #self.var_time_elapsed=elapsed
                    print("it",int(elapsed))
                    #self.UIelement_count_table.item(3, 0).setText(str(elapsed))#("%02d"%elapsed)
                    self.msg_reciever.emit(str(30-int(elapsed)))
                    #send error msg for checking second pass of object
                    if int(elapsed)>28:
                        self.msg_cTime_error.emit("1")
                    #self.time_label.setText(str(elapsed))
                    time.sleep(1)

                if elapsed>29.5:
                    self.flag_start_counting=False

    def update_timer_label(self):
        #print("Elapsed time: ,",self.var_time_elapsed)
        while True:
            if self.flag_start_counting:
                #self.time_label.setText("%02d"%self.var_time_elapsed)
                try:
                    self.UIelement_count_table.item(3, 0).setText(str(int(self.var_time_elapsed)))#("%02d"%self.var_time_elapsed)
                except:
                    print("Error at TimerClass Inheritence")
                    self.timer_logger_object.log_error("Error at TimerClass Inheritence",1)


    def main_watcher(self):
        while True:
            if self.flag_isObjectDetected:
                self.start_counting()
            else:
                self.stop_counting
            time.sleep(0.1)




class MainControlClass(QtWidgets.QWidget, UiClass):
    def __init__(self, parent=None):
        super(MainControlClass, self).__init__(parent)
        self.setupUi(self)
        #loggerclass tryout
        self.logger_object=LoggerClass(self.plaintext_log_peripheral, self.plaintext_log_main)
        #pop-up class
        self.popup_object= WarningPopupClass()
        self.timer_object=TimerClass(self)
        self.communicator_object= SerialComClass(self)
        self.logger_object.log_critical("Initiliazing Main Control Class..",1)
        self.logger_object.log_critical("Done",1)

        #Serial listener thread
        #self.thread_serial_listener= threading.Thread(target=self.sensor_serial_listener)
        #self.thread_serial_listener.daemon=True
        
        #self.popup=WarningPopupClass()
        #self.pushButton.clicked.connect(self.popup.show_popup)#(self.pushButtonClicked)
        #self.lineEdit.setText("click me")
        self.pushButton_start_sys.clicked.connect(self.signal_start_conveyor)
        self.pushButton_stop_sys.clicked.connect(self.signal_stop_conveyor)
        self.ums_check_button.clicked.connect(self.signal_sys_healthcheck_umss)
        self.gas_sensor_check_button.clicked.connect(self.signal_sys_healthcheck_mq2)
        self.pushButton_connect.clicked.connect(self.signal_sys_connect_peripheral)
        
        #self.plaintext_log_peripheral.appendPlainText("")
        #self.plaintext_log_main.appendPlainText("")
        self.fill_scalewidgets()

        self.sonar_1_count=0
        self.sonar_2_count=0
        self.total_sonar_count=0
        #flag for exceeding exit time interval
        self.flag_exceed_exit_time=False
        self.flag_total_update_sonar_1=False
        self.flag_total_update_sonar_2=False


        self.counter_table_w.item(3, 0).setText(str(self.sonar_1_count)+" \t\t "+str(self.sonar_2_count))#("0 \t\t 0")
        self.counter_table_w.item(1, 0).setText(str(self.total_sonar_count))

        self.logger_object.log_info("Checking Ultrasonic Sensors.",1)
        self.logger_object.log_info("Checking Gas Sensor.",1)
        self.logger_object.log_info("Done.",1)
        
    def signal_sys_connect_peripheral(self):
        self.communicator_object.start_com()

    def signal_start_conveyor(self):
        print("Start conveyor.")
        self.logger_object.log_info("Start conveyor.",1)
        #Test Pop-up
        #msg for starting conveyor code on arduino needs 'T'
        msg_start= 'T'
        self.communicator_object.serial_write(msg_start)
        
        #self.popup_object.show_popup()

    def signal_stop_conveyor(self):
        print("Stop conveyor.")
        self.logger_object.log_info("Stop conveyor.",1)
        msg_start= 'P'
        self.communicator_object.serial_write(msg_start)


    def signal_sys_healthcheck_umss(self):
        print("Checking Ultrasonic Sensors.")
        #self.logger_object.log_info("Checking Ultrasonic Sensors.",1)
        self.popup_object.show_popup(0)

    def signal_sys_healthcheck_mq2(self):
        print("Checking Gas Sensor.")
        #self.logger_object.log_info("Checking Gas Sensor.",1)
        self.popup_object.show_popup(1)

    def fill_scalewidgets(self):
        #self.scale_engine = QwtLinearScaleEngine()
        self.scale_map = QwtLinearColorMap(QtGui.QColor(29, 185, 84), QtGui.QColor(28, 61, 89))
        
        self.scale_widget_ums1.setColorMap(QwtInterval(99, 100), self.scale_map)
        self.scale_widget_ums1.setColorBarEnabled(True)
        self.scale_widget_ums1.setColorBarWidth(5)
        self.scale_widget_ums1.setBorderDist(10,10)

        self.scale_widget_ums2.setColorMap(QwtInterval(99, 100), self.scale_map)
        self.scale_widget_ums2.setColorBarEnabled(True)
        self.scale_widget_ums2.setColorBarWidth(5)
        self.scale_widget_ums2.setBorderDist(10,10)

        #self.scale_widget_ums1.colorMap().color(self.scale_widget_ums1.colorBarInterval(), 51.2)
        #self.scale_widget_ums1.setScaleDiv(self.scale_engine.transformation(),a)

    def set_scalewidgets(self,i1,i2):
        self.scale_widget_ums1.setColorMap(QwtInterval(i1, i1+1), self.scale_map)
        self.scale_widget_ums2.setColorMap(QwtInterval(i2, i2+1), self.scale_map)

    def handle_input_cmds(self,msg):
        msg_l=msg.split(",")
        #Msg list, [0]->Conveyor State
        #          [1]->Gas Sensor State
        #          [2]->Sonar 1 Measurement
        #          [3]->Sonar 2 Measurement

        #if gas particle measurements is up to danger level
        if msg_l[1]=="1":
            self.popup_object.show_popup(1)
        #else gas levels ok
        else:
            pass

        #check sonar sensors
        #if both of them return -1 that means system is not started they are in wait mode
        if (msg_l[2]=="-1" and msg_l[3]=="-1"):
            pass
        #if one of them returning wait mode and the other returns  another value, wait mode sonar is broken
        elif (msg_l[2]=="-1" and msg_l[3] !="-1"):
            pass
        elif (msg_l[2]!="-1" and msg_l[3]=="-1"):
            pass
        #otherwise, system is working and sensors are healthy and returning range values.
        else:
            self.sensor_counter(int(msg_l[2]),int(msg_l[3]))
            self.set_scalewidgets(int(msg_l[2]),int(msg_l[3]))

    def sensor_counter(self,sonar1_output, sonar2_output):
        #we will accept that under 10 meter is count of an object
        #higher than 10 meter will be treated as empty conveyor looking from sensors perspective
        #if output of any sonar <10 than we counted an object
    

        if sonar1_output<10:
            self.timer_object.start_counting()
            self.sonar_1_count+=1
            self.counter_table_w.item(3, 0).setText(str(self.sonar_1_count)+" \t\t "+str(self.sonar_2_count))
            self.flag_total_update_sonar_1=True
        else:
            pass

        if sonar2_output<10:
            self.sonar_2_count+=1
            self.counter_table_w.item(3, 0).setText(str(self.sonar_1_count)+" \t\t "+str(self.sonar_2_count))
            self.flag_total_update_sonar_2=True
        else:
            pass

        #time_interval_least=self.counter_table_w.item(7, 0).text()
        #print("interval",time_interval_least)
        if (self.flag_total_update_sonar_1 and self.flag_total_update_sonar_2):
            self.total_sonar_count+=1
            self.counter_table_w.item(1, 0).setText(str(self.total_sonar_count))
            self.flag_total_update_sonar_1=False
            self.flag_total_update_sonar_2=False
            self.timer_object.stop_counting()

        elif (self.flag_total_update_sonar_1) and not (self.flag_total_update_sonar_2) and self.flag_exceed_exit_time:
            self.popup_object.show_popup(0)
            self.flag_exceed_exit_time=False

    def exit_time_callback(self, msg):
        #connected to slot in timerclass send signal when exit time exceedings detected.
        if msg=="1":
            self.flag_exceed_exit_time=True
            #self.popup_object.show_popup(0)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    #ui = UiClass()
    #ui.setupUi(Form)
    #Form.show()
    a=MainControlClass()
    a.show()#showMaximized
    sys.exit(app.exec_())
