#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <numbers>
#include <vector>
#include <iostream>
#include <thread>
#include <numeric>

namespace py = pybind11;
typedef py::array_t<double, py::array::c_style> npy_array;

std::vector<double> npy_to_native(npy_array a);
double vector_sum(const std::vector<double> a, const int start, const int end);
double all_vector_sum(const std::vector<double> a);

std::vector<double> smoothing(
	const std::vector<double> X,
	const std::vector<double> f,
	const double N_oct,
	const int start,
	const int end,
	double* return_val
);

npy_array smoothingMT(npy_array X, npy_array f, double N_oct, int nb_threads = 4);

PYBIND11_MODULE(smoothing, m) {
	m.def("smoothingMT", &smoothingMT);
}