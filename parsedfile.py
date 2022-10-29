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
from includepath import IncludePath
from typemanager import type_manager


class parsed_file(object):
    def __init__(self, parsed_filename, typeman, includelist, include_directories):
        self._my_file = parsed_filename
        self._type_mgr = typeman
        self._includes = []
        for include in includelist:
            self._includes.append(IncludePath(include, include_directories))

    @property
    def all_parsed_compound_types(self):
        return self._type_mgr.get_compound_types()

    @property
    def all_parsed_enum_types(self):
        return self._type_mgr.get_enum_types()

    @property
    def compound_types_parsed_from_file(self):
        return [type for type in self._type_mgr.get_compound_types() if type.declaration_filename == self._my_file]

    @property
    def enum_types_parsed_from_file(self):
        return [type for type in self._type_mgr.get_enum_types() if type.declaration_filename == self._my_file]

    @property
    def union_types_parsed_from_file(self):
        return [type for type in self._type_mgr.get_union_types() if type.declaration_filename == self._my_file]

    @property
    def other_includes(self):
        return self._includes

    @property
    def parsed_filepath(self):
        return self._my_file
