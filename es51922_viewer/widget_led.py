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

from PySide.QtCore import QTimer
from PySide.QtGui import QWidget, QPainter, QPen, QColor, QBrush


class WidgetLed(QWidget):
    def __init__(self, parent, colour='#000000'):
        QWidget.__init__(self, parent)
        self._colour = QColor(colour)

        self.setMinimumSize(10, 10)

        self._lit = False
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self.__flashOff)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        if self._lit:
            self._colour.setAlphaF(1)
        else:
            self._colour.setAlphaF(.25)
        painter.setPen(QPen(self._colour, 1))
        painter.setBrush(QBrush(self._colour))

        rect = event.rect()
        radius = min(rect.width(), rect.height()) / 3
        painter.drawEllipse(rect.center(), radius, radius)

        painter.end()

    def __flashOff(self):
        self._timer.stop()
        self._lit = False
        self.repaint()

    def flash(self):
        self._lit = True
        self._timer.start()
        self.repaint()

    def light(self, on):
        self._timer.stop()
        self._lit = on
        self.repaint()
