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

_our_namespace_name = "h5gen"

_atomic_to_predefined_typemap = {
    atomictype.NativeType.CHAR: "PredType::NATIVE_CHAR",
    atomictype.NativeType.SCHAR: "PredType::NATIVE_SCHAR",
    atomictype.NativeType.UCHAR: "PredType::NATIVE_UCHAR",
    atomictype.NativeType.SHORT: "PredType::NATIVE_SHORT",
    atomictype.NativeType.USHORT: "PredType::NATIVE_USHORT",
    atomictype.NativeType.INT: "PredType::NATIVE_INT",
    atomictype.NativeType.UINT: "PredType::NATIVE_UINT",
    atomictype.NativeType.LONG: "PredType::NATIVE_LONG",
    atomictype.NativeType.ULONG: "PredType::NATIVE_ULONG",
    atomictype.NativeType.LONGLONG: "PredType::NATIVE_LLONG",
    atomictype.NativeType.ULONGLONG: "PredType::NATIVE_ULLONG",
    atomictype.NativeType.FLOAT: "PredType::NATIVE_FLOAT",
    atomictype.NativeType.DOUBLE: "PredType::NATIVE_DOUBLE",
    atomictype.NativeType.LONGDOUBLE: "PredType::NATIVE_LDOUBLE",
    atomictype.NativeType.BOOLEAN: "PredType::NATIVE_HBOOL",

}

'''
    Generates the transform class header file
'''


def generate_output_header_file(logger, output_directory, parsed_file, file_excluder):
    filename_no_dir = os.path.basename(parsed_file.parsed_filepath)
    output_filepath = filegenutils.build_output_filepath(
        output_directory, filename_no_dir, "h")

    with open(output_filepath, "w+") as writefile:
        filegenutils.write_preamble(writefile, filename_no_dir)

        ifdef_symbol = filename_no_dir.upper()[:filename_no_dir.find('.')]
        writefile.write("#ifndef {0}_H5_DATATYPE_H\n".format(ifdef_symbol))
        writefile.write("#define {0}_H5_DATATYPE_H\n\n".format(ifdef_symbol))

        inclist = filegenutils.build_include_list(parsed_file, file_excluder)

        writefile.write("#include \"DxDataType.h\"\n")

        for include in inclist:
            writefile.write("#include \"{0}\"\n".format(include))

        writefile.write('\n')

        for enum in parsed_file.enum_types_parsed_from_file:
            _write_enum_dx_datatype_class(writefile, enum)

        for struct in parsed_file.compound_types_parsed_from_file:
            _write_compound_dx_datatype_class(writefile, struct)

        for union in parsed_file.union_types_parsed_from_file:
            _write_union_dx_datatype_class(writefile, union)

        writefile.write("\n#endif\n")


def _write_enum_dx_datatype_class(output_file, datatype):
    indentation_spaces = filegenutils.Indentation()

    output_file.write(indentation_spaces +
                      "namespace {0} {{\n".format(_our_namespace_name))
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "template <>\n")
    output_file.write(indentation_spaces +
                      "class DxDataType<{0}> {{\n".format(datatype.fully_qualified_typename))

    output_file.write(indentation_spaces + "public:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType& instance() noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType<{0}> e {{}};\n".format(datatype.fully_qualified_typename))
    output_file.write(indentation_spaces + "return e;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n")

    output_file.write(indentation_spaces +
                      "const H5::DataType& h5_datatype() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "return datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    output_file.write(indentation_spaces +
                      "const char* type_name() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "return \"{0}\";\n".format(datatype.typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "private:\n")
    indentation_spaces.increment()

    output_file.write(indentation_spaces + "DxDataType() noexcept:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "datatype_(sizeof({0}))\n".format(datatype.fully_qualified_typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "{\n")

    indentation_spaces.increment()
    backing_int_type = datatype.underlying_int_type
    output_file.write(indentation_spaces +
                      "{0} ev {{}};\n".format(backing_int_type))
    for evp in datatype.get_enum_constants():
        output_file.write(indentation_spaces + "datatype_.insert(\"{0}\", (ev={1},&ev));\n".format(evp.constant_name,
                                                                                                   evp.constant_value))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")
    output_file.write(indentation_spaces + "H5::EnumType datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "};\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n")


def _write_compound_dx_datatype_class(output_file, datatype):
    indentation_spaces = filegenutils.Indentation()

    output_file.write(indentation_spaces +
                      "namespace {0} {{\n".format(_our_namespace_name))
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "template <>\n")
    output_file.write(indentation_spaces +
                      "class DxDataType<{0}> {{\n".format(datatype.fully_qualified_typename))

    output_file.write(indentation_spaces + "public:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType& instance() noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType<{0}> e {{}};\n".format(datatype.fully_qualified_typename))
    output_file.write(indentation_spaces + "return e;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    output_file.write(indentation_spaces +
                      "const H5::DataType& h5_datatype() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "return datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    output_file.write(indentation_spaces +
                      "const char* type_name() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "return \"{0}\";\n".format(datatype.typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "private:\n")
    indentation_spaces.increment()

    output_file.write(indentation_spaces + "DxDataType() noexcept:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "datatype_(sizeof({0}))\n".format(datatype.fully_qualified_typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "{\n")

    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static constexpr {0} zzz_tmp {{}};\n".format(datatype.fully_qualified_typename))

    seen_datatypes = set()
    for field in datatype.fields:
        if field.type_definition.typecode == TypeCode.ATOMIC:
            native_typename = _atomic_to_predefined_typemap[field.type_definition.atomic_type]
            assert native_typename is not None
            if not field.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), H5::{2});\n"
                                  .format(field.name,
                                          field.name,
                                          native_typename))
            else:
                output_file.write(indentation_spaces + "hsize_t {0}_dims[1] = {{{1}}};\n".format(
                    field.name, field.num_array_elems()))
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}[0]), H5::ArrayType(H5::{2}, 1, {3}_dims));\n"
                                  .format(field.name,
                                          field.name,
                                          native_typename,
                                          field.name))

        elif field.type_definition.typecode == TypeCode.COMPOUND:
            safe_typename = field.type_definition.fully_qualified_typename.replace(
                "::", '_')
            if safe_typename not in seen_datatypes:
                output_file.write(indentation_spaces +
                                  "DxDataType<{0}>& zzz_{1}_dxtype = DxDataType<{2}>::instance();\n"
                                  .format(field.type_definition.fully_qualified_typename,
                                          safe_typename,
                                          field.type_definition.fully_qualified_typename))
                seen_datatypes.add(safe_typename)

            if not field.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), zzz_{2}_dxtype.h5_datatype());\n"
                                  .format(field.name,
                                          field.name,
                                          safe_typename))
            else:
                output_file.write(indentation_spaces + "hsize_t {0}_dims[1] = {{{1}}};\n".format(
                    field.name, field.num_array_elems()))
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}[0]), H5::ArrayType(zzz_{2}_dxtype.h5_datatype(), 1, {3}_dims);\n"
                                  .format(field.name,
                                          field.name,
                                          safe_typename,
                                          field.name))

        elif field.type_definition.typecode == TypeCode.ENUM:
            safe_typename = field.type_definition.fully_qualified_typename.replace(
                "::", '_')

            if safe_typename not in seen_datatypes:
                output_file.write(indentation_spaces +
                                  "DxDataType<{0}>& zzz_{1}_dxtype = DxDataType<{2}>::instance();\n"
                                  .format(field.type_definition.fully_qualified_typename,
                                          safe_typename,
                                          field.type_definition.fully_qualified_typename))
                seen_datatypes.add(safe_typename)

            if not field.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), zzz_{2}_dxtype.h5_datatype());\n"
                                  .format(field.name,
                                          field.name,
                                          safe_typename))
            else:
                for i in range(0, field.num_array_elems()):
                    output_file.write(indentation_spaces +
                                      "datatype_.insertMember(\"{0}[{1}]\", HDF5_FIELD_OFFSET(zzz_tmp,{2}[{3}]), zzz_{4}_dxtype.h5_datatype());\n"
                                      .format(field.name,
                                              i,
                                              field.name,
                                              i,
                                              safe_typename))
    indentation_spaces.decrement()

    output_file.write(indentation_spaces + "}\n\n")
    output_file.write(indentation_spaces + "H5::CompType datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "};\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n")


def _write_union_dx_datatype_class(output_file, datatype):
    indentation_spaces = filegenutils.Indentation()

    output_file.write(indentation_spaces +
                      "namespace {0} {{\n".format(_our_namespace_name))
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "template <>\n")
    output_file.write(indentation_spaces +
                      "class DxDataType<{0}> {{\n".format(datatype.fully_qualified_typename))

    output_file.write(indentation_spaces + "public:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType& instance() noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static DxDataType<{0}> e {{}};\n".format(datatype.fully_qualified_typename))
    output_file.write(indentation_spaces + "return e;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    output_file.write(indentation_spaces +
                      "const H5::DataType& h5_datatype() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "return datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    output_file.write(indentation_spaces +
                      "const char* type_name() const noexcept {\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "return \"{0}\";\n".format(datatype.typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "private:\n")
    indentation_spaces.increment()

    output_file.write(indentation_spaces + "DxDataType() noexcept:\n")
    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "datatype_(sizeof({0}))\n".format(datatype.fully_qualified_typename))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "{\n")

    indentation_spaces.increment()
    output_file.write(indentation_spaces +
                      "static constexpr {0} zzz_tmp {{}};\n".format(datatype.fully_qualified_typename))

    seen_datatypes = set()

    # first, we will attempt to use the first compound type if one is available.
    # if we do not find a field who is a compound type, then use the first
    # atomic type or enum type available.
    field_to_use = None
    if len(datatype.fields) > 0:
        field_to_use = next(
            (field for field in datatype.fields if field.type_definition.typecode == TypeCode.COMPOUND), None)
        if field_to_use is None:
            field_to_use = datatype.fields[0]

    if field_to_use is not None:
        if field_to_use.type_definition.typecode == TypeCode.ATOMIC:
            native_typename = _atomic_to_predefined_typemap[field_to_use.type_definition.atomic_type]
            assert native_typename is not None
            if not field_to_use.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), H5::{2});\n"
                                  .format(field_to_use.name,
                                          field_to_use.name,
                                          native_typename))
            else:
                output_file.write(indentation_spaces + "hsize_t {0}_dims[1] = {{{1}}};\n".format(
                    field_to_use.name, field_to_use.num_array_elems()))
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}[0]), H5::ArrayType(H5::{2}, 1, {3}_dims));\n"
                                  .format(field_to_use.name,
                                          field_to_use.name,
                                          native_typename,
                                          field_to_use.name))

        elif field_to_use.type_definition.typecode == TypeCode.COMPOUND:
            safe_typename = field_to_use.type_definition.fully_qualified_typename.replace(
                "::", '_')
            if safe_typename not in seen_datatypes:
                output_file.write(indentation_spaces +
                                  "DxDataType<{0}>& zzz_{1}_dxtype = DxDataType<{2}>::instance();\n"
                                  .format(field_to_use.type_definition.fully_qualified_typename,
                                          safe_typename,
                                          field_to_use.type_definition.fully_qualified_typename))
                seen_datatypes.add(safe_typename)

            if not field_to_use.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), zzz_{2}_dxtype.h5_datatype());\n"
                                  .format(field_to_use.name,
                                          field_to_use.name,
                                          safe_typename))
            else:
                output_file.write(indentation_spaces + "hsize_t {0}_dims[1] = {{{1}}};\n".format(
                    field_to_use.name, field_to_use.num_array_elems()))
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}[0]), H5::ArrayType(zzz_{2}_dxtype.h5_datatype(), 1, {3}_dims);\n"
                                  .format(field_to_use.name,
                                          field_to_use.name,
                                          safe_typename,
                                          field_to_use.name))

        elif field_to_use.type_definition.typecode == TypeCode.ENUM:
            safe_typename = field_to_use.type_definition.fully_qualified_typename.replace(
                "::", '_')

            if safe_typename not in seen_datatypes:
                output_file.write(indentation_spaces +
                                  "DxDataType<{0}>& zzz_{1}_dxtype = DxDataType<{2}>::instance();\n"
                                  .format(field_to_use.type_definition.fully_qualified_typename,
                                          safe_typename,
                                          field_to_use.type_definition.fully_qualified_typename))
                seen_datatypes.add(safe_typename)

            if not field_to_use.is_array():
                output_file.write(indentation_spaces +
                                  "datatype_.insertMember(\"{0}\", HDF5_FIELD_OFFSET(zzz_tmp,{1}), zzz_{2}_dxtype.h5_datatype());\n"
                                  .format(field_to_use.name,
                                          field_to_use.name,
                                          safe_typename))
            else:
                for i in range(0, field_to_use.num_array_elems()):
                    output_file.write(indentation_spaces +
                                      "datatype_.insertMember(\"{0}[{1}]\", HDF5_FIELD_OFFSET(zzz_tmp,{2}[{3}]), zzz_{4}_dxtype.h5_datatype());\n"
                                      .format(field_to_use.name,
                                              i,
                                              field_to_use.name,
                                              i,
                                              safe_typename))
        indentation_spaces.decrement()

    output_file.write(indentation_spaces + "}\n\n")
    output_file.write(indentation_spaces + "H5::CompType datatype_;\n")
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "};\n\n")

    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "}\n")
