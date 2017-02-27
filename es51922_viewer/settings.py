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

from PySide.QtCore import QSettings


class Settings(object):
    def __init__(self):
        self._settings = None

        self._port = ''

        self.__load()

    def __load(self):
        self._settings = QSettings('Ear to Ear Oak', 'es51922_view')
        self._port = self._settings.value('port', self._port)

    def setComboPort(self, comboBox):
        ports = [comboBox.itemText(i) for i in range(comboBox.count())]
        if self._port in ports:
            comboBox.setCurrentIndex(ports.index(self._port))

    def getComboPort(self, comboxBox):
        self._port = comboxBox.currentText()
        self._settings.setValue('port', self._port)
