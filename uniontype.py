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

from fieldelem import field_element
from typecode import TypeCode


class union_type(object):
    def __init__(self, typename, declaration_filename):
        self._typename = typename
        self._header_filename = declaration_filename
        self._fieldlist = []

    def add_field(self, fieldname, fieldtype, num_elems=1):
        self._fieldlist.append(field_element(fieldname, fieldtype, num_elems))

    @property
    def declaration_filename(self):
        return self._header_filename

    @property
    def fully_qualified_typename(self):
        return self._typename

    @property
    def typename(self):
        fqn = self.fully_qualified_typename
        if '::' in fqn:
            return fqn.split('::')[-1]
        else:
            return fqn

    @property
    def typecode(self):
        return TypeCode.UNION

    @property
    def fields(self):
        return self._fieldlist
