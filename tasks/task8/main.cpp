#include <iostream>
#include "integralcalculator.h"

using namespace task8;

static void test(IIntegralCalculator &calculator){
    double res = calculator.calculate([](double x){
        return x;
    }, 0, 1000, 100000000);

    std::cout << res << std::endl;
}

int main() {

    ParallelIntegralCalculator calculator(4, std::make_unique<TrapezoidStrategy>());
    test(calculator);
    calculator.set_strategy(std::make_unique<SimpsonStrategy>());
    test(calculator);

    return 0;
}