#!/usr/bin/env python3

'''
MIT License

Copyright (c) 2022 Johnathon Lewis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from atomictype import *
from typecode import TypeCode


class type_manager(object):
    def __init__(self):
        self._typemap = {
            "bool": native_bool_type(),
            "char": native_char_type(),
            "signed char": native_schar_type(),
            "unsigned char": native_uchar_type(),
            "unsigned short": native_ushort_type(),
            "short": native_short_type(),
            "unsigned int": native_uint_type(),
            "int": native_int_type(),
            "unsigned long": native_ulong_type(),
            "long": native_long_type(),
            "unsigned long long": native_ulonglong_type(),
            "long long": native_longlong_type(),
            "float": native_float_type(),
            "double": native_double_type(),
            "long double": native_long_double_type()
        }

    def add_type(self, typename, type):
        assert typename not in self._typemap, "Type {0} is already in the type manager.".format(
            typename)
        self._typemap[typename] = type

    def is_known_type(self, typename):
        return typename in self._typemap

    def get_type(self, typename):
        assert typename in self._typemap, "Could not find {0} in type map.".format(
            typename)
        return self._typemap[typename]

    def get_compound_types(self):
        return [type for type in self._typemap.values() if type.typecode == TypeCode.COMPOUND]

    def get_enum_types(self):
        return [type for type in self._typemap.values() if type.typecode == TypeCode.ENUM]

    def get_union_types(self):
        return [type for type in self._typemap.values() if type.typecode == TypeCode.UNION]
