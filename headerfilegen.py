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


import filegenutils
from compoundtype import compound_type
from enumtype import enumeration_type
from exceptiontypes import CompilerError
from logger import Logger, LogLevel
from parsedfile import parsed_file
from typemanager import type_manager


'''
    Generates the transform class header file
'''
def generate_output_header_file(logger, output_directory, parsed_file, file_excluder):
    filename_no_dir = os.path.basename(parsed_file.parsed_filepath)
    output_filepath = filegenutils.build_output_filepath(output_directory, filename_no_dir, "h")
    
    with open(output_filepath, "w+") as writefile:
        filegenutils.write_preamble(writefile, filename_no_dir)
        
        ifdef_symbol = filename_no_dir.upper()[:filename_no_dir.find('.')]
        writefile.write("#ifndef {0}_DX_TRANSFORM_H\n".format(ifdef_symbol))
        writefile.write("#define {0}_DX_TRANSFORM_H\n\n".format(ifdef_symbol))

        inclist = filegenutils.build_include_list(parsed_file, file_excluder)

        writefile.write("#include \"DxTransformBase.h\"\n")
        writefile.write("#include \"{0}\"\n".format(filename_no_dir))
            
        writefile.write('\n')

        writefile.write("namespace DxTransform {\n")
        writefile.write("    class DxTransformFactory;\n")
        writefile.write("}\n\n")

        writefile.write("namespace H5 {\n")
        writefile.write("    class DataSet;\n")
        writefile.write("}\n\n")

        for enum in parsed_file.enum_types_parsed_from_file:
            _write_transform_class_declaration(writefile, "EnumType", enum.typename, enum.fully_qualified_typename)

        for struct in parsed_file.compound_types_parsed_from_file:
            _write_transform_class_declaration(writefile, "CompType", struct.typename, struct.fully_qualified_typename)

        writefile.write("\n#endif\n")

def _write_transform_class_declaration(output_file, h5_type, type_basename, type_fqn):
    namespaces = filegenutils.build_namespace_list(type_fqn)
    indentation_spaces = filegenutils.Indentation()
    num_namespaces_to_close = 0
    for ns in namespaces:
        output_file.write(indentation_spaces + "namespace {0}_Dx {{\n".format(ns))
        indentation_spaces.increment()
        num_namespaces_to_close += 1
        
    output_file.write(indentation_spaces + 
                      "class {0}DxTransform : public DxTransform::DxTransformBase<{1}, H5::{2}> {{\n".format(type_basename, 
                                                                                                             type_fqn,
                                                                                                             h5_type))

    
    output_file.write(indentation_spaces + "public:\n")
        
    indentation_spaces.increment()
    output_file.write(indentation_spaces + "{0}DxTransform(DxTransform::DxTransformFactory& parentFac) noexcept;\n".format(type_basename))
    output_file.write(indentation_spaces + "void write(const {0}& data, H5::DataSet& dataset);\n".format(type_fqn))
    indentation_spaces.decrement()
    output_file.write(indentation_spaces + "};\n\n")
    
    for i in range(0, num_namespaces_to_close):
        indentation_spaces.decrement()
        output_file.write(indentation_spaces + "}\n")

    