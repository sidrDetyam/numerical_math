//
// Created by argem on 29.10.2022.
//

#include "BlasBasedMatrix.h"

using namespace task7;

double *BlasBasedMatrix::data_() noexcept {
    return Base::data().data();
}

BlasBasedMatrix::BlasBasedMatrix(size_t n, size_t m) : Base(n, m) {}


BlasBasedMatrix BlasBasedMatrix::id(size_t n) {
    BlasBasedMatrix m(n, n);
    for (size_t i = 0; i < n; ++i) {
        (&m)->Base::operator()(i, i) = 1;
    }
    return m;
}

BlasBasedMatrix &BlasBasedMatrix::daxpy(const double *line, const size_t i, double c) {
    assert(i < size1());
    cblas_daxpy(static_cast<int>(size2()), c, line, 1, &this->Base::operator()(i, 0), 1);
    return *this;
}

BlasBasedMatrix::BlasBasedMatrix(const std::vector<std::vector<double>>& m) :
    Base(m.size(), m.empty()? 0: m[0].size()) {
    for(size_t i=0; i<m.size(); ++i){
        for(size_t j=0; j<m[0].size(); ++j){
            (*this)(i, j) = m[i][j];
        }
    }
}

std::ostream &operator<<(std::ostream &output, Base &matrix) {
    for (size_t i = 0; i < matrix.size1(); ++i) {
        for (size_t j = 0; j < matrix.size2(); ++j) {
            double d = matrix(i, j);
            //printf( d<0? "%.3f ": " %.3f ", d);
            output << std::setprecision(3) << d << " ";
        }
        output << std::endl;
    }
    return output;
}
