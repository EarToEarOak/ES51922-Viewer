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

from PySide.QtCore import QRectF
from PySide.QtGui import QGraphicsItem

import pyqtgraph as pg


class Crosshair(QGraphicsItem):
    def __init__(self):
        QGraphicsItem.__init__(self)

        self.setFlag(self.ItemIgnoresTransformations)

    def paint(self, painter, _option, _widget):
        painter.setPen(pg.mkPen(color=(42, 67, 107)))
        painter.drawLine(5, 5, -5, -5)
        painter.drawLine(-5, 5, 5, -5)

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)
