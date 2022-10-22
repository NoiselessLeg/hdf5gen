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

import atomictype
import filegenutils
from compoundtype import compound_type
from enumtype import enumeration_type
from exceptiontypes import CompilerError
from logger import Logger, LogLevel
from parsedfile import parsed_file
from typecode import TypeCode
from typemanager import type_manager

'''

    LONG = 8
    ULONG = 9
    LONGLONG = 10
    ULONGLONG = 11
    FLOAT = 12
    DOUBLE = 13
    LONGDOUBLE = 14
    BOOLEAN = 15
'''

_atomic_to_predefined_typemap = {
    atomictype.NativeType.CHAR : "PredType::NATIVE_CHAR",
    atomictype.NativeType.SCHAR : "PredType::NATIVE_SCHAR",
    atomictype.NativeType.UCHAR : "PredType::NATIVE_UCHAR",
    atomictype.NativeType.SHORT : "PredType::NATIVE_SHORT",
    atomictype.NativeType.USHORT : "PredType::NATIVE_USHORT",
    atomictype.NativeType.INT : "PredType::NATIVE_INT",
    atomictype.NativeType.UINT : "PredType::NATIVE_UINT",
    atomictype.NativeType.LONG : "PredType::NATIVE_LONG",
    atomictype.NativeType.ULONG : "PredType::NATIVE_ULONG",
    atomictype.NativeType.LONGLONG : "PredType::NATIVE_LLONG",
    atomictype.NativeType.ULONGLONG : "PredType::NATIVE_ULLONG",
    atomictype.NativeType.FLOAT : "PredType::NATIVE_FLOAT",
    atomictype.NativeType.DOUBLE : "PredType::NATIVE_DOUBLE",
    atomictype.NativeType.LONGDOUBLE : "PredType::NATIVE_LDOUBLE",
    atomictype.NativeType.BOOLEAN : "PredType::NATIVE_HBOOL",

}

'''
    Generates the transform class bodies.
'''
def generate_output_cpp_file(logger, output_directory, parsed_file, file_excluder):
    # build the name of the actual output file we're writing to
    filename_no_dir = os.path.basename(parsed_file.parsed_filepath)
    output_filepath = filegenutils.build_output_filepath(output_directory, filename_no_dir, "cpp")
    output_filepath 
    
    with open(output_filepath, "w+") as writefile:
        filegenutils.write_preamble(writefile, filename_no_dir)


        included_header = filegenutils.build_output_filepath(output_directory, filename_no_dir, "h")
        included_header_basename = os.path.basename(included_header)
        writefile.write("#include \"{0}\"\n\n".format(included_header_basename))

        for dependency_include in parsed_file.other_includes:
            if not file_excluder.is_excluded_path(dependency_include):
                fixed_filename = dependency_include.replace(".h", "_DxTransform.h")
                include_filename = os.path.basename(fixed_filename)
                writefile.write("#include \"{0}\"\n".format(include_filename))

        for enum in parsed_file.enum_types_parsed_from_file:
            _write_class_definition_for_type(writefile, enum)

        for struct in parsed_file.compound_types_parsed_from_file:
            _write_class_definition_for_type(writefile, struct)

            
'''
    Writes the class implementation for each custom H5 type (whether that be enum or compound)
'''
def _write_class_definition_for_type(output_file, datatype):
    namespaces = filegenutils.build_namespace_list(datatype.fully_qualified_typename)
    indentation_spaces = filegenutils.Indentation()
    num_namespaces_to_close = 0
    for ns in namespaces:
        output_file.write(indentation_spaces + "namespace {0}_Dx {{\n".format(ns))
        num_namespaces_to_close += 1
        indentation_spaces.increment()

    output_file.write(indentation_spaces +  
                      "void {0}DxTransform::{1}DxTransform(DxTransform::DxTransformFactory& parentFac) noexcept:\n".format(datatype.typename, 
                                                                                                                           datatype.typename))
    
    indentation_spaces.increment()

    if datatype.typecode == TypeCode.COMPOUND:
        hdf5_type = "CompType"

    elif datatype.typecode == TypeCode.ENUM:
        hdf5_type = "EnumType"

    output_file.write(indentation_spaces +
                    "DxTransform::DxTransformBase<{0}, H5::{1}>(parentFac)\n".format(datatype.fully_qualified_typename,
                                                                                     hdf5_type))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "{\n")
    indentation_spaces.increment()
    if datatype.typecode == TypeCode.COMPOUND:
        output_file.write(indentation_spaces + "H5::CompType& my_underlying_type = h5_datatype();\n")
        output_file.write(indentation_spaces + "static constexpr {0} zzz_tmp {{}};\n".format(datatype.fully_qualified_typename))
        for field in datatype.fields:
            if field.type_definition.typecode == TypeCode.ATOMIC:
                native_typename = _atomic_to_predefined_typemap[field.type_definition.atomic_type]
                assert native_typename is not None
                output_file.write(indentation_spaces + "my_underlying_type.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), {2});\n".format(field.name,
                                                                                                                                                 field.name,
                                                                                                                                                 native_typename))
            elif field.type_definition.typecode == TypeCode.COMPOUND:
                output_file.write(indentation_spaces + "my_underlying_type.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), {2});\n".format(field.name,
                                                                                                                                                 field.name,
                                                                                                                                                 native_typename))
        indentation_spaces.decrement()
        output_file.write(indentation_spaces + "}\n\n")
    elif datatype.typecode == TypeCode.ENUM:
        output_file.write(indentation_spaces + "H5::EnumType& my_underlying_type = h5_datatype();\n")
        backing_int_type = datatype.underlying_int_type
        output_file.write(indentation_spaces + "{0} ev {{}};\n".format(backing_int_type))
        for evp in datatype.get_enum_constants():

            output_file.write(indentation_spaces + "my_underlying_type.insert(\"{0}\", (ev={1},&ev);\n".format(evp.constant_name,
                                                                                                               evp.constant_value))
        indentation_spaces.decrement()
        output_file.write(indentation_spaces + "}\n\n")
    else:
        indentation_spaces.decrement()
        output_file.write(indentation_spaces + "}\n\n")
        

    for i in range(0, num_namespaces_to_close):
        indentation_spaces.decrement()
        output_file.write(indentation_spaces + "}\n")