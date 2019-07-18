#include "pybind11/pybind11.h"

#include "xtensor/xmath.hpp"
#include "xtensor/xarray.hpp"

#define FORCE_IMPORT_ARRAY
#include "xtensor-python/pyarray.hpp"
#include "xtensor-python/pyvectorize.hpp"

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>


// our headers
#include "spatial/spatial.hpp"
#include "spatial/spatial_config.hpp"

namespace py = pybind11;



namespace spatial {


    // implementation in def_myclass.cpp
    void def_class(py::module & m);

    // implementation in def_myclass.cpp
    void def_build_config(py::module & m);

    // implementation in def.cpp
    void def_build_config(py::module & m);

}


// Python Module and Docstrings
PYBIND11_MODULE(_spatial , module)
{
    xt::import_numpy();

    module.doc() = R"pbdoc(
        _spatial  python bindings

        .. currentmodule:: _spatial 

        .. autosummary::
           :toctree: _generate

           BuildConfiguration
           MyClass
    )pbdoc";

    spatial::def_build_config(module);
    spatial::def_class(module);

    // make version string
    std::stringstream ss;
    ss<<SPATIAL_VERSION_MAJOR<<"."
      <<SPATIAL_VERSION_MINOR<<"."
      <<SPATIAL_VERSION_PATCH;
    module.attr("__version__") = ss.str().c_str();
}