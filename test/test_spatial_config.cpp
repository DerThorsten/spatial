#include <doctest.h>

#include "spatial/spatial.hpp"
#include "spatial/spatial_config.hpp"



TEST_SUITE_BEGIN("core");

TEST_CASE("check version"){

    #ifndef SPATIAL_VERSION_MAJOR
        #error "SPATIAL_VERSION_MAJOR is undefined"
    #endif
    

    #ifndef SPATIAL_VERSION_MINOR
        #error "SPATIAL_VERSION_MINOR is undefined"
    #endif


    #ifndef SPATIAL_VERSION_PATCH
        #error "SPATIAL_VERSION_PATCH is undefined"
    #endif

    CHECK_EQ(SPATIAL_VERSION_MAJOR , 0);
    CHECK_EQ(SPATIAL_VERSION_MINOR , 1);
    CHECK_EQ(SPATIAL_VERSION_PATCH , 0);
}



TEST_SUITE_END(); // end of testsuite core
