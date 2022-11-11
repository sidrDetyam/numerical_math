//
// Created by argem on 21.10.2022.
//

#ifndef TASK8_LUDECOMPOSER_H
#define TASK8_LUDECOMPOSER_H

#include "BlasBasedMatrix.h"
#include <boost/asio/thread_pool.hpp>
#include <boost/asio/post.hpp>
#include <mutex>
#include <algorithm>
#include <functional>
#include <condition_variable>
#include <thread>

namespace task7 {

    class LUDecomposer {
    public:
        virtual std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) = 0;

        static std::vector<double> solve(const BlasBasedMatrix &l,
                                         const BlasBasedMatrix &u,
                                         const std::vector<double>& b);

        virtual ~LUDecomposer() = default;
    };

    class SeqLUDecomposer : public LUDecomposer {
    public:
        SeqLUDecomposer() = default;

        std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) override;
    };

    class ParallelLUDecomposer : public LUDecomposer {
    private:
        boost::asio::thread_pool pool;
    public:
        ParallelLUDecomposer() = default;

        explicit ParallelLUDecomposer(size_t count);

        std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) override;
    };
}

#endif //TASK8_LUDECOMPOSER_H
