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
            H5::DataType& h5type = data_type.h5_datatype();
            H5DataSetStream& ds = get_or_create_dataset<CompoundOrEnumT>(typeid(data), 
                                                                         data_type.type_name(), 
                                                                         h5type);

            ds.write(data, h5type);
        }


    private:
        template <typename RawType>
        H5DataSetStream& get_or_create_dataset(const std::type_info& tid,
                                               const char* typeName,
                                               H5::DataType& dataType)
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