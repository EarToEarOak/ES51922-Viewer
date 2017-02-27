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

from PySide.QtCore import QDateTime

import pyqtgraph as pg


class WidgetPlot(pg.PlotWidget):
    def __init__(self, parent):
        pg.PlotWidget.__init__(self, parent,
                               background='w',
                               title=' ',
                               axisItems={'bottom':
                                          TimeAxisItem()})

        self._timestamps = []
        self._values = []

        self.setMinimumHeight(100)

        pg.setConfigOptions(antialias=True)
        self.setClipToView(True)
        self.showGrid(True, True, 1.0)

        self._curve = self.plot(pen=(42, 67, 107))

    def set(self, meter):
        self._timestamps.append(meter.timestamp)
        self._values.append(meter.value)
        self._curve.setData(self._timestamps, self._values, connect="finite")

    def clearPlot(self):
        del self._timestamps[:]
        del self._values[:]
        self._curve.clear()


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, 'bottom', *args, **kwargs)

    def tickStrings(self, values, _scale, _spacing):
        return [QDateTime().fromMSecsSinceEpoch(value * 1000).toString('hh:mm:ss.z')
                for value in values]
