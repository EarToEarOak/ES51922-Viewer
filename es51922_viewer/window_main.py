#!/usr/bin/env python
#
#
# ES51022 Viewer
#
# https://eartoearoak/software/es51922-viewer
#
# Copyright 2017 Al Brown
#
# Monitor ES51022 based multimeters
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import time

from PySide.QtCore import Slot
from PySide.QtGui import QMainWindow, QComboBox, QWidget, QSizePolicy, \
    QMessageBox, QIcon
from es51922_viewer.comm import Comm
from es51922_viewer.meter import Meter
from es51922_viewer.ui import loadUi
from es51922_viewer.utils import getResource
from es51922_viewer.widget_lcd import WidgetLcd
from es51922_viewer.widget_led import WidgetLed
from es51922_viewer.widget_plot import WidgetPlot

from es51922_viewer.settings import Settings


class WindowMain(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self._comm = Comm()
        self._isRecording = False
        self._settings = Settings()

        self.customWidgets = {'WidgetLcd': WidgetLcd,
                              'WidgetPlot': WidgetPlot}
        loadUi(self, 'mainwindow.ui')

        self.__setupToolbar()
        self.__setupStatusbar()

        self._settings.setComboPort(self._comboSerial)

        self.adjustSize()

    def __setupToolbar(self):
        widgetSpacer = QWidget()
        widgetSpacer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                               QSizePolicy.Preferred))

        self._comboSerial = QComboBox()
        self._comboSerial.addItems(self._comm.getPorts())
        self._comboSerial.setToolTip('Serial port')

        self.toolbar.addWidget(widgetSpacer)
        self.toolbar.addWidget(self._comboSerial)

        icon = QIcon(getResource('record.png'))
        self.actionRecord.setIcon(icon)
        icon = QIcon(getResource('clear.png'))
        self.actionClear.setIcon(icon)

    def __setupStatusbar(self):
        self._ledData = WidgetLed(self, '#2a426b')
        self._ledData.setToolTip('Data received')
        self._ledBatt = WidgetLed(self, '#ea5b00')
        self._ledBatt.setToolTip('Low battery')
        self.statusbar.addPermanentWidget(self._ledData)
        self.statusbar.addPermanentWidget(self._ledBatt)
        self.statusbar.showMessage('Ready')

    @Slot()
    def on_actionRecord_triggered(self):
        if self.actionRecord.isChecked():
            self.__start()
        else:
            self.__stop()

    @Slot()
    def on_actionClear_triggered(self):
        self._widgetLcd.clear()
        self._widgetPlot.clearPlot()
        self.actionClear.setDisabled(True)

    def __onData(self, meter):
        self.statusbar.showMessage('Recording')
        if self._isRecording:
            self._widgetLcd.set(meter)
            self._widgetPlot.set(meter)
            self.actionClear.setEnabled(True)
            self._ledData.flash()
            if meter.batt:
                self._ledBatt.light(True)

    def __onWarning(self, warning):
        self._widgetLcd.clear()
        self.statusbar.showMessage(warning)

    def __onError(self, error):
        self.__stop()
        QMessageBox.critical(self, 'Error', error, QMessageBox.Ok)

    def closeEvent(self, _event):
        self.__stop()
        self._settings.getComboPort(self._comboSerial)

    def __start(self):
        self._isRecording = True
        self._comboSerial.setDisabled(True)
        port = self._comboSerial.currentText()
        self._comm.start(port, self.__onData, self.__onWarning, self.__onError)
        self.statusbar.showMessage('Started')
        self._widgetPlot.enableAutoRange()

    def __stop(self):
        self.actionRecord.setChecked(False)
        self._comboSerial.setEnabled(True)
        self._comm.stop()
        self.statusbar.showMessage('Stopped')
        self._widgetLcd.clear()
        self._ledBatt.light(False)
        self.__onData(Meter(time.time()))
        self._isRecording = False
