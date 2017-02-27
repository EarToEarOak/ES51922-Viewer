#!/usr/bin/env python
#
#
# ES51022 View
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

hidden = ['PySide.QtXml']
a = Analysis(['es51922_view.py'], hiddenimports=hidden)
a.datas += Tree('es51922_viewer/gui', prefix='gui')

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O', '', 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='es51922_view',
          upx=True)
