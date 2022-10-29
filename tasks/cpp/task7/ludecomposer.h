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

    class ILUDecomposer {
    public:
        virtual std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) = 0;

        virtual ~ILUDecomposer() = default;
    };

    class LUDecomposer : public ILUDecomposer {
    public:
        LUDecomposer() = default;

        std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) override;
    };

    class ParallelLUDecomposer : public ILUDecomposer {
    private:
        boost::asio::thread_pool pool;
    public:
        ParallelLUDecomposer(size_t count): pool(count) {}

        std::pair<BlasBasedMatrix, BlasBasedMatrix> decompose(const BlasBasedMatrix& a) override;
    };
}

#endif //TASK8_LUDECOMPOSER_H
