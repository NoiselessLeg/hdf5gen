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
import os


class IncludePath(object):
    def __init__(self, include_path_str, include_path_directories):
        self._rawpath = include_path_str
        self._abspath = os.path.abspath(include_path_str)
        for path in include_path_directories:
            tmppath = os.path.join(path, include_path_str)
            if os.path.exists(tmppath):
                self._abspath = tmppath
                break

    @property
    def absolute_filepath(self):
        return self._abspath

    @property
    def raw_include_filename(self):
        return self._rawpath

    @property
    def include_filename(self):
        return os.path.basename(self._rawpath)

    def __eq__(self, other):
        return self.absolute_filepath == other.absolute_filepath

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash(self._abspath)
