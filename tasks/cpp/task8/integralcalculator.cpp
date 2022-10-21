#include "integralcalculator.h"

namespace task8 {

    double SimpsonStrategy::calculate(std::function<double(double)> f, double a, double b) const {
        return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b));
    }

    double TrapezoidStrategy::calculate(std::function<double(double)> f, double a, double b) const {
        return (b - a) / 2 * (f(a) + f(b));
    }

    // ParallelIntegralCalculator implementation

    ParallelIntegralCalculator::ParallelIntegralCalculator(int num_of_threads,
                                                           std::unique_ptr<ICalculationStrategy> &&strategy) :
            num_of_workers_(num_of_threads),
            strategy_(std::move(strategy)) {
    }

    double
    ParallelIntegralCalculator::calculate_(const std::function<double(double)> &f, double a, double b, int n) const {
        if (0 == n) {
            return 0;
        }
        double local_result = 0;
        double step = (b - a) / n;

        for (int i = 0; i < n; ++i) {
            local_result += strategy_->calculate(f, a + i * step, a + (i + 1) * step);
        }
        return local_result;
    }

    double ParallelIntegralCalculator::calculate(const std::function<double(double)> &f, double a, double b, int n) {
        double result = 0;
        std::vector<std::future<double>> workers;
        workers.reserve(num_of_workers_);

        const int steps_per_worker = n / num_of_workers_;
        const double width_per_worker = (b - a) / n * steps_per_worker;
        for (int i = 0; i < num_of_workers_; ++i) {
            workers.push_back(std::async(std::launch::async, [&, i]() {
                return calculate_(f, a + width_per_worker * i, a + width_per_worker * (i + 1),
                                  steps_per_worker);
            }));
        }

        result += calculate_(f, a + width_per_worker * num_of_workers_, b, n % num_of_workers_);
        for (auto &worker: workers) {
            result += worker.get();
        }
        
        return result;
    }

    void ParallelIntegralCalculator::set_strategy(std::unique_ptr<ICalculationStrategy> &&strategy) {
        strategy_ = std::move(strategy);
    }

    task8::ParallelIntegralCalculator::~ParallelIntegralCalculator() = default;
}