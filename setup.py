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

from setuptools import setup, find_packages

from es51922_viewer.version import VERSION


setup(name='es51922-viewer',
      version='.'.join([str(x) for x in VERSION]),
      description='Monitor ES51022 based multimeters.',
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Visualization'],
      keywords='multimeter dmm ES51022 ut61',
      url='https://eartoearoak.com/software/es51922-viewer',
      author='Al Brown',
      author_email='al [at] eartoearok.com',
      license='GPLv3',
      packages=find_packages(),
      package_data={'es51922_viewer.gui': ['*']},
      scripts=['es51922_view.py'],
      install_requires=['numpy', 'pyqtgraph', 'pyserial', 'PySide'])
