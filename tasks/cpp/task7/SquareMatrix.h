//
// Created by argem on 29.10.2022.
//

#ifndef CPP_TASKS_SQUAREMATRIX_H
#define CPP_TASKS_SQUAREMATRIX_H

#include <iostream>
#include <vector>
#include <iomanip>
#include <cblas-netlib.h>


namespace task7{
    class SquareMatrix {
    private:
        std::vector<double> mem_;
        size_t n_;
    public:
        explicit SquareMatrix(size_t n) : n_(n), mem_(n * n) {}

        SquareMatrix(SquareMatrix &&other) noexcept {
            mem_ = std::move(other.mem_);
            n_ = other.n_;
            other.n_ = 0;
        }

        SquareMatrix(const SquareMatrix &other) noexcept {
            mem_ = other.mem_;
            n_ = other.n_;
        }

        SquareMatrix &operator=(SquareMatrix &&other) noexcept {
            if (this == &other) {
                return *this;
            }
            mem_ = std::move(other.mem_);
            n_ = other.n_;
            other.n_ = 0;
            return *this;
        }

        SquareMatrix &operator=(std::initializer_list<double> &&mem) noexcept {
            mem_ = mem;
            n_ = static_cast<size_t>(sqrt(static_cast<double>(mem_.size())));
            assert(n_ * n_ == mem_.size());
            return *this;
        }

        SquareMatrix(std::initializer_list<double> &&mem) noexcept {
            mem_ = mem;
            n_ = static_cast<size_t>(sqrt(static_cast<double>(mem_.size())));
            assert(n_ * n_ == mem_.size());
        }

        size_t size() const {
            return n_;
        }

        double &operator()(size_t i, size_t j) noexcept {
            assert(i < n_ && j < n_);
            return mem_[i * n_ + j];
        }

        const double &operator()(size_t i, size_t j) const noexcept {
            assert(i < n_ && j < n_);
            return mem_[i * n_ + j];
        }

        SquareMatrix operator*(const SquareMatrix &other) const {
            assert(this->size() == other.size());

            SquareMatrix res(this->size());
            const double *a = this->mem_.data();
            const double *b = other.mem_.data();
            double *c = res.mem_.data();
            int n = static_cast<int>(this->size());
            cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                        n, n, n, 1.0, a, n, b, n, 0.0, c, n);
            return res;
        }

        SquareMatrix &operator()(const double *line, const size_t i, double c) {
            assert(i < n_);
            for (size_t j = 0; j < n_; ++j) {
                (*this)(i, j) += c * line[j];
            }
            return *this;
        }

        static SquareMatrix id(size_t n) {
            SquareMatrix m(n);
            for (size_t i = 0; i < n; ++i) {
                m(i, i) = 1;
            }
            return m;
        }
    };
}

#endif //CPP_TASKS_SQUAREMATRIX_H
