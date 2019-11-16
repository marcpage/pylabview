# -*- coding: utf-8 -*-

""" LabView RSRC file format support.

Miscelanous generic utilities.
"""

# Copyright (C) 2013 Jessica Creighton <jcreigh@femtobit.org>
# Copyright (C) 2019 Mefistotelis <mefistotelis@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys
from ctypes import *
from collections import OrderedDict

class RSRCStructure(BigEndianStructure):
    _pack_ = 1

    def dict_export(self):
        class ExportDict(OrderedDict): pass
        ExportDict.__name__ = self.__class__.__name__
        d = ExportDict()
        for (varkey, vartype) in self._fields_:
            v = getattr(self, varkey)
            if isinstance(v, Array) and v._type_ == c_ubyte:
                d[varkey] = bytes(v)
            else:
                d[varkey] = v
        return d

    def __repr__(self):
        d = self.dict_export()
        from pprint import pformat
        return pformat(d, indent=0, width=160)


LABVIEW_VERSION_STAGE = ['unknown', 'development', 'alpha', 'beta', 'release']
LABVIEW_COLOR_PALETTE = [0xF1F1F1, 0xCCFFFF, 0x99FFFF, 0x66FFFF, 0x33FFFF,
                 0xFFFF, 0xFFCCFF, 0xCCCCFF, 0x99CCFF, 0x66CCFF,
                 0x33CCFF, 0xCCFF, 0xFF99FF, 0xCC99FF, 0x9999FF,
                 0x6699FF, 0x3399FF, 0x99FF, 0xFF66FF, 0xCC66FF,
                 0x9966FF, 0x6666FF, 0x3366FF, 0x66FF, 0xFF33FF,
                 0xCC33FF, 0x9933FF, 0x6633FF, 0x3333FF, 0x33FF,
                 0xFF00FF, 0xCC00FF, 0x9900FF, 0x6600FF, 0x3300FF,
                 0xFF, 0xFFFFCC, 0xCCFFCC, 0x99FFCC, 0x66FFCC,
                 0x33FFCC, 0xFFCC, 0xFFCCCC, 0xCCCCCC, 0x99CCCC,
                 0x66CCCC, 0x33CCCC, 0xCCCC, 0xFF99CC, 0xCC99CC,
                 0x9999CC, 0x6699CC, 0x3399CC, 0x99CC, 0xFF66CC,
                 0xCC66CC, 0x9966CC, 0x6666CC, 0x3366CC, 0x66CC,
                 0xFF33CC, 0xCC33CC, 0x9933CC, 0x6633CC, 0x3333CC,
                 0x33CC, 0xFF00CC, 0xCC00CC, 0x9900CC, 0x6600CC,
                 0x3300CC, 0xCC, 0xFFFF99, 0xCCFF99, 0x99FF99,
                 0x66FF99, 0x33FF99, 0xFF99, 0xFFCC99, 0xCCCC99,
                 0x99CC99, 0x66CC99, 0x33CC99, 0xCC99, 0xFF9999,
                 0xCC9999, 0x999999, 0x669999, 0x339999, 0x9999,
                 0xFF6699, 0xCC6699, 0x996699, 0x666699, 0x336699,
                 0x6699, 0xFF3399, 0xCC3399, 0x993399, 0x663399,
                 0x333399, 0x3399, 0xFF0099, 0xCC0099, 0x990099,
                 0x660099, 0x330099, 0x99, 0xFFFF66, 0xCCFF66,
                 0x99FF66, 0x66FF66, 0x33FF66, 0xFF66, 0xFFCC66,
                 0xCCCC66, 0x99CC66, 0x66CC66, 0x33CC66, 0xCC66,
                 0xFF9966, 0xCC9966, 0x999966, 0x669966, 0x339966,
                 0x9966, 0xFF6666, 0xCC6666, 0x996666, 0x666666,
                 0x336666, 0x6666, 0xFF3366, 0xCC3366, 0x993366,
                 0x663366, 0x333366, 0x3366, 0xFF0066, 0xCC0066,
                 0x990066, 0x660066, 0x330066, 0x66, 0xFFFF33,
                 0xCCFF33, 0x99FF33, 0x66FF33, 0x33FF33, 0xFF33,
                 0xFFCC33, 0xCCCC33, 0x99CC33, 0x66CC33, 0x33CC33,
                 0xCC33, 0xFF9933, 0xCC9933, 0x999933, 0x669933,
                 0x339933, 0x9933, 0xFF6633, 0xCC6633, 0x996633,
                 0x666633, 0x336633, 0x6633, 0xFF3333, 0xCC3333,
                 0x993333, 0x663333, 0x333333, 0x3333, 0xFF0033,
                 0xCC0033, 0x990033, 0x660033, 0x330033, 0x33,
                 0xFFFF00, 0xCCFF00, 0x99FF00, 0x66FF00, 0x33FF00,
                 0xFF00, 0xFFCC00, 0xCCCC00, 0x99CC00, 0x66CC00,
                 0x33CC00, 0xCC00, 0xFF9900, 0xCC9900, 0x999900,
                 0x669900, 0x339900, 0x9900, 0xFF6600, 0xCC6600,
                 0x996600, 0x666600, 0x336600, 0x6600, 0xFF3300,
                 0xCC3300, 0x993300, 0x663300, 0x333300, 0x3300,
                 0xFF0000, 0xCC0000, 0x990000, 0x660000, 0x330000,
                 0xEE, 0xDD, 0xBB, 0xAA, 0x88, 0x77, 0x55, 0x44,
                 0x22, 0x11, 0xEE00, 0xDD00, 0xBB00,
                 0xAA00, 0x8800, 0x7700, 0x5500, 0x4400,
                 0x2200, 0x1100, 0xEE0000, 0xDD0000, 0xBB0000,
                 0xAA0000, 0x880000, 0x770000, 0x550000, 0x440000,
                 0x220000, 0x110000, 0xEEEEEE, 0xDDDDDD, 0xBBBBBB,
                 0xAAAAAA, 0x888888, 0x777777, 0x555555, 0x444444,
                 0x222222, 0x111111, 0x0]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getPrettyStrFromRsrcType(rsrc_ident):
    """ Gives alphanumeric string representation of a 4-byte identifier, like block ident
    """
    pretty_ident = bytes(rsrc_ident).decode(encoding='utf-8')
    pretty_ident = re.sub('#', 'sh', pretty_ident)
    pretty_ident = re.sub('[^a-zA-Z0-9_-]+', '', pretty_ident)
    if len(pretty_ident) < 3:
        eprint("Warning: Identifier has more than one special character.")
        pretty_ident += 'spec'
    return pretty_ident

def getRsrcTypeFromPrettyStr(pretty_ident):
    """ Gives 4-byte identifier from alphanumeric string representation
    """
    rsrc_ident = str(pretty_ident).encode(encoding='utf-8')
    if len(rsrc_ident) > 4:
        rsrc_ident = re.sub(b'sh', b'#', rsrc_ident)
    if len(rsrc_ident) > 4:
        rsrc_ident = re.sub(b'spec', b'?', rsrc_ident)
    while len(rsrc_ident) < 4: rsrc_ident += b' '
    rsrc_ident = rsrc_ident[:4]
    return rsrc_ident

def getVersion(vcode):
    ver = {}
    ver['major'] = ((vcode >> 28) & 0x0F) * 10 + ((vcode >> 24) & 0x0F)
    ver['minor'] = (vcode >> 20) & 0x0F
    ver['bugfix'] = (vcode >> 16) & 0x0F
    ver['stage'] = (vcode >> 13) & 0x07
    ver['flags'] = (vcode >> 8) & 0x1F  # 5 bit??
    ver['build'] = ((vcode >> 4) & 0x0F) * 10 + ((vcode >> 0) & 0x0F)
    ver['stage_text'] = LABVIEW_VERSION_STAGE[0]
    if ver['stage'] < len(LABVIEW_VERSION_STAGE):
        ver['stage_text'] = LABVIEW_VERSION_STAGE[ver['stage']]
    return ver

def crypto_xor(data):
    rol = lambda val, l_bits, max_bits: \
      ((val & ((1<<max_bits-(l_bits%max_bits))-1)) << l_bits%max_bits) | \
      (val >> (max_bits-(l_bits%max_bits)) & ((1<<max_bits)-1))
    out = bytearray(data)
    key = 0xEDB88320
    for i in range(len(out)):
        nval = (key ^ out[i]) & 0xff
        out[i] = nval
        key = nval ^ rol(key, 1, 32)
    return out
