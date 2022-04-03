#include "smoothing.h"

double all_vector_sum(const std::vector<double> a) {
	return std::accumulate(a.begin(), a.end(), 0.0);
}

double vector_sum(const std::vector<double> a, const int start, const int end) {
	return std::accumulate(a.begin() + start, a.begin() + end, 0.0);
}

std::vector<double> npy_to_native(npy_array a) {
	return std::vector<double>(a.data(), a.data() + a.size());
}

std::vector<double> smoothing(
	const std::vector<double> X,
	const std::vector<double> f,
	const double N_oct,
	const int start,
	const int end,
	double* return_val
) {
	std::vector<double> X_res;

	for (int i = start; i < end; i++) {
		std::vector<double> g;
		const double f_i = f[i];

		const double sigma = -((((f_i / N_oct) / std::numbers::pi)) * ((f_i / N_oct) / std::numbers::pi)) * 2;

		for (int j = start; j < end; j++) {
			g.emplace_back(pow(std::numbers::e, pow(f[j] - f_i, 2) / sigma));
		}

		const double sum = 1 / all_vector_sum(g);
		for (int j = 0; j < g.size(); j++) {
			g[j] *= sum * (X[j + start]);
		}

		X_res.emplace_back(all_vector_sum(g));
	}

	std::copy(X_res.begin(), X_res.end(), &return_val[start]);
}

npy_array smoothingMT(npy_array X, npy_array f, double N_oct, int nb_threads) {
	auto X_nat = npy_to_native(X);
	auto f_nat = npy_to_native(f);

	std::cout << X.size() << " values to compute." << std::endl;

	std::cout << "Creating " << nb_threads << " threads with " << X.size() / nb_threads << " values per thread." << std::endl;

	std::vector<std::thread> threads;
	int batch_size = X.size() / nb_threads;
	int remainder = X.size() % nb_threads;

	std::vector<double> res(f.size(), 0);
	for (int i = 0; i < nb_threads; i++) {
		if (i == nb_threads - 1) {
			threads.push_back(std::thread(&smoothing, X_nat, f_nat, N_oct, i * batch_size, (i + 1) * batch_size + remainder, res.data()));
		}

		threads.push_back(std::thread(&smoothing, X_nat, f_nat, N_oct, i * batch_size, (i + 1) * batch_size, res.data()));
	}

	for (auto& t : threads) {
		t.join();
	}

	return py::array(res.size(), res.data());
}