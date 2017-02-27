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

import numpy as np


class Meter(object):
    CURRENT_NONE, CURRENT_AC, CURRENT_DC = range(3)

    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.batt = False
        self.current = self.CURRENT_NONE
        self.auto = False
        self.display = None
        self.value = np.nan
        self.bar = 0
