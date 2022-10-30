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

import clang.cindex
from clang.cindex import CursorKind, TypeKind

import clangworkarounds
from compoundtype import compound_type
from enumtype import enumeration_type
from exceptiontypes import CompilerError
from logger import Logger, LogLevel
from parsedfile import parsed_file
from typemanager import type_manager
from uniontype import union_type


def _build_typeman_recurse(logger, typeman, cursor):
    for child in cursor.get_children():
        if len(child.spelling) > 0:
            if child.kind == CursorKind.NAMESPACE:
                _build_typeman_recurse(logger, typeman, child)
            elif child.kind == CursorKind.STRUCT_DECL or child.kind == CursorKind.CLASS_DECL:
                if child.is_definition():
                    type_location = child.type.get_declaration().location.file.name
                    ctype = compound_type(child.type.spelling, type_location)
                    typeman.add_type(child.type.spelling, ctype)
                    _build_typeman_recurse(logger, typeman, child)
            elif child.kind == CursorKind.UNION_DECL:
                if child.is_definition():
                    type_location = child.type.get_declaration().location.file.name
                    ctype = union_type(child.type.spelling, type_location)
                    typeman.add_type(child.type.spelling, ctype)
                    _build_typeman_recurse(logger, typeman, child)
            elif child.kind == CursorKind.ENUM_DECL:
                if child.is_definition():
                    enum_location = child.type.get_declaration().location.file.name
                    etype = enumeration_type(
                        child.type.spelling, child.enum_type.spelling, enum_location)
                    typeman.add_type(child.type.spelling, etype)
                    _build_typeman_recurse(logger, typeman, child)

            # we take advantage of the fact that we only ever expect to see this
            # cursor kind if we are parsing an enumeration. we assume that the parent
            # cursor is the enum that we are parsing.
            elif child.kind == CursorKind.ENUM_CONSTANT_DECL:
                active_enum_type = typeman.get_type(cursor.type.spelling)
                active_enum_type.add_enum_elem(
                    child.spelling, child.enum_value)

            # the field declaration logic takes advantage of an assumption that we will only
            # see this cursor type when parsing an existing structure/class definition.
            elif child.kind == CursorKind.FIELD_DECL:

                # see if the type is an array. if so, try to rip out
                # the type information from it. we work in the opposite fashion
                # of clang; whereas clang encodes the array information into the type,
                # we want to encode that information on a per-field basis
                if child.type.kind == TypeKind.CONSTANTARRAY:
                    realtype = child.type.element_type.get_canonical()
                    if len(realtype.spelling) == 0:
                        realtype = child.type.element_type

                    numelems = child.type.element_count
                    if typeman.is_known_type(realtype.spelling):
                        logger.log(LogLevel.Debug1, "Array var: {0} (child of struct: {1})".format(
                            child.spelling, cursor.type.spelling))
                        field_type = typeman.get_type(realtype.spelling)
                        active_compound_type = typeman.get_type(
                            cursor.type.spelling)
                        active_compound_type.add_field(
                            child.spelling, field_type, numelems)
                    else:
                        logger.log(LogLevel.Warning, "Unknown array type not known to type manager: {0} | {1}".format(
                            realtype.spelling, child.type.spelling))

                else:
                    canonical_type = child.type.get_canonical()

                    # workaround for constructs like old-style C "typedef struct"
                    if len(canonical_type.spelling) == 0:
                        canonical_type = child.type

                    if typeman.is_known_type(canonical_type.spelling):
                        logger.log(LogLevel.Debug1, "Non-array var: {0} (child of struct: {1})".format(
                            child.spelling, cursor.type.spelling))
                        field_type = typeman.get_type(canonical_type.spelling)
                        active_compound_type = typeman.get_type(
                            cursor.type.spelling)
                        active_compound_type.add_field(
                            child.spelling, field_type)
                    else:
                        logger.log(LogLevel.Warning, "Unknown type not known to type manager: {0}".format(
                            child.type.spelling))


def _build_include_list(typeman, additional_include_dirs):
    inclist = []
    for type in typeman.get_compound_types():
        inclist.append(type.declaration_filename)
    for type in typeman.get_enum_types():
        inclist.append(type.declaration_filename)
    for type in typeman.get_union_types():
        inclist.append(type.declaration_filename)
    return inclist


def parse_input_file(input_filename, logger, additional_include_dirs=[]):
    index = clang.cindex.Index.create()

    default_parser_options = (
        # needed for preprocessing parsing
        clangworkarounds.CXTranslationUnit_DetailedPreprocessingRecord |
        clangworkarounds.CXTranslationUnit_SkipFunctionBodies |  # for faster parsing
        clangworkarounds.CXTranslationUnit_KeepGoing  # don't stop on errors
    )

    # force C++ parsing, so that way headers are parsed correctly if they contain
    # C++-style declarations.
    arglist = ['-x', 'c++', '-std=c++11']
    for dir in additional_include_dirs:
        arglist.append('-I')
        arglist.append(dir)

    translation_unit = index.parse(
        input_filename, args=arglist, options=default_parser_options)

    compiler_errorlist = []
    for diagnostic in translation_unit.diagnostics:
        if diagnostic.severity == clang.cindex.Diagnostic.Error or diagnostic.severity == clang.cindex.Diagnostic.Fatal:
            compiler_errorlist.append(diagnostic)

    if len(compiler_errorlist) > 0:
        raise CompilerError(compiler_errorlist)

    # old way
    typeman = type_manager()

    _build_typeman_recurse(logger, typeman, translation_unit.cursor)
    include_list = _build_include_list(typeman, additional_include_dirs)

    return parsed_file(input_filename, typeman, include_list, additional_include_dirs)
