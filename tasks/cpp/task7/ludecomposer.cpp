//
// Created by argem on 21.10.2022.
//

#include <boost/asio/post.hpp>
#include "ludecomposer.h"

using namespace boost;
using namespace task7;

std::pair<BlasBasedMatrix, BlasBasedMatrix> SeqLUDecomposer::decompose(const BlasBasedMatrix &a) {
    assert(a.size1() == a.size2());

    const size_t n = a.size1();
    BlasBasedMatrix u(a);
    BlasBasedMatrix l = BlasBasedMatrix::id(n);

    for (size_t i = 0; i < n; ++i) {
        for (size_t j = i + 1; j < n; ++j) {
            double c = -u(j, i) / u(i, i);
            u.daxpy(&u(i, 0), j, c);
            l(j, i) = -c;
        }
    }
    return std::make_pair(std::move(l), std::move(u));
}


static std::function<void()> fork_(boost::asio::thread_pool &pool, BlasBasedMatrix &u, BlasBasedMatrix &l,
                        std::vector<std::tuple<std::mutex, std::condition_variable, int>> &v, size_t i){
    using namespace std;

    return [i, &pool, &u, &l, &v](){
        for (size_t j = i + 1; j < u.size1(); ++j) {
            std::unique_lock<mutex> lk(get<0>(v[j]));

            while(get<2>(v[j]) != i){
                get<1>((v[j])).wait(lk);
            }

            double c = -u(j, i) / u(i, i);
            u.daxpy(&u(i, 0), j, c);
            l(j, i) = -c;
            ++get<2>(v[j]);
            get<1>((v[j])).notify_all();

            if(get<2>(v[j]) == j){
                boost::asio::post(pool, fork_(pool, u, l, v, j));
            }
        }
    };
}


std::pair<BlasBasedMatrix, BlasBasedMatrix> ParallelLUDecomposer::decompose(const BlasBasedMatrix &a) {
    assert(a.size1() == a.size2());
    using namespace std;

    BlasBasedMatrix u(a);
    BlasBasedMatrix l = BlasBasedMatrix::id(a.size1());
    vector<tuple<mutex, std::condition_variable, int>> v(a.size1());

    boost::asio::post(pool, fork_(pool, u, l, v, 0));
    pool.join();

    return std::make_pair(std::move(l), std::move(u));
}


ParallelLUDecomposer::ParallelLUDecomposer(size_t count): pool(count) {
}

std::vector<double> LUDecomposer::solve(const BlasBasedMatrix &l,
                                        const BlasBasedMatrix &u,
                                        const std::vector<double>& b) {
    assert(l.size1() == u.size1() && l.size1() == b.size() && l.size1());
    std::vector<double> y(b.size());
    std::vector<double> x(b.size());
    for(size_t i=0; i<b.size(); ++i){
        assert(l(i, i));
        y[i] = b[i];
        for(size_t j=0; j<i; ++j){
            y[i] -= y[j] * l(i, j);
        }
        y[i] /= l(i, i);
    }

    for(int64_t i = static_cast<int64_t>(b.size()) - 1; i > -1; --i){
        assert(u(i, i));
        x[i] = y[i];
        for(int64_t j = static_cast<int64_t>(b.size()) - 1; j > i; --j){
            x[i] -= x[j] * u(i, j);
        }
        x[i] /= u(i, i);
    }

    return x;
}
