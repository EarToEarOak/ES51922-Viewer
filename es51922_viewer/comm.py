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

from PySide.QtCore import QThread, Signal, QTimer
from PySide.QtGui import QApplication
from es51922_viewer.meter import Meter
from es51922_viewer.parser import Parser
import serial
from serial.tools import list_ports


class Comm(object):
    def __init__(self):
        self._reader = None

    def getPorts(self):
        ports = list(list_ports.comports())
        return [port.device for port in ports]

    def start(self, port, callbackData, callbackWarning, callbackError):
        self._reader = Reader(port)
        self._reader.data.connect(callbackData)
        self._reader.warning.connect(callbackWarning)
        self._reader.error.connect(callbackError)
        self._reader.start()

    def stop(self):
        if self._reader is not None:
            self._reader.stop()
            self._reader.wait()


class Reader(QThread):
    data = Signal(Meter)
    warning = Signal(str)
    error = Signal(str)

    def __init__(self, port):
        QThread.__init__(self)

        self._port = port
        self._serial = None
        self._parser = Parser()
        self._cancel = False
        self._timeout = None

    def run(self):
        self._timeout = QTimer()
        self._timeout.setInterval(2000)
        self._timeout.timeout.connect(self.__onTimeout)

        try:
            self._serial = serial.Serial(self._port,
                                         baudrate=19200,
                                         bytesize=serial.SEVENBITS,
                                         stopbits=serial.STOPBITS_ONE,
                                         parity=serial.PARITY_ODD,
                                         timeout=1)
            self._serial.dtr = True
            self._serial.rts = False

            while not self._cancel:
                if not self._timeout.isActive():
                    self._timeout.start()
                data = self._serial.readline()
                data = data.strip()
                if len(data) == 12:
                    timestamp = time.time()
                    result = self._parser.parse(data, timestamp)
                    if result is not None:
                        self._timeout.stop()
                        self.data.emit(result)
                    else:
                        self.warning.emit('Invalid data received')
                QApplication.processEvents()
            self._serial.close()
        except serial.SerialException as e:
            self.error.emit(e.message)

    def __onTimeout(self):
        self.warning.emit('No data received')

    def stop(self):
        self._cancel = True
