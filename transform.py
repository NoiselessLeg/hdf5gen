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
import argparse
import os
import time

import clang.cindex

from exceptiontypes import CompilerError, SevereLogMsgException
from fileexclusion import FileExcluder
from filegen import generate_output_header_file
from fileparse import parse_input_file
from logger import Logger, LogLevel
from parsedfile import parsed_file
from typemanager import type_manager

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Generates C++ shim code to transform most arbitrary structs into an HDF5 data type.")
        parser.add_argument('target_file',
                            help='the file that the transform will be generated for.')

        parser.add_argument('--output-dir', '-o', metavar=("output directory"),
                            help='the directory the transforms will be generated in.', default=os.getcwd())

        parser.add_argument('--include-directory', '-I', help='additional include path to search when generating the transform.',
                            metavar=("additional include path"), action='append')

        parser.add_argument('--clang-library-file', '-l',
                            help='the Clang library file the generator will use as the parser front-end.',
                            default='libclang-12.so')

        parser.add_argument('--verbosity', '-v',
                            help='the verbosity of information output to the screen. The higher the value, the more debug output is generated.',
                            default=2, type=int)

        parser.add_argument('--ignore-file', '-i',
                            help='the text file specifying which include directories that potentially can be pulled into a parse chain should be skipped.',
                            default='ignore.txt')

        parser.add_argument('--enable-warnings-as-errors', '-w',
                            help='all tool-generated warnings will emit a fatal error and stop further generation.',
                            default=False, action='store_true')

        args = parser.parse_args()
        logger = Logger(args.verbosity, args.enable_warnings_as_errors)
        clang.cindex.Config.set_library_file(args.clang_library_file)

        logger.log(LogLevel.Info, "Parsing file {0}.".format(args.target_file))

        if not os.path.exists(args.target_file):
            logger.log(LogLevel.Severe, "Could not find file {0} to read.".format(
                args.target_file))
            exit()

        start = time.time()
        if args.include_directory is not None:
            parsed_file = parse_input_file(
                args.target_file, logger, args.include_directory)
        else:
            parsed_file = parse_input_file(args.target_file, logger)
        end = time.time()

        logger.log(LogLevel.Info, "Parsing of {0} completed in {1} seconds.".format(
            args.target_file, end - start))
        logger.log(LogLevel.Info, "Generating code.")

        file_excluder = FileExcluder(args.ignore_file)
        generate_output_header_file(
            logger, args.output_dir, parsed_file, file_excluder)

    except CompilerError as err:
        print("The following compiler error(s) were encountered when parsing {0}:".format(
            args.target_file))
        print(err)
        print("The process was aborted and the output was not successfully generated.")
    except SevereLogMsgException as logerr:
        pass
