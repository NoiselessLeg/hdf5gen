#ifndef DX_TRANSFORM_FACTORY_H
#define DX_TRANSFORM_FACTORY_H
#include <type_traits>

#include "H5Cpp.h"

namespace DxTransform
{
    template <typename EType>
    using enum_transform_t = DxTransformBase<EType, H5::EnumType>

    template <typename CType>
    using compound_transform_t = DxTransformBase<CType, H5::CompType>

    class DxTransformFactory
    {
    public:
        template<typename EType>
        enum_transform_t& get_enum_transform() const noexcept
        {
            static_assert(std::is_enum_v<EType>, "Enum transform cannot be used with compound or atomic type");
            static enum_transform_t ref(*this);
            return ref;
        }

        template<typename CType>
        compound_transform_t& get_compound_transform() const noexcept
        {
            static_assert(!std::is_enum_v<CType>, "Compound transform cannot be used with enum type");
            static compound_transform_t ref(*this);
            return ref;
        }

    };


}


#endif