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

from enum import Enum
from typecode import TypeCode

class NativeType(Enum):
    CHAR = 1
    SCHAR = 2
    UCHAR = 3
    SHORT = 4
    USHORT = 5
    INT = 6
    UINT = 7
    LONG = 8
    ULONG = 9
    LONGLONG = 10
    ULONGLONG = 11
    FLOAT = 12
    DOUBLE = 13
    LONGDOUBLE = 14
    BOOLEAN = 15
    
class native_base_type(object):
    @property
    def typecode(self):
        return TypeCode.ATOMIC
        
    @property
    def fully_qualified_typename(self):
        return self.typename

class native_char_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.CHAR
        
    @property
    def typename(self):
        return "char"

class native_schar_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.SCHAR
        
    @property
    def typename(self):
        return "signed char"

class native_uchar_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.UCHAR
        
    @property
    def typename(self):
        return "unsigned char"
        
    @property
    def fully_qualified_typename(self):
        return self.typename

class native_ushort_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.USHORT
        
    @property
    def typename(self):
        return "unsigned short"

class native_short_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.SHORT
        
    @property
    def typename(self):
        return "short"
        
    @property
    def fully_qualified_typename(self):
        return self.typename

class native_uint_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.UINT
        
    @property
    def typename(self):
        return "unsigned int"
        
    @property
    def fully_qualified_typename(self):
        return self.typename

class native_int_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.INT
        
    @property
    def typename(self):
        return "int"
        
        
class native_ulong_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.ULONG
        
    @property
    def typename(self):
        return "unsigned long"

class native_long_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.LONG
        
    @property
    def typename(self):
        return "long"
        
        
class native_ulonglong_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.ULONGLONG
        
    @property
    def typename(self):
        return "unsigned long long"

class native_longlong_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.LONGLONG
        
    @property
    def typename(self):
        return "long long"
        
        
class native_float_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.FLOAT
        
    @property
    def typename(self):
        return "float"

class native_double_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.DOUBLE
        
    @property
    def typename(self):
        return "double"
        
        
class native_long_double_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.LONGDOUBLE
        
    @property
    def typename(self):
        return "long double"

class native_bool_type(native_base_type):
        
    @property
    def atomic_type(self):
        return NativeType.BOOLEAN
        
    @property
    def typename(self):
        return "bool"