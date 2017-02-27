#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import struct

from es51922_viewer.meter import Meter


class Parser(object):
    FUNC_VOLTAGE = 0b0111011
    FUNC_CURRENT_AUTO_UA = 0b0111101
    FUNC_CURRENT_AUTO_MA = 0b0111111
    FUNC_CURRENT_22A = 0b0110000
    FUNC_CURRENT_MANUAL = 0b0111001
    FUNC_RESISTANCE = 0b0110011
    FUNC_CONTINUITY = 0b0110101
    FUNC_DIODE = 0b0110001
    FUNC_FREQUENCY = 0b0110010
    FUNC_CAPACITANCE = 0b0110110
    FUNC_TEMPERATURE = 0b0110100
    FUNC_ADP = 0b0111110

    SUBFUNC_FREQUENCY = 1
    SUBFUNC_DUTY = 2

    # Decimal point location, Scaling, Units
    RANGE_VOLTAGE = {
        0b0110000: (4, 1e0, 'V'),  # 2.2000
        0b0110001: (3, 1e0, 'V'),  # 22.000
        0b0110010: (2, 1e0, 'V'),  # 220.00
        0b0110011: (1, 1e0, 'V'),  # 2200.0
        0b0110100: (2, 1e-3, 'mV')}  # 220.00

    RANGE_CURRENT_AUTO_UA = {
        0b0110000: (2, 1e-6, u'μA'),  # 220.00u
        0b0110001: (1, 1e-6, u'μA')}  # 2200.00u

    RANGE_CURRENT_AUTO_MA = {
        0b0110000: (3, 1e-3, 'mA'),  # 22.000m
        0b0110001: (2, 1e-3, 'mA')}  # 220.00m

    RANGE_CURRENT_22A = {
        0b0110000: (3, 1e0, 'A')}  # 22.000 A

    RANGE_CURRENT_MANUAL = {
        0b0110000: (4, 1e0, 'A'),  # 2.2000
        0b0110001: (3, 1e0, 'A'),  # 22.000
        0b0110010: (2, 1e0, 'A'),  # 220.00
        0b0110011: (1, 1e0, 'A'),  # 2200.0
        0b0110100: (0, 1e0, 'A')}  # 22000

    RANGE_RESISTANCE = {
        0b0110000: (2, 1e0, u'Ω'),  # 220.00
        0b0110001: (4, 1e3, u'kΩ'),  # 2.2000k
        0b0110010: (3, 1e3, u'kΩ'),  # 22.000k
        0b0110011: (2, 1e3, u'kΩ'),  # 220.00k
        0b0110100: (4, 1e6, u'MΩ'),  # 2.2000M
        0b0110101: (3, 1e6, u'MΩ'),  # 22.000M
        0b0110110: (2, 1e6, u'MΩ')}  # 220.00M

    RANGE_CONTINUITY = {
        0b0110000: (2, 1e0, u'Ω')}  # 220.00

    RANGE_DIODE = {
        0b0110000: (4, 1e0, 'V')}  # 2.2000V

    RANGE_FREQUENCY = {
        0b0110000: (1, 1e0, 'Hz'),  # 22.00
        0b0110001: (1, 1e0, 'Hz'),  # 220.0
        0b0110011: (3, 1e3, 'kHz'),  # 22.000k
        0b0110100: (2, 1e3, 'kHz'),  # 220.00k
        0b0110101: (4, 1e6, 'MHz'),  # 2.2000M
        0b0110110: (3, 1e6, 'MHz'),  # 22.000M
        0b0110111: (2, 1e6, 'MHz')}  # 220.00M

    RANGE_CAPACITANCE = {
        0b0110000: (3, 1e-9, 'nF'),  # 22.000n
        0b0110001: (2, 1e-9, 'nF'),  # 220.00n
        0b0110010: (4, 1e-6, u'μF'),  # 2.2000u
        0b0110011: (3, 1e-6, u'μF'),  # 22.000u
        0b0110100: (2, 1e-6, 'μF'),  # 220.00u
        0b0110101: (4, 1e-3, 'mF'),  # 2.2000m
        0b0110110: (3, 1e-3, 'mF'),  # 22.000m
        0b0110111: (2, 1e-3, 'mF')}  # 220.00m

    RANGE_TEMPERATURE = {
        0: (2, 1e0, u'°F'),  # 220.00
        1: (1, 1e0, u'°F'),  # 2200.0
        2: (2, 1e0, u'°C'),  # 220.00
        3: (1, 1e0, u'°C')}  # 2200.0

    RANGE_ADP = {
        0b0110000: (4, 1e0, ''),  # 2.2000
        0b0110001: (3, 1e0, ''),  # 22.000
        0b0110010: (2, 1e0, ''),  # 220.00
        0b0110011: (1, 1e0, ''),  # 2200.0
        0b0110100: (0, 1e0, '')}  # 22000

    SUBRANGE_FREQUENCY = {
        0: (1, 1e0, "Hz")}  # 2200.0

    SUBRANGE_DUTY = {
        0: (1, 1e0, "%")}  # 2200.0

    RANGES = {
        FUNC_VOLTAGE: RANGE_VOLTAGE,
        FUNC_CURRENT_AUTO_UA: RANGE_CURRENT_AUTO_UA,
        FUNC_CURRENT_AUTO_MA: RANGE_CURRENT_AUTO_MA,
        FUNC_CURRENT_22A: RANGE_CURRENT_22A,
        FUNC_CURRENT_MANUAL: RANGE_CURRENT_MANUAL,
        FUNC_RESISTANCE: RANGE_RESISTANCE,
        FUNC_CONTINUITY: RANGE_CONTINUITY,
        FUNC_DIODE: RANGE_DIODE,
        FUNC_FREQUENCY: RANGE_FREQUENCY,
        FUNC_CAPACITANCE: RANGE_CAPACITANCE,
        FUNC_TEMPERATURE: RANGE_TEMPERATURE,
        FUNC_ADP: RANGE_ADP,
        SUBFUNC_FREQUENCY: SUBRANGE_FREQUENCY,
        SUBFUNC_DUTY: SUBRANGE_DUTY}

    def parse(self, data, timestamp):
        if not self.__checkData(data):
            return None

        span, \
            digit4, digit3, digit2, digit1, digit0, \
            function, status, \
            _option1, option2, option3, option4 = struct.unpack('B' * 12, data)

        meter = Meter(timestamp)

        judge = self.__testBit(status, 3)
        vahz = self.__testBit(option3, 0)
        vbar = self.__testBit(option4, 2)
        if function == self.FUNC_TEMPERATURE:
            span = 0
            if judge:
                span += 2
            if vbar:
                span += 1
        elif function == self.FUNC_VOLTAGE:
            if vahz and not judge:
                function = self.SUBFUNC_FREQUENCY
                span = 0
            elif vahz and judge:
                function = self.SUBFUNC_DUTY
                span = 0

        scaling = self.RANGES[function][span]

        ol = self.__testBit(status, 0)
        ul = self.__testBit(option2, 3)
        peak = self.__testBit(option2, 2) or self.__testBit(option2, 1)
        if not ol and not ul and not peak:
            self.__parseDigits(meter,
                               digit0, digit1, digit2, digit3, digit4,
                               status, scaling)
        elif ol:
            meter.display = '    OL'
        elif ul:
            meter.display = '    UL'

        meter.batt = self.__testBit(status, 1)
        if self.__testBit(option3, 3):
            meter.current = Meter.CURRENT_DC
        elif self.__testBit(option3, 2):
            meter.current = Meter.CURRENT_AC
        else:
            meter.current = Meter.CURRENT_NONE
        meter.auto = self.__testBit(option3, 1)

        return meter

    def __checkData(self, data):
        packets = struct.unpack('B' * 12, data)
        for packet in packets:
            if packet & 0b1110000 != 0b0110000:
                return False

        return True

    def __testBit(self, byte, bit):
        return (byte & (1 << bit)) != 0

    def __parseDigits(self, meter,
                      digit0, digit1, digit2, digit3, digit4,
                      status, scaling):
        digits = [d & 0xf for d in [digit4, digit3, digit2, digit1, digit0]]
        sign = self.__testBit(status, 2)
        value = 0
        for i, digit in zip(range(5), digits):
            value += digit * (10 ** (4 - i))
        if sign:
            value *= -1

        dp = scaling[0]
        sf = 6 + dp
        count = value / 10. ** scaling[0]
        meter.display = u'{: {}.{}f} {:>3}'.format(count, sf, dp, scaling[2])
        meter.value = count * scaling[1]
        meter.bar = abs(int(count * 2))
