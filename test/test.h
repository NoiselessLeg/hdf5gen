#pragma once
#include <cstddef>
#include <cstdint>
#include "test2.h"

class MyClass;

static constexpr size_t MAX_NUM_ARRAY_ELEMS = 21;

namespace testns
{
    enum my_cool_enum
    {
        value_1 = 1,
        value_2 = 3
    };
}

struct BitfieldTest
{
    uint32_t val1 : 8;
    uint32_t val2 : 16;
    uint32_t spare: 8;
};

class MyClass
{
public:
    uint32_t i[MAX_NUM_ARRAY_ELEMS];
    int k[MAX_NUM_ARRAY_ELEMS];
    testns::my_cool_enum enuma;
};

struct SampleStruct2
{
    my_using_statement type1;
    MyClass testType;
    Sample1::Inner innerStruct;
    another_typedef_lol typedeftest;
    
};