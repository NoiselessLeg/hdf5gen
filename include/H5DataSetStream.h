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
#include "H5Cpp.h"

#include <array>

namespace dxtrans
{ 

    namespace detail
    {
        // this is basically a temporary type used so that we can define
        // a constructor that takes a templated parameter, without
        // necessarily declaring the entire DataSetInfo struct
        // as a templated struct.
        template <typename T>
        struct type_holder 
        {
            using type = T;
        };

        static constexpr size_t DEFAULT_CHUNKSIZE = 8;
        static constexpr size_t RANK = 1;
    }

    class H5DataSetStream
    {
    public:
    
        template <class UnderlyingT>
        H5DataSetStream(const std::string& typeName,
                        H5::H5File& fileHandle,
                        H5::DataType& dataType,
                        detail::type_holder<UnderlyingT>&& tmp):
            num_written_elems_(0),
            typename_(typeName)
        {
            static constexpr UnderlyingT fill_value {};

            static constexpr hsize_t chunkdims[] { 1 };
        
            H5::DSetCreatPropList cparms {};
            cparms.setChunk(detail::RANK, chunkdims);
            cparms.setFillValue(dataType, &fill_value);

            static constexpr hsize_t dim[] { 0 };
            static constexpr hsize_t maxdim[] {H5S_UNLIMITED};
            dataspace_ = H5::DataSpace(detail::RANK, dim, maxdim);

            dataset_ = fileHandle.createDataSet(H5std_string(typeName), dataType, dataspace_, cparms);
        }

        template <typename T>
        void write(const T& data, H5::DataType& datatype)
        {
            // get the hyperslab that we're 
            const hsize_t dims[] { 1 };
            const hsize_t maxdims[] { H5S_UNLIMITED };

            H5::DataSpace memspace(detail::RANK, dims, maxdims);

            H5::DataSpace filespace = dataset_.getSpace();
            const hsize_t filedim = filespace.getSimpleExtentNpoints();

            // extend the dataset
            hsize_t newSize[] { filedim + 1 };
            dataset_.extend(newSize);

            // select the hyperslab to write to in the file
            filespace = dataset_.getSpace();
            hsize_t offset[] { filedim };
            hsize_t dims1[] { 1 };

            filespace.selectHyperslab(H5S_SELECT_SET, dims1, offset);

            dataset_.write(&data, datatype, memspace, filespace);
        }
    

    private:
        size_t num_written_elems_;
        std::string typename_;
        H5::DataSpace dataspace_;
        H5::DataSet dataset_;

    };

    template <typename UnderlyingT>
    H5DataSetStream make_dataset_stream(const std::string& typeName,
                                        H5::H5File& fileHandle,
                                        H5::DataType& dataType)
    {
        return H5DataSetStream(typeName,
                               fileHandle,
                               dataType, 
                               detail::type_holder<UnderlyingT>());
    }

}