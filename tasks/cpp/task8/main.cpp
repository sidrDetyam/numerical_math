#include <iostream>
#include <cmath>
#include "integralcalculator.h"
#include <cstdio>

using namespace task8;

static void test(IIntegralCalculator &calculator) {
    double res = calculator.calculate([](double x) {
        return log(1 + x);
    }, 0, 2, 100000);

    printf("%.30f\n", res);
}


int main(int argc, char** argv) {

    ParallelIntegralCalculator calculator(4, std::make_unique<TrapezoidStrategy>());
    test(calculator);
    calculator.set_strategy(std::make_unique<SimpsonStrategy>());
    test(calculator);

    return 0;
}