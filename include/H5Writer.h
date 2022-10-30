// MIT License

// Copyright (c) 2022 Johnathon Lewis

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#pragma once

#include "DxDataType.h"
#include "H5Cpp.h"
#include "H5DataSetStream.h"

#include <array>
#include <cassert>
#include <map>
#include <string>
#include <typeindex>
#include <typeinfo>



namespace dxtrans
{
    class H5Writer
    {
    public:
        H5Writer(const std::string& applicationName) noexcept
        {
            //todo: optimize
            std::string outputFilename = applicationName + "_DxData.h5";
            file_ = H5::H5File(H5std_string(outputFilename.c_str()), H5F_ACC_TRUNC);
            filename_ = outputFilename;

        }
    
        template <typename CompoundOrEnumT>
        void write(const CompoundOrEnumT& data)
        {
            DxDataType<CompoundOrEnumT> data_type = DxDataType<CompoundOrEnumT>::instance();
            const H5::DataType& h5type = data_type.h5_datatype();
            H5DataSetStream& ds = get_or_create_dataset<CompoundOrEnumT>(typeid(data), 
                                                                         data_type.type_name(), 
                                                                         h5type);

            ds.write(data, h5type);
        }


    private:
        template <typename RawType>
        H5DataSetStream& get_or_create_dataset(const std::type_info& tid,
                                               const char* typeName,
                                               const H5::DataType& dataType)
        {
            auto typeIdx = std::type_index(tid);
            auto elem = datasets_.find(typeIdx);
            if (elem != datasets_.end())
            {
                return elem->second;
            }
            else
            {
                auto result = datasets_.emplace(typeIdx, 
                                                make_dataset_stream<RawType>(typeName, 
                                                                             file_, 
                                                                             dataType));
                assert(result.second);
                return result.first->second;
            }
        }


        std::string filename_;
        H5::H5File file_;

        std::map<std::type_index, H5DataSetStream> datasets_;
    };
}