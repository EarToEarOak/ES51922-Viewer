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

from PySide.QtGui import QWidget, QFont, QPainter, QColor, QPen

from es51922_viewer.meter import Meter


class WidgetLcd(QWidget):
    WEIGHT_CURRENT = 1
    WEIGHT_VALUE = 4
    WEIGHT_RANGE = 1
    WEIGHT_SCALE = 0.5

    WEIGHT_BAR = 0.1
    WEIGHT_MARGIN = 0.1

    TICKS = 22

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self._fontCurrent = QFont('Monospace', self.WEIGHT_CURRENT * 10)
        self._fontValue = QFont('Monospace', self.WEIGHT_VALUE * 10)
        self._fontRange = QFont('Monospace', self.WEIGHT_RANGE * 10)
        self._fontScale = QFont('Monospace', self.WEIGHT_SCALE * 10)

        self.setFont(self._fontCurrent)
        self._sizeCurrent = self.fontMetrics().tightBoundingRect('#')

        self.setFont(self._fontValue)
        self._sizeValue = self.fontMetrics().tightBoundingRect('-#########. ###')

        self.setFont(self._fontRange)
        self._sizeRange = self.fontMetrics().tightBoundingRect('#')

        self.setFont(self._fontScale)
        self._sizeScale = self.fontMetrics().tightBoundingRect('##')

        self.setMinimumWidth(self._sizeValue.width())
        self.setMinimumHeight(self._sizeValue.width() / 5)

        self._meter = None

    def paintEvent(self, event):
        width = event.rect().width() - 1
        scale = float(width) / self._sizeValue.width()

        self._fontCurrent.setPointSizeF(scale * self.WEIGHT_CURRENT * 10)
        self._fontValue.setPointSizeF(scale * self.WEIGHT_VALUE * 10)
        self._fontRange.setPointSizeF(scale * self.WEIGHT_RANGE * 10)

        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(QColor(42, 67, 107), 4 * scale))

        pos = self.__drawText(painter, scale)
        pos = self.__drawBar(painter, scale, width, pos)

        painter.end()

        self.setMinimumHeight(pos)

    def __drawText(self, painter, scale):
        margin = self._sizeCurrent.height() * self.WEIGHT_MARGIN * 10 * scale
        top = self._sizeCurrent.height() * scale + margin
        middle = top + (self._sizeValue.height() * scale) + margin
        bottom = middle + (self._sizeRange.height() * scale) + margin

        if self._meter is not None and self._meter.display is not None:
            if self._meter.current == Meter.CURRENT_DC:
                current = 'DC'
            elif self._meter.current == Meter.CURRENT_AC:
                current = 'AC'
            else:
                current = ''
            painter.setFont(self._fontCurrent)
            painter.drawText(margin, top, current)

            painter.setFont(self._fontValue)
            painter.drawText(margin, middle, self._meter.display)

            if self._meter.auto:
                rang = 'AUTO'
            else:
                rang = 'MANUAL'
            painter.setFont(self._fontRange)
            painter.drawText(margin, bottom, rang)
        else:
            painter.setFont(self._fontValue)
            painter.drawText(margin, middle, '    ------')

        return bottom + margin

    def __drawBar(self, painter, scale, width, pos):
        margin = self._sizeCurrent.height() * self.WEIGHT_MARGIN * 10 * scale
        height = self._sizeCurrent.height() * self.WEIGHT_BAR * 10 * scale

        self._fontScale.setPointSizeF(scale * self.WEIGHT_SCALE * 10)
        painter.setFont(self._fontScale)

        for i in range(self.TICKS * 2 - 1):
            x = (i * (width - margin) / float(self.TICKS * 2)) + margin
            length = height / 2
            if i % 10 == 0:
                length = height
                centre = self.fontMetrics().width(str(i / 2)) / 2
                painter.drawText(x - centre, pos + margin * 2, str(i / 2))
            elif i % 2 == 0:
                length = height * 2 / 3
            if self._meter is not None and i <= self._meter.bar:
                painter.drawLine(x, pos + height,
                                 x, pos + height - length)

        return pos + height + margin * 2

    def set(self, meter):
        self._meter = meter
        self.repaint()

    def clear(self):
        self._meter = None
        self.repaint()
