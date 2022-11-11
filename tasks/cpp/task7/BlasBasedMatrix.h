//
// Created by argem on 29.10.2022.
//

#ifndef CPP_TASKS_BLASBASEDMATRIX_H
#define CPP_TASKS_BLASBASEDMATRIX_H

#include <boost/numeric/ublas/matrix.hpp>
#include <iostream>
#include <vector>
#include <iomanip>
#include <openblas-pthread/cblas.h>

namespace task7{

    using namespace boost::numeric;

    using Base = ublas::matrix<double, ublas::row_major, std::vector<double>>;
    class BlasBasedMatrix: public Base{
    private:
        double* data_() noexcept;

    public:
        explicit BlasBasedMatrix(size_t n, size_t m);

        explicit BlasBasedMatrix(const std::vector<std::vector<double>> &m);

        explicit BlasBasedMatrix(Base&& ) noexcept;

        static BlasBasedMatrix id(size_t n);

        BlasBasedMatrix &daxpy(const double *line, size_t i, double c);
    };
}

task7::BlasBasedMatrix operator * (const task7::Base& a, const task7::Base& b);

task7::ublas::vector<double> operator * (const task7::Base& a, const task7::ublas::vector<double>& b);

std::ostream& operator <<(std::ostream& output, task7::Base& matrix);

#endif //CPP_TASKS_BLASBASEDMATRIX_H
