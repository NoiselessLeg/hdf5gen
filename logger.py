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
from enum import IntEnum

from exceptiontypes import SevereLogMsgException

class LogLevel(IntEnum):
    Severe = 0
    Warning = 1
    Info = 2
    Debug1 = 3
    Debug2 = 4
    Debug3 = 5
    
    

class Logger:
    def __init__(self, log_level, warnings_are_errors=False):
        self._log_level = log_level
        self._warnings_are_errors = warnings_are_errors
    
    
    def log(self, log_level, logstr):
        fixed_lvl = log_level
        
        if fixed_lvl == LogLevel.Warning and self._warnings_are_errors:
            fixed_lvl = LogLevel.Severe
            logstr += " (Would normally be a warning, but --enable-warnings-as-errors or -w was provided as a command line argument)"
            
        if fixed_lvl > self._log_level:
            return
            
        print("{0}: {1}".format(Logger._get_log_prefix(fixed_lvl), logstr))
        if fixed_lvl == LogLevel.Severe:
            raise SevereLogMsgException(logstr)
            
    @staticmethod
    def _get_log_prefix(loglevel):
        logdic = {
                    LogLevel.Severe    : "SEVERE",
                    LogLevel.Warning   : "WARNING",
                    LogLevel.Info      : "INFO",
                    LogLevel.Debug1    : "DEBUG1",
                    LogLevel.Debug2    : "DEBUG2",
                    LogLevel.Debug3    : "DEBUG3"
                }
        return logdic[loglevel]

