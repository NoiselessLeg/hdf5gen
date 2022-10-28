#pragma once
#include "H5Cpp.h"

#define HDF5_FIELD_OFFSET(StructVarName, FieldName) \
static_cast<std::size_t>(reinterpret_cast<const char*>(&StructVarName.FieldName) - reinterpret_cast<const char*>(&StructVarName))
    
namespace dxtrans
{
    template <typename CompoundOrEnumT>
    class DxDataType {};
}