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

from typecode import TypeCode

class enum_value_pair(object):
    def __init__(self, enum_value, enum_constant):
        self._value = enum_value
        self._const = enum_constant
        
    @property
    def constant_name(self):
        return self._value
        
    @property 
    def constant_value(self):
        return self._const

class enumeration_type(object):
    def __init__(self, name, int_type, declaration_filename):
        self._name = name
        self._underlying_type = int_type
        self._header_filename = declaration_filename
        self._enum_dic = {}
        
    def add_enum_elem(self, value_name, value_constant):
        self._enum_dic[value_name] = value_constant
        
    def get_enum_constants(self):
        ret = []
        for k, v in self._enum_dic.items():
            ret.append(enum_value_pair(k, v))
        
        return ret
        
    @property
    def declaration_filename(self):
        return self._header_filename
        
        
    @property
    def fully_qualified_typename(self):
        return self._name
    
    @property
    def typecode(self):
        return TypeCode.ENUM
        
    @property
    def typename(self):
        fqn = self.fully_qualified_typename
        if '::' in fqn:
            return fqn.split('::')[-1]
        else:
            return fqn

    @property
    def underlying_int_type(self):
        return self._underlying_type