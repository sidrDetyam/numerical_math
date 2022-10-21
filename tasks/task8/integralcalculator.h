
#ifndef INTEGRAL_CALCULATOR
#define INTEGRAL_CALCULATOR

#include <functional>
#include <thread>
#include <atomic>
#include <vector>
#include <mutex>
#include <pthread.h>
#include <iostream>
#include <future>

namespace task8 {

    class IIntegralCalculator {
    public:
        virtual double calculate(const std::function<double(double)> &f, double a, double b, int n) = 0;

        virtual ~IIntegralCalculator() = default;
    };

    class ICalculationStrategy {
    public:
        virtual double calculate(std::function<double(double)> f, double a, double b) const = 0;

        virtual ~ICalculationStrategy() = default;
    };

    class SimpsonStrategy : public ICalculationStrategy {
    public:
        SimpsonStrategy() = default;

        double calculate(std::function<double(double)> f, double a, double b) const override;

        ~SimpsonStrategy() override = default;
    };

    class TrapezoidStrategy : public ICalculationStrategy {
    public:
        TrapezoidStrategy() = default;

        double calculate(std::function<double(double)> f, double a, double b) const override;

        ~TrapezoidStrategy() override = default;
    };

    class ParallelIntegralCalculator : public IIntegralCalculator {
    private:
        int num_of_workers_;
        std::unique_ptr<ICalculationStrategy> strategy_;

        double calculate_(const std::function<double(double)> &f, double a, double b, int n) const;

    public:
        explicit ParallelIntegralCalculator(int num_of_threads, std::unique_ptr<ICalculationStrategy> &&strategy);

        ~ParallelIntegralCalculator() override;

        double calculate(const std::function<double(double)> &f, double a, double b, int n) override;

        void set_strategy(std::unique_ptr<ICalculationStrategy> &&strategy);
    };
}

#endif