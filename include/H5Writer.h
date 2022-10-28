#pragma once
#include <cassert>
#include <map>
#include <string>
#include <string_view>
#include <typeindex>
#include <typeinfo>

#include "H5Cpp.h"

#include "DxDataType.h"

namespace dxtrans
{
    class H5Writer
    {
    public:
        H5Writer(const std::string& applicationName) noexcept
        {
            //todo: optimize
            std::string outputFilename = std::string("./") + applicationName + "_DxData.h5";
            file_ = H5::H5File(H5std_string(outputFilename.c_str()), H5F_ACC_TRUNC);
            filename_ = outputFilename;

        }
    
        template <typename CompoundOrEnumT>
        void write(const CompoundOrEnumT& data)
        {
            DxDataType<CompoundOrEnumT> data_type = DxDataType<CompoundOrEnumT>::instance();
            H5::DataType& h5type = data_type.h5_datatype();
            H5::DataSet& ds = get_or_create_dataset<CompoundOrEnumT>(typeid(data), h5type);

            ds.write(&data, h5type);
        }


    private:
        template <typename T>
        struct type_holder 
        {
            using type = T;
        };
    
        struct DataSetInfo
        {
            template <typename RawType>
            DataSetInfo(const std::string& typeName,
                        const size_t rawTypeSize,
                        H5::H5File& fileHandle,
                        H5::DataType& dataType,
                        type_holder<RawType>&& tmp):
                TypeName(typeName)
            {
                static constexpr RawType fill_value {};
                static constexpr size_t RANK = 1;
                const size_t DEFAULT_CHUNKSIZE = 8;
                // for now, start with 32 elements.
                static const hsize_t dim[] {DEFAULT_CHUNKSIZE};
                static const hsize_t maxdim[] {H5S_UNLIMITED};
            
                H5::DSetCreatPropList cparms {};
                cparms.setChunk(RANK, dim);
                cparms.setFillValue(dataType, &fill_value);

                DataSpaceHandle = H5::DataSpace(RANK, dim, maxdim);
                DataSetHandle = fileHandle.createDataSet(H5std_string(typeName), dataType, DataSpaceHandle, cparms);

            }


            std::string TypeName;
            H5::DataSpace DataSpaceHandle;
            H5::DataSet DataSetHandle;
        };

        template <typename RawType>
        H5::DataSet& get_or_create_dataset(const std::type_info& tid,
                                           H5::DataType& dataType)
        {
            auto typeIdx = std::type_index(tid);
            auto elem = datasets_.find(typeIdx);
            if (elem != datasets_.end())
            {
                return elem->second.DataSetHandle;
            }
            else
            {
                auto result = datasets_.emplace(typeIdx, DataSetInfo(tid.name(), sizeof(RawType), file_, dataType, type_holder<RawType>()));
                assert(result.second);
                return result.first->second.DataSetHandle;
            }
        }


        std::string filename_;
        H5::H5File file_;

        std::map<std::type_index, DataSetInfo> datasets_;
    };
}