#!/usr/bin/env python
#
#
# ES51022 Viewer
#
#
# Copyright 2017 Al Brown
#
# Monitor ES51022 based multimeters
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from PySide.QtGui import QApplication

from es51922_viewer.window_main import WindowMain


if __name__ == '__main__':
    app = QApplication([])
    win = WindowMain()
    win.show()
    app.exec_()
