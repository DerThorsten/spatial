#pragma once
#ifndef SPATIAL_SPATIAL_HPP
#define SPATIAL_SPATIAL_HPP

#include <cstdint>
#include <iostream>

namespace spatial {
    
    class MyClass
    {
    public:
        MyClass(const uint64_t size)
        : m_size(size)
        {

        }
        
        void hello_world()
        {
            std::cout<<"Hello World!\n";
        }
    private:
        uint64_t m_size;
    };

} // end namespace spatial


#endif // SPATIAL_SPATIAL_HPP